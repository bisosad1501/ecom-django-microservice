# Contributing Guidelines

Thank you for your interest in contributing to the Recommendation Service! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

We expect all contributors to adhere to our code of conduct. Please be respectful, inclusive, and considerate in all interactions within this project.

## Getting Started

1. Fork the repository
2. Clone your fork to your local machine
3. Set up the development environment as described in the README.md
4. Create a new branch for your feature or bug fix

## Development Workflow

1. Ensure you have the latest changes from the main branch:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, commit them with clear and descriptive commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) format:
   ```
   feat: add new recommendation algorithm
   fix: resolve issue with caching
   docs: update API documentation
   test: add tests for sentiment recommendations
   ```

3. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a pull request against the main repository

## Pull Request Process

1. Ensure your PR includes the following:
   - A clear description of the changes
   - Any relevant issue numbers
   - Tests for new functionality
   - Updated documentation if necessary

2. Address any feedback from code reviews
3. Maintain the PR until it's merged or closed

## Coding Standards

We follow PEP 8 style guidelines for Python code. Additionally:

- Use type hints where possible
- Write docstrings for all functions, classes, and modules
- Keep functions focused on a single responsibility
- Use meaningful variable and function names

We use the following tools for code quality:
- `flake8` for linting
- `black` for code formatting
- `isort` for import sorting

You can set up pre-commit hooks to run these automatically:
```bash
pip install pre-commit
pre-commit install
```

## Testing Guidelines

- Write unit tests for all new functionality
- Ensure all existing tests pass before submitting a PR
- Aim for high test coverage (>90%)
- Include both positive and negative test cases

Run tests with:
```bash
pytest
```

For coverage:
```bash
pytest --cov=src tests/
```

## Documentation

- Keep the README.md up to date
- Update API documentation for any changed or new endpoints
- Document complex algorithms and design decisions
- Add comments explaining non-obvious code segments

## Dependency Management

- Minimize dependencies when possible
- Pin dependency versions in requirements.txt
- Document the purpose of new dependencies in PR descriptions

## Questions?

If you have any questions or need help, please open an issue or contact the maintainers. 