# pip: Python Package Installer

`pip` is the standard package manager for Python. It allows you to install, upgrade, and manage Python packages that are not included in the standard library. It downloads packages from the Python Package Index (PyPI) and helps manage project dependencies efficiently.

## Most Frequently Used pip Commands

### 1. Install Packages
Install the latest version of a package:
```bash
$ pip install package_name
$ pip install package_name==1.2.3
$ pip install uv==3.10
$ pip install -r requirements.txt
```
### 2. Upgrade a package to the latest 
```bash
$pip install --upgrade package_name
```
### 3. Uninstalling a package
```bash
$ pip uninstall package_name
$ pip uninstall -r requirements.txt
$ pip uninstall -y package_name
```
### 4. Listing package
```bash
$ pip list
$ pip list --outdated
$ pip list --uptodate
$ pip show package_name # check package info
```

### 5. Save the list to `requirements.txt` for reproducibility:
```bash
$ pip freeze
$ pip freeze > requriements.txt
```

#### About pip
```bash 
$ python.exe -m pip install --upgrade pip
$ pip check
$ pip install --upgrade pip
```


