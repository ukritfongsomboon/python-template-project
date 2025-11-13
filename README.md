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
- [Makefile Commands](#makefile-commands)
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

The API uses **OpenAPI 3.0** specification with multiple interactive documentation formats powered by FastAPI.

### Base URL
```
http://localhost:3000
```

### Documentation Endpoints

Access the API documentation through these interactive interfaces:

| Format | URL | Features |
|--------|-----|----------|
| **Swagger UI** | http://localhost:3000/api/docs | Interactive UI, "Try it out", Schema exploration |
| **ReDoc** | http://localhost:3000/redoc | Modern read-only documentation |
| **OpenAPI JSON** | http://localhost:3000/openapi.json | Raw OpenAPI 3.0 specification |

### 🌐 Swagger UI Guide

**Access:** http://localhost:3000/api/docs

#### Features

Swagger UI provides an interactive interface to explore and test your API:

- **Endpoint Overview**: See all available endpoints grouped by tags
- **Try It Out**: Execute real API requests directly from the browser
- **Request/Response Examples**: View sample data for each endpoint
- **Schema Exploration**: Inspect data models and their properties
- **Authorization**: Configure authentication headers (if required)
- **Response Examples**: Preview different response codes and formats

#### How to Use Swagger UI

1. **Find an Endpoint**
   - Scroll through the endpoint list
   - Click on an endpoint to expand it

2. **View Details**
   - Read the endpoint description
   - Check required parameters and headers
   - Review response models and examples

3. **Try It Out**
   - Click the "Try it out" button
   - Fill in any required parameters or request body
   - Click "Execute" to send the request
   - View the response status, headers, and body

4. **Explore Models**
   - Scroll to the bottom to see all data models
   - Click on a model to expand and view its structure
   - Understand required fields and their types

#### Example: Testing the Users Endpoint

```
1. Open http://localhost:3000/api/docs
2. Find "GET /api/v1/users" endpoint
3. Click on it to expand
4. Click "Try it out" button
5. Click "Execute" button
6. View the response with all users
```

### 📖 ReDoc Guide

**Access:** http://localhost:3000/redoc

**Best for:**
- Generating static documentation
- Reading-only mode (no request execution)
- Cleaner, more traditional API documentation format
- Printing and exporting documentation
- Mobile-friendly viewing

### API Endpoints

#### Get All Users
```http
GET /api/v1/users
```

**Description:** Retrieve all users from the JSONPlaceholder API

**Parameters:** None

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

**Response (500):**
```json
{
  "status": false,
  "code": 500,
  "message": "Failed to retrieve users",
  "data": null
}
```

#### Health Check
```http
GET /health
```

**Description:** Check if the API is running and healthy

**Parameters:** None

**Response (200):**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

### API Response Format

All API responses follow a consistent format:

```json
{
  "status": true|false,           // Boolean indicating success/failure
  "code": 200|400|404|500|...,   // HTTP status code
  "message": "string",            // Human-readable message
  "data": {}|[]|null              // Response payload or null on error
}
```

### Request Headers

Common headers supported by the API:

```bash
# Content-Type (usually automatic)
Content-Type: application/json

# User-Agent (optional)
User-Agent: MyApp/1.0

# Accept (optional)
Accept: application/json
```

### Example API Requests

#### Using curl

```bash
# Get all users
curl http://localhost:3000/api/v1/users

# Check health
curl http://localhost:3000/health

# With headers
curl -H "Content-Type: application/json" \
  http://localhost:3000/api/v1/users
```

#### Using httpie

```bash
# Get all users
http localhost:3000/api/v1/users

# Check health
http localhost:3000/health

# Pretty print with verbose output
http -v localhost:3000/api/v1/users
```

#### Using Python requests

```python
import requests

# Get all users
response = requests.get('http://localhost:3000/api/v1/users')
print(response.json())

# Check health
health = requests.get('http://localhost:3000/health')
print(health.json())

# Handle errors
if response.status_code == 200:
    users = response.json()['data']
else:
    error = response.json()['message']
    print(f"Error: {error}")
```

#### Using JavaScript/Fetch

```javascript
// Get all users
fetch('http://localhost:3000/api/v1/users')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));

// Using async/await
async function getUsers() {
  const response = await fetch('http://localhost:3000/api/v1/users');
  const data = await response.json();
  console.log(data);
}
```

### OpenAPI Specification

#### Export OpenAPI JSON

```bash
# Get the raw OpenAPI specification
curl http://localhost:3000/openapi.json > openapi.json

# View in formatted JSON
curl http://localhost:3000/openapi.json | python -m json.tool
```

#### Generate Client Code

Use the OpenAPI specification to generate API clients for different languages:

```bash
# Using OpenAPI Generator (JavaScript)
openapi-generator-cli generate \
  -i http://localhost:3000/openapi.json \
  -g javascript \
  -o generated-client/

# Using Swagger Codegen (Python)
swagger-codegen generate \
  -i http://localhost:3000/openapi.json \
  -l python \
  -o generated-client/

# For other languages and tools, see:
# https://openapi-generator.tech/
```

### Swagger UI Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + F` | Search endpoints |
| `Click endpoint` | Expand/collapse details |
| `Try it out` | Enable request editor |
| `Execute` | Send the request |

### Troubleshooting API Documentation

#### Swagger UI Not Loading

```bash
# Verify the API is running
curl http://localhost:3000/health

# Check if Swagger endpoint is accessible
curl http://localhost:3000/api/docs

# Check API logs for errors
docker logs <container-name>
```

#### CORS Issues with Swagger UI

If testing cross-origin requests from Swagger:

```bash
# The application already handles CORS for local development
# For production, configure CORS in the FastAPI app:
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Response Codes

| Code | Description |
|------|-------------|
| `200` | Success - Request completed successfully |
| `400` | Bad Request - Invalid request parameters |
| `404` | Not Found - Resource not found |
| `500` | Internal Server Error - Server error occurred |
| `503` | Service Unavailable - API temporarily unavailable |

### Best Practices for API Testing

1. **Start with Health Check**
   ```bash
   curl http://localhost:3000/health
   ```

2. **Use Swagger UI for Exploration**
   - Visit http://localhost:3000/api/docs
   - Try endpoints directly from the browser

3. **Test Error Scenarios**
   - Invalid parameters
   - Missing required fields
   - Network timeouts

4. **Monitor Response Times**
   - Use Swagger UI's network tab
   - Check logs for slow queries

5. **Validate Response Structure**
   - Always check the `status` field
   - Verify `data` payload matches schema
   - Handle error messages gracefully

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

## 🛠️ Makefile Commands

The project includes a Makefile to streamline common development tasks:

### Quick Reference

```bash
# View help information
make help

# Initialize virtual environment
make init

# Install dependencies (creates venv if needed)
make install

# List all installed packages
make list

# Run the application
make run

# Run database migrations
make migration

# Clean up Python cache files
make clean
```

### Detailed Command Documentation

#### `make help`
Displays instructions for activating and deactivating the virtual environment.

**Usage:**
```bash
make help
```

#### `make init`
Creates a Python virtual environment in the `./venv` directory. Safe to run multiple times (won't recreate if already exists).

**Usage:**
```bash
make init
```

**Output:**
```
Creating virtual environment...
Virtual environment created/exists in ./venv
```

#### `make install`
Creates a virtual environment (if needed) and installs all dependencies from `requirements.txt`. Also freezes the installed packages back to `requirements.txt`.

**Usage:**
```bash
make install
```

**What it does:**
1. Creates venv if it doesn't exist
2. Installs all dependencies from requirements.txt
3. Freezes current packages to requirements.txt

#### `make list`
Lists all installed packages in the virtual environment and updates `requirements.txt`.

**Usage:**
```bash
make list
```

**Output:**
```
fastapi==0.121.1
uvicorn==0.38.0
pydantic==2.12.4
...
```

#### `make run`
Starts the FastAPI backend application. Updates requirements.txt before running.

**Usage:**
```bash
make run
```

**Accesses:**
- API: http://localhost:3000
- Swagger UI: http://localhost:3000/api/docs
- Health Check: http://localhost:3000/health

#### `make migration`
Runs database migration scripts located in `cmd/migration/app.py`.

**Usage:**
```bash
make migration
```

#### `make clean`
Removes all Python cache files including:
- `__pycache__` directories
- `.pyc` files
- `.pyo` files
- `.DS_Store` files

**Usage:**
```bash
make clean
```

**Output:**
```
Cleaned up __pycache__, Python cache files, and .DS_Store
```

### Recommended Workflow

```bash
# 1. Initial setup
make init
make install

# 2. View help (optional)
make help

# 3. Run the application
make run

# 4. When done or before committing
make clean
make list
```

### Windows Users

The Makefile uses bash syntax. For Windows, consider:

1. **Using Windows Subsystem for Linux (WSL):**
   ```bash
   wsl make install
   wsl make run
   ```

2. **Using Git Bash:**
   ```bash
   bash -c "make install"
   bash -c "make run"
   ```

3. **Manual commands:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python cmd/backend/app.py
   ```

## 🐳 Docker

The project includes optimized Docker configuration for containerized deployment with multi-stage builds, security hardening, and comprehensive health checks.

### Docker Quick Start

#### Using Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f api

# View container status
docker-compose ps

# Stop the application
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild images and start
docker-compose up -d --build
```

**Output:**
```
Creating user-api-api-1 ... done
Attaching to user-api-api-1
api-1  | INFO:     Uvicorn running on http://0.0.0.0:3000
```

#### Manual Docker Build and Run

```bash
# Build image
docker build -t user-api:latest -f cmd/backend/Dockerfile .

# Run container
docker run -p 3000:3000 user-api:latest

# Run with environment variables
docker run -p 3000:3000 \
  -e API_URL=https://jsonplaceholder.typicode.com \
  -e DEBUG=False \
  -e HOST=0.0.0.0 \
  -e PORT=3000 \
  user-api:latest

# Run with custom name and detached mode
docker run -d --name my-api \
  -p 3000:3000 \
  -e API_URL=https://jsonplaceholder.typicode.com \
  user-api:latest

# View logs
docker logs -f my-api

# Stop container
docker stop my-api

# Remove container
docker rm my-api
```

### Using Build Script

The included `build.sh` script automates Docker image building and optional registry push:

```bash
# Build and test image locally
bash build.sh

# Build and push to container registry
bash build.sh push ghcr.io/username/user-api

# Build and push to Docker Hub
bash build.sh push docker.io/username/user-api
```

### Image Details

| Property | Value |
|----------|-------|
| **Base Image** | `python:3.11-slim` |
| **Image Size** | ~200-250 MB (optimized with multi-stage build) |
| **Port** | 3000 |
| **Non-root User** | appuser (UID: 1000) |
| **Health Check** | Enabled (30s interval, 10s timeout) |
| **Supported Architectures** | linux/amd64, linux/arm64 |

### Docker Compose Configuration

The `docker-compose.yml` includes:

```yaml
services:
  api:
    build:
      context: .
      dockerfile: cmd/backend/Dockerfile
    ports:
      - "3000:3000"
    environment:
      API_URL: https://jsonplaceholder.typicode.com
      DEBUG: "False"
      HOST: 0.0.0.0
      PORT: 3000
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    restart: unless-stopped
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Environment Variables in Docker

Configure these environment variables when running containers:

```env
# Required
API_URL=https://jsonplaceholder.typicode.com    # External API endpoint

# Optional
DEBUG=False                                       # Enable debug mode (True/False)
HOST=0.0.0.0                                     # Server host
PORT=3000                                        # Server port
```

**Example with custom environment:**
```bash
docker run -p 3000:3000 \
  -e API_URL=https://api.example.com \
  -e DEBUG=True \
  -e PORT=8000 \
  -p 8000:8000 \
  user-api:latest
```

### Multi-Stage Build Optimization

The Dockerfile uses a multi-stage build to reduce image size:

1. **Builder Stage**: Installs all build dependencies and requirements
2. **Production Stage**: Contains only runtime dependencies and application code

**Benefits:**
- Reduced final image size (~200MB vs ~400MB)
- Smaller attack surface
- Faster deployment
- Lower bandwidth requirements

### Docker Network Configuration

The application uses a custom bridge network (`app-network`) for container communication:

```bash
# View network details
docker network inspect user-api_app-network

# Connect additional containers to the network
docker run --network app-network --name other-service myimage
```

### Container Health Monitoring

Built-in health checks monitor application status:

```bash
# Check container health status
docker ps

# The output shows:
# STATUS: Up 5 minutes (healthy)
# STATUS: Up 2 minutes (unhealthy)

# View health check logs
docker inspect --format='{{json .State.Health}}' container-id | python -m json.tool
```

### Production Deployment

For comprehensive deployment guidance, security best practices, and troubleshooting, see [DOCKER.md](DOCKER.md) which includes:

- ✓ Multi-stage Dockerfile explanation and optimization
- ✓ Docker Compose advanced configuration
- ✓ Server deployment guide (AWS, Digital Ocean, etc.)
- ✓ Nginx reverse proxy setup
- ✓ SSL/TLS configuration with Let's Encrypt
- ✓ Security hardening best practices
- ✓ Performance optimization
- ✓ Troubleshooting guide and common issues
- ✓ Monitoring and logging setup

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
