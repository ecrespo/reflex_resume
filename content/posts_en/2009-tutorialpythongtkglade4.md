Title: Developing graphical applications with python+gtk+glade. Part 4
Date: 2009-06-17 10:00
Category: Tutorial Python
Tags: Linux,Python,gtk,glade
lang: en
translation: true

The following example will explain how to handle 2 windows in an application.

The first window shows 2 labels, one with some text and the other blank, then
a data entry field asking for the name, and 2 buttons, one to capture the text and one
to exit. When you click the capture text button, another window opens asking whether you are
sure about what you want to do; if you accept, the text is shown in the label.

The following figure shows the interface developed with glade.

![Tutorial 4 Glade 1](./images/tutorialpythongtkglade4-1.png)

The program code is the following:

![Code](./images/tutorialpythongtkglade4-codigo.png)

When the program runs, the following figure is shown:

![Tutorial 4 Glade 2](./images/tutorialpythongtkglade4-2.png)

Type the name and press capture text:
![Tutorial 4 Glade 3](./images/tutorialpythongtkglade4-3.png)

When you press capture text, a window opens asking whether you want to
accept or quit the application.

![Tutorial 4 Glade 4](./images/tutorialpythongtkglade4-4.png)

Finally, the captured text is shown in the label.

![Tutorial 4 Glade 5](./images/tutorialpythongtkglade4-5.png)

You can download the application code from github at the following
[link (broken link)](https://github.com/ecrespo/ecrespo.github.io/blob/master/content/code/2009/tutorialgtkglade4.py).

===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
