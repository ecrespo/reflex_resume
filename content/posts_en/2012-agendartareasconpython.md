Title: Scheduling tasks with python
Date: 2012-07-18 9:00 
Category: Tutorial Python
Tags: Canaima,Debian,Linux,Python,Ubuntu,Tareas periodicas
lang: en
translation: true

In Linux you can run processes periodically thanks to `cron` or at a given time thanks to `at`.

In python there is a library that lets you run tasks periodically or on a given date in the style of `cron` or `at`; the library is called [APScheduler](https://pypi.org/project/APScheduler/) (Advanced Python Scheduler). You can read the `SPScheduler` documentation at this [link](https://apscheduler.readthedocs.io/en/latest/).

The example shown below runs 2 tasks: the first task runs at 1 minute intervals, and the second task runs Monday through Friday at a specific time.

The example code is shown below:
```python
#!/usr/bin/env python

#Se importa Scheduler

from apscheduler.scheduler import Scheduler

#Se importa ctime y sleep

from time import ctime,sleep

#Se crea la instancia de la clase Scheduler

sched = Scheduler()

#Se crea una funcion con la tarea1, pero se dfine

#un decorador para la tarea para que sea periodica

#Cada minuto se ejecutara la tarea.

@sched.interval_schedule(minutes=1)

def Tarea1():

    #Muestra en pantalla la fecha y hora

    print "Se ejecuta cada minuto: %s" %ctime()

#Se crea la tarea2 al estilo cron por medio de un decorador cron

#que se ejecuta de lunes a viernes a las 9:40pm.

@sched.cron_schedule(day_of_week='mon-fri', hour=21,minute=30)

def Tarea2():

    #Se muestra en pantalla la hora del momento que se ejecuta la aplicacion.

    print "Se ejecuto a las : %s" %ctime()

#Se pasa la configuracion al scheduler

sched.configure()

#Se inicia el scheduler

sched.start()

#Se muestra las tareas definidas.

print sched.print_jobs()

#Se crea un ciclo de 10 iteraciones

#Donde se espera un minuto por cada iteracion

#Se muestra en pantalla las veces que se ejecuta.

for i in range(10):

    print "---- %s" %i

    sleep(60)

#Se detiene las tareas del scheduler al finalizar

#las iteraciones

sched.shutdown(wait=False)
```
The output of the program's execution is shown below:

```
ernesto@clara:~/bin/python/procesos$ sudo ./procesos2.py 

Jobstore default:

    Tarea1 (trigger: interval[0:01:00], next run at: 2012-07-18 21:27:59.911483)

    Tarea2 (trigger: cron[day_of_week='mon-fri', hour='21', minute='30'], next run at: 2012-07-18 21:30:00)

None

---- 0

Se ejecuta cada minuto: Wed Jul 18 21:27:59 2012

---- 1

Se ejecuta cada minuto: Wed Jul 18 21:28:59 2012

---- 2

Se ejecuta cada minuto: Wed Jul 18 21:29:59 2012

Se ejecuto a las : Wed Jul 18 21:30:00 2012

---- 3

Se ejecuta cada minuto: Wed Jul 18 21:30:59 2012

---- 4

Se ejecuta cada minuto: Wed Jul 18 21:31:59 2012

---- 5

Se ejecuta cada minuto: Wed Jul 18 21:32:59 2012

---- 6

Se ejecuta cada minuto: Wed Jul 18 21:33:59 2012

---- 7

Se ejecuta cada minuto: Wed Jul 18 21:34:59 2012

---- 8

Se ejecuta cada minuto: Wed Jul 18 21:35:59 2012

---- 9

Se ejecuta cada minuto: Wed Jul 18 21:36:59 2012
```
With this library you can schedule processes to run on certain days and times, or periodically.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)