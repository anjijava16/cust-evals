# Makefile for Custom Evals

.PHONY: help install install-dev install-docs clean test docs-serve docs-build docs-deploy

help:
	@echo "Custom Evals - Available Commands"
	@echo "=================================="
	@echo ""
	@echo "Installation:"
	@echo "  make install       - Install package"
	@echo "  make install-dev   - Install with dev dependencies"
	@echo "  make install-docs  - Install documentation dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run tests"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs-serve    - Serve docs locally (http://127.0.0.1:8000)"
	@echo "  make docs-build    - Build static docs site"
	@echo "  make docs-deploy   - Deploy docs to GitHub Pages"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove build artifacts"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-docs:
	pip install mkdocs mkdocs-material pymdown-extensions

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	pytest tests/

# Documentation commands
docs-serve:
	@echo "Starting documentation server..."
	@echo "Open http://127.0.0.1:8000 in your browser"
	@echo "Press Ctrl+C to stop"
	mkdocs serve

docs-build:
	@echo "Building documentation site..."
	mkdocs build
	@echo "Documentation built in site/ directory"

docs-deploy:
	@echo "Deploying documentation to GitHub Pages..."
	mkdocs gh-deploy --force
	@echo "Documentation deployed to GitHub Pages!"
