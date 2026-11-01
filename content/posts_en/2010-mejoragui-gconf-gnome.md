Title: Update to the program for a graphical interface to configure keyboard shortcuts
Date: 2010-08-08 09:00
Category: Tutorial Python
Tags: Linux,  accesibilidad, gconf, glade, gnome, gtk, Linux, python, tiflotecnologia
lang: en
translation: true

In the previous article I explained the improvement to the script that changes the shortcut key settings in gnome. Now I will explain the improvement to the program mentioned in this [article](/blog/gui-gconf-gnome).

Compared to the previous article, the screenshot shows a combobox that is disabled at the moment; this combobox will let you choose between 3 distributions: Debian, Ubuntu or Canaima.

The image is shown in the following figure:

![GUI](./images/gui-gconf-gnome-2010.png)

The idea is to be able to configure the shortcuts of all the applications shown, or only the ones you want.

```python
def on_button2_clicked(self,*args):
                #Se crea el objeto config de la clase Conf
                Config = configGconf.Conf()
                #Se crea un ciclo con la lista de las aplicaciones.
                for aplicacion in self.__aplicaciones:
                        #Se modifica las aplicaciones una por una pasando la aplicación.
                        Config.modificar_opcion(aplicacion,1)
```

You can download the complete code of the program from [pyconfig-accessgnome-ui.py (broken link)](http://python-config-accesskey-gnome.googlecode.com/hg/pyconfig-accessgnome-ui.py), and the graphical interface built in glade from [pyconfig-accessgnome.glade](http://code.google.com/p/python-config-accesskey-gnome/source/browse/pyconfig-accessgnome.glade).

The next article will explain how to create the python package.

===

Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)