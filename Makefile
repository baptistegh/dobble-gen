ARGS ?= 

.PHONY: install
install: | install-uv
	@uv sync --locked --dev

.PHONY: install-uv
.ONESHELL:
install-uv:
	@command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up the virtual environment and install dependencies
.PHONY: lint
lint: 
	@uv run mypy src/
	@uv run ruff check --diff
	@uv run ruff format --check --diff

.PHONY: style
style:
	@uv run mypy src/
	@uv run ruff check --fix
	@uv run ruff format

# Run the application
.PHONY: run
run:
	@uv run dobble-gen run $(ARGS)

# Clean up the virtual environment
.PHONY: clean
clean:
	@find . -type d -name __pycache__ | xargs rm -rf;
	@rm -rf .mypy_cache/ .ruff_cache/ dist/
