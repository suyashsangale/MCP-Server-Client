# 🚀 Deployment Guide

This guide covers deploying the MCP platform in various production environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Security Considerations](#security-considerations)
- [Monitoring & Maintenance](#monitoring--maintenance)

## Prerequisites

- Docker & Docker Compose
- Python 3.9+
- SSL Certificate (for production)
- Domain Name (optional)
- Cloud Account (if using cloud deployment)

## Docker Deployment

### 1. Create Docker Files

**`Dockerfile.server`**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/app ./app
COPY .env .

EXPOSE 8000
CMD ["uvicorn", "app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`Dockerfile.client`**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY client/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY client ./client
COPY .env .

EXPOSE 8501
CMD ["streamlit", "run", "client/streamlit_app.py"]
```

**`docker-compose.yml`**:
```yaml
version: '3.8'

services:
  server:
    build:
      context: .
      dockerfile: Dockerfile.server
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  client:
    build:
      context: .
      dockerfile: Dockerfile.client
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    depends_on:
      - server
    restart: unless-stopped
```

### 2. Deploy with Docker Compose

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

## Cloud Deployment

### AWS Deployment

1. **Set up AWS Infrastructure**
   ```bash
   # Install AWS CLI
   pip install awscli
   aws configure
   
   # Deploy with CloudFormation
   aws cloudformation create-stack --stack-name mcp-stack --template-body file://deploy/aws.yml
   ```

2. **Deploy to ECS**
   ```bash
   # Push images to ECR
   aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
   docker push aws_account_id.dkr.ecr.region.amazonaws.com/mcp-server
   docker push aws_account_id.dkr.ecr.region.amazonaws.com/mcp-client
   ```

### Google Cloud Platform

1. **Set up GCP Project**
   ```bash
   # Install Google Cloud SDK
   gcloud init
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy to Cloud Run**
   ```bash
   # Build and deploy server
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mcp-server
   gcloud run deploy mcp-server --image gcr.io/YOUR_PROJECT_ID/mcp-server
   
   # Build and deploy client
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/mcp-client
   gcloud run deploy mcp-client --image gcr.io/YOUR_PROJECT_ID/mcp-client
   ```

## Security Considerations

1. **Environment Variables**
   - Use secret management services
   - Never commit `.env` files
   - Rotate API keys regularly

2. **API Security**
   ```python
   # server/app/fastapi_app.py
   from fastapi.security import APIKeyHeader
   
   api_key_header = APIKeyHeader(name="X-API-Key")
   
   @app.post("/tools/{tool_name}")
   async def tool_endpoint(tool_name: str, api_key: str = Depends(api_key_header)):
       if api_key != os.getenv("API_KEY"):
           raise HTTPException(status_code=403)
   ```

3. **CORS Configuration**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-domain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Rate Limiting**
   ```python
   from fastapi.middleware import Middleware
   from slowapi import Limiter
   from slowapi.util import get_remote_address
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   ```

## Monitoring & Maintenance

1. **Logging Setup**
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s %(levelname)s %(message)s',
       handlers=[
           logging.FileHandler("logs/app.log"),
           logging.StreamHandler()
       ]
   )
   ```

2. **Health Checks**
   ```python
   @app.get("/health")
   async def health_check():
       return {
           "status": "healthy",
           "timestamp": datetime.utcnow(),
           "version": "1.0.0"
       }
   ```

3. **Metrics with Prometheus**
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator
   
   Instrumentator().instrument(app).expose(app)
   ```

4. **Backup Strategy**
   ```bash
   # Backup script example
   #!/bin/bash
   timestamp=$(date +%Y%m%d_%H%M%S)
   backup_dir="backups/$timestamp"
   
   mkdir -p $backup_dir
   cp -r config/ $backup_dir/
   cp .env $backup_dir/
   ```

## Scaling Considerations

1. **Load Balancing**
   - Use Nginx/HAProxy
   - Configure auto-scaling
   - Implement caching

2. **Database Integration**
   ```python
   from databases import Database
   
   database = Database(DATABASE_URL)
   
   @app.on_event("startup")
   async def startup():
       await database.connect()
   ```

3. **Caching Layer**
   ```python
   from fastapi_cache import FastAPICache
   from fastapi_cache.backends.redis import RedisBackend
   
   @app.on_event("startup")
   async def startup():
       FastAPICache.init(RedisBackend(), prefix="mcp-cache:")
   ```

## Troubleshooting

1. **Common Issues**
   - Check logs: `docker-compose logs`
   - Verify environment variables
   - Check network connectivity
   - Validate API keys

2. **Performance Issues**
   - Monitor resource usage
   - Check for memory leaks
   - Optimize database queries
   - Implement caching

## Need Help?

- Check our [FAQ](faq.md)
- Join our [Discord](https://discord.gg/your-server)
- Open an issue on GitHub
- Contact support@your-domain.com

---

Remember to regularly update dependencies and monitor security advisories! 