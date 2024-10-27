.PHONY: help install test format lint clean run example setup

# Variables
PYTHON = poetry run python
PYTEST = poetry run pytest
BLACK = poetry run black
ISORT = poetry run isort
FLAKE8 = poetry run flake8
SRC_DIR = src
PYTHONPATH = PYTHONPATH=$(SRC_DIR)

# Default target
help:
	@echo "Available commands:"
	@echo "  make help       Show this help message"
	@echo "  make install    Install project dependencies"
	@echo "  make test       Run tests with coverage"
	@echo "  make format     Format code using Black and isort"
	@echo "  make lint       Run linters (flake8, black, and isort)"
	@echo "  make clean      Remove cache files"
	@echo "  make run        Run the research script"
	@echo "  make example    Run the research example"
	@echo "  make setup      Setup initial project structure"

# Poetry installation and environment setup
install:
	@echo "Installing dependencies..."
	@if [ ! -f pyproject.toml ]; then \
		echo "Error: pyproject.toml not found. Make sure you're in the correct directory."; \
		exit 1; \
	fi
	poetry install --no-root

# Run tests with coverage
test:
	@echo "Running tests..."
	$(PYTHONPATH) $(PYTEST) $(SRC_DIR)/tests --cov=$(SRC_DIR) --cov-report=term-missing

# Format code with black and isort
format:
	@echo "Formatting code..."
	$(BLACK) $(SRC_DIR)
	$(ISORT) $(SRC_DIR)

# Run linting checks
lint:
	@echo "Running linting checks..."
	$(FLAKE8) $(SRC_DIR)
	$(BLACK) --check $(SRC_DIR)
	$(ISORT) --check-only $(SRC_DIR)

# Clean up cache files
clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

# Run the example
example:
	@echo "Running research example..."
	$(PYTHONPATH) $(PYTHON) $(SRC_DIR)/examples/research_example.py

# Run specific research topic
run:
	@echo "Running research..."
	$(PYTHONPATH) $(PYTHON) $(SRC_DIR)/main.py

# Setup initial project structure
setup: install
	@echo "Creating necessary directories..."
	mkdir -p $(SRC_DIR)/tests
	mkdir -p $(SRC_DIR)/examples
	touch .env
	@echo "OPENAI_API_KEY=your-api-key-here" > .env
	@echo "Project setup complete. Don't forget to add your OpenAI API key to .env"
