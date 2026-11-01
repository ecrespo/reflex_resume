Title: Creating a personal Debian repository
Date: 2009-04-04 08:00
Category: Linux
Tags: Debian,Empaquetado
lang: en
translation: true

After a week in which I ended up with an injured left elbow and shoulder, I am going to
explain how to create a personal repository of packages for Debian.

This post is based on the Debian Administration tutorial and on the tutorial
from the Mario Debian blog.

Debian has a program for creating a personal repository, reprepro:

```
aptitude install reprepro
```

You need to install a web server such as:

* apache2
* lighttpd
* cherokee

The structure that reprepro uses is the following:

```
|-- conf
|-- dists
`-- pool
```

In the dist directory there is one directory for each
version of the distribution (etc, lenny, squeeze, sid, etc).
The pool directory holds the packages classified by
section (main, contrib, non-free) and in directories in
alphabetical order.

You need to create the conf directory inside the root directory of the
web server. In it you will create the distributions file with the following
configuration:

```
Origin: Paquetes Ernesto
Label: Paquetes Ernesto
Suite: unstable
Codename: sid
Architectures: i386 source
Components: main
Description: Paquetes elaborados por Ernesto Crespo

Origin: Paquetes Ernesto
Label: Paquetes Ernesto
Suite: testing
Codename: lenny
Architectures: i386 source
Components: main
Description: Paquetes elaborados por Ernesto Crespo


Origin: Paquetes Ernesto
Label: Paquetes Ernesto
Suite: stable
Codename: etch
Architectures: i386 source
Components: main
Description: Paquetes elaborados por Ernesto Crespo
```
This example handles the repositories for lenny, etch and sid with the
binaries for i386 and the sources in the main section of the repository.

To start using reprepro:

1. To upload the binary package to the repository, run:

```
reprepro -b . -V -C main includedeb sid  accesibilidad_1.0_all.deb
```

2. To upload the sources of a package, run:

```
reprepro -b . -V -C main includedsc sid sshguard_1.4rc3-1.dsc
```

3. And its binary:

```
reprepro -b . -V -C main includedeb sid sshguard_1.4rc3-1_i386.deb
```

4. To remove a package from the repository, run:

```
reprepro -b . -V -C main remove sid sshguard_1.4rc3-1_i386.deb
```

5. To use the repository, add the following URL to /etc/apt/sources.list:

```
deb http://midominio/repo/ sid main
```

The directory structure of the repository looks like this:

![Repository](./images/reprepo.png)


===

Make a donation!
If you liked this article you can donate with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)