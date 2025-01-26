# Nastran To Kratos

This repository stores code for converting between nastran and kratos simulation files. You can see examples of this in the `example` directory

# How to Use It

## Importing the Functions

If you simply want to use the functions from this repo, you can import them similar to other external dependencies like `numpy`. Once you have installed the repo (see below), you can import is via
```python
from nastran_to_kratos import nastran_to_kratos, kratos_to_nastran, ...
```

### Using Poetry (recommended)

If you use poetry (which is good practice in professional python repos) then you can add the following line to your `[tool.poetry.dependencies]` section in your `pyproject.toml`
```toml
nastran_to_kratos = { git = "git@gitlab.lrz.de:tobias_group/nastran_to_kratos.git", branch = "main" }
```

### Using Pip

The same is possible when you use the default python package manager `pip`. Just enter the following line into your terminal:
```bash
pip install git+ssh://git@gitlab.lrz.de/tobias_group/nastran_to_kratos.git@main
```
Just make sure you update your packages every once in a while!

## Contributing to the Repository

Hi, so you are the next contributor to this repo? Welcome onboard! I have tried to optimize the code for maintainability so that you don't have to spend too much time reading into it. However, that comes with a few prerequisites that ensure that you can hand over high-quality code to the next maintainer. To get started you need to
1. Install [python](https://www.python.org/downloads/) with a version higher or equal to `3.10` (higher is better tho). You can check by running `python --version` in your terminal
2. Check if python virtual environment is installed as well with `python -m venv --help` (it is not included in all python distributions)
3. Create a virtual environment by opening a terminal window in this repository and running `python -m venv .venv`
4. Activate your virtual environment by running `.venv/Scripts/activate` if you are on Windows or `source .venv/bin/activate` if you are on Linux/MacOS
5. Install [poetry](https://python-poetry.org/)
6. Install the dependencies by typing `poetry install` into your terminal
7. Verify installation with a terminal application called `pytest`
8. Install [pre-commit](https://pre-commit.com/) to your system
9. Initiate pre-commit in this repo via `pre-commit install`
10. (recommended) if you are using Visual Studio Code, also install the [python](https://marketplace.visualstudio.com/items?itemName=ms-python.python), [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) and [mypy](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker) extensions

Now that you are ready, I highly suggest you read the [wiki entry for code quality](https://gitlab.lrz.de/tobias_group/nastran_to_kratos/-/wikis/Code-Quality) to understand the principles of high quality code.

### Committing Your Code

If you followed every step of the installation guide above you might notice that your commits take a few seconds longer than they used to or they fail with an error message. This is because I snuck in `pre-commit`, which will be your worst enemy (in the beginning) but this repository's best friend. `pre-commmit` ensures that the code quality is up to the standard before you are even allowed to commit. This means that no bad code can make it to the git history and you can safely revert to any commit in this timeline - isn't his amazing? 

`pre-commit` runs a few checks like a linter, a formatter, a type checker and the unit tests. If your commit fails, than often the issues (like formatting) have automatically been fixed and if you stage and commit again, it might already work. If it still fails, then carefully read the error message and fix the issues. I know it is frustrating at first, but it ensures that everyone will be able to read your code in the future, including you.

### Adding Dependencies

Since this repo uses `poetry` instead of `pip` to manage dependencies, adding a new library is a little different. If before you added an external package like this:
```bash
pip install <package>  # <- do not do this!
```
now you need to do it like this:
```bash
poetry add <package>   # <- do this
```