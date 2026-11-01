Title: An introduction to Beautiful Soup 4 in Python.
Date: 2013-10-23 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,Beautiful Soup,webscraping
lang: en
translation: true

`Beautiful Soup` is a Python library that makes it easy to extract data from html and xml files.

This article is based on the article from [Python For Beginners](https://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/) .

The official documentation can be read at the following [link](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).

To install `beautifulsoup` you need to have the `python-bs4` library installed, which is an html parser.
```
#apt-get install python-bs4
```
Then `beautiful soup 4` is installed:
```
#pip install beautifulsoup4
```
To use `beautifulsoup` you can pass it an html file or a URL, but to fetch the html file you have to use `urllib2`; `beautifulsoup` does not do it on its own.

The API has several ways of filtering a search:
1. Search by string, using the `find_all` function:
```python
soup.find_all("Prueba)
```

This searches for every occurrence of the word Prueba in the file.
2. Regular expression:
The following code shows all the html tags that start with the letter b.
```python
import re

for tag in soup.find_all(re.compile("^b")):

    print(tag.name)
```
The following code shows all the html tags that contain the letter b:
```python
import re

for tag in soup.find_all(re.compile("b")):

    print(tag.name)
```

3. A list.
When a list is passed, `beautifulsoup` will find any element of the list.
The following code shows how to find every a and every b that appears:
```python
print soup.find_all(["a","b"])
```
To demonstrate the use of `beautifulsoup` I will use a django application that keeps a registry of internet radios for the Linux radiotray application.

Here is a screenshot:

![](./images/unaintroduccionabeautifulsoup4enpython-1.png) 

The example code is the following:

```python
#!/usr/bin/env python


from bs4 import BeautifulSoup


import urllib2




#Se crea la instancia de BS pasando la URL con urllib2.


soup = BeautifulSoup(urllib2.urlopen("http://127.0.0.1:8000").read())


print "--------------------"


#Se muestra todo el contenido de la pagina


print soup.prettify()


print "---------------------"


#Se muestra el titulo de la pagina


print "Titulo" ,soup.title.string


print "----------------------"


#Se muestra el tag p de html que contiene la pagina


print soup.p


print "----------------------"


#Se muestra el tag a de html que contiene la pagina

print soup.a
```

Below is an image with the result of the program:

![](./images/unaintroduccionabeautifulsoup4enpython-2.png) 

To extract URLs from the page, search for the html tag a, then whatever contains the word href:
```python
#!/usr/bin/env python


from bs4 import BeautifulSoup


import urllib2


#Se crea la instancia de BS pasando la URL con urllib2.


soup = BeautifulSoup(urllib2.urlopen("http://127.0.0.1:8000").read())


print "--------------------"


#Para extraer url de la pagina.


for link in soup.find_all('a'):

    print(link.get('href'))
```
The result is shown below:
```python
--------------------
/
/radios/pagina/1/
/acerca/
/login/
```

To extract all the text from the page:

```python
#!/usr/bin/env python

from bs4 import BeautifulSoup

import urllib2

#Se crea la instancia de BS pasando la URL con urllib2.

soup = BeautifulSoup(urllib2.urlopen("http://127.0.0.1:8000").read())

print "--------------------"

#Para extraer todo el texto de la pagina.

print(soup.get_text())
```
The result is shown below:
```python
....
 Bienvenido 
/span
Radio
              	L
/.well 
Nuevas radios
/.well 
/span
/row
© Registro Radiotray 2013  
/.fluid-container
 Le javascript
    ================================================== 
 Placed at the end of the document so the pages load faster
```

This is the basis for doing [webscraping](https://es.wikipedia.org/wiki/Web_scraping), which will be explained in the next article.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)