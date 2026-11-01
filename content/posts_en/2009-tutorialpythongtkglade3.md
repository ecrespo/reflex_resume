Title: Developing graphical applications with python+gtk+glade. Part 3
Date: 2009-06-17 08:00
Category: Tutorial Python
Tags: Linux,Python,gtk,glade
lang: en
translation: true

Now I will show how to use the combobox widget. The idea is to show a list of countries
in the first combo and, when it changes, to change the list of cities according to the country.

In the interface developed with glade I place 2 comboboxes, 1 label and 2 buttons. The
first combobox contains the countries and is filled in from glade; the 2nd combobox is
left empty and handled via python. The following figure shows the interface in glade.

The interface created with glade is shown in the following figure:

![Tutorial 3 Glade 1](./images/tutorialpythongtkglade3-1.png)

The program code is the following:

![Code](./images/tutorialpythongtkglade3-codigo.png)

When you run the program, the following is shown:
![Tutorial 3 Glade 2](./images/tutorialpythongtkglade3-2.png)

Then you select the country: Venezuela, Argentina or Scotland. Each time you change the
country and select the city, then you click the accept button and the country and the city
appear in the label.

![Tutorial 2 Glade 3](./images/tutorialpythongtkglade3-3.png)

![Tutorial 2 Glade 3](./images/tutorialpythongtkglade3-4.png)

![Tutorial 2 Glade 3](./images/tutorialpythongtkglade3-5.png)

You can download the application code from github at the following
[link (broken link)](https://github.com/ecrespo/ecrespo.github.io/blob/master/content/code/2009/tutorialgtkglade3.py).

===

Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
