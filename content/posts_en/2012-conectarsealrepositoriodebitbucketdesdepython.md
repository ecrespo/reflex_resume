Title: Connecting to a bitbucket repository from python
Date: 2012-02-19 09:00
Category: Tutorial de Python
Tags: Canaima,Control de versiones,Debian,General,Linux,Mercurial,Python,Ubuntu
lang: en
translation: true


To have a project under mercurial version control I only see 2 options: [Google Code ](https://code.google.com/) or [Bitbucket](https://bitbucket.org/product/).  For Google Code you can use the API to work with mercurial from python, as explained in a [previous](/blog/apidemercurialparapython) article.

For Bitbucket there is an API to access the repository information, which in python is called [python-bitbucket. (broken link)](https://bitbucket.org/jmoiron/python-bitbucket/).  

To install it, follow these steps:  

The Debian/Canaima/Ubuntu/LinuxMint way:  

```
#apt-get install python-bitbucket
```

With the `easy_install` tool:  

```
#easy_install bitbucket
```

With the `pip` tool:  

```
#pip install bitbucket
```

Using the bitbucket API:  

From the python console, import the `bitbucket` module  

```python 
$python
	
>>> import bitbucket
```
	
Create the bitbucket instance.
	
```python 
>>> bb = bitbucket.BitBucket()
```
	
Connect to the `bitbucket` account:  

```python 
>>> bb = bitbucket.BitBucket('ecrespo', 'clave')
```

Verify that you authenticated with the service:  
```python 
>>> bb
<BitBucket API (auth: ecrespo)>
```

Associate the account:  
```python 
>>> ecrespo = bb.user('ecrespo')
>>> ecrespo
<User: ecrespo>
```

List the user's repositories (a list with the user's repositories is returned; each element of the list is a dictionary with the repository information):  
```python 
>>> ecrespo.repositories()
[{u'scm': u'hg', u'has_wiki': True, u'last_updated': u'2011-09-12 	03:56:37', u'created_on': u'2009-04-09 22:42:58', u'owner': u'ecrespo', 	u'logo': None, u'email_mailinglist': u'', u'is_mq': False, u'size': 747499, u'read_only': False, u'fork_of': None, u'mq_of': None, u'state': u'available', u'utc_created_on': u'2009-04-09 20:42:58+00:00', u'website': u'', u'description': u'Script que automatiza el proceso de conversi\xf3n de un sistema Debian/Ubuntu para que sea accesible para las personas con discapacidad visual', u'has_issues': True, u'is_fork': False, u'slug': u'automatizar-accesibilidad', u'is_private': False, u'name': u'automatizar-accesibilidad', u'language': u'', u'utc_last_updated': u'2011-09-12 01:56:37+00:00', u'email_writers': True, u'main_branch': u'default', u'no_public_forks': False, u'resource_uri': u'/api/1.0/repositories/ecrespo/automatizar-accesibilidad'}, {u'scm': u'hg', u'has_wiki': True, u'last_updated': u'2011-09-08 13:09:06', u'created_on': u'2011-08-04 05:02:06', u'owner': u'ecrespo', u'logo': None, u'email_mailinglist': u'', u'is_mq': False, u'size': 545, u'read_only': False, u'fork_of': None, u'mq_of': None, u'state': u'available', u'utc_created_on': u'2011-08-04 03:02:06+00:00', u'website': u'', u'description': u'Lista de paquetes para la accesibilidad con una descripci\xf3n y pruebas de los mismos', u'has_issues': False, u'is_fork': False, u'slug': u'accesibilidad', u'is_private': True, u'name': u'accesibilidad', u'language': u'', u'utc_last_updated': u'2011-09-08 11:09:06+00:00', u'email_writers': True, u'main_branch': None, u'no_public_forks': False, u'resource_uri': u'/api/1.0/repositories/ecrespo/accesibilidad'}]
```

Get the repository description and its path:  
```python 
>>> ecrespo.repositories()[0]['description']
u'Script que automatiza el proceso de conversi\xf3n de un sistema Debian/Ubuntu para que sea accesible para las personas con discapacidad visual'

>>> ecrespo.repositories()[0]['resource_uri']
u'/api/1.0/repositories/ecrespo/automatizar-accesibilidad'
```
Associate one of the repositories, in this case accesibilidad.  
```python 
>>> pyaccesibilidad=ecrespo.repository('accesibilidad')

>>> pyaccesibilidad
<Repository: ecrespo's accesibilidad>
```
List the tags or branches (for the accesibilidad repository it returns empty dictionaries):  
```python 
>>> pyaccesibilidad.tags()
{}

>>> pyaccesibilidad.branches()
{}
```

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
