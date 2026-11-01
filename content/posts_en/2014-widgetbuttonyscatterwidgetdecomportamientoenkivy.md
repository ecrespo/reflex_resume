Title: Button widget and Scatter (behavior widget) in kivy.  
Date: 2014-04-19 08:00  
Category: Tutorial Python  
Tags: Canaima,Debian,General,gnome,Python,Ubuntu,kivy  
lang: en
translation: true  


The [previous article](/blog/desarrollodeaplicacionesmultiplataformaconpythonykivy) showed a short introduction to kivy and how to have a window with a label.

It also showed how to separate the layout from the programming.
Next I will show two examples, one using the button widget and another with a label inside a Scatter (a behavior widget that allows dragging, rotating and scaling a widget).
The article is based on [video tutorial No. 1](https://www.youtube.com/watch?v=F7UKmK9eQLY) from the kivy team:

The python code of the button example is shown below:
```python
#!/usr/bin/env python

#Se importa kivy

import kivy

#Se valida que se tiene la versión 1.8.0 de kivy

kivy.require('1.8.0')



#Se importa la clase App y el widget Button

from kivy.app import App

from kivy.uix.button import Button



#Se crea la clase Hola3App que hereda de App

class Hola3App(App):

    #Se define el método build que devuelve el widget Button sin argumentos.

    def build(self):

        return Button()





if __name__ == "__main__":

    #Se crea la instancia de la clase y se ejecuta.

    Hola3App().run()
```
The file `hola3.kv` with the layout of `hola3.py` is shown below:
It defines the button text, its color (blue) and its size.
```python
# File name: hello2.kv

#:kivy 1.8.0

<Button>: 

  text: 'Hola mundo v3!'

  font_size:100

  background_color:(0,0,1,1)

```

The following video shows the script running:

[https://youtu.be/gFk4w-p4qhc (broken link)](https://youtu.be/gFk4w-p4qhc "https://youtu.be/gFk4w-p4qhc")


The next example uses the Scatter behavior widget; this widget allows dragging, scaling whatever the widget contains and rotating, and it is also a widget that supports multitouch.

The code of ´hola4.py´ is shown below:
```python
#!/usr/bin/env python

#se importa kivy

import kivy

#Se válida que la versión de kivy sea la 1.8.0

kivy.require('1.8.0')



#Se importa la clase App

from kivy.app import App

#Se importa Scatter, Label y FloatLayout

from kivy.uix.scatter import Scatter

from kivy.uix.label import Label

from kivy.uix.floatlayout import FloatLayout





#Se crea la clase Hola4App que hereda de App

class Hola4App(App):

    #Se define el método build

    def build(self):

        #Se instancia al objeto FloatLayout

        f = FloatLayout()

        #Se instancia al objeto Scatter

        s = Scatter()

        #Se instancia al objeto Label con el texto y el tamaño.

        l = Label(text="Hola v4",font_size=100)

        #Se agrega a FloatLayout la instancia del widget scatter

        f.add_widget(s)

        #Se agrega el widget Label a Scatter

        s.add_widget(l)

        #Se retorna la instancia de FloatLayout

        return f





if __name__ == "__main__":

    #Se ejecuta run de la instancia del objeto Hola4App 

    Hola4App().run()

```

The following video shows the result of running the script:

[https://youtu.be/_AeT3LkVwkk (broken link)](https://youtu.be/_AeT3LkVwkk "https://youtu.be/_AeT3LkVwkk")

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)