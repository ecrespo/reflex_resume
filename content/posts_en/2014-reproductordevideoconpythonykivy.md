Title: Video player with python and kivy  
Date: 2014-04-19 10:00  
Category: Tutorial Python  
Tags: Android,Canaima,Debian,General,gnome,Python,Ubuntu,kivy
lang: en
translation: true  


From the two previous articles, the [introductory one with label handling](/blog/desarrollodeaplicacionesmultiplataformaconpythonykivy); and 
[the one on button and scatter](/blog/widgetbuttonyscatterwidgetdecomportamientoenkivy) now I will explain something more complete, playing a video.

This article is based on an [English article about a video player and scatter with kivy (broken link)](http://karanbalkar.com/2012/10/learning-kivy-video-player-and-scatter-widgets/).

Now I will show how to associate an event (a function) with the button when it is clicked.

Below is the player code:
```python
#Se importa kivy y se valida que es la versión 1.8.0

import kivy

kivy.require('1.8.0')



#Se importa la clase App

from kivy.app import App

#Se importa Button, Widget y VideoPlayer

from kivy.uix.button import Button

from kivy.uix.widget import Widget

from kivy.uix.videoplayer import VideoPlayer



#Se instancia Widget y Button.

parent= Widget()

button= Button()



#Se crea la clase MyApp que hereda de App

class MyApp(App):

    #Se define el método build.

    def build(self):

         #Se instancia Button con su texto y tamaño del  mismo.

         button = Button(text='Reproductor Video', font_size=14)

         #Se asocia al boton la función on_button_press al argumento on_press

         button.bind(on_press=on_button_press)  

         #Se agrega button a la instancia de parent

         parent.add_widget(button) #agrega el boton

         #Retorna parent 

         return parent



#Se define la función on_button_press

def on_button_press(self):

        #Se crea la instancia de VideoPlayer donde se le pasa como argumento la fuente de vídeo,

        #el estado y la opción allow_stretch True.

        video= VideoPlayer(source='Tribus-SethGodin.webm', state='play',options={'allow_stretch': True})

        #Se agrega el vídeo a la instancia parent

        parent.add_widget(video) #add videoplayer

        #Se retorna parent

        return parent

     

if __name__ == '__main__':

    MyApp().run()

```



The result of running the script is shown in the following video:

[https://youtu.be/todhoMD1jBY (broken link)](https://youtu.be/todhoMD1jBY "https://youtu.be/todhoMD1jBY")

[!embed](https://youtu.be/todhoMD1jBY)


Note: The player video has no audio problems; the problem is with the screencast generator, which I have not managed to make record audio :-/ ...


If you want to know more about the VideoPlayer widget you can see the following [link](https://kivy.org/doc/stable/api-kivy.uix.videoplayer.html#kivy.uix.videoplayer.VideoPlayer.allow_fullscreen).

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
