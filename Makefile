.PHONY: install test format lint clean run example

# Poetry installation and environment setup
install:
	@echo "Installing dependencies..."
	poetry install

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
