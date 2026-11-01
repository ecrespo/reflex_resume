Title: Getting EXIF metadata from an image with Python
Date: 2013-10-14 9:00
Category: Tutorial Python
Tags: Canaima,Debian,General,Linux,Python,Ubuntu,exif
lang: en
translation: true

With a simple script we will test how to get EXIF metadata from two images. They are two photos: the first directly from the mobile device that took the photo, and the second image was downloaded from Google+.

The idea is to notice the difference in the information obtained from the metadata of two identical photos obtained in two different ways.

The first thing to do is install the Python module called `pyexiv2`. You can find its documentation [here](https://tilloy.net/dev/pyexiv2/index.html).
It can be installed on Debian wheezy as follows:
```
#apt-get install python-pyexiv2 python-pyexiv2-doc
```
The original image was taken with a Motorola Razr XT910 phone and the second image was downloaded from Google+.
Original image with md5:
md5sum ecrespo-orig.jpg
a74977dbbd40d228658435b03db9a4c3  ecrespo-orig.jpg

The image size is 248k:
du  ecrespo-orig.jpg
248	ecrespo-orig.jpg

![](./images/obtenerinformaciondemetadatosexifdeunaimagenconpython-1.jpg) 
ecrespo-orig.jpg

Image downloaded from Google+ with md5:
md5sum ecrespo.jpg
d1d41f5865bbb8360e6a748e38ae5ee1  ecrespo.jpg
The image size is 32k:
du ecrespo.jpg
32	ecrespo.jpg

![](./images/obtenerinformaciondemetadatosexifdeunaimagenconpython-2.jpg) 

ecrespo.jpg

The code that shows the exif metadata of each image is the following:
```python
#!/usr/bin/env python

#Se importa el modulo para analisis de metadatos de exif

import pyexiv2

#Se crea una funcion que devuelve en pantalla la informacion exif

def Meta(archivo):

    #Se crea la instancia metadata al pasarle el archivo que se quiere analizar

    metadata = pyexiv2.ImageMetadata(archivo)

    #Se lee el metadato

    metadata.read()

    #Se muestra en pantalla un mensaje

    print "Se muestra la informacion exif del archivo %s" %archivo

    print  "---------------------------------------------"

    #Se despliega la informacion de metadatos exif que contiene la imagen

    for metadato in metadata.exif_keys:

        texto = metadato + ": " + metadata[metadato].raw_value

        print texto


if __name__ == "__main__":

    Meta("ecrespo-orig.jpg")

    print "********************************************"

    Meta("ecrespo.jpg")
```
The output of the script is the following:
```python
Se muestra la informacion exif del archivo ecrespo-orig.jpg

---------------------------------------------

Exif.Image.YCbCrPositioning: 1

Exif.Image.XResolution: 72/1

Exif.Image.YResolution: 72/1

Exif.Image.ResolutionUnit: 2

Exif.Image.DateTime: 2013:09:08 13:10:00

Exif.Image.Make: Motorola

Exif.Image.Model: XT910

Exif.Image.ExifTag: 449

Exif.Photo.ExifVersion: 48 50 50 48

Exif.Photo.FlashpixVersion: 48 48 48 48

Exif.Photo.ColorSpace: 1

Exif.Photo.ComponentsConfiguration: 1 2 3 0

Exif.Photo.CompressedBitsPerPixel: 0/1

Exif.Photo.ExposureTime: 0/1000000

Exif.Photo.FNumber: 24/10

Exif.Photo.ExposureProgram: 0

Exif.Photo.ISOSpeedRatings: 0

Exif.Photo.ShutterSpeedValue: 0/1

Exif.Photo.ApertureValue: 3/1

Exif.Photo.BrightnessValue: 0/1

Exif.Photo.ExposureBiasValue: 0/10

Exif.Photo.MaxApertureValue: 3/1

Exif.Photo.SubjectDistance: 0/1

Exif.Photo.MeteringMode: 1

Exif.Photo.LightSource: 3

Exif.Photo.Flash: 24

Exif.Photo.FocalLength: 460/100

Exif.Photo.FlashEnergy: 0/1

Exif.Photo.ExposureIndex: 0/0

Exif.Photo.SceneType: 1

Exif.Photo.CustomRendered: 1

Exif.Photo.ExposureMode: 0

Exif.Photo.WhiteBalance: 0

Exif.Photo.DigitalZoomRatio: 65536/65535

Exif.Photo.SceneCaptureType: 0

Exif.Photo.GainControl: 0

Exif.Photo.Contrast: 0

Exif.Photo.Saturation: 0

Exif.Photo.Sharpness: 0

Exif.Photo.SubjectDistanceRange: 0

Exif.Image.GPSTag: 1243

Exif.Thumbnail.ImageWidth: 200

Exif.Thumbnail.ImageLength: 120

Exif.Thumbnail.Compression: 6

Exif.Thumbnail.XResolution: 72/1

Exif.Thumbnail.YResolution: 72/1

Exif.Thumbnail.ResolutionUnit: 2

Exif.Thumbnail.JPEGInterchangeFormat: 2027

Exif.Thumbnail.JPEGInterchangeFormatLength: 8033

********************************************

Se muestra la informacion exif del archivo ecrespo.jpg

---------------------------------------------

Exif.Image.Software: Google

Exif.Image.ExifTag: 46

Exif.Photo.ExifVersion: 48 50 50 48

Exif.Photo.0x9009: 10 39 8 1 16 1 24 0 32 0 40 0 48 0 56 0 64 0 72 1 80 0 88 0 96 1 104 1 112 0 120 1 128 1 1 136 1 1 144 1 1

```

As you can see, the original image downloaded from the Android device has more exif metadata than the image downloaded from Google+. The first photo has information about the device, model and other things, while the second photo only carries information about the software that processed the image, which is Google.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)