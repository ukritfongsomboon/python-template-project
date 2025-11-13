# User API - Hexagonal Architecture with FastAPI

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121+-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Professional REST API built with **FastAPI** and **Hexagonal Architecture** pattern for managing user data from JSONPlaceholder API.

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)

## ✨ Features

- 🏗️ **Hexagonal Architecture** - Clean separation of concerns (Ports & Adapters)
- 📚 **FastAPI** - Modern async Python web framework
- 🔍 **Type Safety** - beartype for runtime type checking
- 📖 **Auto Documentation** - Swagger UI at `/api/docs`
- 🐳 **Docker Ready** - Multi-stage Dockerfile for production
- ✅ **Health Check** - Built-in health check endpoint
- 🔐 **Security** - Non-root Docker user, no hardcoded secrets
- 📝 **Comprehensive Docs** - Detailed API & deployment documentation
- 🚀 **Production Ready** - Environment configuration, error handling

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Docker & Docker Compose (optional)

### Installation

```bash
# Clone or download project
cd "Python Hexagonal Template"

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Run Application

```bash
# Development mode
python -m cmd.backend.app

# Or using uvicorn directly
uvicorn cmd.backend.app:app --reload --host 0.0.0.0 --port 3000
```

**Access API:**
- 🌐 API: http://localhost:3000
- 📖 Swagger UI: http://localhost:3000/api/docs
- ❤️ Health Check: http://localhost:3000/health

## 📦 Project Structure

```
.
├── cmd/
│   └── backend/
│       ├── app.py                  # FastAPI application entry point
│       ├── Dockerfile              # Production Docker configuration
│       └── __init__.py
├── core/
│   ├── handlers/
│   │   ├── user.py                 # User handler interface (port)
│   │   ├── user_res.py             # User handler implementation (adapter)
│   │   └── __init__.py
│   ├── models/
│   │   ├── api_response.py         # API response Pydantic models
│   │   ├── srv_global.py           # Global service models
│   │   ├── srv_user.py             # User service models
│   │   ├── repo_jsonplacehodel.py  # Repository models
│   │   └── __init__.py
│   ├── services/
│   │   ├── user.py                 # User service interface
│   │   ├── user_srv.py             # User service implementation
│   │   └── __init__.py
│   ├── repositories/
│   │   ├── jsonplaceholder.py      # Repository interface
│   │   ├── jsonplaceholder_api.py  # JSONPlaceholder API adapter
│   │   └── __init__.py
│   └── __init__.py
├── .dockerignore                   # Docker ignore patterns
├── .env.example                    # Environment variables example
├── DOCKER.md                       # Docker deployment guide
├── docker-compose.yml              # Docker Compose configuration
├── build.sh                        # Build script for Docker
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🏛️ Architecture

### Hexagonal Architecture Pattern

```
┌─────────────────────────────────────────────────┐
│              REST API (FastAPI)                 │
│           Handlers (HTTP Adapter)               │
└────────────┬────────────────────────────────────┘
             │
┌────────────┴────────────────────────────────────┐
│           Service Layer (Business Logic)        │
│              UserService Implementation         │
└────────────┬────────────────────────────────────┘
             │
┌────────────┴────────────────────────────────────┐
│        Repository Layer (Data Access)           │
│       JsonplaceHolderRepository Adapter         │
└────────────┬────────────────────────────────────┘
             │
             ▼
      JSONPlaceholder External API
```

### Layer Responsibilities

| Layer | Responsibility |
|-------|-----------------|
| **Handlers** | HTTP request/response handling, validation |
| **Services** | Business logic, data transformation, error handling |
| **Repositories** | External data source integration, API calls |
| **Models** | Data structure definitions (Pydantic models) |

## 📚 API Documentation

### Base URL
```
http://localhost:3000
```

### Endpoints

#### Get All Users
```http
GET /api/v1/users
```

**Response (200):**
```json
{
  "status": true,
  "code": 200,
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": 1,
      "name": "Leanne Graham",
      "username": "Bret",
      "email": "Sincere@april.biz"
    }
  ]
}
```

#### Health Check
```http
GET /health
```

**Response (200):**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### Interactive API Documentation

Open Swagger UI at: **http://localhost:3000/api/docs**

All endpoints include:
- ✓ Full parameter documentation
- ✓ Response models with examples
- ✓ Try it out functionality
- ✓ Error response documentation

## 💻 Development

### Environment Variables

```env
# External API Configuration
API_URL=https://jsonplaceholder.typicode.com

# Debug Mode
DEBUG=False

# Server Configuration
HOST=0.0.0.0
PORT=3000
```

### Type Checking

The project uses **beartype** for runtime type checking:

```python
@beartype
def get_all_users(self) -> ResponseModel:
    """Method with runtime type validation"""
    return self.userService.getAllUser()
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.121.1 | Web framework |
| uvicorn | 0.38.0 | ASGI server |
| pydantic | 2.12.4 | Data validation |
| beartype | 0.22.5 | Runtime type checking |
| requests | 2.32.5 | HTTP client |
| python-dotenv | 1.2.1 | Environment variables |

## 🐳 Docker

### Quick Start with Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop
docker-compose down
```

