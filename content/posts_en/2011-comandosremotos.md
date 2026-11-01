Title: Running remote commands and transferring files with Python
Date: 2011-02-09 09:00
Category: Tutorial Linux y Python
Tags: Linux, Debian, Paramiko, Python, ssh
lang: en
translation: true

This article explains how to make ssh connections automatically and transfer files using Python.

The first thing to do is create the public and private keys for ssh so you can run remote commands without a password. A guide on how to do it is on [Rafael Bonifaz's blog](http://rafael.bonifaz.ec/blog/2011/01/ssh-con-claves-publicas-y-privadas/).

The first example establishes a remote ssh connection and runs a command on the remote machine.

```python
!/usr/bin/env python
#Programa que ejecuta un comando de forma remota


#Se importa el módulo paramiko
import paramiko


#Se crea la función ssh donde se le pasa el usuario, la IP del equipo remoto, el comando a ejecutar, la clave
#del usuario en el equipo remoto (en este caso se autentica por llaves), puerto de la conexión ssh y se guarda
#un log de la conexión.


def ssh(usuario,hostname,comando,puerto=22,log="paramiko.log"):
        #Se guarda el log
        paramiko.util.log_to_file(log)
        #Se define la ruta donde se encuentra la llave RSA
        llave = "/home/ernesto/.ssh/id_rsa"
        #Se carga la llave RSA
        key = paramiko.RSAKey.from_private_key_file(llave)
        #Se crea la instancia del cliente ssh
        conexion = paramiko.SSHClient()
        #Se carga las llaves del host para validar la autenticación por llaves.
        conexion.load_system_host_keys()
        #Se establece la conexión pasando la IP, puerto del equipo, el usuario y su clave.
        conexion.connect(hostname,puerto,usuario,pkey=key)
        #Se crea una tupla con la entrada estándar, salida estándar y los mensajes de error al ejecutar el comando.
        stdin,stdout,stderr = conexion.exec_command(comando)
        #Se lee la salida estándar y se presenta la información en pantalla.
        print stdout.read()
        #Se cierra la conexión ssh.
        conexion.close()


if __name__ == "__main__":
        #Se ejecuta la función
        ssh("admin","80.13.11.25","ls -l")


```

The output of the command is the following:

```
total 93960


drwxr-xr-x  2 admin admin     4096 feb  3 01:00 prueba
drwxr-xr-x  2 admin admin     4096 may  4  2010 public_html
-rw-r--r--  1 admin admin  3180604 ene 30 16:17 web2py-manual.pdf
```

For file transfer, RSA keys will be used so the user's password does not have to be passed in the Python script. The idea is to connect to the remote machine and transfer the files found in a directory.


Here is the program code:

```python
#!/usr/bin/env python
#Programa que permite transferir archivos de un equipo remoto al local
#Se importa los módulos paramiko y os.
import paramiko,os


#Se crea la función recuperar archivo con los argumentos equipo, puerto, usuario y ruta del directorio donde
#se encuentran los archivos.


def recuperar_archivos(equipo,puerto,usuario,dir_path):
    #Se define la ruta donde se encuentra la llave RSA
    llave = "/home/ernesto/.ssh/id_rsa"
    #Se carga las llaves en la variable key
    key = paramiko.RSAKey.from_private_key_file(llave)
    #Se le pasa el equipo y puerto como parámetro de transporte
    c = paramiko.Transport((equipo,puerto))
    #Se crea la conexión pasando el usuario y la llave RSA.
    c.connect(username=usuario,pkey=key)
    #Se crea la conexión sftp donde se le pasa la conexión definida anteriormente.
    sftp = paramiko.SFTPClient.from_transport(c)
    #Se captura la lista de archivos de la ruta que se le pasa a la función.
    archivos = sftp.listdir(dir_path)
    #Se presenta un mensaje de recibiendo los archivos y se realiza la transferencia.
    for f in archivos:
        print "Recibiendo ",f
        sftp.get(os.path.join(dir_path,f),f)
    #Al finalizar se cierra la conexión.
    c.close()


if __name__ == "__main__":
    #Se ejecuta la función donde se le pasa la IP del equipo remoto con el puerto, luego el usuario y la ruta de
    #los archivos a transferir.
    recuperar_archivos("80.13.11.25",22,"admin","/home/admin/prueba/")

```

The output is the following:

```
Recibiendo  control-python.pdf
Recibiendo  web2py-manual.pdf
```




===

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
