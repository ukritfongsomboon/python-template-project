# ============================================================================
# Makefile for Python Hexagonal Template
# ============================================================================

# help: Create and display virtual environment setup instructions
help:
	@echo "To activate the virtual environment, run:"
	@echo "  source venv/bin/activate"
	@echo ""
	@echo "To deactivate the virtual environment, run:"
	@echo "  deactivate"
	@echo ""

init:
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv venv; \
	fi
	@echo ""
	@echo "Virtual environment created/exists in ./venv"
	@echo ""

# env: Create virtual environment and generate requirements.txt
# This will freeze all installed packages into requirements.txt
# env:
# 	@if [ ! -d "venv" ]; then \
# 		echo "Creating virtual environment..."; \
# 		python3 -m venv venv; \
# 	fi
# 	@bash -c "source venv/bin/activate && pip freeze > requirements.txt && echo 'requirements.txt created successfully'"

# install: Install all dependencies from requirements.txt
install:
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv venv; \
	fi
	@bash -c "source venv/bin/activate && pip install -r requirements.txt && echo 'All dependencies installed successfully'"
	@bash -c "source venv/bin/activate && pip freeze > requirements.txt && echo 'requirements.txt created successfully'"

# list: Display all installed packages (pip freeze)
list:
	@bash -c "source venv/bin/activate && pip freeze"
	@bash -c "source venv/bin/activate && pip freeze > requirements.txt"

# run: Start the backend application
run:
	@bash -c "source venv/bin/activate && pip freeze > requirements.txt"
	python3 ./cmd/backend/app.py

# migration: Run database migration scripts
migration:
	@bash -c "source venv/bin/activate && pip freeze > requirements.txt"
	python3 ./cmd/migration/app.py

# clean: Remove all __pycache__ directories and Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	echo "Cleaned up __pycache__, Python cache files, and .DS_Store"