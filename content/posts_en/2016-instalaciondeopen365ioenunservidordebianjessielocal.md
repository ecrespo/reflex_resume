Title: Installing open365.io on a local Debian Jessie server  
Date: 2016-09-16 09:00  
Category: Tutorial de Linux
Tags: Python,Linux,Open365, Debian,Ubuntu
lang: en  
translation: true  

Open365 is a SaaS that lets you work collaboratively and in the cloud with the Libre Office suite version 5.1. Open365 is in beta but is stable at this point.

On the [project's official page (broken link)](https://open365.io/) you can find more information, including a demo video:

[https://www.youtube.com/watch?v=S2DH8bpCf1shttps://www.youtube.com/watch?v=S2DH8bpCf1s (broken link)](https://www.youtube.com/watch?v=S2DH8bpCf1shttps://www.youtube.com/watch?v=S2DH8bpCf1s "https://www.youtube.com/watch?v=S2DH8bpCf1s")

The idea is to install it on a machine with Debian Jessie.

Requirements:
The following must be installed:

1. Docker ([Installing docker on Debian Jessie](/blog/instalardockerendebianjessie)).
2. Python3.
3. Docker-compose (install via pip3:  pip3 install docker-compose).


#### Installation procedure:
Via `apt-get` install the following: 
```
apt-get install libmysqlclient-dev python3-dev python3-pip
```
Via pip3 install pymongo, ldap3, requests and mysqlclient:
```
pip3 install mysqlclient  pymongo ldap3 requests
```

Download open365 from [github](https://github.com/Open365/Open365) via git: 
```
git clone  https://github.com/Open365/Open365.git
```
Enter the Open365 directory:
```
cd Open365
```
Start the installation: 
```
sudo ./open365 install
```
A series of questions follows:
```
Additionally this will consume over 15gb of space.
Are you sure you want to continue? [y/n] y
Enter your domain or IP: midominio.prueba
We detected you are using a newer version of Docker. Unfortunately, Open365 isn't yet fully
compatible with docker versions newer than 1.9. A workaround involves running the virtualized
applications in privileged mode. Do you want to launch the applications in privileged mode?
This is potentially unsafe, specially if you are going to give accounts to third parties.
You won't be able to save documents edited in virtual applications. [y/n] y
```
This last question appears because the Docker version is very new and open365 has not been tested on it. 

After answering the questions, the process of downloading the open365 docker images begins. 

To uninstall open365, run:
```
sudo ./open365 destroy
```

Open365 has clients for:
- Windows  
- Mac  
- Linux  
- Iphone  
- Android  

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)




