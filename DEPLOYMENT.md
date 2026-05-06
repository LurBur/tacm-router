# Deployment Guide

## Pre-Deployment Checklist

### Code Quality
- [ ] Run all tests: `pytest -v`
- [ ] Check test coverage: `pytest --cov=app --cov=engine`
- [ ] No syntax errors: `python -m py_compile app/*.py`
- [ ] No security issues: `pip audit` (or similar tool)

### Documentation
- [ ] README.md updated
- [ ] CHANGELOG.md entry added
- [ ] API_GUIDE.md reviewed
- [ ] DEVELOPER_GUIDE.md reviewed
- [ ] .env.example matches settings

### Configuration
- [ ] .env file created from .env.example
- [ ] All settings properly configured for environment
- [ ] DEBUG mode disabled for production
- [ ] LOG_LEVEL set to INFO (not DEBUG)
- [ ] Rate limiting enabled

### Dependencies
- [ ] requirements.txt is up to date
- [ ] All dependencies are pinned to specific versions
- [ ] No conflicting versions
- [ ] Python version 3.8+ verified

---

## Deployment Options

### Option 1: Systemctl Service (Linux Production)

#### 1. Install as Service

Create `/etc/systemd/system/siphon.service`:

```ini
[Unit]
Description=Siphon MVP Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/siphon-mvp
Environment="PATH=/opt/siphon-mvp/.venv/bin"
ExecStart=/opt/siphon-mvp/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 2. Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable siphon.service
sudo systemctl start siphon.service

# Check status
sudo systemctl status siphon.service

# View logs
sudo journalctl -u siphon.service -f
```

---

### Option 2: Docker Container

#### 1. Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Build and Run

```bash
# Build
docker build -t siphon-mvp:0.2.0 .

# Run
docker run -d \
  --name siphon-mvp \
  -p 8000:8000 \
  -e DEBUG=False \
  -e LOG_LEVEL=INFO \
  -e MAX_INPUT_LENGTH=50000 \
  siphon-mvp:0.2.0

# Check logs
docker logs -f siphon-mvp

# Stop
docker stop siphon-mvp
```

#### 3. Docker Compose (Production)

```yaml
version: '3.9'

services:
  siphon:
    build: .
    image: siphon-mvp:0.2.0
    container_name: siphon-mvp
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - LOG_LEVEL=INFO
      - MAX_INPUT_LENGTH=50000
      - SIGNAL_SCORE_THRESHOLD=70
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:latest
    container_name: siphon-nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - siphon
    restart: always
```

---

### Option 3: AWS EC2/ECS/Lambda

#### EC2 Deployment

```bash
# Connect to instance
ssh ec2-user@your-instance.amazonaws.com

# Install dependencies
sudo yum update -y
sudo yum install -y python3 python3-pip

# Clone/setup application
git clone https://github.com/yourusername/tacm-router.git
cd tacm-router

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Create .env
cp .env.example .env
# Edit .env with production settings

# Run with supervisor or systemd
# (See systemctl service above)
```

#### ECS (Container) Deployment

1. Push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker tag siphon-mvp:0.2.0 123456789.dkr.ecr.us-east-1.amazonaws.com/siphon-mvp:0.2.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/siphon-mvp:0.2.0
```

2. Create ECS Task Definition (JSON)
3. Create ECS Service
4. Configure ALB

#### Lambda Deployment

```python
# lambda_handler.py
from fastapi import FastAPI
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

Deploy with Serverless Framework:
```bash
serverless deploy
```

---

### Option 4: Heroku Deployment

#### 1. Create Procfile

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 2. Deploy

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create siphon-mvp

# Set environment variables
heroku config:set DEBUG=False LOG_LEVEL=INFO

# Deploy
git push heroku main

# View logs
heroku logs -t
```

---

## Reverse Proxy Configuration

### Nginx

```nginx
upstream siphon {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.siphon.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.siphon.example.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/api.siphon.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.siphon.example.com/privkey.pem;

    location / {
        proxy_pass http://siphon;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 12 4k;
    }

    # Health check endpoint (no logging)
    location /health {
        proxy_pass http://siphon;
        access_log off;
    }
}
```

### Apache

```apache
<VirtualHost *:80>
    ServerName api.siphon.example.com
    Redirect permanent / https://api.siphon.example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName api.siphon.example.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/api.siphon.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/api.siphon.example.com/privkey.pem

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    RequestHeader set X-Forwarded-Proto https
</VirtualHost>
```

---

## Monitoring & Logging

### Application Logging

```bash
# Watch real-time logs
tail -f /var/log/siphon/app.log

# Search logs
grep "error" /var/log/siphon/app.log
grep "req-abc123" /var/log/siphon/app.log  # By request ID

