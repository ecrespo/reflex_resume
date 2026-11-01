Title: Running a task on a future date (APScheduler) 
Date: 2012-07-19 9:00 
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,Tareas
lang: en
translation: true

The [previous](/blog/agendartareasconpython) article explains 2 ways to define tasks periodically and in the style of `crond`. This time I explain how to run a function on a future date.

```python
#!/usr/bin/env python
#Se importa date
from datetime import date
#Se importa Scheduler
from apscheduler.scheduler import Scheduler
#Se importa sleep
from time import sleep

# Se instancia la clase scheduler
sched = Scheduler()
#Se inicia el scheduler
sched.start()

# Se define la función a ser ejecutada.
#La función toma un texto y lo presenta en pantalla.
def Tarea(texto):
    print texto

# La tarea será ejecutada el 19 de Julio de 2012.
fecha_ejecucion = date(2012, 07, 19)

# se alamacena la tarea en la variable tarea en caso que se quiera suspender
#Se le pasa la función Tarea, la fecha a ejecutar y los argumentos solicitados de la función
tarea = sched.add_date_job(Tarea, fecha_ejecucion, ['texto a escribir'])

#Se muestra las tareas definidas.
print sched.print_jobs()
#Se crea un ciclo de 10 iteraciones
#Donde se espera 60 minutos por cada iteracion
#Se muestra en pantalla las veces que se ejecuta.
for i in range(10):
    print "---- %s" %i
    sleep(3600)
#Se detiene el scheduler
sched.shutdown(wait=False)
```

Running the program shows the following:

```
ernesto@clara:~/bin/python/procesos$ sudo ./procesos3.py

Jobstore default:

    Tarea (trigger: date[2012-07-19 00:00:00], next run at: 2012-07-19 00:00:00)

None

---- 0

---- 1

text

---- 2

---- 3

---- 4

---- 5

---- 6

---- 7

---- 8

---- 9
```

This article completes the three ways of running processes with `APScheduler` (periodic execution, crond style and execution on a future date).

##  ##
Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)