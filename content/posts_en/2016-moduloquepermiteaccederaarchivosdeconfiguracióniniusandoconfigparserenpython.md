Title: A module to access .ini configuration files using ConfigParser in Python
Date: 2016-01-04 09:00
Category: Tutorial Python
Tags: Python
lang: en
translation: true

Years ago I had a Python module that gave access to .ini type configuration files (sections, key-value) through the [ConfigParser](https://docs.python.org/2/library/configparser.html) module (you can see an example of how to use ConfigParser [here](https://pymotw.com/2/ConfigParser/)).

That script or module has been used in several projects, and lately I was updating it and incorporating it into an SMS sending development.

This module is general-purpose and should not be embedded in one specific application or in every application that needs it, so [I have created a project on github where I will host this module](https://github.com/Mangoosta/pywrapper-config), and in the near future I hope to upload it to the [Python repositories](https://pypi.org/).

The second version of this module takes concepts from the object-oriented programming articles of previous articles:

1. [Back to basics, OOP in Python (part 1)](/blog/volviendoalobasicopooenpython-1)  
2. [Back to basics, OOP in Python (part 2)](/blog/volviendoalobasicopooenpython-2)  
3. [Back to basics, OOP in Python (part 3)](/blog/volviendoalobasicopooenpython-3)

You can see the first version of the code below:
```
#!/usr/bin/env python
import ConfigParser,os
"""
Descripcion: Modulo que permite manipular archivos de configuracion.
Autor: Ernesto Crespo
Correo: ecrespo@gmail.com
Licencia: GPL Version 3
Copyright: Copyright (C) 2011 Ernesto Nadir Crespo Avila
Version: 0.2

"""

class config:
    """Modulo que permite manejar archivo de configuracion"""    
    def __init__(self,cnffile):
        self.__cnffile = cnffile
        self.__config = ConfigParser.ConfigParser()
        self.__config.read(self.__cnffile)
        
        
    def ShowItemSection(self,section):
        return self.__config.items(section)
    
    def ShowValueItem(self,section,option):
        return self.__config.get(section,option)
    
    def change(self,section,option,value):
        self.__config.set(section,option,value)

    
    def write(self):
        self.__config.write(open(self.__cnffile,'w'))
```

The new version changes the declaration of the object, uses the @property decorator to define the getter and the setter, defines the getattr method and adds the method that shows the sections:

The code of the new version is shown below:
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import ConfigParser
from ConfigParser import ConfigParser

"""
Nombre: pywrapper_config
Descripcion: Modulo que permite manipular archivos de configuracion.
Autor: Ernesto Crespo
Correo: ecrespo@gmail.com
Licencia: GPL Version 3
Copyright: Copyright (C) 2016 Ernesto Nadir Crespo Avila <ecrespo@gmail.com> 
Version: 0.3

"""

#Clase config
class Config(object):
    """Clase Config: facilita el uso del modulo ConfigParser"""

    def __init__(self, cnffile):
        """Constructor toma el archivo de configuracion e inicializa ConfigParser"""
        self._cnffile = cnffile
        self._config = ConfigParser()
        self._config.read(self._cnffile)

    @property
    def cnffile(self):
        """Se consulta el valor del archivo de configuracion"""
        return self._cnffile
    
    @cnffile.setter
    def cnffile(self,cnffile):
        """Se modifica el valor del archivo de configuración y se vuelve a leer el mismo"""
        self._cnffile = cnffile
        self._config.read(self._cnffile)

    def __getattr__(self):
        """__getattr__ devuelve None si se trata de acceder a un atributo que no existe"""
        return None 

    def show_sections(self):
        """Muestra las secciones del archivo de configuracion"""
        return self._config.sections()

    def show_item_section(self, section):
        """Se define la funcion que muestra los item de una seccion"""
        return self._config.items(section)

#
    def show_value_item(self, section, option):
        """Se muestra el valor de los item"""
        return self._config.get(section, option)

#
    def change(self, section, option, value):
        """Se cambia el valor de la opcion"""
        self._config.set(section, option, value)

#
    def write(self):
        """Se escribe al archivo de configuracion"""
        self._config.write(open(self._cnffile,'w'))



if __name__ == '__main__':
    #Se crea la instancia de Config pasando el archivo de configuracion ini
    configuracion = Config("./conf/androidsms.conf")
    #Se muestra las secciones
    print("Secciones: {0} ".format(configuracion.show_sections()))
    #Se muestra los items de la seccion server
    print("Items de la seccion server: {0} ".format(configuracion.show_item_section("server")))
    #Se muestra la ip de la seccion server
    print("IP: {0}".format(configuracion.show_value_item("server","ip")))
    #Se muestra el archivo de configuracion
    print("Archivo de configuracion: {0}".format(configuracion.cnffile))
    #Se cambia en caliente de archivo de configuracion
    configuracion.cnffile = "./conf/python_android_sms.conf"
    print("Archivo de configuracion: {0}".format(configuracion.cnffile))
    #Se muestra las secciones del nuevo archivo de configuracion
    print("Secciones: {0}".format(configuracion.show_sections()))
```
The result of running the previous code is shown below:
```
$ python pywrapper_config.py 
Secciones: ['sqlite', 'time', 'server'] 
Items de la seccion server: [('ip', '"127.0.0.1"'), ('port', '"8080"')] 
IP: "127.0.0.1"
Archivo de configuracion: ./conf/androidsms.conf
Archivo de configuracion: ./conf/python_android_sms.conf
Secciones: ['sqlite', 'time', 'server', 'tiempo', 'usb', 'paths']
```

The trick for switching configuration files is in the setter; here is the code: 
```
    @cnffile.setter
    def cnffile(self,cnffile):
        """Se modifica el valor del archivo de configuración y se vuelve a leer el mismo"""
        self._cnffile = cnffile
        self._config.read(self._cnffile)
```
Besides assigning the configuration file to the private variable cnffile, the configuration file is read again; this makes it easy to switch configuration files on the fly without having to instantiate the Config class again.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)