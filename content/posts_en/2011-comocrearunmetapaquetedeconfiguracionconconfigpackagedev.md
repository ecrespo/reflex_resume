Title: How to create a configuration metapackage with config-package-dev
Date: 2011-11-13 09:00
Category: Linux,Empaquetado 
Tags: Canaima,Debian,Empaquetado,General,ssh,Ubuntu 
lang: en
translation: true

I previously explained how to create a metapackage with `equivs`. There is also the `config-package-dev` package, which lets you create configuration packages that can change the configuration of other files inside the `/etc/` directory.

This article is based on the [MIT tutorial on creating configuration packages for Debian and a guide on the Debian wiki](https://debathena.mit.edu/config-package-dev/) and a guide on the [Debian wiki](https://wiki.debian.org/ConfigPackages). The process of adopting a package and packaging it is explained in a guide on the [Debian wiki (broken link)](https://wiki.debian.org/AdoptarUnPaquete).

As an example I will use the `openssh-server` package, which creates a file named `/etc/ssh/sshd_config` . This file contains the configuration needed to start an `ssh` server.


Installing `openssh-server`:  

```
apt-get install openssh-server config-package-dev
```

The contents of the file are the following:  

```
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_dsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
UsePrivilegeSeparation yes
KeyRegenerationInterval 3600
ServerKeyBits 768
SyslogFacility AUTH
LogLevel INFO
LoginGraceTime 120
PermitRootLogin yes
StrictModes yes
RSAAuthentication yes
PubkeyAuthentication yes
IgnoreRhosts yes
RhostsRSAAuthentication no
HostbasedAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
X11Forwarding yes
X11DisplayOffset 10
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
```

This file has the following md5 hash.  

```
8caefdd9e251b7cc1baa37874149a870  /etc/ssh/sshd_config
```

The idea is to modify this file so that it does not allow the `root` user to connect via `ssh` and does not allow forwarding of graphical applications.

#### Procedure to create the `sshd-config` configuration package:

##### 1. Create the working directory  
 
```
mkdir canaima-sshd-config-0.1
```

##### 2. Change to that directory

```
cd canaima-sshd-config-0.1
```

##### 3. Create the debian and files directories

```
mkdir -p debian files
```

##### 4. In `files` create the `etc` directory, then inside it the `ssh` directory, and copy the `sshd_config` file from `/etc/ssh/` into the created directory.

```
mkdir -p files/etc
mkdir -p files/etc/ssh
cp /etc/ssh/sshd_config ./files/etc/ssh/sshd_config.canaima
```

##### 5. Modify the file so that the root user cannot access the `ssh` server and `X11` packets cannot be forwarded. The lines are:

```
PermitRootLogin no
X11Forwarding no
```  

##### 6. Inside the debian directory, the `changelog` file was created with the following contents:

```
canaima-sshd-config (0.1) unstable; urgency=low

* Initial release.

-- Ernesto Nadir Crespo Avila <ecrespo@gmail.com>  Sun, 13 Nov 2011 10:22:48 -0430
```

##### 7. Create the `debian/compat` file with the value 7.

##### 8. Create the `debian/control` and `debian/control.in` files with the following information:

```
Source: canaima-sshd-config
Section: config
Priority: extra
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@gmail.com>
Build-Depends: cdbs (>= 0.4.23-1.1), debhelper (>= 4.2.0), config-package-dev (>= 4.5~)
Standards-Version: 3.9.2

Package: canaima-sshd-config
Architecture: all
Pre-Depends: openssh-server
Depends: cdbs, ${misc:Depends}
Provides: ${diverted-files}
Conflicts: ${diverted-files}
Description: Archivo de configuracion de ssh
Archivo de configuracion del servidor ssh.
```

In this case the `Pre-Depends` parameter is used because the `openssh` server must be installed and properly configured before changes can be added to the `/etc/ssh/sshd_config` file.

##### 9. Create the `debian/copyright` file. In this case I am using the same copyright as the `config-package-dev` example files:

```
canaima-ssh-config package.

Author: Ernesto Nadir Crespo Avila <ecrespo@gmail.com>

Copyright © 2011 Ernesto Nadir Crespo Avila <ecrespo@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

##### 10. Create the `debian/canaima-sshd-config.install` file. This file defines where the configuration files are taken from and where they are copied to.
 
```
files/* /
```

##### 11. Create the `debian/rules` file. This file defines the `.canaima` extension, which distinguishes the base Debian packages from those of the canaima meta distribution, as well as the file to modify, and then the `cdbs` includes:

```
#!/usr/bin/make -f

DEB_DIVERT_EXTENSION = .canaima
# Replace some base files with simple replacements.
DEB_DIVERT_FILES_canaima-sshd-config += \
/etc/ssh/sshd_config.canaima 
# These files are installed via dh_install from the files/ directory
# (see debian/canaima-sshd-config.install)

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/rules/config-package.mk
```

##### 12. Build the debian package and sign it with the `gpg` key:

```
dpkg-buildpackage -rfakeroot -kC97E7015
```

If you run an `ls` you can see the files that were created:
	
```
ls -l canaima-sshd*
-rw-r--r-- 1 ecrespo ecrespo 3948 nov 13 16:09 canaima-sshd-config_0.1_all.deb
-rw-r--r-- 1 ecrespo ecrespo  864 nov 13 16:09 canaima-sshd-config_0.1.dsc
-rw-r--r-- 1 ecrespo ecrespo 1521 nov 13 16:09 canaima-sshd-config_0.1_i386.changes
-rw-r--r-- 1 ecrespo ecrespo 2745 nov 13 16:09 canaima-sshd-config_0.1.tar.gz
```


##### 13. Check that the Debian package complies with Debian policy:

```
lintian -i canaima-sshd-config_0.1.dsc
```

##### 14. Verify the installation of the Debian package.
```
sudo dpkg -i canaima-sshd-config_0.1_all.deb 
[sudo] password for ecrespo: 
Selecting previously unselected package canaima-sshd-config.
(Leyendo la base de datos ... 418546 ficheros o directorios instalados actualmente.)
Desempaquetando canaima-sshd-config (de canaima-sshd-config_0.1_all.deb) ...
Configurando canaima-sshd-config (0.1) ...
Añadiendo `desviación de /etc/ssh/sshd_config a /etc/ssh/sshd_config.canaima-orig por canaima-sshd-config'
```

##### 15. If you run `ls -l` on `/etc/ssh/sshd_config*` you will see that a link to the original file is created and the files added with the canaima extension are shown:
```
root@jewel:/etc/ssh# ls -l sshd_config*
lrwxrwxrwx 1 root root   19 nov 13 16:16 sshd_config -> sshd_config.canaima
-rw-r--r-- 1 root root 2487 nov 13 10:15 sshd_config.canaima
-rw-r--r-- 1 root root 2489 nov 13 13:20 sshd_config.canaima-orig
```

##### 16. When you check the file you will notice that the field that lets root connect to the ssh server is set to no, and likewise the `X11` forwarding parameter. If you check the file's `md5` hash you will notice that the original file and the current one are different:

```
a358d423fa6b8bf640a7fd1e06731ea3  sshd_config
```

When you create configuration packages this way (a clean way to modify configuration files), removing the configuration package makes the original files get used again:
	
```
apt-get remove -f canaima-sshd-config

root@jewel:/etc/ssh# md5sum sshd_config
8caefdd9e251b7cc1baa37874149a870  sshd_config
``` 

There are several examples of using `config-package-dev`, such as binary packages, cron configuration, etc.


##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
