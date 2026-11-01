Title: RESTful API for Python with Eve (part 1).  
Date: 2015-04-07 9:00  
Category: Tutorial Python  
Tags: Canaima,Debian,Python,Ubuntu,Eve, API restfull 
lang: en  
translation: true  

`Eve` is a REST API framework designed "for humans"; the link to see the project is the [following](https://docs.python-eve.org/en/stable/).

It supports mongodb and SQL backends. You can review its features [here](https://docs.python-eve.org/en/stable/features.html).

This article is based on the [quickstart of the application](https://docs.python-eve.org/en/stable/quickstart.html).

To install Eve, use the `pip` or `easy_install` command:
```python
#pip install Eve
```
or
```python
#easy_install Eve
```
Then create a file named `run.py`. Its code is the following:
```python
#Se importa eve de Eve
from eve import Eve

#Se crea la instancia de Eve
app = Eve()

#Se ejecuta run.
if __name__ == '__main__':
        app.run()
```

Now create a `settings.py` file with the following contents:
```python
DOMAIN = {'persona': {}}
```
Both files must be saved in the same directory.

Now run `run.py`:
```python
ernesto@grievous:~/bin/apirest$ python run.py
 * Running on http://127.0.0.1:5000/
```
Now query the API with curl:
```
ernesto@grievous:~$ curl -i http://127.0.0.1:5000
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 64
Server: Eve/0.5.3 Werkzeug/0.9.6 Python/2.7.8
Date: Wed, 08 Apr 2015 00:09:14 GMT

{"_links": {"child": [{"href": "persona", "title": "persona"}]}}
```

Now query persona:
```
ernesto@grievous:~$ curl http://127.0.0.1:5000/persona
{"_items": [], "_links": {"self": {"href": "persona", "title": "persona"}, "parent": {"href": "/", "title": "home"}}, "_meta": {"max_results": 25, "total": 0, "page": 1}}
```
What the execution of `run.py` shows is the following:
```
ernesto@grievous:~/bin/apirest$ python run.py
 * Running on http://127.0.0.1:5000/
127.0.0.1 - - [07/Apr/2015 19:39:14] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [07/Apr/2015 19:41:35] "GET /persona HTTP/1.1" 200 -
```
The 2 requests are shown in the log.

The next article will explain the use of `Eve` with `mongodb`.

##  ##
Make a donation!
If you liked the article you can make a donation in Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
