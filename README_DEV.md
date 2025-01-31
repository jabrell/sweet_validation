# Environment setup

We use [uv](https://docs.astral.sh/uv/) for dependency management. Use

``
uv sync
``

to create an environment with all dev dependencies.


# Pre-commit hooks
We use pre-commit hooks. Linting and formatting takes place before pushing. To
enable this, you have to install the pre-push hook:

``
pre-commit install --hook-type pre-push
``

You can manually run the pre-push (and pre-commit) hooks using

``
pre-commit run --all-files --hook-stage pre-push
``

Fixing ruff issues can also done with

``
uvx ruff check --fixAll
``