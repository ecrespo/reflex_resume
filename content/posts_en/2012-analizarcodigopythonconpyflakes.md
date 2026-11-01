Title: Analyzing Python code with Pyflakes
Date: 2012-12-10 9:00
Category: Tutorial Python
Tags: General,Linux,Python,Pyflakes
lang: en
translation: true

Pyflakes is a Python code analysis tool.

Pyflakes can detect potential problems such as:

Unused imported modules.
Unused variables.

To install it you can download it from [PyPI](https://pypi.org/project/pyflakes/) or from the [Launchpad](https://launchpad.net/pyflakes) site; it can also be installed with easy_install or pip, and on Debian-based distributions it is installed via `apt-get` or `aptitude`.
```
easy_install pyflakes
```

```
pip install pyflakes
```

```
apt-get install pyflakes
```

To try out `pyflakes` we will use the code from the debugging tutorial, adding the import of string and an if statement that compares the value of i with a variable called plataforma.

Here is the code:
```python
#!/usr/bin/env python

# -*- coding: utf-8 -*-



#Se importa numpy como np

import numpy as np



from pudb import set_trace; set_trace()

import string



a = np.arange(10)

print a

print a[8]

print a[9]



for i in a:

    if i == plataforma:

        print i
```
This script will be saved with the name `arreglo.py`.

Now `pyflakes` will be run:
```python
pyflakes arreglo.py 

arreglo.py:8: 'string' imported but unused

arreglo.py:18: undefined name 'plataforma'
```

The run returns the line with an unused import (import string) and an undefined variable (plataforma).

By removing the import on line 8 and fixing the definition of the plataforma variable, or changing that part of the code, the messages that pyflakes returns will go away. This helps prevent errors in the code.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)