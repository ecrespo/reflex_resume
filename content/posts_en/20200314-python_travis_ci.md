Title: Python tools for developing secure, quality code.
Date:  2020-03-14 15:33
Category: Tutorial de Python
Tags: Python,Flask,Quality Code,Secure,Pipenv,Safety, Bandit,Black,Mypy,
lang: en
translation: true
Slug: python-tools-security-quality-code
Authors: Ernesto Crespo
Summary: Python tools to secure your code and keep it high quality


This article is based on [Top Python Tools for Developing Secure, Quality Code](https://levelup.gitconnected.com/top-python-tools-for-developing-secure-quality-code-4b3f5ec1e2de). A basic application (Hello world) will be created in flask, incorporating a series of tools that make it possible to evaluate the code, checking among other things compliance with Python's PEP8 and the security of the code. The tools and their links are shown below:

* [Pipenv](https://github.com/pypa/pipenv): Pipenv is a tool that aims to bring the best of all packaging worlds (bundler, composer, npm, cargo, yarn, etc.) to the Python world. It automatically creates and manages a virtualenv for your projects, and also adds/removes packages from your Pipfile as you install/uninstall packages.

```bash
pip install pipenv
```

* [Safety](https://pyup.io/safety/): Safety checks your dependencies for known security vulnerabilities (Ochrona is the one recommended in the original article, but since there are no details for installing it, Safety will be used).

```bash
pip install safety  
```

* [Bandit](https://github.com/PyCQA/bandit): Bandit is a tool designed to find common security issues in Python code.

```bash
pip3 install bandit
```

* [Black](https://github.com/psf/black): The uncompromising Python code formatter (complying with Pep-8).

```bash
pip install black
```

* [Mypy](http://mypy-lang.org/): Mypy is an optional static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing.

```bash
pip install mypy
```

* [pylint](https://www.pylint.org): Checks compliance with PEP8.

```bash
pip install pylint
```

* [pycodestyle](https://github.com/pycqa/pycodestyle): Pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

```bash
pip install pycodestyle
```


You can see the source code used in the article on [Github](https://github.com/ecrespo/tutorialci).

# Putting it all together

The article will use [Travis-CI](https://travis-ci.com/) as the Continuous Integration tool, although any other continuous integration tool can be used. For more information about Travis-CI, here is a link to the [tutorial (broken link)](https://docs.travis-ci.com/user/tutorial/).

## File structure:

```
tutorialci/
├── app.py
├── .gitignore
├── Pipfile
├── .pylintrc
├── README.md
├── requirements.txt
└── .travis.yml
```


The necessary files are the following:

* app.py: Flask application.
* .gitignore: File that lets git ignore files or directories.
* PipFile: pipenv file.
* .pylintrc: pylint configuration file.
* README.md: readme file in markdown.
* requirements.txt: Requirements file to be used with pip (pip install -r requirements.txt).
* .travis.yml: yml file to configure travis-ci for the project.


### app.py file

This file creates a web page that shows hello world.
```python
from flask import Flask

app = Flask(__name__)

@app.route('/<nombre>')
def hola_mundo(nombre: str) -> str:
    return hola_nombre(nombre)

def hola_nombre(nombre: str) -> int:
    return f"hola, {nombre}"

if __name__ == '__main__':
    app.run(debug=True)
```
Note: This code has errors on purpose in order to see how continuous integration works.

### Pipfile file:

The Pipfile file has the following content:

```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]
bandit = "*"
v = {editable = true,version = "*"}
black = "*"
mypy = "*"
safety = "*"
pycodestyle = "*"
pylint = "*"

[packages]
flask = "==0.12.2"
[requires]
python_version = "3.7"

```


It defines the package name, the packages for development (the ones mentioned above are included), then the packages required for the application to work, together with the required python version.


### .pylintrc file

At the beginning the file will be empty, but its final content will be:

```
[MASTER]
disable=
    C0111,

```

### .travis.yml file

The travis file is in charge of the continuous integration flow; its content follows:

```yml
language: python
python:
  - 3.7
install:
  - pip install -U pip
  - pip install pipenv
  #- pip install -r requirements.txt
  - pipenv install --dev
script:
  - bandit ./*
  - black --check .
  - safety check -r requirements.txt
  - mypy .
  - pylint app.py
  - pycodestyle app.py

```

It defines the programming language and its version, then the package installation procedure (note that pipenv install --dev is used to install the packages defined in Pipfile).


### Github Repository

This is the github repository:

![Github: tutorialci](./images/repo_github_tutorial_ci.png)


### Connecting the github repository with Travis-CI

The github repository is connected to Travis-ci; the process is explained in the [travis-ci (broken link)](https://docs.travis-ci.com/user/tutorial/) documentation.

![Travis-ci: tutorialci](./images/repo_travis_ci_tutorialci.png)

### Integration Process

The start of the continuous integration process is shown below:

![Travis-ci](./images/travis_ci.png)


#### errors
After committing and then pushing to github, Travis-ci shows an error in the package versions, which is solved with the following change in Pipfile:

##### PipFile
![Github: PipFile](./images/cambios_pipfile.png)

##### Bandit

The error that bandit returns is about flask running in debug mode; setting it to False solves it.

![Bandit](./images/bandit.png)


![Github: app.py](./images/fixed_bandit_error.png)


##### Safety

Safety did not return an error.


![Safety](./images/safety.png)

##### mypy

The Mypy errors are about type declarations.

![Mypy](./images/mypy.png)

The errors are on lines 7 and 10. The int on line 9 has to be changed to str, which would be the correct output.

##### PEP8 errors

* Black: Returns an error.

![Black](./images/black.png)

It says the code does not comply with the PEP8 format.

* pylint

![Pylint](./images/pylint.png)

There are errors on lines 13,1, 3,6 and 9.

The errors on lines 1, 6 and 9 are solved by putting the code C0111 in the .pylintrc file, as shown in its section.  


* pycodestyle

![Pycodestyle](./images/pycodestyle.png)

There are errors on lines 5,9,12 and 13.


After fixing the errors, the integration returns no errors:

![Travis: tutorialci](./images/travis_final.png)

The final app.py file with its changes is shown below:

![Github: app.py](./images/final_app.png)

As you can see, the tools help you have quality code without security problems.


####
####
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
