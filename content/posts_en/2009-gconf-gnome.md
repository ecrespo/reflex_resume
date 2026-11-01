Title: Changing the gnome configuration with gconf from python
Date: 2009-07-17 10:00
Category: Tutorial,Desarrollo
Tags: Python,Gnome
lang: en
translation: true

In gnome there is the gconf-editor tool, where you can change the configuration
of the desktop and of applications.

The figure shows the editor:

![gconf Gnome](./images/gconf-gnome.png)

The idea is to use the python module called gconf to manipulate the desktop
configuration parameters.

```
Se importa el módulo gconf
>>> import gconf
#Conectarse con el escritorio gnome.
>>> gconfClient = gconf.client_get_default()
#Se le asigna el nombre de usuario a la aplicación apps/pyconchatter/
>>> gconfClient.set_string("/apps/pyconchatter/username", "ecrespo")
True
#Se obtiene el nombre de usuario de la aplicación pyconchatter
>>> usuario = gconfClient.get_string("/apps/pyconchatter/username")
>>> print usuario
ecrespo
>>>
>>> panel = gconfClient.get_string("/apps/panel/toplevels/panel_1/auto_hide")
>>> print panel
None
#Se obtiene los valores de los accesos rápidos del teclado para el orca.
>>> print gconfClient.get_string("/apps/metacity/keybinding_commands/command_1")
orca
>>> print gconfClient.get_string("/apps/metacity/global_keybindings/run_command_1")
o
>>>
#Devuelve el nombre del archivo del fondo de pantalla del escritorio.
>>> print gconfClient.get_string("/desktop/gnome/background/picture_filename")
/home/ernesto/Escritorio/12003375.jpg
```

With this module you can build graphical applications with gtk, and the application's
configuration parameters can be handled from gconf with python.


===

Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)