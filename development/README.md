# Dev Environment Setup

The shell scripts in this project assume that a [virtual environment](https://docs.python.org/3/library/venv.html) is being used at `{root}/venv/`.

Python dependencies are listed in [requirements.txt](./requirements.txt).

## Setting up virtual environment

Please run `sh development/createVirtualEnvAndInstallDependencies.sh` to automatically create the venv, source it and install the pip dependencies at [requirements.txt](./requirements.txt).

> Alternatively, you can run `pip install -r requirements.txt` to install dependencies directly using the active pip.
>
> Note: if you do this, please run all the python scripts directly (in other words, don't use the shell scipts, because they try to `source` venv).

## Git Hooks

You can install git hooks using `sh development/installGitHooks.sh`.

### pre-commit hook

The pre commit hook will run [../runTests.sh](../runTests.sh), which will run unit tests under [tests/](../tests/).
