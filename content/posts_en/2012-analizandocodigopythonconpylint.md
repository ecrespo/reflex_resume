Title: Analyzing Python code with Pylint
Date: 2012-12-11 9:00
Category: Tutorial Python
Tags: General,Linux,numpy,python,PyLint
lang: en
translation: true

`Pylint` is a code analysis tool created by LogiLab.  It is more complex than `Pyflakes` and allows more customization. For more information about pylint you can check the [manual (broken link)](https://www.logilab.org/card/pylint_manual).

You can install `pylint` through `easy_install` or `pip`, and if you use a Debian-based Linux distribution you can install it via `apt-get`:

```python
easy_install  pylint
```
```python
pip install pylint
```
```
apt-get install pylint
```
The output of `pylint` can be raw text or html format. Messages have the following format:
MESSAGE_TYPE: LINE:[OBJECT:] MESSAGE

The message type can be one of the following:

- [R]: Means that refactoring the code is recommended.
- [C]: Means that there was a style violation in the code.
- [W]: A warning about a minor problem.
- [E]: Means an error message or a potential bug.
- [F]: Indicates a fatal error, blocking any further analysis.
- The same code from the previous article will be used:

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

This script is saved with the name `arreglo.py`.

Now `pylint` will be run, passing the file `arreglo.py` as an argument:

The output of running `pylint` is shown below:

```python
************* Module arreglo


C:  1,0: Missing docstring


C:  7,28: More than one statement on a single line


W:  8,0: Uses of a deprecated module 'string'


C: 12,0: Invalid name "a" (should match (([A-Z_][A-Z0-9_]*)|(__.*__))$)


E: 18,12: Undefined variable 'plataforma'


W:  8,0: Unused import string








Report


======


12 statements analysed.





Duplication


-----------





+-------------------------+------+---------+-----------+


|                         |now   |previous |difference |


+=========================+======+=========+===========+


|nb duplicated lines      |0     |0        |=          |


+-------------------------+------+---------+-----------+


|percent duplicated lines |0.000 |0.000    |=          |


+-------------------------+------+---------+-----------+











Statistics by type


------------------




+---------+-------+-----------+-----------+------------+---------+


|type     |number |old number |difference |%documented |%badname |


+=========+=======+===========+===========+============+=========+


|module   |1      |1          |=          |0.00        |0.00     |


+---------+-------+-----------+-----------+------------+---------+


|class    |0      |0          |=          |0           |0        |


+---------+-------+-----------+-----------+------------+---------+


|method   |0      |0          |=          |0           |0        |


+---------+-------+-----------+-----------+------------+---------+


|function |0      |0          |=          |0           |0        |


+---------+-------+-----------+-----------+------------+---------+











External dependencies


---------------------


::





    numpy (arreglo)


    pudb 


      \-set_trace (arreglo)




Raw metrics


-----------





+----------+-------+------+---------+-----------+


|type      |number |%     |previous |difference |


+==========+=======+======+=========+===========+


|code      |11     |64.71 |11       |=          |


+----------+-------+------+---------+-----------+


|docstring |0      |0.00  |0        |=          |


+----------+-------+------+---------+-----------+


|comment   |3      |17.65 |3        |=          |


+----------+-------+------+---------+-----------+


|empty     |3      |17.65 |3        |=          |


+----------+-------+------+---------+-----------+











Messages by category


--------------------




+-----------+-------+---------+-----------+


|type       |number |previous |difference |


+===========+=======+=========+===========+


|convention |3      |3        |=          |


+-----------+-------+---------+-----------+


|refactor   |0      |0        |=          |


+-----------+-------+---------+-----------+


|warning    |2      |2        |=          |


+-----------+-------+---------+-----------+


|error      |1      |1        |=          |


+-----------+-------+---------+-----------+











Messages


--------




+-----------+------------+


|message id |occurrences |


+===========+============+


|W0611      |1           |


+-----------+------------+


|W0402      |1           |


+-----------+------------+


|E0602      |1           |


+-----------+------------+


|C0321      |1           |


+-----------+------------+


|C0111      |1           |


+-----------+------------+


|C0103      |1           |


+-----------+------------+











Global evaluation


-----------------


Your code has been rated at 1.67/10 (previous run: 1.67/10)
```


If you want more information about what is generated in the pylint report, you can check the documentation [mentioned above (broken link)](https://www.logilab.org/card/pylint_manual).

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)