Title: Matplotlib tutorials with Python. Part 1
Date: 2009-06-16 08:00
Category: Tutorial Python
Tags: Linux,Python,Matplotlib
lang: en
translation: true

After some time spent on other matters, and because I am on medical rest, I am going to start a
series of short tutorials about matplotlib.

The first thing you need is to have matplotlib installed.
As root:

```
aptitude install python-matplotlib python-matplotlib-data python-matplotlib-doc
```

Then run python from the command line
```
ernesto@zvezda:~/bin$ python2.5
Python 2.5.4 (r254:67916, Feb 17 2009, 20:16:45)
[GCC 4.3.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.

>>> import matplotlib.pyplot as plt
>>> plt.plot([1,2,3],[5,7,9])
[]
>>> plt.ylabel('Eje Y')

>>> plt.xlabel('Eje X')
>>> plt.show()
```

The first command imports the matplotlib library, then the points to plot are passed in,
those for the X axis and for the Y axis; then labels are set on the Cartesian
axes and the plot is displayed.


===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)