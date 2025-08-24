venv --> to create virtual env --> requirements.txt
### Install uv package manager
```bash
$ pip install uv
```
### Working on project
uv is equivalent to npm basically a package manager.

###  to create project
```bash
$ uv init my-project
$ uv init my-proj --app
$ uv init my-proj --lib # if you want to build python packages
$ uv init -p 3.13.7 my-project-name
# pyproject.toml is like package.json file only
# uv.lock file --> similar to package-lock file

$ uv run main.py # uv creates a virtual environment by itself and then runs the script
$ uv add fastapi # to add any package inside project, it will automatically update pyproject.toml

# Even you can build binaries using uv makes wheels file
$ uv build 

$ uv #help

# running a file without installing packages required by it.
$ uv run --with 'falsk' --with 'requests' main.py

# This command will add all required pacakges into the script directly so we can relax in future
$ uv add --script main.py 'flask' 'requests'

# Listing dependency tree
$ uv tree
```
https://docs.astral.sh/uv/getting-started/installation/

```markdown
# uv: Fast Python Package & Project Manager

`uv` is an extremely fast all-in-one package and project manager for Python, written in Rust. Designed as a drop-in alternative to pip and pip-tools, it also replaces tools like pipx, poetry, pyenv, virtualenv, and twine, offering streamlined and much faster workflows for managing Python dependencies, virtual environments, and even Python versions[^2_1][^2_2][^2_3][^2_4]. Its core strengths include speed (10-100x faster than pip), unified project management, and a familiar CLI interface[^2_1][^2_4].

## Most Frequently Used uv Commands

### 1. Install Packages
Install a package:
```

uv pip install package_name

```
Install a specific version:
```

uv pip install package_name==1.2.3

```
Upgrade a package:
```

uv pip install --upgrade package_name

```
Install from a requirements file:
```

uv pip install -r requirements.txt

```
Install all dependencies from a pyproject (recommended modern format):
```

uv pip install

```
[^2_1][^2_3][^2_4]

### 2. Uninstall Packages
Remove a package:
```

uv pip uninstall package_name

```
Remove all from requirements:
```

uv pip uninstall -r requirements.txt

```
[^2_1][^2_4]

### 3. List & Show Packages
List installed packages:
```

uv pip list

```
Show package information:
```

uv pip show package_name

```
[^2_4]

### 4. Freeze Environment
Output installed packages (pip-compatible):
```

uv pip freeze

```
[^2_3][^2_4]

### 5. Managing Virtual Environments
Create and activate a new virtual environment:
```

uv venv new .venv
source .venv/bin/activate

```
Remove a virtual environment:
```

uv venv remove .venv

```
[^2_1][^2_4]

### 6. Python Version Management
Install a specific Python version:
```

uv python install 3.12

```
List available versions:
```

uv python list

```
Set global/local Python version:
```

uv python use 3.11

```
[^2_1][^2_4]

### 7. Project Initialization & Management
Start a new Python project (scaffold full structure):
```

uv init

```
[^2_1][^2_4]

### 8. Lock Dependencies
Generate a lockfile for reproducible environments:
```

uv pip compile

```
[^2_1][^2_3][^2_4]

### Additional Features
- Build and publish packages to PyPI:
```

uv publish

```
- Run scripts and development tools (pytest, Black, Ruff) via uv:
```

uv run pytest

```

## Further Reading

- Official documentation: https://docs.astral.sh/uv/
- Project homepage & binaries: https://astral.sh/uv/
- Real Python’s uv tutorial: https://realpython.com/python-uv/

---