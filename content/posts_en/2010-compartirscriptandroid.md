Title: Sharing scripts for Android
Date: 2010-07-03 10:00
Category: Tutorial Android
Tags: Android, Python
lang: en
translation: true

This article explains the process of sharing files for Android; the English guide can be found on the [ASE](http://code.google.com/p/android-scripting/wiki/SharingScripts) site. 

The process is based on generating a QR barcode. The ZXing project lets you generate barcodes from the internet; you can find the link to generate the code [here](http://zxing.appspot.com/generator/).

The process for sharing python, perl, tcl, bash, ruby or lua scripts is the following:
Generate the QR barcode: 

1. Go to the ZXing project's online code generator.
2. Select text as the content
3. In the text field, add the script name on the first line, for example prueba.py
4. On the following lines, put the program code
5. Select the barcode size L
6. Click generate
7. Share the barcode image or embed the generated link

Download the script to the phone:

1. Run ASE and go back to the list of scripts
2. Press the Menu button
3. Select add
4. Select scan barcode
5. Scan the previously generated code and the script will be added to the list of scripts


Keep in mind that the scripts have to be small, since QR only supports 4,296 characters.

Below I add the QR codes of the scripts explained in the previous articles:

* Sending text messages from Android with python

![chart1](./images/chart1.png)

* Sending emails from Android with python.

![Email](./images/chart_correo.png)

* Barcode reader made in python.

![Barcode](./images/codigobarras.png)

* Scanning wireless networks with python from Android. 

![Scan wifi](./images/scan_wifi.png)

In the following articles about scripts for Android, the QR codes will be included to make the scripts easier to use.



===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)