# Analyze logs
cat /var/log/siphon/app.log | grep "ERROR" | wc -l
```

### Health Monitoring

```bash
# Simple HTTP check
curl http://localhost:8000/health

# With request ID
curl -v http://localhost:8000/health | grep X-Request-ID

# Periodic monitoring
watch -n 5 'curl -s http://localhost:8000/health | jq'
```

### Metrics Collection

```python
# Example: Prometheus metrics
from prometheus_client import Counter, Histogram

request_count = Counter('siphon_requests_total', 'Total requests')
request_duration = Histogram('siphon_request_duration_seconds', 'Request duration')

# In your endpoint
with request_duration.time():
    result = engine.run(...)
request_count.inc()
```

---

## SSL/TLS Configuration

### Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d api.siphon.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Self-Signed Certificate

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

---

## Security Best Practices

### 1. Environment Variables
- Never commit `.env` file
- Use strong, random values for API keys
- Different values for dev/staging/production

### 2. Database Security
- Use parameterized queries
- Encrypt sensitive data at rest
- Use SSL for database connections

### 3. API Security
- Enable HTTPS/TLS
- Implement rate limiting
- Use API keys/JWT for authentication
- CORS configuration for allowed origins
- Input validation (you've got this!)

### 4. System Security
- Run as non-root user
- Keep dependencies updated
- Regular security audits
- Monitor for suspicious activity

### 5. Secrets Management
```bash
# Use AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id siphon/prod

# Or: HashiCorp Vault
vault kv get secret/siphon/prod

# Or: Azure Key Vault
az keyvault secret show --name siphon-api-key --vault-name siphon-vault
```

---

## Performance Tuning

### Uvicorn Settings

```bash
# For production
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --loop uvloop \
    --http httptools \
    --access-log \
    --log-level info
```

### Configuration Optimization

```python
# app/config.py adjustments
RATE_LIMIT_REQUESTS_PER_MINUTE = 60  # Adjust based on load
MAX_INPUT_LENGTH = 50000  # Balance between features and performance
REQUEST_TIMEOUT_SECONDS = 30  # Adjust for pipeline speed
```

### Database Connection Pooling
```python
# If using database
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)
```

---

## Rollback Plan

### Version 1: Keep Previous Version Running

```bash
# Current running
siphon-v0.2.0/

# Deploy new version
mkdir siphon-v0.3.0
# Deploy files
cd siphon-v0.3.0
# If issues, switch back
cd ../siphon-v0.2.0
systemctl restart siphon
```

### Version 2: Database Migrations

```bash
# Always test migrations on staging first
alembic upgrade head  # Forward
alembic downgrade -1  # Rollback

# Keep rollback scripts ready
```

---

## Post-Deployment Verification

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. API availability
curl http://localhost:8000/docs

# 3. Full pipeline test
curl -X POST http://localhost:8000/siphon \
  -H "Content-Type: application/json" \
  -d '{"raw_text": "A very long test text with meaningful content to validate the pipeline..."}'

# 4. Monitor logs
tail -f /var/log/siphon/app.log

# 5. Performance baseline
# Make 100 requests and measure response time
for i in {1..100}; do
  time curl -s http://localhost:8000/health > /dev/null
done
```

---

## Troubleshooting Deployment Issues

### Issue: Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --port 8001
```

### Issue: Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade --force-reinstall -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"

# Verify imports
python -c "import app.main"
```

### Issue: Permission Errors
```bash
# Check file permissions
ls -la /opt/siphon-mvp/

# Fix ownership
sudo chown -R www-data:www-data /opt/siphon-mvp/

# Make executable
chmod +x /opt/siphon-mvp/.venv/bin/uvicorn
```

### Issue: High Memory Usage
```bash
# Check memory
ps aux | grep uvicorn
free -h

# Reduce workers
uvicorn app.main:app --workers 2

# Monitor with top
top -p $(pgrep -f uvicorn)
```

---

## Continuous Deployment (CI/CD)

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Tests
        run: |
          pip install -r requirements.txt
          pytest -v
      
      - name: Deploy to Production
        run: |
          # SSH into server
          ssh user@server.com << 'EOF'
          cd /opt/siphon-mvp
          git pull origin main
          ./venv/bin/pip install -r requirements.txt
          sudo systemctl restart siphon
          EOF
```

---

## Production Checklist

- [ ] Deployment script tested
- [ ] Rollback plan documented
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] SSL/TLS enabled
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Database backups enabled
- [ ] Incident response plan ready
- [ ] Team trained on procedures

---

**Status:** ✅ Ready for Production  
**Last Updated:** May 6, 2026  
**Version:** 0.2.0
