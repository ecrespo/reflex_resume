Title: Creating a Debian package that contains a cron file with config-package-dev
Date: 2011-11-14 09:00
Category: Linux,Empaquetado
Tags: Canaima,Debian,Empaquetado,General,Ubuntu
lang: en
translation: true

The `config-package-dev` package makes it easy to create a Debian package that contains a cron configuration file.

In this case I will create a cron file for the `logcheck` program. This program will be a Pre-Depends so that it is installed and configured before installing the package with the `logcheck` configuration in cron.

Install `logcheck`:  

```
apt-get install logcheck
```

The cron file for `logcheck` will contain the following:

```
# /etc/cron.d/logcheck: crontab entries for the logcheck package

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

@reboot logcheckif [ -x /usr/sbin/logcheck ]; then nice -n10 /usr/sbin/logcheck -R; fi
* * * * *   logcheckif [ -x /usr/sbin/logcheck ]; then nice -n10 /usr/sbin/logcheck; fi

# EOF
```

##Procedure to create the package:  

 
#### 1. Create the working directory and the Debian directory

``` 
mkdir -p canaima-cron-logcheck-0.1

mkdir -p canaima-cron-logcheck-0.1/debian
```

#### 2. Create the `debian/changelog` file.  

```
canaima-cron-logcheck (0.1) unstable; urgency=low

* Initial release.

-- Ernesto Nadir Crespo Avila <ecrespo@gmail.com>  Mon, 14 Nov 2011 21:48:20 -0430
```

#### 3. Create the `compat` file with the value 7.

#### 4. Create the `control` and `control.in` files with the following:

`logcheck` is set as a pre-dependency, and the `standar version` is set to `3.9.2`.  

```
Source: canaima-cron-logcheck
Section: config
Priority: extra
Maintainer: Ernesto Nadir Crespo Avila <ecrespo@gmail.com>
Build-Depends: cdbs (>= 0.4.23-1.1), debhelper (>= 4.2.0), config-package-dev (>= 4.5~)
Standards-Version: 3.9.2

Package: canaima-cron-logcheck
Architecture: all
Depends: cdbs, ${misc:Depends}
Pre-Depends: logcheck
Provides: ${diverted-files}
Conflicts: ${diverted-files}
Description: Configuracion de cron para logcheck
Configuracion de cron para logcheck.
```

#### 5. Create the `debian/copyright` file:
The package author is kept because the `config-package-dev` cron example for logcheck is being used as is.  

```
canaima-cron-logcheck.
Example config-package-dev package.

Author: Tim Abbott <tabbott@mit.edu>

Copyright © 2008 Tim Abbott <tabbott@mit.edu>

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

#### 6. Create the `debian/canaima-cron-logcheck.cron.d` file with the cron contents for `logcheck`:  
```
# /etc/cron.d/logcheck: crontab entries for the logcheck package

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root

@reboot logcheckif [ -x /usr/sbin/logcheck ]; then nice -n10 /usr/sbin/logcheck -R; fi
* * * * *   logcheckif [ -x /usr/sbin/logcheck ]; then nice -n10 /usr/sbin/logcheck; fi

# EOF
```

#### 7. Create the `debian/rules` file with the following contents:
```
#!/usr/bin/make -f

DEB_DIVERT_EXTENSION = .canaima

 # This will remove /etc/cron.d/logcheck
  DEB_REMOVE_FILES_canaima-cron-logcheck += \
/etc/cron.d/logcheck

 # We will install (using dh_installcron, by placing the new cron job
 # at debian/canaima-cron-logcheck.cron.d) a new version that runs
 # every minute, rather than every 30 minutes.  This will generate a
 # lot of mail.  Note that we cannot install a new file to the path
 # /etc/cron.d/logcheck from which a file was removed using
 # DEB_REMOVE_FILES.

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/rules/config-package.mk
```

#### 8. Add execute permission to the `debian/rules` file:
	
```
chmod a+x debian/rules
```

#### 9. In the end you have the following files:
```
ecrespo@jewel:~/canaima/canaima-cron-logcheck-0.1$ ls -l debian/
total 28
-rw-r--r-- 1 ecrespo ecrespo  347 nov 14 22:02 canaima-cron-logcheck.cron.d
-rw-r--r-- 1 ecrespo ecrespo  157 nov 14 21:50 changelog
-rw-r--r-- 1 ecrespo ecrespo2 nov 14 21:50 compat
-rw-r--r-- 1 ecrespo ecrespo  481 nov 14 21:55 control
-rw-r--r-- 1 ecrespo ecrespo  481 nov 14 21:55 control.in
-rw-r--r-- 1 ecrespo ecrespo 1169 nov 14 22:01 copyright
-rwxr-xr-x 1 ecrespo ecrespo  612 nov 14 22:06 rules
```

#### 10. Build and sign the `canaima-cron-logcheck-0.1` package:

```
dpkg-buildpackage -rfakeroot -kC97E7015
```

#### 11. In the end the following files are created:  
```
ls -l canaima-cron-logcheck*
-rw-r--r-- 1 ecrespo ecrespo 2902 nov 14 22:08 canaima-cron-logcheck_0.1_all.deb
-rw-r--r-- 1 ecrespo ecrespo  876 nov 14 22:08 canaima-cron-logcheck_0.1.dsc
-rw-r--r-- 1 ecrespo ecrespo 1551 nov 14 22:09 canaima-cron-logcheck_0.1_i386.changes
-rw-r--r-- 1 ecrespo ecrespo 1807 nov 14 22:08 canaima-cron-logcheck_0.1.tar.gz
```

#### 12. Check whether the package complies with Debian policy using `lintian`:

```
lintian -i canaima-cron-logcheck_0.1.dsc
```

#### 13. Install the package:

```
dpkg -i canaima-cron-logcheck_0.1_all.deb
```

#### 14. The cron file is now installed:  
```
ls -l /etc/cron.d
total 12
-rw-r--r-- 1 root root 244 nov  1  2009 anacron
-rw-r--r-- 1 root root 347 nov 14 22:08 canaima-cron-logcheck
-rw-r--r-- 1 root root 544 sep 13 05:59 php5
```

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)