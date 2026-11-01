Title: How to use the Wikipedia API with Python
Date:  2019-06-08 11:33
Category: Tutorial de Python
Tags: Debian,Python,Wikipedia,Ubuntu
lang: en
translation: true
Slug: python-wikipedia-2019
Authors: Ernesto Crespo
Summary: Using the Wikipedia API with Python



Resuming article writing, now using pelican and github pages.

Today we will cover how to access Wikipedia through its API from Python.

This article is based on the Stack Abuse article [Getting Started with Python's Wikipedia API](https://stackabuse.com/getting-started-with-pythons-wikipedia-api/).

### Installing and testing the Wikipedia API


The first thing to do is install the wikipedia library for Python:

```
pip install wikipedia
```

To test that the API works, import wikipedia from the python console:

```python
import wikipedia
```

### Querying the API

By default the Wikipedia API runs searches in English.

To start, you can search for a word, for example Venezuela:

```python
print(wikipedia.search("Venezuela"))
['Venezuela', 'Venezuelans', 'Economy of Venezuela', 'Caracas', 'Venezuela national football team', 'President of Venezuela', 'Crisis in Venezuela', 'Mestizos in Venezuela', 'List of Presidents of Venezuela', 'Crime in Venezuela']

```
It returns a list of words or phrases about Venezuela.

You can limit the search result to, for example, 3:

```python
print(wikipedia.search("Venezuela", results=3))
['Venezuela', 'Venezuelans', 'Economy of Venezuela']
```


Now we can search for Linux:
```python
print(wikipedia.search("Linux"))
['Linux', 'Linux kernel', 'Linux distribution', 'List of Linux distributions', 'Kali Linux', 'Astra Linux', 'Linux Mint', 'Red Hat Enterprise Linux', 'Ubuntu', 'Arch Linux']
```

There is a suggest method that helps with the search if we misspell the search term; for example, you can search for "Simon Boliva" and the method will return the correct name "Simón Bolivar":

```python
>>> print(wikipedia.suggest("Simon Boliva"))
simon bolivar
```

### Extracting a summary of a wikipedia article

To extract a summary of an article, the summary method is used:

```python
print(wikipedia.summary("Debian"))  
Debian () is a Unix-like operating system consisting entirely of free software. Ian Murdock founded the Debian Project on August 16, 1993. Debian 0.01 was released on September 15, 1993, and the first stable version, 1.1, was released on June 17, 1996. The Debian Stable branch is the most popular edition for personal computers and network servers, and is used as the basis for many other Linux distributions.
Debian is one of the earliest operating systems based on the Linux kernel. The project is coordinated over the Internet by a team of volunteers guided by the Debian Project Leader and three foundational documents: the Debian Social Contract, the Debian Constitution, and the Debian Free Software Guidelines. New distributions are updated continually, and the next candidate is released after a time-based freeze.
Debian has been developed openly and distributed freely according to the principles of the GNU Project. Because of this, the Free Software Foundation sponsored the project from November 1994 to November 1995. The popular Linux operating system Ubuntu was also released based on Debian. When the sponsorship ended, the Debian Project formed the nonprofit Software in the Public Interest to continue financially supporting development.
```

You can limit the amount of text shown with the sentences option, which here we will set to 3:

```python
print(wikipedia.summary("Debian", sentences=3))  
Debian () is a Unix-like operating system consisting entirely of free software. Ian Murdock founded the Debian Project on August 16, 1993. Debian 0.01 was released on September 15, 1993, and the first stable version, 1.1, was released on June 17, 1996.
```

Note that the article content is in English; if you want to get the information in another language, change the API configuration as follows:

```python
wikipedia.set_lang("es")  
```

Now run the previous query again:

```python
print(wikipedia.summary("Debian", sentences=3))
Debian o Proyecto Debian,[1]​ (en inglés, Debian Project) [2]​ es una comunidad conformada por desarrolladores y usuarios, que mantiene un sistema operativo GNU basado en software libre. El sistema se encuentra precompilado, empaquetado y en formato deb para múltiples arquitecturas de computador y para varios núcleos.
El proyecto Debian fue anunciado inicialmente 1993 por Ian Murdock.
```

To list the supported languages, run the languages() method; it returns a dictionary with all the languages supported by the API:

```python
print(wikipedia.languages())
{'aa': 'Qafár af', 'ab': 'Аҧсшәа', 'abs': 'bahasa ambon', 'ace': 'Acèh', 'ady': 'адыгабзэ', 'ady-cyrl': 'адыгабзэ', 'aeb': 'تونسي/Tûnsî', 'aeb-arab': 'تونسي', 'aeb-latn': 'Tûnsî', 'af': 'Afrikaans', 'ak': 'Akan', 'aln': 'Gegë', 'als': 'Alemannisch', 'am': 'አማርኛ', 'an': 'aragonés', 'ang': 'Ænglisc', 'anp': 'अङ्गिका', 'ar': 'العربية', 'arc': 'ܐܪܡܝܐ', 'arn': 'mapudungun', 'arq': 'جازايرية', 'ary': 'Maġribi', 'arz': 'مصرى', 'as': 'অসমীয়া', 'ase': 'American sign language', 'ast': 'asturianu', 'atj': 'Atikamekw', 'av': 'авар', 'avk': 'Kotava', 'awa': 'अवधी', 'ay': 'Aymar aru', 'az': 'azərbaycanca', 'azb': 'تۆرکجه', 'ba': 'башҡортса', 'ban': 'Basa Bali', 'bar': 'Boarisch', 'bat-smg': 'žemaitėška', 'bbc': 'Batak Toba', 'bbc-latn': 'Batak Toba', 'bcc': 'جهلسری بلوچی', 'bcl': 'Bikol Central', 'be': 'беларуская', 'be-tarask': 'беларуская (тарашкевіца)\u200e', 'be-x-old': 'беларуская (тарашкевіца)\u200e', 'bg': 'български', 'bgn': 'روچ کپتین بلوچی', 'bh': 'भोजपुरी', 'bho': 'भोजपुरी', 'bi': 'Bislama', 'bjn': 'Bahasa Banjar', 'bm': 'bamanankan', 'bn': 'বাংলা', 'bo': 'བོད་ཡིག', 'bpy': 'বিষ্ণুপ্রিয়া মণিপুরী', 'bqi': 'بختیاری', 'br': 'brezhoneg', 'brh': 'Bráhuí', 'bs': 'bosanski', 'btm': 'Batak Mandailing', 'bto': 'Iriga Bicolano', 'bug': 'ᨅᨔ ᨕᨘᨁᨗ', 'bxr': 'буряад', 'ca': 'català', 'cbk-zam': 'Chavacano de Zamboanga', 'cdo': 'Mìng-dĕ̤ng-ngṳ̄', 'ce': 'нохчийн', 'ceb': 'Cebuano', 'ch': 'Chamoru', 'cho': 'Choctaw', 'chr': 'ᏣᎳᎩ', 'chy': 'Tsetsêhestâhese', 'ckb': 'کوردی', 'co': 'corsu', 'cps': 'Capiceño', 'cr': 'Nēhiyawēwin / ᓀᐦᐃᔭᐍᐏᐣ', 'crh': 'qırımtatarca', 'crh-cyrl': 'къырымтатарджа (Кирилл)\u200e', 'crh-latn': 'qırımtatarca (Latin)\u200e', 'cs': 'čeština', 'csb': 'kaszëbsczi', 'cu': 'словѣньскъ / ⰔⰎⰑⰂⰡⰐⰠⰔⰍⰟ', 'cv': 'Чӑвашла', 'cy': 'Cymraeg', 'da': 'dansk', 'de': 'Deutsch', 'de-at': 'Österreichisches Deutsch', 'de-ch': 'Schweizer Hochdeutsch', 'de-formal': 'Deutsch (Sie-Form)\u200e', 'din': 'Thuɔŋjäŋ', 'diq': 'Zazaki', 'dsb': 'dolnoserbski', 'dtp': 'Dusun Bundu-liwan', 'dty': 'डोटेली', 'dv': 'ދިވެހިބަސް', 'dz': 'ཇོང་ཁ', 'ee': 'eʋegbe', 'egl': 'Emiliàn', 'el': 'Ελληνικά', 'eml': 'emiliàn e rumagnòl', 'en': 'English', 'en-ca': 'Canadian English', 'en-gb': 'British English', 'eo': 'Esperanto', 'es': 'español', 'es-419': 'español de América Latina', 'es-formal': 'español (formal)\u200e', 'et': 'eesti', 'eu': 'euskara', 'ext': 'estremeñu', 'fa': 'فارسی', 'ff': 'Fulfulde', 'fi': 'suomi', 'fit': 'meänkieli', 'fiu-vro': 'Võro', 'fj': 'Na Vosa Vakaviti', 'fo': 'føroyskt', 'fr': 'français', 'frc': 'français cadien', 'frp': 'arpetan', 'frr': 'Nordfriisk', 'fur': 'furlan', 'fy': 'Frysk', 'ga': 'Gaeilge', 'gag': 'Gagauz', 'gan': '贛語', 'gan-hans': '赣语（简体）\u200e', 'gan-hant': '贛語（繁體）\u200e', 'gcr': 'kriyòl gwiyannen', 'gd': 'Gàidhlig', 'gl': 'galego', 'glk': 'گیلکی', 'gn': "Avañe'ẽ", 'gom': 'गोंयची कोंकणी / Gõychi Konknni', 'gom-deva': 'गोंयची कोंकणी', 'gom-latn': 'Gõychi Konknni', 'gor': 'Bahasa Hulontalo', 'got': '𐌲𐌿𐍄𐌹𐍃𐌺', 'grc': 'Ἀρχαία ἑλληνικὴ', 'gsw': 'Alemannisch', 'gu': 'ગુજરાતી', 'gv': 'Gaelg', 'ha': 'Hausa', 'hak': '客家語/Hak-kâ-ngî', 'haw': 'Hawaiʻi', 'he': 'עברית', 'hi': 'हिन्दी', 'hif': 'Fiji Hindi', 'hif-latn': 'Fiji Hindi', 'hil': 'Ilonggo', 'ho': 'Hiri Motu', 'hr': 'hrvatski', 'hrx': 'Hunsrik', 'hsb': 'hornjoserbsce', 'ht': 'Kreyòl ayisyen', 'hu': 'magyar', 'hu-formal': 'magyar (formal)\u200e', 'hy': 'հայերեն', 'hyw': 'Արեւմտահայերէն', 'hz': 'Otsiherero', 'ia': 'interlingua', 'id': 'Bahasa Indonesia', 'ie': 'Interlingue', 'ig': 'Igbo', 'ii': 'ꆇꉙ', 'ik': 'Iñupiak', 'ike-cans': 'ᐃᓄᒃᑎᑐᑦ', 'ike-latn': 'inuktitut', 'ilo': 'Ilokano', 'inh': 'ГӀалгӀай', 'io': 'Ido', 'is': 'íslenska', 'it': 'italiano', 'iu': 'ᐃᓄᒃᑎᑐᑦ/inuktitut', 'ja': '日本語', 'jam': 'Patois', 'jbo': 'la .lojban.', 'jut': 'jysk', 'jv': 'Jawa', 'ka': 'ქართული', 'kaa': 'Qaraqalpaqsha', 'kab': 'Taqbaylit', 'kbd': 'Адыгэбзэ', 'kbd-cyrl': 'Адыгэбзэ', 'kbp': 'Kabɩyɛ', 'kg': 'Kongo', 'khw': 'کھوار', 'ki': 'Gĩkũyũ', 'kiu': 'Kırmancki', 'kj': 'Kwanyama', 'kjp': 'ဖၠုံလိက်', 'kk': 'қазақша', 'kk-arab': 'قازاقشا (تٴوتە)\u200f', 'kk-cn': 'قازاقشا (جۇنگو)\u200f', 'kk-cyrl': 'қазақша (кирил)\u200e', 'kk-kz': 'қазақша (Қазақстан)\u200e', 'kk-latn': 'qazaqşa (latın)\u200e', 'kk-tr': 'qazaqşa (Türkïya)\u200e', 'kl': 'kalaallisut', 'km': 'ភាសាខ្មែរ', 'kn': 'ಕನ್ನಡ', 'ko': '한국어', 'ko-kp': '조선말', 'koi': 'Перем Коми', 'kr': 'Kanuri', 'krc': 'къарачай-малкъар', 'kri': 'Krio', 'krj': 'Kinaray-a', 'krl': 'karjal', 'ks': 'कॉशुर / کٲشُر', 'ks-arab': 'کٲشُر', 'ks-deva': 'कॉशुर', 'ksh': 'Ripoarisch', 'ku': 'kurdî', 'ku-arab': 'كوردي (عەرەبی)\u200f', 'ku-latn': 'kurdî (latînî)\u200e', 'kum': 'къумукъ', 'kv': 'коми', 'kw': 'kernowek', 'ky': 'Кыргызча', 'la': 'Latina', 'lad': 'Ladino', 'lb': 'Lëtzebuergesch', 'lbe': 'лакку', 'lez': 'лезги', 'lfn': 'Lingua Franca Nova', 'lg': 'Luganda', 'li': 'Limburgs', 'lij': 'Ligure', 'liv': 'Līvõ kēļ', 'lki': 'لەکی', 'lmo': 'lumbaart', 'ln': 'lingála', 'lo': 'ລາວ', 'loz': 'Silozi', 'lrc': 'لۊری شومالی', 'lt': 'lietuvių', 'ltg': 'latgaļu', 'lus': 'Mizo ţawng', 'luz': 'لئری دوٙمینی', 'lv': 'latviešu', 'lzh': '文言', 'lzz': 'Lazuri', 'mai': 'मैथिली', 'map-bms': 'Basa Banyumasan', 'mdf': 'мокшень', 'mg': 'Malagasy', 'mh': 'Ebon', 'mhr': 'олык марий', 'mi': 'Māori', 'min': 'Baso Minangkabau', 'mk': 'македонски', 'ml': 'മലയാളം', 'mn': 'монгол', 'mni': 'মেইতেই লোন্', 'mnw': 'ဘာသာ မန်', 'mo': 'молдовеняскэ', 'mr': 'मराठी', 'mrj': 'кырык мары', 'ms': 'Bahasa Melayu', 'mt': 'Malti', 'mus': 'Mvskoke', 'mwl': 'Mirandés', 'my': 'မြန်မာဘာသာ', 'myv': 'эрзянь', 'mzn': 'مازِرونی', 'na': 'Dorerin Naoero', 'nah': 'Nāhuatl', 'nan': 'Bân-lâm-gú', 'nap': 'Napulitano', 'nb': 'norsk bokmål', 'nds': 'Plattdüütsch', 'nds-nl': 'Nedersaksies', 'ne': 'नेपाली', 'new': 'नेपाल भाषा', 'ng': 'Oshiwambo', 'niu': 'Niuē', 'nl': 'Nederlands', 'nl-informal': 'Nederlands (informeel)\u200e', 'nn': 'norsk nynorsk', 'no': 'norsk', 'nov': 'Novial', 'nqo': 'ߒߞߏ', 'nrm': 'Nouormand', 'nso': 'Sesotho sa Leboa', 'nv': 'Diné bizaad', 'ny': 'Chi-Chewa', 'nys': 'Nyunga', 'oc': 'occitan', 'olo': 'Livvinkarjala', 'om': 'Oromoo', 'or': 'ଓଡ଼ିଆ', 'os': 'Ирон', 'pa': 'ਪੰਜਾਬੀ', 'pag': 'Pangasinan', 'pam': 'Kapampangan', 'pap': 'Papiamentu', 'pcd': 'Picard', 'pdc': 'Deitsch', 'pdt': 'Plautdietsch', 'pfl': 'Pälzisch', 'pi': 'पालि', 'pih': 'Norfuk / Pitkern', 'pl': 'polski', 'pms': 'Piemontèis', 'pnb': 'پنجابی', 'pnt': 'Ποντιακά', 'prg': 'Prūsiskan', 'ps': 'پښتو', 'pt': 'português', 'pt-br': 'português do Brasil', 'qu': 'Runa Simi', 'qug': 'Runa shimi', 'rgn': 'Rumagnôl', 'rif': 'Tarifit', 'rm': 'rumantsch', 'rmy': 'romani čhib', 'rn': 'Kirundi', 'ro': 'română', 'roa-rup': 'armãneashti', 'roa-tara': 'tarandíne', 'ru': 'русский', 'rue': 'русиньскый', 'rup': 'armãneashti', 'ruq': 'Vlăheşte', 'ruq-cyrl': 'Влахесте', 'ruq-latn': 'Vlăheşte', 'rw': 'Kinyarwanda', 'sa': 'संस्कृतम्', 'sah': 'саха тыла', 'sat': 'ᱥᱟᱱᱛᱟᱲᱤ', 'sc': 'sardu', 'scn': 'sicilianu', 'sco': 'Scots', 'sd': 'سنڌي', 'sdc': 'Sassaresu', 'sdh': 'کوردی خوارگ', 'se': 'davvisámegiella', 'sei': 'Cmique Itom', 'ses': 'Koyraboro Senni', 'sg': 'Sängö', 'sgs': 'žemaitėška', 'sh': 'srpskohrvatski / српскохрватски', 'shi': 'Tašlḥiyt/ⵜⴰⵛⵍⵃⵉⵜ', 'shi-latn': 'Tašlḥiyt', 'shi-tfng': 'ⵜⴰⵛⵍⵃⵉⵜ', 'shn': 'ၽႃႇသႃႇတႆး ', 'shy-latn': 'tachawit', 'si': 'සිංහල', 'simple': 'Simple English', 'sk': 'slovenčina', 'skr': 'سرائیکی', 'skr-arab': 'سرائیکی', 'sl': 'slovenščina', 'sli': 'Schläsch', 'sm': 'Gagana Samoa', 'sma': 'Åarjelsaemien', 'sn': 'chiShona', 'so': 'Soomaaliga', 'sq': 'shqip', 'sr': 'српски / srpski', 'sr-ec': 'српски (ћирилица)\u200e', 'sr-el': 'srpski (latinica)\u200e', 'srn': 'Sranantongo', 'ss': 'SiSwati', 'st': 'Sesotho', 'stq': 'Seeltersk', 'sty': 'cебертатар', 'su': 'Basa Sunda', 'sv': 'svenska', 'sw': 'Kiswahili', 'szl': 'ślůnski', 'ta': 'தமிழ்', 'tay': 'Tayal', 'tcy': 'ತುಳು', 'te': 'తెలుగు', 'tet': 'tetun', 'tg': 'тоҷикӣ', 'tg-cyrl': 'тоҷикӣ', 'tg-latn': 'tojikī', 'th': 'ไทย', 'ti': 'ትግርኛ', 'tk': 'Türkmençe', 'tl': 'Tagalog', 'tly': 'толышә зывон', 'tn': 'Setswana', 'to': 'lea faka-Tonga', 'tpi': 'Tok Pisin', 'tr': 'Türkçe', 'tru': 'Ṫuroyo', 'ts': 'Xitsonga', 'tt': 'татарча/tatarça', 'tt-cyrl': 'татарча', 'tt-latn': 'tatarça', 'tum': 'chiTumbuka', 'tw': 'Twi', 'ty': 'reo tahiti', 'tyv': 'тыва дыл', 'tzm': 'ⵜⴰⵎⴰⵣⵉⵖⵜ', 'udm': 'удмурт', 'ug': 'ئۇيغۇرچە / Uyghurche', 'ug-arab': 'ئۇيغۇرچە', 'ug-latn': 'Uyghurche', 'uk': 'українська', 'ur': 'اردو', 'uz': 'oʻzbekcha/ўзбекча', 'uz-cyrl': 'ўзбекча', 'uz-latn': 'oʻzbekcha', 've': 'Tshivenda', 'vec': 'vèneto', 'vep': 'vepsän kel’', 'vi': 'Tiếng Việt', 'vls': 'West-Vlams', 'vmf': 'Mainfränkisch', 'vo': 'Volapük', 'vot': 'Vaďďa', 'vro': 'Võro', 'wa': 'walon', 'war': 'Winaray', 'wo': 'Wolof', 'wuu': '吴语', 'xal': 'хальмг', 'xh': 'isiXhosa', 'xmf': 'მარგალური', 'xsy': 'saisiyat', 'yi': 'ייִדיש', 'yo': 'Yorùbá', 'yue': '粵語', 'za': 'Vahcuengh', 'zea': 'Zeêuws', 'zgh': 'ⵜⴰⵎⴰⵣⵉⵖⵜ ⵜⴰⵏⴰⵡⴰⵢⵜ', 'zh': '中文', 'zh-classical': '文言', 'zh-cn': '中文（中国大陆）\u200e', 'zh-hans': '中文（简体）\u200e', 'zh-hant': '中文（繁體）\u200e', 'zh-hk': '中文（香港）\u200e', 'zh-min-nan': 'Bân-lâm-gú', 'zh-mo': '中文（澳門）\u200e', 'zh-my': '中文（马来西亚）\u200e', 'zh-sg': '中文（新加坡）\u200e', 'zh-tw': '中文（台灣）\u200e', 'zh-yue': '粵語', 'zu': 'isiZulu'}
```

You can also query a certain wikipedia page:

```python
wikipedia.page("Debian")  
<WikipediaPage 'Debian'>
```

And see its content (the end of the wikipedia content about Debian is shown):

```python

print(wikipedia.page("Debian").content)

== Distribuciones derivadas ==
En la actualidad, como Debian es una distro que ha demostrado su estabilidad y utilidad, muchos desarrolladores la han tomado para crear a partir de ella nuevas distribuciones. Se las conoce como distribuciones basadas en Debian.
En septiembre de 2010 existen 121 distribuciones activas basadas en Debian; según el buscador de DistroWatch, además Debian posee en su sitio web una lista oficial de sus distribuciones descendientes.[25]​


== Comunidades ==
Existen muchas y variadas comunidades relacionadas con el Proyecto Debian. Algunas de ellas:

Brasil,[26]​
Colombia,[27]​
Costa Rica,[28]​
Chile,[29]​
España,[30]​
México,[31]​
Nicaragua,[32]​
Venezuela[33]​


== Véase también ==
 Portal:Software libre. Contenido relacionado con Software libre.
Distribuciones basadas en Debian


=== Adaptaciones a otros núcleos ===
Debian GNU/Linux
Debian GNU/Hurd
Debian GNU/NetBSD
Debian GNU/kFreeBSD


=== Filosofía ===
Manifiesto Debian
Directrices de software libre de Debian
Contrato Social de Debian


=== Varios ===
Debconf


== Referencias ==


== Enlaces externos ==
 Wikimedia Commons alberga una galería multimedia sobre Debian.
 Wikinoticias tiene noticias relacionadas con Debian.
Sitio web oficial de Debian
```

You can also query the URL of the page about the topic being queried:

```python

print(wikipedia.page("Debian").url)  
https://es.wikipedia.org/wiki/Debian

```

Or query its references (the urls are returned in a list):

```python

print(wikipedia.page("Debian").references)
['http://www.debianchile.cl/', 'http://maslinux.es/debian-8-jessie-ha-alcanzado-el-fin-del-soporte-de-seguridad/', 'http://www.debian.mx/', 'http://www.debian.org.ni/', 'http://web.archive.org/web/20070408162722/http://www.us.debian.org/News/2005/20050606', 'http://web.archive.org/web/20071011203303/http://www.us.debian.org/News/2002/20020719', 'http://web.archive.org/web/20071013115846/http://www.us.debian.org/News/2000/20000815', 'http://web.archive.org/web/20080511183553/http://www.us.debian.org/News/2007/20070408', 'http://web.archive.org/web/20080706192105/http://www.us.debian.org/News/1999/19990309', 'http://web.archive.org/web/20080723214102/http://www.us.debian.org/News/1997/19970602', 'http://web.archive.org/web/20080724051253/http://www.us.debian.org/News/1998/19980724', 'http://lists.debian.org/debian-devel-announce/2008/09/msg00000.html', 'http://lists.debian.org/debian-devel-announce/2013/04/msg00006.html', 'http://www.us.debian.org/News/1997/19970602', 'http://www.us.debian.org/News/1998/19980724', 'http://www.us.debian.org/News/1999/19990309', 'http://www.us.debian.org/News/2000/20000815', 'http://www.us.debian.org/News/2002/20020719', 'http://www.us.debian.org/News/2005/20050606', 'http://www.us.debian.org/News/2007/20070408', 'http://www.debian.org/', 'http://www.debian.org/News/2009/20090214', 'http://www.debian.org/devel/join/newmaint', 'http://www.debian.org/doc/manuals/project-history/ch-intro.en.html', 'http://www.debian.org/donations.es.html#money_donations', 'http://www.debian.org/misc/children-distros.html', 'http://www.debianbrasil.org/', 'http://www.debianchile.org/', 'http://www.esdebian.org/', 'http://www.ibiblio.org/pub/historic-linux/distributions/debian-0.91/ChangeLog', 'https://web.archive.org/web/20070203111437/http://www.debiancolombia.org/', 'https://web.archive.org/web/20070307094321/http://www.debianbrasil.org/', 'https://web.archive.org/web/20070406065849/http://cr.debian.net/', 'https://web.archive.org/web/20070929040145/http://www.debian.org.ve/', 'https://web.archive.org/web/20110816182444/http://www.jus.uio.no/sisu/debian_constitution_v1.2/opendocument.es.odt', 'https://web.archive.org/web/20180621121330/http://maslinux.es/debian-8-jessie-ha-alcanzado-el-fin-del-soporte-de-seguridad/', 'https://web.archive.org/web/20181221235131/https://www.debian.org/intro/about.en.html', 'https://web.archive.org/web/20181221235714/https://www.debian.org/intro/about.es.html', 'https://lists.debian.org/debian-devel-announce/2012/07/msg00004.html', 'https://lists.debian.org/debian-devel-announce/2014/11/msg00003.html', 'https://lists.debian.org/debian-devel-announce/2015/03/msg00016.html', 'https://lists.debian.org/debian-security-announce/2014/msg00082.html', 'https://www.debian.org/', 'https://www.debian.org/News/2014/20140424', 'https://www.debian.org/News/2017/20170617', 'https://www.debian.org/doc/manuals/project-history/ch-releases.en.html', 'https://www.debian.org/intro/about.en.html', 'https://www.debian.org/intro/about.es.html']
```

You can query the title of the page:

```python
print(wikipedia.page("Debian").title)  
Debian
```

You can also query the categories in which the queried topic appears:

```python
print(wikipedia.page("Debian").categories)  
['Categoría:Debian', 'Categoría:Organizaciones de Linux', 'Categoría:Proyectos', 'Categoría:Sistemas operativos PowerPc', 'Categoría:Software de 1993', 'Categoría:Wikipedia:Artículos sin coordenadas', 'Categoría:Wikipedia:Páginas que utilizan Timeline']
```

You can query the links that the page has:

```python
print(wikipedia.page("Debian").links)
['17 de junio', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2005', '2006', '2007', '2008', '2009', '2010', '2013', '2015', '2016', '2017', '2019', 'Acrónimo', 'Advanced Packaging Tool', 'Alemania', 'Anthony Towns', 'Arquitectura de computador', 'Arquitectura de computadores', 'Asociación voluntaria', 'Australia', 'Austria', 'Bdale Garbee', 'Ben Collins', 'BitTorrent', 'Branden Robinson', 'Bruce Perens', 'Cargador de arranque', 'Chris Lamb', 'Comunidad', 'Contrato Social de Debian', 'Corel Linux', 'Código fuente', 'Deb', 'Debconf', 'Debian GNU/Hurd', 'Debian GNU/Linux', 'Debian GNU/NetBSD', 'Debian GNU/kFreeBSD', 'Desarrollador de software', 'Directrices de software libre de Debian', 'Distribución GNU/Linux', 'Distribución Linux', 'DistroWatch', 'Empresa', 'Error de software', 'Estados Unidos', 'Francia', 'FreeBSD', 'Free Software Foundation', 'Freenode', 'GNOME', 'GNU', 'GNU GRUB', 'GNU Hurd', 'Gestor de paquetes', 'Gnome', 'Hurd', 'IRC', 'Ian Jackson', 'Ian Murdock', 'Ibiblio', 'Idioma inglés', 'Inglaterra', 'Internet', 'Italia', 'Jigdo', 'KDE', 'Kfreebsd', 'LXDE', 'Licencia de software', 'Linux', 'Linux (núcleo)', 'Lista de correo', 'Lucas Nussbaum', 'Manifiesto Debian', 'Manifiesto de Debian', 'Martin Michlmayr', 'Mehdi Dogguy', 'Movimiento del software libre', 'Mozilla Firefox', 'Método Schulze', 'Neil McGovern', 'NetBSD', 'Núcleo (informática)', 'Open Source', 'Organización', 'Organización sin ánimo de lucro', 'Paquete de software', 'Paquetes de software', 'Países Bajos', 'Plataforma (informática)', 'SQL', 'Sam Hartman', 'Sam Hocevar', 'Servidor', 'Sistema operativo', 'Software', 'Software in the Public Interest', 'Software libre', 'Software no libre', 'Sources.list', 'Stefano Zacchiroli', 'Steve McIntyre', 'Stormix', 'Systemd', 'Tar', 'Toy Story', 'Túnez', 'USB en vivo', 'Universidad Purdue', 'Usuario', 'Usuario root', 'Wayback Machine', 'Wichert Akkerman', 'Wikimedia Commons', 'Wikinoticias', 'Xfce']
```


You can find out how many images the wikipedia page of the selected topic has:
```python
len(wikipedia.page("Debian").images)
15
```

And to see the URL of the first image:

```python
print(wikipedia.page("Debian").images[0])
https://upload.wikimedia.org/wikipedia/commons/4/4a/Commons-logo.svg
```

Finally, you can get the html of the page of the queried topic:

```python
print(wikipedia.page("Debian").html())
```

Output:
```html
<div class="mw-parser-output"><div class="rellink noprint"> Para el sistema operativo que usa el núcleo <a href="/wiki/Linux_(n%C3%BAcleo)" class="mw-redirect" title="Linux (núcleo)">Linux</a> y las herramientas <a href="/wiki/GNU" title="GNU">GNU</a>, véase <a href="/wiki/Debian_GNU/Linux" title="Debian GNU/Linux">Debian GNU/Linux</a>.</div>
<table class="infobox" style="width:22.7em; line-height: 1.4em; text-align:left; padding:.23em;"><tbody><tr><th colspan="3" class="cabecera organización" style="text-align:center;background-color:#DDD;color:black;"><b>Debian</b></th></tr><tr><td colspan="3" style="text-align:center;font-size:95%;;">
<a href="/wiki/Archivo:Debian-OpenLogo.svg" class="image"><img alt="Debian-OpenLogo.svg" src="//upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/245px-Debian-OpenLogo.svg.png" decoding="async" importance="high" elementtiming="thumbnail-high" width="245" height="324" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/368px-Debian-OpenLogo.svg.png 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Debian-OpenLogo.svg/490px-Debian-OpenLogo.svg.png 2x" data-file-width="109" data-file-height="144" /></a></td></tr><tr><th scope="row" style="text-align:left;font-size:95%;;">Tipo</th><td colspan="2" style="font-size:95%;;">
<a href="/wiki/Comunidad" title="Comunidad">comunidad</a> y <a href="/wiki/Organizaci%C3%B3n" title="Organización">organización</a></td></tr><tr><th scope="row" style="text-align:left;font-size:95%;;">Fundación</th><td colspan="2" style="font-size:95%;;">
<a href="/wiki/1993" title="1993">1993</a></td></tr><tr><th scope="row" style="text-align:left;font-size:95%;;">Fundador(es)</th><td colspan="2" style="font-size:95%;;">
<a href="/wiki/Ian_Murdock" title="Ian Murdock">Ian Murdock</a></td></tr><tr><th scope="row" style="text-align:left;font-size:95%;;">Dependiente de</th><td colspan="2" style="font-size:95%;;">
<a href="/wiki/Software_in_the_Public_Interest" title="Software in the Public Interest">Software in the Public Interest</a></td></tr><tr><th scope="row" style="text-align:left;font-size:95%;;">Sitio web</th><td colspan="2" style="font-size:95%;;">
```

The API is very useful both for downloading content from the wiki and for fetching links, image urls or the complete html code, which is useful for webscraping.

In the next article the Wikipedia API will be used again to do natural language processing (NLP) with Python.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)