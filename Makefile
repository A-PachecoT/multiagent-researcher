.PHONY: help install test format lint clean run example setup

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
	poetry run pytest tests/ --cov=src --cov-report=term-missing

# Format code with black and isort
format:
	@echo "Formatting code..."
	poetry run black src/
	poetry run isort src/

# Run linting checks
lint:
	@echo "Running linting checks..."
	poetry run flake8 src/
	poetry run black --check src/
	poetry run isort --check-only src/

# Clean up cache files
clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

# Run the example
example:
	@echo "Running research example..."
	poetry run python src/examples/research_example.py

# Run specific research topic
run:
	@echo "Running research..."
	poetry run python src/main.py

# Setup initial project structure
setup: install
	@echo "Creating necessary directories..."
	mkdir -p src/tests
	touch .env
	@echo "OPENAI_API_KEY=your-api-key-here" > .env
	@echo "Project setup complete. Don't forget to add your OpenAI API key to .env"
