Title: Mercurial API for Python
Date: 2012-01-24 09:00
Category: Tutorial de Python 
Tags: Canaima,Control de versiones,Debian,General,Linux,Mercurial,Python,Ubuntu
lang: en
translation: true

Mercurial, as already explained, is a distributed version control system developed in python. Other version control systems have APIs or modules for python, but for mercurial I had not seen an API to use it from python.

While going through the articles published in the python sparks on Google+, I found out that there is an API called [hgapi (broken link)](https://bitbucket.org/haard/hgapi).

The API supports the following:
```
hg init
hg id
hg add <file>
hg commit [files] [-u name] [--close-branch]
hg update <rev>
hg heads
hg log
hg remove
hg status
hg merge (fails on conflict)
hg revert
```

The installation procedure is the following:  
```python 
# pip install hgapi
Downloading/unpacking hgapi
Downloading hgapi-1.1.0.tar.gz
Running setup.py egg_info for package hgapi
	  
Installing collected packages: hgapi
Running setup.py install for hgapi
	  
Successfully installed hgapi
Cleaning up...
```
Create the pruebas directory:

```
$mkdir pruebas
```

Inside the pruebas directory, create the file `hora.txt`:  

```
cd pruebas
touch hora.txt
```

Everything is now ready to try the API.

###### 1.  Import the `hgapi` module:  
```python 
import hgapi
```  

###### 2. Outside the `pruebas` directory, create the repository instance:
```python 
repo = hgapi.Repo("pruebas")
```  

######3. Initialize the repository:
```python 
repo.hg_init()
```  

###### 4. Add the file hora.txt:
```python 
repo.hg_add("hora.txt")
```  

###### 5. Make the commit, giving the description and the user who makes the commit:
```python 
repo.hg_commit("Agregando archivo hora.txt",user="ernesto")
```  

###### 6. Get the description:
```python 
str(repo['tip'].desc)
'Agregando archivo hora.txt'
```

This is the basics covered on the hgapi site. The interesting part is that you can now automate mercurial processes from python.

You can check the hgapi documentation [here](https://pythonhosted.org/hgapi/).


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)