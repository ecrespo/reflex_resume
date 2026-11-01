Title: Downloading youtube videos from Python with Pafy.
Date: 2013-09-01 9:00
Category: General
Tags: General
lang: en
translation: true

`Pafy` lets you search for youtube videos and download them.

The `Pafy` site is on [github (broken link)](http://np1.github.io/pafy/); there you can download the library in zip or tar.gz format, or visit the project's git repository.

To install `Pafy` on Linux you can use `easy_install` or `pip`:
```
pip install Pafy
```
Run python:
```python
ernesto@grievous:~$ python

Python 2.7.3 (default, Jan  2 2013, 13:56:14) 

[GCC 4.7.2] on linux2

Type "help", "copyright", "credits" or "license" for more information.

>>> 
```

Import Pafy:
```python
>>> from pafy import Pafy
```

Create the variable holding the video url:
```python
>>> url="http://www.youtube.com/watch?v=YOZjaqHioro"
```

Create the video instance:
```python
>>> video = Pafy(url)
```

Get the video title:
```python
>>> video.title

u'Jimmy Fallon, Robin Thicke & The Roots Sing "Blurred Lines" (w/ Classroom Instruments)'
```
The video rating and length:

```python
>>> video.rating


4.9188302785




>>> video.length


214

```

Show the video metadata:
```python
>>> print video


Title: Jimmy Fallon, Robin Thicke & The Roots Sing "Blurred Lines" (w/ Classroom Instruments)


Author: latenight


ID: YOZjaqHioro


Duration: 00:03:34


Rating: 4.9188302785


Views: 10459846


Thumbnail: https://i1.ytimg.com/vi/YOZjaqHioro/default.jpg


Keywords: Jimmy Fallon, Late Night With Jimmy Fallon, Late Night, NBC, NBC TV, Television, Funny, Talk Show, comedic, humor, stand-up, snl, Fallon Stand-up, Fallon monologue, latenight, jokes, funny video, interview, variety, comedy sketches, talent, celebrities, music, musical performance, The Roots, video, clip, highlight, talking, youtube, jimmy fallon & robin thicke, robin thicke, blurred lines, classroom instruments, late night music room
```

It shows the video title, the author, the video ID, the duration, the rating, the number of times it has been viewed, and other information.

Show all the video formats and their resolution:
```python
>>> streams = video.streams


>>> for s in streams: print s.resolution, s.extension


... 


1080x1920 webm


1080x1920 mp4


720x1280 webm


720x1280 mp4


480x854 webm


480x854 flv


360x640 webm


360x640 flv


360x640 mp4


240x400 flv


320x240 3gp


144x176 3gp

```

Show all the formats, their resolution and the url to download them:

```python
>>> for s in streams: print s.resolution, s.extension, s.url


... 


1080x1920 webm http://r14---sn-ab5e6nll.c.youtube.com...


1080x1920 mp4 http://r14---sn-ab5e6nll.c.youtube.com...


720x1280 webm http://r14---sn-ab5e6nll.c.youtube.com...


720x1280 mp4 http://r14---sn-ab5e6nll.c.youtube.com...


480x854 webm http://r14---sn-ab5e6nll.c.youtube.com...


480x854 flv http://r14---sn-ab5e6nll.c.youtube.com...


360x640 webm http://r14---sn-ab5e6nll.c.youtube.com...


360x640 flv http://r14---sn-ab5e6nll.c.youtube.com...


360x640 mp4 http://r14---sn-ab5e6nll.c.youtube.com...


240x400 flv http://r14---sn-ab5e6nll.c.youtube.com...


320x240 3gp http://r14---sn-ab5e6nll.c.youtube.com...


144x176 3gp http://r14---sn-ab5e6nll.c.youtube.com...

```

Get the best resolution and its extension:

```python
>>> best = video.getbest()


>>> best.resolution, best.extension


('1080x1920', 'webm')

```

Best resolution for a specific format:

```python

>>> best = video.getbest(preftype="mp4")


>>> best.resolution, best.extension


('1080x1920', 'mp4')


```

Get the url to download the video:

```python
>>> best.url


'http://r14---sn-ab5e6nll.c.youtube.com/videoplayback...'

```

Download the video with a name and into a predefined path:

```python
>>> myfilename = "/home/ernesto/videos/" + "JimmtFallon" + "." + best.extension


>>> best.download(progress=False, filepath=myfilename)


-Downloading 'Jimmy Fallon, Robin Thicke & The Roots Sing "Blurred Lines" (w/ Classroom Instruments).webm' [157,236,345 Bytes]



Done
```

Exit python:

```python
>>> exit()

```

Verify that the file was downloaded:

```
ernesto@grievous:~/videos$ ls -l


total 153556


-rw-r--r-- 1 ernesto ernesto 157236345 sep  1 11:03 JimmtFallon.webm

```

Now you can run your preferred video player to watch the video.  

The following figure shows a screenshot of the desktop while playing the video with VLC:

![](./images/bajarvideosdeyoutubedesdepythonconpafy-1.png) 


If you want to watch the video, here is the youtube link:

[https://youtu.be/YOZjaqHioro](https://youtu.be/YOZjaqHioro) 

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)