Title: Hello world, 2nd version with hildon and Python
Date: 2008-03-23 10:40
lang: en
Category: Debian, maemo, Nokia N810, Python

The second version of hello world is based on the hildon 
framework, which lets you manage the look and themes of the maemo 
environment, and access the toolbar and menus.

```
#!/usr/bin/env python2.5

import gtk
import hildon

window = hildon.Window()
window.connect("destroy", gtk.main_quit)
label = gtk.Label("Hola mundo!")
window.add(label)

label.show()
window.show()

gtk.main()
```

Screenshot of the script running:

![Hello World from Maemo](./images/fhildon.png)