### Manual Docker Build and Run

```bash
# Build image
docker build -t user-api:latest -f cmd/backend/Dockerfile .

# Run container
docker run -p 3000:3000 user-api:latest

# Run with environment variables
docker run -p 3000:3000 \
  -e API_URL=https://jsonplaceholder.typicode.com \
  -e DEBUG=False \
  user-api:latest
```

### Using Build Script

```bash
# Build and test
bash build.sh

# Build and push to registry
bash build.sh push ghcr.io/username/user-api
```

### Image Details

- **Base Image**: `python:3.11-slim`
- **Image Size**: ~200-250 MB (optimized with multi-stage build)
- **Port**: 3000
- **Non-root User**: appuser (UID: 1000)
- **Health Check**: Enabled

### Production Deployment

See [DOCKER.md](DOCKER.md) for:
- ✓ Multi-stage Dockerfile explanation
- ✓ Docker Compose configuration
- ✓ Server deployment guide
- ✓ Nginx reverse proxy setup
- ✓ Security best practices
- ✓ Troubleshooting guide

## ✅ Testing

### Test Health Endpoint

```bash
# Using curl
curl http://localhost:3000/health

# Get users
curl http://localhost:3000/api/v1/users

# Using httpie
http localhost:3000/health
http localhost:3000/api/v1/users
```

### Test Docker Image

```bash
# Build
docker build -t user-api:latest -f cmd/backend/Dockerfile .

# Test import
docker run user-api:latest python -c "from cmd.backend.app import app; print('✓ Application loaded')"

# Run and test endpoint
docker run -d -p 3000:3000 user-api:latest
sleep 2
curl http://localhost:3000/health
docker ps -q | xargs docker stop
```

## 📖 Documentation Files

- **[DOCKER.md](DOCKER.md)** - Complete Docker setup, deployment, and troubleshooting
- **[Swagger UI](http://localhost:3000/api/docs)** - Interactive API documentation
- **[ReDoc](http://localhost:3000/redoc)** - Alternative API documentation

## 🛠️ Troubleshooting

### Module Import Errors

```bash
# Verify virtual environment
which python  # Should be in venv/bin/

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check installed packages
pip list
```

### Port Already in Use

```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Use different port
python -m cmd.backend.app --port 8001
```

### Docker Build Issues

```bash
# Clean build (no cache)
docker build --no-cache -t user-api:latest -f cmd/backend/Dockerfile .

# Debug build output
docker build --progress=plain -t user-api:latest -f cmd/backend/Dockerfile .

# Check Docker daemon
docker version
```

### API Returns 500 Error

```bash
# Check application logs
docker logs user-api

# Verify API_URL environment variable
docker inspect user-api | grep -i api_url

# Test connectivity to JSONPlaceholder
curl https://jsonplaceholder.typicode.com/users/1
```

## 🔐 Security Features

✅ **Implemented:**
- Non-root Docker user (appuser, UID: 1000)
- No hardcoded secrets (environment variables only)
- Type validation with beartype
- Input validation with Pydantic
- Health check endpoint for monitoring
- `.dockerignore` to exclude sensitive files
- Multi-stage build to reduce attack surface

## 📋 Project Checklist

- [x] Hexagonal Architecture implementation
- [x] FastAPI REST API
- [x] Swagger/OpenAPI documentation
- [x] Docker containerization
- [x] Docker Compose configuration
- [x] Build automation script
- [x] Environment configuration
- [x] Health check endpoint
- [ ] Unit tests
- [ ] Integration tests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Database integration
- [ ] Authentication (JWT)
- [ ] Rate limiting
- [ ] Request logging

## 📄 License

MIT License - feel free to use this as a template for your projects.

## 🎯 Next Steps

1. **Understand Architecture**: Review the hexagonal architecture pattern in `core/`
2. **Extend Services**: Add new service implementations in `core/services/`
3. **Add Repositories**: Implement new repository adapters in `core/repositories/`
4. **Dockerize**: Use provided Dockerfile for production deployment
5. **Add Tests**: Implement unit and integration tests
6. **Deploy**: Follow [DOCKER.md](DOCKER.md) for production deployment

## 💡 Example: Adding a New Feature

```python
# 1. Create repository interface in core/repositories/
class UserRepository(ABC):
    @abstractmethod
    def get_users(self) -> List[User]:
        pass

# 2. Implement repository adapter
class UserRepositoryImpl(UserRepository):
    def get_users(self) -> List[User]:
        # Implementation here
        pass

# 3. Create service
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self) -> List[User]:
        return self.repo.get_users()

# 4. Add handler
class UserHandler:
    def __init__(self, service: UserService):
        self.service = service

    def get_users(self):
        return self.service.list_users()

# 5. Add FastAPI endpoint
@app.get("/api/v1/users")
def get_users(handler: UserHandler):
    return handler.get_users()
```

---

**Built with FastAPI & Hexagonal Architecture** 🚀

For questions or issues, check [DOCKER.md](DOCKER.md) or review the Swagger documentation at `/api/docs`.
