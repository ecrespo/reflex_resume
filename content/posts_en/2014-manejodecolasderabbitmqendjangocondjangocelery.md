Title: Managing RabbitMQ queues in Django with Django-Celery  
Date: 2014-04-29 9:00  
Category: Tutorial Python  
Tags: Canaima,Debian,Python,Ubuntu,Django,Django-Celery
lang: en    
translation: true  
 
[A while ago I wrote about 3 articles about Django](/blog/tags), and now I will cover a somewhat more complex topic that is useful when you need performance in processes.

Below I explain a simple process for managing `RabbitMQ` queues through `Django-Celery`.

The idea is to do a basic installation and configuration, without having `RabbitMQ` on several virtual machines and handling the authentication of the different queues of the different machines.

You can find the documentation at the following [link](https://celery.readthedocs.io/en/latest/getting-started/first-steps-with-celery.html).

The first thing you need is to have `rabbitMQ` installed on Debian Wheezy.
```
#aptitude install rabbitmq-server
```
After the installation, verify that the service starts:
```
root@pruebas:~# invoke-rc.d rabbitmq-server status 
Status of node rabbit@pruebas ...
[{pid,3595},
 {running_applications,[{rabbit,"RabbitMQ","2.8.4"},
                        {mnesia,"MNESIA  CXC 138 12","4.7"},
                        {os_mon,"CPO  CXC 138 46","2.2.9"},
                        {sasl,"SASL  CXC 138 11","2.2.1"},
                        {stdlib,"ERTS  CXC 138 10","1.18.1"},
                        {kernel,"ERTS  CXC 138 10","2.15.1"}]},
 {os,{unix,linux}},
 {erlang_version,"Erlang R15B01 (erts-5.9.1) [source] [64-bit] [async-threads:30] [kernel-poll:true]\n"},
 {memory,[{total,26213352},
          {processes,10386936},
          {processes_used,10386922},
          {system,15826416},
          {atom,504409},
          {atom_used,473948},
          {binary,263704},
          {code,11874771},
          {ets,771120}]},
 {vm_memory_high_watermark,0.39999999862767177},
 {vm_memory_limit,233180364},
 {disk_free_limit,1000000000},
 {disk_free,6221991936},
 {file_descriptors,[{total_limit,924},
                    {total_used,8},
                    {sockets_limit,829},
                    {sockets_used,5}]},
 {processes,[{limit,1048576},{used,167}]},
 {run_queue,0},
 {uptime,5808}]
...done.
```

You can also verify it with the `rabbitctl` command:
``` 
root@pruebas:~# rabbitmqctl status 
Status of node rabbit@pruebas ...
[{pid,3595},
 {running_applications,[{rabbit,"RabbitMQ","2.8.4"},
                        {mnesia,"MNESIA  CXC 138 12","4.7"},
                        {os_mon,"CPO  CXC 138 46","2.2.9"},
                        {sasl,"SASL  CXC 138 11","2.2.1"},
                        {stdlib,"ERTS  CXC 138 10","1.18.1"},
                        {kernel,"ERTS  CXC 138 10","2.15.1"}]},
 {os,{unix,linux}},
 {erlang_version,"Erlang R15B01 (erts-5.9.1) [source] [64-bit] [async-threads:30] [kernel-poll:true]\n"},
 {memory,[{total,26211600},
          {processes,10386952},
          {processes_used,10386938},
          {system,15824648},
          {atom,504409},
          {atom_used,473972},
          {binary,262176},
          {code,11874771},
          {ets,771120}]},
 {vm_memory_high_watermark,0.39999999862767177},
 {vm_memory_limit,233180364},
 {disk_free_limit,1000000000},
 {disk_free,6221991936},
 {file_descriptors,[{total_limit,924},
                    {total_used,8},
                    {sockets_limit,829},
                    {sockets_used,5}]},
 {processes,[{limit,1048576},{used,167}]},
 {run_queue,0},
 {uptime,5848}]
...done.
```
Since the Django connection is with a single machine, `rabbitMQ` authentication is not required, so you can see that step at the following [link (broken link)](https://celery.readthedocs.io/en/latest/getting-started/brokers/rabbitmq.html).

Now `python`, `celery` and `django-celery` will be installed:
``` 
#aptitude install python2.7 python2.7-dev python-django python-django-celery python-celery
```

Once the installation finishes, a django project will be created:
The django directory is created in `/srv/`
```
#mkdir -p /srv/django 
```
Then the pasarela project is created with the `django-admin` command:
```
root@pruebas:/srv/django# django-admin startproject pasarela
```
Inside the pasarela directory you will find the file structure that django uses:
```
-rwxr-xr-x 1 pasarela pasarela   251 abr 29 15:32 manage.py
drwxr-xr-x 3 pasarela pasarela  4096 abr 29 16:49 pasarela
-rw-rw-rw- 1 pasarela pasarela 69632 abr 29 16:59 pasarela.db
```  

Then inside the pasarela directory you have the following:
```  
root@pruebas:/srv/django/pasarela/pasarela# ls -l
total 32
-rw-r--r-- 1 pasarela pasarela    0 abr 29 15:32 __init__.py
-rw-r--r-- 1 pasarela pasarela 5464 abr 29 16:46 settings.py
-rw-r--r-- 1 pasarela pasarela  562 abr 29 15:32 urls.py
-rw-r--r-- 1 pasarela pasarela 1138 abr 29 15:32 wsgi.py
```
Create the `apps` directory:
```
root@pruebas:/srv/django/pasarela/pasarela#mkdir -p apps
```
Inside the directory, create the `__init__.py` file:
```
root@pruebas:/srv/django/pasarela/pasarela/apps# touch __init__,py
```
Now create the `sms` application:
``` 
root@pruebas:/srv/django/pasarela/pasarela/apps# django-admin startapp sms
```
The `sms` directory contains the following:
``` 
root@pruebas:/srv/django/pasarela/pasarela/apps/sms# ls -l
total 24
-rw-r--r-- 1 pasarela pasarela   0 abr 29 15:46 __init__.py
-rw-r--r-- 1 pasarela pasarela  57 abr 29 15:46 models.py
-rw-r--r-- 1 pasarela pasarela 383 abr 29 15:46 tests.py
-rw-r--r-- 1 pasarela pasarela  26 abr 29 15:46 views.py
```
In this directory, create the `tasks.py` file with the following contents: 
```
#Se importa Celery
from celery import Celery
#Se instancia Celery importando tasks, se define el broker (quien recibe los procesos en este 
#caso rabbitMQ con el protocolo amgp) y se define el backend (quien recibe los resultado
#del proceso encolado en este caso con rabbitMQ y el protocolo amgp) 
app = Celery('tasks', broker='amqp://',backend='amqp')

#Se usa el decorador task de app y se define la suma.
@app.task
def add(x, y):
    return x + y
```
What we are going to do is handle the addition through the `rabbitMQ` queue.

Now let's look at the contents of the `settings.py` file (the most relevant parts): 

For now we will work with the `sqlite` database:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pasarela.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
```
Define the application's time zone: 
```
TIME_ZONE = 'America/Caracas'
```
Define the language:
``` 
LANGUAGE_CODE = 'es-ve'
```
Add the `djcelery` and `sms` applications:
``` 
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'djcelery',
    'pasarela.apps.sms',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
```
Now what remains is to synchronize the database (this creates the database for django, what django celery needs, and the application's administrator account):
``` 
root@pruebas:/srv/django/pasarela# python manage.py syncdb
```

Now what remains is to start `celery`: 
Start django's `manage.py`, telling it to start celery at info level and with two concurrent processes.
```
ernesto@pruebas:/srv/django/pasarela$ python manage.py celeryd -E -l info -c 2
/usr/lib/python2.7/dist-packages/djcelery/loaders.py:108: UserWarning: Using settings.DEBUG leads to a memory leak, never use this setting in production environments!
  warnings.warn("Using settings.DEBUG leads to a memory leak, never "
[2014-04-29 17:22:37,272: WARNING/MainProcess]  

 -------------- celery@pruebas v2.5.3
---- **** -----
--- * ***  * -- [Configuration]
-- * - **** ---   . broker:      amqp://guest@localhost:5672//
- ** ----------   . loader:      djcelery.loaders.DjangoLoader
- ** ----------   . logfile:     [stderr]@INFO
- ** ----------   . concurrency: 2
- ** ----------   . events:      ON
- *** --- * ---   . beat:        OFF
-- ******* ----
--- ***** ----- [Queues]
 --------------   . celery:      exchange:celery (direct) binding:celery
                  

[Tasks]
  . pasarela.apps.sms.tasks.add

[2014-04-29 17:22:37,293: INFO/PoolWorker-1] child process calling self.run()
[2014-04-29 17:22:37,297: INFO/PoolWorker-2] child process calling self.run()
[2014-04-29 17:22:37,307: WARNING/MainProcess] celery@pruebas has started.
```

In another console, start django's `manage.py` shell: 
Import the add function that was defined in the `tasks.py` file.
```
ernesto@pruebas:/srv/django/pasarela$ python manage.py shell
Python 2.7.3 (default, Mar 13 2014, 11:03:55) 
[GCC 4.7.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

>>> from pasarela.apps.sms.tasks import add
#Se realiza la suma de 11+19
>>> result = add.delay(11, 19)
#Se obtiene el resultado:
>>> result.get()
30
#Se verifica si ya celery está listo para recibir más procesos:
>>> result.ready()
True
#Se verifica si ya el proceso termino.
>>> result.successful()
True
```
The celery output shows the following:
``` 
[2014-04-29 17:25:36,200: INFO/MainProcess] Got task from broker: pasarela.apps.sms.tasks.add[64275874-545b-4ab9-bfc8-ea38904d2320]
[2014-04-29 17:25:36,228: INFO/MainProcess] Task pasarela.apps.sms.tasks.add[64275874-545b-4ab9-bfc8-ea38904d2320] succeeded in 0.0155239105225s: 30
```

As shown, `celery` receives and returns the result of the addition together with its execution time. If you have several machines with `rabbitMQ`, you can significantly improve how functions are executed in django.

You can check out the following [presentation](https://es.scribd.com/document/57279486/Celery-An-A-Synchronous-Task-Queue-Not-Only-for-Django).


##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)