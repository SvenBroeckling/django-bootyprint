# GitHub Actions Workflows

## Build and Publish Workflow

The `build-and-publish.yml` workflow handles:

1. Running tests for every push to main and pull requests
2. Building and publishing the package to PyPI when a new tag is pushed

### Workflow Triggers

- Push to `main` branch
- Push of tags matching pattern `v*` (e.g., v0.1.0)
- Pull requests to `main` branch

### Jobs

#### Test

Runs the test suite using pytest to ensure everything works correctly.

#### Build and Publish

Only runs when a tag is pushed. This job:

1. Builds the Python package
2. Validates the package with twine
3. Uploads the package to PyPI

### Required Secrets

To publish to PyPI, you need to add a secret called `PYPI_API_TOKEN` in your GitHub repository settings.

1. Generate a PyPI API token from your PyPI account
2. Add it as a secret in GitHub repository settings
