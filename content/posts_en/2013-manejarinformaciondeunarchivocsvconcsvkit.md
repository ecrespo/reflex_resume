Title: Handling the information in a csv file with csvkit
Date: 2013-02-19 10:00
Category: Tutorial Python
Tags: General,Python,csv,csvkit
lang: en
translation: true

The `csvkit` program is a tool developed in Python that makes it easy to manipulate the information contained in a file in `csv` format.

The example will use data from the data.gov site. The data used comes from the United States Department of Veterans Affairs on educational benefits (excuse the translation) for the year 2009.

You need to install `csvkit`; in this case Python's `pip` command is used:  
```python
pip install csvkit
```
Get the data:
```
mkdir beneficios

cd beneficios 
```
Download the `2009.csv` file with the `wget` command:
```
wget -O 2009.csv -U "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.16 (JHTML, like Gecko) chrome/10.0.648.205 Safari/534.16" http://www.data.gob/download/4029/csv 
```
Check the first 5 lines of the file:
```
head -n 5 2009.csv 

State Name,State Abbreviate,Code,Montgomery GI Bill-Active Duty,Montgomery GI Bill- Selective Reserve,Dependents' Educational Assistance,Reserve Educational Assistance Program,Post-Vietnam Era Veteran's Educational Assistance Program,TOTAL,

ALABAMA,AL,01,"6,718","1,728","2,703","1,269",8,"12,426",

ALASKA,AK,02,776,154,166,60,2,"1,158",

ARIZONA,AZ,04,"26,822","2,005","3,137","2,011",11,"33,986",

ARKANSAS,AR,05,"2,061",988,"1,575",886,3,"5,513",
```
You can use the same `wget` command to download the files for the years 2010.csv, 2011.csv and 2012.csv.

Get the column information with `csvcut`:
```
csvcut -n 2009.csv

  1: State Name

  2: State Abbreviate

  3: Code

  4: Montgomery GI Bill-Active Duty

  5: Montgomery GI Bill- Selective Reserve

  6: Dependents' Educational Assistance

  7: Reserve Educational Assistance Program

  8: Post-Vietnam Era Veteran's Educational Assistance Program

  9: TOTAL

 10: 
```

As you can see, the `csv` file has 9 columns. 

With the `csvcut` command you can get the information from columns 2 and 3 (State Abbreviate and Code); here we only want to show the first 5 lines of the file: 
```
csvcut -c 2,3 2009.csv | head -n 5

State Abbreviate,Code
AL,01
AK,02
AZ,04
AR,05
```

You can also compute statistics on demand with `csvstat`. Here we generate the statistics for columns 1, 4, 9 and 10. In this case `csvcut` is used and its output is passed to `csvstat`:
```
csvcut -c 1,4,9,10 2009.csv | csvstat

  1. State Name
	<type 'unicode'>
	Nulls: True
	Unique values: 52
	Max length: 17
  2. Montgomery GI Bill-Active Duty
	<type 'int'>
	Nulls: True
	Min: 435
	Max: 34942
	Sum: 325723
	Mean: 6263.90384615
	Median: 3548.0
	Standard Deviation: 7537.86225373
	Unique values: 52
  3. TOTAL
	<type 'int'>
	Nulls: True
	Min: 768
	Max: 46897
	Sum: 506914
	Mean: 9748.34615385
	Median: 6520.0
	Standard Deviation: 10070.4022127
	Unique values: 52
  4. _unnamed
	<type 'NoneType'>
	Nulls: True
	Values: 
```

You can search rows with `csvgrep`. In this case, the total information for the State of Illinois:
```
csvcut -c 1,"TOTAL" 2009.csv | csvgrep -c 1 -m ILLINOIS

State Name,TOTAL

ILLINOIS,"21,964"
```

Reverse the order of the columns with `csvcut`: 
```
csvcut -c 9,1 2009.csv | head -n 5

TOTAL,State Name
"12,426",ALABAMA
"1,158",ALASKA
"33,986",ARIZONA
"5,513",ARKANSAS
```
In this case the column order is changed by telling csvcut the order of the columns. 

Sort with `csvsort`: 
```
csvcut -c 9,1 2009.csv | csvsort -r | head -n 5

TOTAL,State Name
46897,CALIFORNIA
40402,TEXAS
36394,FLORIDA
33986,ARIZONA
```
You can format the information so it is readable with `csvlook`:
```
csvcut -c 9,1 2009.csv | csvsort -r -l | csvlook

|--------------+-------+--------------------|
|  line_number | TOTAL | State Name         |
|--------------+-------+--------------------|
|  1           | 46897 | CALIFORNIA         |
|  2           | 40402 | TEXAS              |
|  3           | 36394 | FLORIDA            |
|  4           | 33986 | ARIZONA            |
|  5           | 21964 | ILLINOIS           |
|  6           | 20541 | VIRGINIA           |
|  7           | 18236 | GEORGIA            |
|  8           | 15730 | NORTH CAROLINA     |
|  9           | 13967 | NEW YORK           |
|  10          | 13962 | MISSOURI           |
|  11          | 13614 | COLORADO           |
|  12          | 13314 | OHIO               |
|  13          | 13011 | PENNSYLVANIA       |
|  14          | 12426 | ALABAMA            |
|  15          | 11492 | WASHINGTON         |
|  16          | 10085 | MARYLAND           |
|  17          | 9791  | MINNESOTA          |
|  18          | 9344  | MICHIGAN           |
|  19          | 9206  | OKLAHOMA           |
|  20          | 9013  | IOWA               |
|  21          | 8840  | WEST VIRGINIA      |
|  22          | 8757  | TENNESSEE          |
|  23          | 8081  | WISCONSIN          |
|  24          | 7872  | SOUTH CAROLINA     |
|  25          | 7809  | INDIANA            |
|  26          | 6652  | LOUISIANA          |
|  27          | 6388  | KENTUCKY           |
|  28          | 6009  | MASSACHUSETTS      |
|  29          | 5870  | OREGON             |
|  30          | 5513  | ARKANSAS           |
|  31          | 5511  | NEW JERSEY         |
|  32          | 5416  | NEBRASKA           |
|  33          | 5345  | UTAH               |
|  34          | 4947  | KANSAS             |
|  35          | 4551  | NEW MEXICO         |
|  36          | 4424  | PUERTO RICO        |
|  37          | 4299  | MISSISSIPPI        |
|  38          | 3728  | NEVADA             |
|  39          | 2997  | CONNECTICUT        |
|  40          | 2751  | IDAHO              |
|  41          | 2521  | HAWAII             |
|  42          | 1992  | SOUTH DAKOTA       |
|  43          | 1920  | MAINE              |
|  44          | 1795  | MONTANA            |
|  45          | 1778  | NORTH DAKOTA       |
|  46          | 1326  | NEW HAMPSHIRE      |
|  47          | 1175  | RHODE ISLAND       |
|  48          | 1158  | ALASKA             |
|  49          | 1145  | DELAWARE           |
|  50          | 1117  | WYOMING            |
|  51          | 1084  | DIST. OF COLUMBIA  |
|  52          | 768   | VERMONT            |
|  53          |       |                    |
|--------------+-------+--------------------|
```

Finally, you can save the work to a new csv file:
```
csvcut -c 9,1 2009.csv | csvsort -r -l > 2009_ranking.csv
```

 If you want to learn more about the `csvkit` tool, you can check the [documentation](https://csvkit.readthedocs.io/en/latest/index.html) page. 

The next article will show how to use `csvkit` from a Python program.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice at the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)