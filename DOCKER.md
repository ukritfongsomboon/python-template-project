# Docker Deployment Guide

Guide สำหรับ build และ deploy User API บน Docker

## Prerequisites

- Docker Desktop ≥ 20.10
- Docker Compose ≥ 1.29
- (Optional) Docker Registry สำหรับ push image

## Quick Start

### 1. Build Docker Image

```bash
# Build local image
docker build -t user-api:latest -f cmd/backend/Dockerfile .

# Or using build script
bash build.sh
```

### 2. Run Container

```bash
# Run locally
docker run -p 3000:3000 user-api:latest

# Run with environment variables
docker run -p 3000:3000 \
  -e API_URL=https://jsonplaceholder.typicode.com \
  -e DEBUG=False \
  user-api:latest

# Run in background
docker run -d -p 3000:3000 --name user-api user-api:latest
```

### 3. Using Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop container
docker-compose down

# Rebuild
docker-compose up --build -d
```

## Image Information

- **Base Image**: `python:3.11-slim`
- **Image Size**: ~200-250 MB (optimized with multi-stage)
- **Port**: 3000
- **Health Check**: Enabled
- **Non-root User**: appuser (UID: 1000)

## Environment Variables

```bash
API_URL              # JSONPlaceholder API URL (default: https://jsonplaceholder.typicode.com)
DEBUG                # Debug mode (default: False)
HOST                 # Server host (default: 0.0.0.0)
PORT                 # Server port (default: 3000)
```

## Testing Image

```bash
# Test image builds correctly
docker run --rm user-api:latest python -c "from cmd.backend.app import app; print('✓ OK')"

# Run container and test endpoint
docker run -d -p 3000:3000 --name test-api user-api:latest
sleep 2
curl http://localhost:3000/health
docker stop test-api
```

## Production Deployment

### On Server

```bash
# 1. Pull image from registry
docker pull your-registry/user-api:latest

# 2. Run with restart policy
docker run -d \
  --name user-api \
  --restart unless-stopped \
  -p 3000:3000 \
  -e API_URL=https://jsonplaceholder.typicode.com \
  your-registry/user-api:latest

# 3. View logs
docker logs -f user-api

# 4. Monitor health
curl http://localhost:3000/health
```

### Using Docker Compose on Server

```bash
# 1. Copy docker-compose.yml and .env
scp docker-compose.yml user@server:/path/to/app/
scp .env user@server:/path/to/app/

# 2. SSH to server
ssh user@server

# 3. Run compose
cd /path/to/app
docker-compose pull
docker-compose up -d

# 4. Monitor
docker-compose logs -f api
```

## Nginx Reverse Proxy

```nginx
# /etc/nginx/sites-available/user-api
upstream user_api {
    server localhost:3000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://user_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/docs {
        proxy_pass http://user_api/api/docs;
    }
}
```

## Troubleshooting

### Image build fails

```bash
# Check Dockerfile syntax
docker build --no-cache -t user-api:latest -f cmd/backend/Dockerfile .

# View build logs
docker build --progress=plain -t user-api:latest -f cmd/backend/Dockerfile . 2>&1 | tee build.log
```

### Container won't start

```bash
# Check logs
docker logs user-api

# Run interactively for debugging
docker run -it -p 3000:3000 user-api:latest /bin/bash
```

### Health check failing

```bash
# Test health endpoint
docker exec user-api python -c "import urllib.request; urllib.request.urlopen('http://localhost:3000/health')"

# Disable health check temporarily
docker run -p 3000:3000 --no-healthcheck user-api:latest
```

## Cleanup

```bash
# Remove container
docker rm user-api

# Remove image
docker rmi user-api:latest

# Prune unused resources
docker system prune -a
```

## Security Best Practices

✓ Non-root user (appuser)
✓ Minimal base image (slim)
✓ Multi-stage build (smaller size)
✓ Health check enabled
✓ No hardcoded secrets (use .env)
✓ Read-only filesystem (recommended for production)

## Additional Resources

- [Docker Official Python Image](https://hub.docker.com/_/python)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
