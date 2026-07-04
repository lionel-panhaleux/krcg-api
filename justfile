# Default recipe to list all available recipes
default:
    @just --list

# Install the project in editable mode with dev dependencies
install:
    uv pip install -e ".[dev]"

# Ensure we're on master branch and working tree is clean
check:
    @echo "🔍 Checking release prerequisites..."
    @if [[ "$(git branch --show-current)" != "master" ]]; then echo "❌ Not on master branch"; exit 1; fi
    @if [[ -n "$(git status --porcelain)" ]]; then echo "❌ Working directory is dirty"; exit 1; fi
    @echo "✅ Release checks passed!"

# Check code quality (formatting, linting, OpenAPI spec)
quality:
    @echo "🔍 Running quality checks..."
    uv run ruff check
    uv run ruff format --check
    uv run ty check krcg_api
    @echo "✅ Quality checks passed!"

# Run tests (depends on quality checks)
test: quality
    @echo "🧪 Running tests..."
    uv run pytest -vvs
    @echo "✅ Tests passed!"

# Start the API server
serve:
    uv run uvicorn krcg_api:application --reload

# Clean build artifacts
clean-build:
    @echo "🧹 Cleaning build artifacts..."
    rm -rf build dist
    @echo "✅ Cleaned!"

# Clean build and cache artifacts
clean: clean-build
    @echo "🧹 Cleaning cache..."
    rm -rf .pytest_cache .ruff_cache
    @echo "✅ Cleaned!"

# Bump the version, tag, and push (level: minor | major)
bump level="minor": check
    #!/usr/bin/env bash
    set -euo pipefail
    uv version --bump "{{ level }}"
    VERSION="$(uv version --short)"
    echo "📝 Committing version ${VERSION}..."
    git add pyproject.toml CHANGES.md
    git commit -m "Release ${VERSION}" && git tag "v${VERSION}"
    echo "📤 Pushing to remote..."
    git push origin master --tags

# Update CHANGELOG.md with release notes, clear CHANGES.md
changelog:
    #!/usr/bin/env bash
    set -euo pipefail
    VERSION="$(uv version --short)"
    DATE="$(date +%Y-%m-%d)"
    echo "📝 Updating changelog..."
    { echo "# Changelog"; echo; echo "## ${VERSION} (${DATE})"; echo; cat CHANGES.md; echo; tail -n +2 CHANGELOG.md; } > CHANGELOG.tmp
    mv CHANGELOG.tmp CHANGELOG.md
    > CHANGES.md
    git add CHANGELOG.md CHANGES.md
    git commit -m "Update changelog"
    git push origin master

# Create a release (bump, tag, push — CI handles PyPI + GitHub release)
release level="minor": clean-build check test
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ ! -s CHANGES.md ]] || [[ -z "$(tr -d '[:space:]' < CHANGES.md)" ]]; then
        echo "❌ CHANGES.md is empty — add release notes before releasing"
        exit 1
    fi
    just bump {{ level }}
    just changelog

# Update all dependencies to latest versions
update:
    uv sync --upgrade
