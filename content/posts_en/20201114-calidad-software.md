Title: Writing clean Python code
Date:  2020-11-15 12:01
Category: Tutorial de Python
Tags: Python,pydocstyle,bandit, Black, pylint, pre-commit,pyupgrade,flake8,pep8-naming,pycodestyle,pylint,isort,mypy,wily,streamlit 
lang: en
translation: true
Slug: python-clean-python-code
Authors: Ernesto Crespo
Summary: This article explains the use of several quality assurance tools and how to run them before making a commit with pre-commit.

In a previous article ([Python tools for developing secure and quality code](/blog/python-tools-security-quality-code)) I covered tools that make it easier to comply with Python's PEP8, improve code security and format it; in that case circle-ci was used for the evaluations. 

In this article the evaluation will be done before pushing code to a git repository. The article is based on the following articles:

* [Python Code Quality: Tools & Best Practices](https://realpython.com/python-code-quality/)
* [Python Code Quality](https://testdriven.io/blog/python-code-quality/)
* [pre-commit hooks you must know (broken link)](https://towardsdatascience.com/pre-commit-hooks-you-must-know-ff247f5feb7e)
* [Simplify your Python Code: Automating Code Complexity Analysis with Wily](https://towardsdatascience.com/simplify-your-python-code-automating-code-complexity-analysis-with-wily-5c1e90c9a485)
* [How to Improve your Python Code Style with Pre-commit Hooks (broken link)](https://medium.com/python-in-plain-english/how-to-improve-your-python-code-style-with-pre-commit-hooks-e7fe3fd43bfa)
* [Keeping python code clean with pre-commit hooks: black, flake8 and isort (broken link)](https://medium.com/staqu-dev-logs/keeping-python-code-clean-with-pre-commit-hooks-black-flake8-and-isort-cac8b01e0ea1)


The tools explained in the previous article will be covered again.

The code that will be evaluated is the following (it does not pass the checks):
```python 

import numpy as np
from scipy import signal as sp
import matplotlib.pylab as plt
import scipy.signal as signal
import scipy.stats as stats
import streamlit as st


def u(amplitud, t):
    """Función escalón unitario

    Args:
        amplitud (int): Amplitud del escalon
        t (list): Lista de tiempo

    Returns:
        list: Lista de valores
    """
    return amplitud*np.piecewise(t, [t < 0.0, t >= 0.0], [0, 1])


def OndaCuadrada(amplitud, t, fs=1):
    """Función  de Onda Cuadrada

    Args:
        amplitud (int): Amplitud de la segnal
        t (list): Lista de valores de tiempo
        fs (int, optional): Frecuencia.. Defaults to 1.

    Returns:
        list: Lista de valores
    """
    return ((sp.square(2 * fs*t)) * (amplitud / 2.0)) + (amplitud / 2.0)


def segnal_triangular(amplitud, simetria, t, fs=1):
    """Señal triangular 

    Args:
        amplitud (int): Amplitud de la señal
        simetria (float): simetria de la señal
        t (list): Lista de valores que definen el tiempo.
        fs (int, optional): Frecuencia de la señal. Defaults to 1.

    Returns:
        list: Lista de valores de la señal
    """
    return amplitud*(signal.sawtooth(2 * np.pi * fs * t, simetria))


def seno(amplitud, t, fs=1):
    """ Onda Seno

    Args:
        amplitud (int): Amplitud de la señal
        t (list): Lista de valores de tiempo
        fs (int, optional): Frecuencia de la señal. Defaults to 1.

    Returns:
        list: Lista de valores de la señal de seno
    """
    return amplitud*np.sin(fs*t)


def coseno(amplitud, t, fs=1):
    """Señal de coseno

    Args:
        amplitud (int): Amplitud de la señal
        t (list): lista de valores para generar la señal
        fs (int, optional): Frecuencia de la señal. Defaults to 1.

    Returns:
        list: Lista de valores de la señal
    """
    return amplitud*np.cos(fs*t)


def tiempo(lim_inf, lim_sup, n):
    """Lista de valores que definen el tiempo de la señal

    Args:
        lim_inf (int): Límite inferior del tiempo 
        lim_sup (int): Límite superior del tiempo
        n (int): Cantidad de valores a generar del tiempo

    Returns:
        list: Lista de valores del tiemmpo
    """
    return np.linspace(lim_inf, lim_sup, n)


def plot_signal(xi, xf, yi, yf, t, titulo, etiqueta, values):
    """Generación de la gráfica de la señal.

    Args:
        xi (int): x inicial
        xf (int): x final
        yi (int): y inicial
        yf (int): y final
        t (list): lista de valores de tiempo
        titulo (str): Título de la gráfica
        etiqueta (str): Etiqueta de la señal.
        values (list): Valores de la señal 
    """
    plot(t, values, 'k', label=etiqueta, lw=2)
    xlim(xi, xf)


def main():
    # Definir título
    st.title("Generación de gráficas de señales")
    st.sidebar.header("Entradas:")
    segnales = ["Escalon Unitario", "Onda Cuadrada",
                "Onda triangular", "Seno", "Coseno"]

    resp = st.sidebar.selectbox("Tipo de señal", segnales)

    st.sidebar.header("Definición del tiempo:")
    st.sidebar.subheader("Rango")
    # SelectBox
    t0 = int(st.sidebar.selectbox(
        "", range(0, 10)
    ))
    ti = 0
    tf = t0
    n = 10000
    t = tiempo(ti, tf, n)
    st.sidebar.subheader("Amplitud de la señal")
    amplitud = int(st.sidebar.selectbox(
        "", range(1, 10)
    ))

    # numpy.ndarray
    if resp == "Escalon Unitario":
        ti = -tf
        resultado = u(amplitud, t)
    elif resp == "Onda Cuadrada":
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox(
            "", range(1, 11)
        ))
        resultado = OndaCuadrada(amplitud, t, fs)
    elif resp == "Onda triangular":
        simetria = 0.5
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox(
            "", range(1, 11)
        ))
        resultado = segnal_triangular(amplitud, simetria, t, fs)
    elif resp == "Seno":
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox(
            "", range(1, 11)
        ))
        resultado = seno(amplitud, t, fs)
    elif resp == "Coseno":
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox(
            "", range(1, 11)
        ))
        resultado = coseno(amplitud, t, fs)
    else:
        resultado = 0
        st.error("Error")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    st.header(f"Gráfica de {resp}")
    ax.plot(t, resultado)
    ax.set_xlim(ti, tf)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("f(t)")
    ax.set_ylim(2*amplitud*-1, 2*amplitud)
    st.pyplot(fig)


if __name__ == "__main__":
    main()


```

Its requirements file is the following: 

```
streamlit==0.70.0
scipy==1.5.4
numpy==1.19.3
matplotlib==3.3.3
```

Its initial file structure is the following (including hidden files): 

```
signals_fft_streamlit
├── .git
│   ├── branches
│   ├── config
│   ├── description
│   ├── HEAD
│   ├── hooks
│   │   ├── applypatch-msg.sample
│   │   ├── commit-msg.sample
│   │   ├── fsmonitor-watchman.sample
│   │   ├── post-update.sample
│   │   ├── pre-applypatch.sample
│   │   ├── pre-commit.sample
│   │   ├── pre-merge-commit.sample
│   │   ├── prepare-commit-msg.sample
│   │   ├── pre-push.sample
│   │   ├── pre-rebase.sample
│   │   ├── pre-receive.sample
│   │   └── update.sample
│   ├── index
│   ├── info
│   │   └── exclude
│   ├── logs
│   │   ├── HEAD
│   │   └── refs
│   │       ├── heads
│   │       │   └── main
│   │       └── remotes
│   │           └── origin
│   │               └── HEAD
│   ├── objects
│   │   ├── info
│   │   └── pack
│   │       ├── pack-a6d9863d11286fbea66f5aafa93a9dbafaf3f4fc.idx
│   │       └── pack-a6d9863d11286fbea66f5aafa93a9dbafaf3f4fc.pack
│   ├── packed-refs
│   └── refs
│       ├── heads
│       │   └── main
│       ├── remotes
│       │   └── origin
│       │       └── HEAD
│       └── tags
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── src
    └── app.py
```

In the hooks you can define what runs before a commit using pre-commit, which will be covered later. 

# Code validation

## Linters 

[Linters](https://es.wikipedia.org/wiki/Lint) are programming tools that check code in any programming language.

### Flake8 

A tool that checks that the code complies with Python's PEP-8.

It can be installed via pip:

```
pip install flake8
```

Run flake8 on the app.py file: 

```
python -m flake8 src/app.py
src/app.py:5:1: F401 'scipy.stats' imported but unused
src/app.py:22:6: N802 function name 'OndaCuadrada' should be lowercase
src/app.py:37:20: W291 trailing whitespace
src/app.py:83:50: W291 trailing whitespace
src/app.py:104:43: W291 trailing whitespace
src/app.py:106:5: F821 undefined name 'plot'
src/app.py:107:5: F821 undefined name 'xlim'
```
The command output shows the lines of code where there are errors, the type of error and a description of it. 

###  pep8-naming

In addition to flake you can use pep8-naming to comply with PEP8's naming rules. 

To install it, use pip: 
```
pip install pep8-naming
```

Run the same flake8 command; the error message is: 
```
src/app.py:22:6: N802 function name 'OndaCuadrada' should be lowercase
```
Which already appeared in the previous run. 


### pycodestyle

It is another PEP-8 validation tool. png

Install it: 

```
pip install pycodestyle
```

Run it: 
```
pycodestyle src/app.py
```

In this case, since the flake8 error messages were already fixed, it returns no messages. 

### pylint 

Install it: 
```
pip install pylint 
```

Run it: 
```
pylint src/app.py 
```

## Code formatter

It lets you reformat the code so that it complies with a set of standards. 

### isort 

It reorders the imports as follows: 

1. Standard library 
2. Third-party libraries 
3. Local libraries

Install it: 
```
pip install isort 
```

It is used as follows: 
```
isort src/app.py 
Fixing /home/ernesto/proyectos/signals_fft_streamlit/src/app.py
```

Before, the imports looked like this: 
```python 

import numpy as np
from scipy import signal as sp
import matplotlib.pylab as plt
import scipy.signal as signal
import scipy.stats as stats
import streamlit as st

```

Now: 
```python 

import matplotlib.pylab as plt
import numpy as np
import scipy.signal as signal
import streamlit as st
from scipy import signal as sp

```

To only check the import order without making the change you can run: 
```
python -m isort src/app.py --check-only
```

To see the changes without applying them you can use: 
```
python -m isort src/app.py --diff
```

### Black 

A code formatter used to reformat code based on the [Black code style (broken link)](https://black.readthedocs.io/en/stable/the_black_code_style.html), which is very close to PEP-8. 

To install it: 

```
pip install black 
```

To check the code without modifying it:

```
python -m black src/app.py --check  
would reformat src/app.py
Oh no! 💥 💔 💥
1 file would be reformatted.

```

To see the differences without modifying it (only part of the code is shown): 
```
--- src/app.py	2020-11-15 01:20:29.525556 +0000
+++ src/app.py	2020-11-15 01:29:54.278851 +0000
@@ -13,11 +13,11 @@
         t (list): Lista de tiempo
 
     Returns:
         list: Lista de valores
     """
-    return amplitud*np.piecewise(t, [t < 0.0, t >= 0.0], [0, 1])
+    return amplitud * np.piecewise(t, [t < 0.0, t >= 0.0], [0, 1])

```

To make the modifications:

```
python -m black src/app.py       
reformatted src/app.py
All done! ✨ 🍰 ✨
1 file reformatted.
```

The code changed to (only part of the code is shown): 

```python 
def u(amplitud, t):
    """Función escalón unitario

    Args:
        amplitud (int): Amplitud del escalon
        t (list): Lista de tiempo

    Returns:
        list: Lista de valores
    """
    return amplitud * np.piecewise(t, [t < 0.0, t >= 0.0], [0, 1])
```

Other similar tools are [YAPF](https://github.com/google/yapf) and [autopep8](https://github.com/hhatto/autopep8)

## Security vulnerability scanning

There are tools that evaluate the security vulnerabilities of the code and its dependencies. 

### Bandit 

[Bandit](https://github.com/PyCQA/bandit) is a tool designed to find security issues in Python code.


Install it: 
```
pip install bandit 
```

Run it as follows:  

```
bandit -r src/app.py 
[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.8.3
Run started:2020-11-15 01:44:06.048642

Test results:
	No issues identified.

Code scanned:
	Total lines of code: 119
	Total lines skipped (#nosec): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0.0
		Low: 0.0
		Medium: 0.0
		High: 0.0
	Total issues (by confidence):
		Undefined: 0.0
		Low: 0.0
		Medium: 0.0
		High: 0.0
Files skipped (0):
```

As you can see, the code has no security problems. 


### Safety

[Safety](https://github.com/pyupio/safety) is a tool that checks the application's dependencies for security issues. 

Install it: 
```
pip install safety
```

Run it as follows:  

```
safety check
+==============================================================================+
|                                                                              |
|                               /$$$$$$            /$$                         |
|                              /$$__  $$          | $$                         |
|           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           |
|          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           |
|         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           |
|          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           |
|          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           |
|         |_______/  \_______/|__/     \_______/   \___/   \____  $$           |
|                                                          /$$  | $$           |
|                                                         |  $$$$$$/           |
|  by pyup.io                                              \______/            |
|                                                                              |
+==============================================================================+
| REPORT                                                                       |
| checked 136 packages, using default DB                                       |
+==============================================================================+
| No known security vulnerabilities found.                                     |
+==============================================================================+

```

To check only the list of packages in requirements.txt, run: 
```
safety check -r requirements.txt
+==============================================================================+
|                                                                              |
|                               /$$$$$$            /$$                         |
|                              /$$__  $$          | $$                         |
|           /$$$$$$$  /$$$$$$ | $$  \__//$$$$$$  /$$$$$$   /$$   /$$           |
|          /$$_____/ |____  $$| $$$$   /$$__  $$|_  $$_/  | $$  | $$           |
|         |  $$$$$$   /$$$$$$$| $$_/  | $$$$$$$$  | $$    | $$  | $$           |
|          \____  $$ /$$__  $$| $$    | $$_____/  | $$ /$$| $$  | $$           |
|          /$$$$$$$/|  $$$$$$$| $$    |  $$$$$$$  |  $$$$/|  $$$$$$$           |
|         |_______/  \_______/|__/     \_______/   \___/   \____  $$           |
|                                                          /$$  | $$           |
|                                                         |  $$$$$$/           |
|  by pyup.io                                              \______/            |
|                                                                              |
+==============================================================================+
| REPORT                                                                       |
| checked 4 packages, using default DB                                         |
+==============================================================================+
| No known security vulnerabilities found.                                     |
+==============================================================================+

```

## Static typing verification 

Since Python 3.7, Python supports, as a form of documentation, the definition of the types of a function's output and its arguments, and there are now tools that verify static typing.

### Mypy 

[Mypy](http://mypy-lang.org/) is an optional static type checker for Python that aims to combine the benefits of dynamic (or "duck") typing and static typing.


Install it:

```
pip install mypy 
``` 

Use it: 
```
mypy src/app.py 
src/app.py:1: error: No library stub file for module 'matplotlib.pylab'
src/app.py:1: note: (Stub files are from https://github.com/python/typeshed)
src/app.py:1: error: No library stub file for module 'matplotlib'
src/app.py:2: error: No library stub file for module 'numpy'
src/app.py:3: error: No library stub file for module 'scipy.signal'
src/app.py:3: error: No library stub file for module 'scipy'
src/app.py:4: error: Cannot find module named 'streamlit'
src/app.py:4: note: See https://mypy.readthedocs.io/en/latest/running_mypy.html#missing-imports
```

To ignore these errors use # type: ignore, as shown below:

```python 

import matplotlib.pylab as plt  # type: ignore
import numpy as np  # type: ignore
import scipy.signal as signal  # type: ignore
import streamlit as st  # type: ignore
from scipy import signal  # type: ignore

```

Run it again and those initial errors no longer appear. 

An example of static typing is shown below: 
```python 

def u(amplitud: int, t: np.ndarray) -> np.ndarray:
    """Función escalón unitario

    Args:
        amplitud (int): Amplitud del escalon
        t (np.ndarray): Lista de tiempo

    Returns:
        np.ndarray: Lista de valores
    """
    return amplitud * np.piecewise(t, [t < 0.0, t >= 0.0], [0, 1])

def onda_cuadrada(amplitud: int, t: np.ndarray, fs: int = 1) ->np.ndarray:
    """Función  de Onda Cuadrada

    Args:
        amplitud (int): Amplitud de la segnal
        t (list): Lista de valores de tiempo
        fs (int, optional): Frecuencia.. Defaults to 1.

    Returns:
        list: Lista de valores
    """
    return ((sp.square(2 * fs * t)) * (amplitud / 2.0)) + (amplitud / 2.0)


```

Another way to ignore all errors is the following: 
```python 
#!/usr/bin/env python 
#-*- coding: utf-8 -*-
# mypy: ignore-errors
```


## Documentation validation 

### pydocstyle

[pydocstyle](https://github.com/PyCQA/pydocstyle) is a tool that validates the format of the documentation.


Install it: 
```
pip install pydocstyle
```

Use it: 
```
pydocstyle src/app.py 
src/app.py:1 at module level:
        D100: Missing docstring in public module
src/app.py:9 in public function `u`:
        D400: First line should end with a period (not 'o')
src/app.py:22 in public function `onda_cuadrada`:
        D400: First line should end with a period (not 'a')
src/app.py:36 in public function `segnal_triangular`:
        D205: 1 blank line required between summary line and description (found 0)
src/app.py:36 in public function `segnal_triangular`:
        D400: First line should end with a period (not 'r')
src/app.py:50 in public function `seno`:
        D400: First line should end with a period (not 'o')
src/app.py:64 in public function `coseno`:
        D400: First line should end with a period (not 'o')
src/app.py:78 in public function `tiempo`:
        D205: 1 blank line required between summary line and description (found 0)
src/app.py:78 in public function `tiempo`:
        D400: First line should end with a period (not 'l')
src/app.py:90 in public function `main`:
        D103: Missing docstring in public function
```


## Cyclomatic Complexity, number of lines of code

There are tools to validate cyclomatic complexity, such as: 

* [wily](https://wily.readthedocs.io/en/latest/) 
* [mccabe](https://github.com/PyCQA/mccabe)
* [radon](https://radon.readthedocs.io/)

In this case wily will be tried

### Wily 

Wily is an application for tracking the complexity of Python code and applications.

Install it: 
```
pip install wily
```

You need to index the project by running: 

```
wily build src/
Found 1 revisions from 'git' archiver in '/home/ernesto/proyectos/signals_fft_streamlit'.
Running operators - maintainability,raw,cyclomatic,halstead
Processing |################################| 4/4
Completed building wily history, run `wily report <file>` or `wily index` to see more.

```

To generate the report for app.py, run: 

```
wily report src/app.py 
Using default metrics ['maintainability.mi', 'raw.loc', 'cyclomatic.complexity', 'halstead.h1']
-----------History for ['maintainability.mi', 'raw.loc', 'cyclomatic.complexity', 'halstead.h1']------------
╒════════════╤════════════════╤════════════╤═════════════════════════╤═════════════════╤═════════════════════════╤═══════════════════╕
│ Revision   │ Author         │ Date       │ Maintainability Index   │ Lines of Code   │ Cyclomatic Complexity   │ Unique Operands   │
╞════════════╪════════════════╪════════════╪═════════════════════════╪═════════════════╪═════════════════════════╪═══════════════════╡
│ f2679c6    │ Ernesto Crespo │ 2020-11-14 │ 68.1377 (0)             │ 153 (0)         │ 12 (0)                  │ 7 (0)             │
╘════════════╧════════════════╧════════════╧═════════════════════════╧═════════════════╧═════════════════════════╧═══════════════════╛
```

In the report you can pass specific metrics: 

```
wily report src/app.py loc sloc comments --message
-----------History for ('loc', 'sloc', 'comments')------------
╒════════════╤════════════════╤════════════════╤════════════╤═════════════════╤═══════════════════╤═══════════════════════╕
│ Revision   │ Message        │ Author         │ Date       │ Lines of Code   │ S Lines of Code   │ Multi-line comments   │
╞════════════╪════════════════╪════════════════╪════════════╪═════════════════╪═══════════════════╪═══════════════════════╡
│ f2679c6    │ Initial commit │ Ernesto Crespo │ 2020-11-14 │ 153 (0)         │ 71 (0)            │ 8 (0)                 │
╘════════════╧════════════════╧════════════════╧════════════╧═════════════════╧═══════════════════╧═══════════════════════╛

```

####  Cyclomatic Complexity

According to the publication by [The Software Engineering Institute at Carnegie Mellon defines](https://resources.sei.cmu.edu/asset_files/Handbook/1997_002_001_16523.pdf), which defines the complexity ranges: 
* 1-10: Low risk, simple program. 
* 11-20: Moderate risk, more complex program. 
* 21-50: High risk, very difficult program. 
* >50: Very high risk, unstable program. 

#### Maintainability index

For this case: 
* <65: Hardly maintainable.
* 65-85: Moderately maintainable.
* >85: Easy to maintain. 

In the case of app.py it has a moderate risk and is moderately maintainable. 

For more information on cyclomatic complexity, you can check [Simplify your Python Code: Automating Code Complexity Analysis with Wily
](https://towardsdatascience.com/simplify-your-python-code-automating-code-complexity-analysis-with-wily-5c1e90c9a485) or the pdf from [The Software Engineering Institute at Carnegie Mellon defines](https://resources.sei.cmu.edu/asset_files/Handbook/1997_002_001_16523.pdf).



# Putting it all together with pre-commit 

## pre-commit 

[Pre-commit](https://pre-commit.com/) is a framework for managing git hooks. 

To install it: 
```
pip install pre-commit
```

To initialize pre-commit, run: 

```
$pre-commit install
pre-commit installed at .git/hooks/pre-commit
```

### Yaml verification

To format yaml you can use the following configuration: 
```yaml
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
      - id: check-yaml
        exclude: (template|ci).*\.(json|yml|yaml)$
```

### isort 

To validate with isort you have the following: 

```yaml 
  - repo: https://github.com/asottile/seed-isort-config
    rev: v1.9.3
    hooks:
      - id: seed-isort-config
  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v4.3.21
    hooks:
      - id: isort
```

### For Wily

```yaml 
  - repo: local
    hooks:
      - id: wily
        name: wily
        entry: wily diff
        verbose: true
        language: python
        additional_dependencies: [wily]
```

### Safety

```yaml 
  - repo: git://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.1.3
    hooks:
      - id: python-safety-dependencies-check
```

### Black 

```yaml 
  - repo: https://github.com/ambv/black
    rev: stable
    hooks:
      - id: black
        language_version: python3.8

```

### Pylint 

```yaml 
  - repo: https://github.com/PyCQA/pylint
    rev: "pylint-2.6.0"
    hooks:
      - id: pylint
        args: ["--disable=similarities"]
```

### Mypy

```yaml 

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.790
    hooks:
      - id: mypy
        exclude: ^testing/resources/
```

### Pyupgrade

```yaml 
  - repo: https://github.com/asottile/pyupgrade
    rev: v2.7.3
    hooks:
      - id: pyupgrade
        args: [--py36-plus]
```

### Flake8 

```yaml 
  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.4
    hooks:
      - id: flake8
        additional_dependencies: [flake8-typing-imports==1.10.0]
```

### Autopep8

```yaml 

  - repo: https://github.com/pre-commit/mirrors-autopep8
    rev: v1.5.4
    hooks:
      - id: autopep8

```

### Blacken

```yaml 

  - repo: https://github.com/asottile/blacken-docs
    rev: v1.8.0
    hooks:
      - id: blacken-docs
        additional_dependencies: [black==20.8b1]

```
### Bandit 

```yaml 
  - repo: git://github.com/Lucas-C/pre-commit-hooks-bandit
    rev: v1.0.4
    hooks:
      - id: python-bandit-vulnerability-check
        exclude: /home/ernesto/proyectos/magnetic_fields/.virtualenvs/*

``` 

### pydoctstyle 

```yaml 
  - repo: local
    hooks:
      - id: pydocstyle
        name: pydocstyle
        entry: pydocstyle
        files: src/app.py
        verbose: true
        language: python
        additional_dependencies: [pydocstyle]

```

## Complete file

The complete .pre-commit-config.yaml file contains the following:
```yaml 
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
      - id: check-yaml
        exclude: (template|ci).*\.(json|yml|yaml)$
  - repo: https://github.com/asottile/seed-isort-config
    rev: v1.9.3
    hooks:
      - id: seed-isort-config
  - repo: https://github.com/pre-commit/mirrors-isort
    rev: v4.3.21
    hooks:
      - id: isort
  - repo: local
    hooks:
      - id: wily
        name: wily
        entry: wily diff
        verbose: true
        language: python
        additional_dependencies: [wily]
  - repo: local
    hooks:
      - id: pydocstyle
        name: pydocstyle
        entry: pydocstyle
        files: src/app.py
        verbose: true
        language: python
        additional_dependencies: [pydocstyle]
  - repo: git://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.1.3
    hooks:
      - id: python-safety-dependencies-check
  - repo: https://github.com/ambv/black
    rev: stable
    hooks:
      - id: black
        language_version: python3.8
  - repo: https://github.com/PyCQA/pylint
    rev: "pylint-2.6.0"
    hooks:
      - id: pylint
        args: ["--disable=similarities"]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.790
    hooks:
      - id: mypy
        exclude: ^testing/resources/
  - repo: https://github.com/asottile/pyupgrade
    rev: v2.7.3
    hooks:
      - id: pyupgrade
        args: [--py36-plus]
  - repo: https://gitlab.com/pycqa/flake8
    rev: 3.8.4
    hooks:
      - id: flake8
        additional_dependencies: [flake8-typing-imports==1.10.0]
  - repo: https://github.com/pre-commit/mirrors-autopep8
    rev: v1.5.4
    hooks:
      - id: autopep8
  - repo: https://github.com/asottile/blacken-docs
    rev: v1.8.0
    hooks:
      - id: blacken-docs
        additional_dependencies: [black==20.8b1]
  - repo: git://github.com/Lucas-C/pre-commit-hooks-bandit
    rev: v1.0.4
    hooks:
      - id: python-bandit-vulnerability-check
        exclude: /home/ernesto/proyectos/magnetic_fields/.virtualenvs/*

```

You can run the following command for the verification: 
```
pre-commit run --all-files
```

This returns the messages as shown in the following image: 
![pre-commit](./images/pre-commits.png)

From now on, when you want to make a commit, pre-commit will evaluate the hooks and you have to fix the errors until there are none, and that is when the commit will be made.


# Final file structure.

```
ignals_fft_streamlit
├── .bandit
├── .git
│   ├── branches
│   ├── COMMIT_EDITMSG
│   ├── config
│   ├── description
│   ├── HEAD
│   ├── hooks
│   │   ├── applypatch-msg.sample
│   │   ├── commit-msg.sample
│   │   ├── fsmonitor-watchman.sample
│   │   ├── post-update.sample
│   │   ├── pre-applypatch.sample
│   │   ├── pre-commit
│   │   ├── pre-commit.sample
│   │   ├── pre-merge-commit.sample
│   │   ├── prepare-commit-msg.sample
│   │   ├── pre-push.sample
│   │   ├── pre-rebase.sample
│   │   ├── pre-receive.sample
│   │   └── update.sample
│   ├── index
│   ├── info
│   │   └── exclude
│   ├── logs
│   │   ├── HEAD
│   │   └── refs
│   │       ├── heads
│   │       │   ├── feat
│   │       │   │   └── validado
│   │       │   └── main
│   │       └── remotes
│   │           └── origin
│   │               └── HEAD
│   ├── ORIG_HEAD
│   ├── packed-refs
│   └── refs
│       ├── heads
│       │   ├── feat
│       │   │   └── validado
│       │   └── main
│       ├── remotes
│       │   └── origin
│       │       └── HEAD
│       └── tags
├── .gitignore
├── .isort.cfg
├── LICENSE
├── .pre-commit-config.yaml
├── .pylintrc
├── README.md
├── requirements.txt
└── src
    └── app.py
```

The final app.py file ended up like this: 

```python

"""WebApp with streamlit graph signals."""
import matplotlib.pylab as plt  # type: ignore
import numpy as np  # type: ignore
import streamlit as st  # type: ignore
from scipy import signal  # type: ignore # pylint: disable=import-error


def u(amplitud: int, t: np.ndarray) -> np.ndarray:
    """Función escalón unitario.

    Args:
        amplitud(int): Amplitud del escalon
        t(np.ndarray): Lista de tiempo

    Returns:
        np.ndarray: Lista de valores
    """
    return amplitud * np.piecewise(t, [t < 0.0, t >= 0.0], [0, 1])


def onda_cuadrada(amplitud: int, t: np.ndarray, fs: int = 1) -> np.ndarray:
    """Función  de Onda Cuadrada.

    Args:
        amplitud(int): Amplitud de la segnal
        t(list): Lista de valores de tiempo
        fs(int, optional): Frecuencia.. Defaults to 1.

    Returns:
        list: Lista de valores
    """
    return ((signal.square(2 * fs * t)) * (amplitud / 2.0)) + (amplitud / 2.0)


def segnal_triangular(
    amplitud: int, simetria: float, t: np.ndarray, fs: int = 1
) -> np.ndarray:
    """Señal triangular.

    Args:
        amplitud(int): Amplitud de la señal
        simetria(float): simetria de la señal
        t(np.ndarray): Lista de valores que definen el tiempo.
        fs(int, optional): Frecuencia de la señal. Defaults to 1.

    Returns:
        np.ndarray: Lista de valores de la señal
    """
    return amplitud * (signal.sawtooth(2 * np.pi * fs * t, simetria))


def seno(amplitud: int, t: np.ndarray, fs: int = 1) -> np.ndarray:
    """Onda Seno.

    Args:
        amplitud(int): Amplitud de la señal
        t (np.ndarray): Lista de valores de tiempo
        fs (int, optional): Frecuencia de la señal. Defaults to 1.

    Returns:
        np.ndarray: Lista de valores de la señal de seno
    """
    return amplitud * np.sin(fs * t)


def coseno(amplitud: int, t: np.ndarray, fs: int = 1) -> np.ndarray:
    """Señal de coseno.

    Args:
        amplitud (int): Amplitud de la señal
        t (np.ndarray): lista de valores para generar la señal
        fs (int, optional): Frecuencia de la señal. Defaults to 1.

    Returns:
        np.ndarray: Lista de valores de la señal
    """
    return amplitud * np.cos(fs * t)


def tiempo(lim_inf: int, lim_sup: int, n: int) -> np.ndarray:
    """Lista de valores que definen el tiempo de la señal.

    Args:
        lim_inf (int): Límite inferior del tiempo
        lim_sup (int): Límite superior del tiempo
        n (int): Cantidad de valores a generar del tiempo

    Returns:
        np.ndarray: Lista de valores del tiemmpo
    """
    return np.linspace(lim_inf, lim_sup, n)


def main():
    """Ejecución Streamlit webApp."""
    st.title(  # pylint: disable=no-value-for-parameter
        "Generación de gráficas de señales"
    )  # pylint: disable=no-value-for-parameter
    st.sidebar.header("Entradas:")  # pylint: disable=no-value-for-parameter
    segnales = [
        "Escalon Unitario",
        "Onda Cuadrada",
        "Onda triangular",
        "Seno",
        "Coseno",
    ]

    resp = st.sidebar.selectbox("Tipo de señal", segnales)

    st.sidebar.header("Definición del tiempo:")
    st.sidebar.subheader("Rango")
    # SelectBox
    t0 = int(st.sidebar.selectbox("", range(0, 10)))
    ti = 0
    tf = t0
    n = 10000
    t = tiempo(ti, tf, n)
    st.sidebar.subheader("Amplitud de la señal")
    amplitud = int(st.sidebar.selectbox("", range(1, 10)))

    # numpy.ndarray
    if resp == "Escalon Unitario":
        ti = -tf
        resultado = u(amplitud, t)
    elif resp == "Onda Cuadrada":
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox("", range(1, 11)))
        resultado = onda_cuadrada(amplitud, t, fs)
    elif resp == "Onda triangular":
        simetria = 0.5
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox("", range(1, 11)))
        resultado = segnal_triangular(amplitud, simetria, t, fs)
    elif resp == "Seno":
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox("", range(1, 11)))
        resultado = seno(amplitud, t, fs)
    elif resp == "Coseno":
        st.sidebar.subheader("Frecuencia de la señal")
        fs = int(st.sidebar.selectbox("", range(1, 11)))
        resultado = coseno(amplitud, t, fs)
    else:
        resultado = 0
        st.error("Error")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    st.header(f"Gráfica de {resp}")
    ax.plot(t, resultado)
    ax.set_xlim(ti, tf)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("f(t)")
    ax.set_ylim(2 * amplitud * -1, 2 * amplitud)
    st.pyplot(fig)


if __name__ == "__main__":
    main()

```

The repository where you can see the files is on [github](https://github.com/ecrespo/signals_fft_streamlit)




####

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
