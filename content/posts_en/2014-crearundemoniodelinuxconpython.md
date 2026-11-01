Title: Creating a Linux daemon with Python  
Date: 2014-02-02 9:00  
Category: Tutorial Python  
Tags: Canaima,Debian,Fedora,General,Linux,Python,Ubuntu,Python-daemon,Python-lockfile  
lang: en
translation: true  
 
This article is based on the [following article in English](http://www.gavinj.net/2012/06/building-python-daemon-process.html).  
The idea is to create a Linux daemon process with Python.  
For that, the following 2 python libraries are required:

- `Python-daemon`
- `Python-lockfile`

The Debian way uses the `apt-get` command:
```
#apt-get install python-daemon python-lockfile
```
The python way runs the pip command:
```python
#pip install python-daemon lockfile
```
Below is the file `demonioprueba.py`, which will be placed in the directory `/usr/share/demonioprueba/`.

```python
#!/usr/bin/env python


# -*- coding: utf-8 -*-





#libreria estándar loggin y time


import logging


import time





#de python-daemon import runner


from daemon import runner





class App():


    def __init__(self):


        #Se define unos path estándar en linux.


        self.stdin_path = '/dev/null'


        self.stdout_path = '/dev/tty'


        self.stderr_path = '/dev/tty'


        #Se define la ruta del archivo pid del demonio.


        self.pidfile_path =  '/var/run/demonioprueba/demonioprueba.pid'


        self.pidfile_timeout = 5





    def run(self):


        i = 0


        while True:


            #El código principal va acá


            i += 1


            #Diferentes niveles de registro de bitacora


            logger.debug("Debug message %s" %i)


            logger.info("Info message %s" %i)


            logger.warn("Warning message %s" %i)


            logger.error("Error message %s" %i)


            time.sleep(1)





#Se crea la instancia de la clase


app = App()


#define la instancia de la clase logging para generar la bitacora


logger = logging.getLogger("demonioprueba log")


logger.setLevel(logging.INFO)


#Se define el forma del log


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


handler = logging.FileHandler("/var/log/demonioprueba/demoniopruebas.log")


handler.setFormatter(formatter)


logger.addHandler(handler)





#Se ejecuta el demonio llamando al objeto app


daemon_runner = runner.DaemonRunner(app)


#Esto evita que el archivo log no se cierre durante la ejecución del demonio


daemon_runner.daemon_context.files_preserve=[handler.stream]


#Ejecuta el método run del objeto app


daemon_runner.do_action()

```

The file is saved at the path `/usr/share/demonioprueba/demonioprueba.py`.
The directories `/var/log/demonioprueba` and `/var/run/demonioprueba/` are created:
```
#mkdir -p /var/log/demonioprueba
#mkdir -p /var/run/demonioprueba
```
You can test the daemon by running the following command:
```python
python/usr/share/demonioprueba/demonioprueba.py start
root@heimdal:~# started with pid 5915
```
It shows that the daemon started with pid 5915.
Running `ps aux  | grep demonioprueba.py` shows the running process:  
```
root@heimdal:~# ps aux | grep demonioprueba.py
root      5915  0.0  0.1  38088  6656 ?        S    17:00   0:00 python /usr/share/demonioprueba/demonioprueba.py start
```
As you can see, the process started with pid 5915. 

You can see the log by running:
```
tail -f /var/log/demonioprueba/demonioprueba.log
```
Below is part of the log:
```
2014-02-02 17:01:25,516 - demonioprueba log - WARNING - Warning message 80
2014-02-02 17:01:25,516 - demonioprueba log - ERROR - Error message 80
2014-02-02 17:01:26,517 - demonioprueba log - INFO - Info message 81
2014-02-02 17:01:26,517 - demonioprueba log - WARNING - Warning message 81
2014-02-02 17:01:26,518 - demonioprueba log - ERROR - Error message 81
2014-02-02 17:01:27,519 - demonioprueba log - INFO - Info message 82
2014-02-02 17:01:27,519 - demonioprueba log - WARNING - Warning message 82
2014-02-02 17:01:27,519 - demonioprueba log - ERROR - Error message 82
2014-02-02 17:01:28,520 - demonioprueba log - INFO - Info message 83
2014-02-02 17:01:28,521 - demonioprueba log - WARNING - Warning message 83
2014-02-02 17:01:28,521 - demonioprueba log - ERROR - Error message 83
2014-02-02 17:01:29,522 - demonioprueba log - INFO - Info message 84
2014-02-02 17:01:29,523 - demonioprueba log - WARNING - Warning message 84
2014-02-02 17:01:29,523 - demonioprueba log - ERROR - Error message 84
2014-02-02 17:01:30,523 - demonioprueba log - INFO - Info message 85
2014-02-02 17:01:30,524 - demonioprueba log - WARNING - Warning message 85
2014-02-02 17:01:30,524 - demonioprueba log - ERROR - Error message 85
```
You can stop the daemon by running:
```
root@heimdal:~# python /usr/share/demonioprueba/demonioprueba.py stop
Terminating on signal 15
```

Now the init file for demonioprueba will be created (save the file at `/etc/init.d/demonioprueba`):

Below is the bash script used as a template for the init daemon:
```python
#!/bin/bash

# Copyright (c) 1996-2012 My Company.

# All rights reserved.

#

# Author: Bob Bobson, 2012

#

# Please send feedback to bob@bob.com

#

# /etc/init.d/demonioprueba

#

### BEGIN INIT INFO

# Provides: demonioprueba

# Required-Start:

# Should-Start:

# Required-Stop:

# Should-Stop:

# Default-Start:  3 5

# Default-Stop:   0 1 2 6

# Short-Description: Test daemon process

# Description:    Runs up the test daemon process

### END INIT INFO



# Activate the python virtual environment

#    . /path_to_virtualenv/activate



case "$1" in

  start)

    echo "Starting server"

    # Start the daemon

    python /usr/share/demonioprueba/demonioprueba.py start

    ;;

  stop)

    echo "Stopping server"

    # Stop the daemon

    python /usr/share/demonioprueba/demonioprueba.py stop

    ;;

  restart)

    echo "Restarting server"

    python /usr/share/demonioprueba/demonioprueba.py restart

    ;;

  *)



    # Refuse to do other stuff


    echo "Usage: /etc/init.d/demonioprueba.sh {start|stop|restart}"


    exit 1


    ;;


esac





exit 0

```


Change the permissions of the script:
```
chmod u+x demonioprueba.sh
```
Enable the script for automatic execution:
```
root@heimdal:/etc/init.d# insserv demonioprueba.sh
```
Here is [a similar example (broken link)](https://nanvel.name/weblog/python-unix-daemon/).


##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)