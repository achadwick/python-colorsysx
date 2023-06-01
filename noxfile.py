import os
import nox

# Roughly the approach in https://hynek.me/articles/python-app-deps-2018/

nox.options.sessions = ["tests", "lint"]
MAIN_PYTHON = "3.11"
PYTHONS = [MAIN_PYTHON] + ["3.10", "3.9"]


def _sync_venv(session):
    """Sync the current virtualenv with a pip-sync, if reusing venvs."""
    pip_sync = "pip-sync-faster"
    requirements = [
        f"requirements/dev-{session.python}.txt",
    ]
    if not os.path.exists(os.path.join(session.bin, pip_sync)):
        for req in requirements:
            session.install("-r", req)
    session.run(pip_sync, *requirements)


@nox.session(reuse_venv=True, python=PYTHONS)
def tests(session):
    """Run the test suites."""
    _sync_venv(session)
    session.run('pytest', '-p', 'no:cacheprovider', 'tests')


@nox.session(reuse_venv=True, python=MAIN_PYTHON)
def run(session):
    """Run a command (command following '--')"""
    _sync_venv(session)
    session.install(".")
    session.run(*session.posargs)


@nox.session(reuse_venv=True, python=MAIN_PYTHON)
def lint(session):
    """Run the flake8 linter."""
    _sync_venv(session)
    session.run('flake8', 'colorsysx')


@nox.session(reuse_venv=True, python=MAIN_PYTHON)
def repl(session):
    """Invoke a ptpython repl with all deps installed, in a venv."""
    if not session.interactive:
        session.error("Cannot run ptpython non-interactively")
    else:
        _sync_venv(session)
        session.run("ptpython")


@nox.session(reuse_venv=False, python=PYTHONS)
def freeze(session):
    """Update requirements/*.txt for a new development cycle."""
    session.install(".[dev]")
    session.run(
        "pip-compile",
        f"--output-file=requirements/dev-{session.python}.txt",
        "--resolver=backtracking",
        "--extra=dev",
        "--quiet",
        "--no-upgrade",
        "pyproject.toml",
    )
