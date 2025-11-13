#!/bin/bash

# ================================================================
# Docker Build Script
# ================================================================

set -e

# Configuration
IMAGE_NAME="user-api"
IMAGE_TAG="latest"
REGISTRY="${DOCKER_REGISTRY:-}"  # Set your Docker registry (e.g., ghcr.io/username)
DOCKERFILE="cmd/backend/Dockerfile"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Build Docker image
build_image() {
    print_info "Building Docker image: $IMAGE_NAME:$IMAGE_TAG"

    docker build \
        -t $IMAGE_NAME:$IMAGE_TAG \
        -f $DOCKERFILE \
        .

    if [ $? -eq 0 ]; then
        print_info "Docker image built successfully!"
    else
        print_error "Failed to build Docker image"
        exit 1
    fi
}

# Tag image for registry
tag_image() {
    if [ -z "$REGISTRY" ]; then
        print_warning "No registry specified. Skipping push."
        return
    fi

    FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
    print_info "Tagging image as: $FULL_IMAGE_NAME"

    docker tag $IMAGE_NAME:$IMAGE_TAG $FULL_IMAGE_NAME
}

# Push image to registry
push_image() {
    if [ -z "$REGISTRY" ]; then
        print_warning "No registry specified. Skipping push."
        return
    fi

    FULL_IMAGE_NAME="$REGISTRY/$IMAGE_NAME:$IMAGE_TAG"
    print_info "Pushing image to registry: $FULL_IMAGE_NAME"

    docker push $FULL_IMAGE_NAME

    if [ $? -eq 0 ]; then
        print_info "Docker image pushed successfully!"
    else
        print_error "Failed to push Docker image"
        exit 1
    fi
}

# Test image
test_image() {
    print_info "Testing Docker image..."

    docker run --rm \
        -e API_URL=https://jsonplaceholder.typicode.com \
        -e DEBUG=False \
        $IMAGE_NAME:$IMAGE_TAG \
        python -c "from cmd.backend.app import app; print('✓ Application loaded successfully')"

    if [ $? -eq 0 ]; then
        print_info "Image test passed!"
    else
        print_error "Image test failed"
        exit 1
    fi
}

# Show image info
show_info() {
    print_info "Image Information:"
    docker inspect $IMAGE_NAME:$IMAGE_TAG | python -m json.tool
}

# Main
main() {
    echo "================================================"
    echo "Docker Build Script"
    echo "================================================"
    echo ""
    echo "Image Name: $IMAGE_NAME"
    echo "Image Tag: $IMAGE_TAG"
    echo "Dockerfile: $DOCKERFILE"
    echo "Registry: ${REGISTRY:-None (local only)}"
    echo ""

    # Build
    build_image

    # Test
    test_image

    # Tag and push if registry is set
    if [ ! -z "$REGISTRY" ]; then
        tag_image
        push_image
    fi

    print_info "Build complete!"
    print_info "To run locally: docker run -p 3000:3000 $IMAGE_NAME:$IMAGE_TAG"
}

# Parse arguments
if [ "$1" == "push" ]; then
    if [ -z "$2" ]; then
        print_error "Registry URL required. Usage: ./build.sh push <registry-url>"
        exit 1
    fi
    DOCKER_REGISTRY=$2
fi

main
