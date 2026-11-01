Title: How to get Financial data from Quandl with Python and Pandas  
Date: 2018-05-25 09:00  
Category: Tutorial Python
Tags: Python, Matplotlib, Pandas, Quandl
lang: en  
translation: true  

The idea of this article is to explain in a basic way how to use Pandas to get financial data, in this case the value of the currencies of countries such as Argentina, Brazil, Chile, Mexico and Venezuela.
Quandl is a financial and economic alternative data platform that serves professional investors. The Quandl API gives access to its data through the R language, Python, Matlab, Maple and Stata. More information on [wikipedia (broken link)](https://en.wikipedia.org/wiki/Quandl) and on its [site](https://www.quandl.com/).  

In this case the data will be accessed through Python and visualized with Pandas and matplotlib.  

The Quandl information for the countries:  
- Venezuela : [Dicom (broken link)](https://www.quandl.com/data/BUNDESBANK/BBEX3_M_VEF_USD_CA_AB_B09-Exchange-Rates-For-The-Us-Dollar-In-The-Bolivarian-Republic-Of-Venezuela-Dicom-Usd-1-Vef-selling) and [Dolar Today (broken link)](https://www.quandl.com/data/DOLARTODAY/BSF_USD-DolarToday-Bolivar-Fuerte-USD-Exchange-Rate)  
- [Argentina (broken link)](https://www.quandl.com/data/BUNDESBANK/BBEX3_D_ARS_USD_CA_AC_000-Exchange-Rates-For-The-Us-Dollar-In-Argentina-Usd-1-Ars-middle)  
- [Brazil (broken link)](https://www.quandl.com/data/BUNDESBANK/BBEX3_D_BRL_USD_CA_AC_000-Exchange-Rates-For-The-Us-Dollar-In-Brazil-Usd-1-Brl-middle)  
- [Chile (broken link)](https://www.quandl.com/data/BUNDESBANK/BBEX3_D_CLP_USD_CA_AC_000-Exchange-Rates-For-The-Us-Dollar-In-Chile-Usd-1-Clp-middle)  
- [Mexico (broken link)](https://www.quandl.com/data/BUNDESBANK/BBEX3_M_MXN_USD_CA_AB_A01-Exchange-Rates-For-The-Us-Dollar-In-Mexico-Usd-1-Mxn-selling)  

The process would be the following:


1. Import libraries  
2. Access the countries' data in Quandl  
3. Sort the columns, remove NaN.  
4. Create a portfolio  
5. Visualize the data  

You can see the codes to access the data, for example for Mexico, in the following image.

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-1.png)

Quandl page with the Dollar information for Mexico

1. Import the pandas, quandl and matplotlib libraries

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-2.png)

2. Define the start and end dates of the analysis

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-3.png)

3. Get data from quandl

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-4.png)

4. Visualize the Dicom and Dolar today data

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-5.png)

5. Create the portfolio that groups all the quotes

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-6.png)

6. Drop the NaN fields and rename the columns

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-7.png)

7. Plot all the quotes

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-8.png)

8. Plot for Argentina

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-9.png)

9. Plot for Brazil

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-10.png)

10. Plot for Chile

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-11.png)

11. Plot for Mexico

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-12.png)

12. Plot for Venezuela

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-13.png)

13. Dicom and Dolar Today plots separately

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-14.png)  

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-15.png)  

![](./images/comoobtenerdatosfinancierosdequandlconpythonypandas-16.png)

You can see the complete notebook at:  
[ecrespo/articulos-cienciadedatos
Contribute to articulos-cienciadedatos development by creating an account on GitHub.github.com](https://github.com/ecrespo/articulos-cienciadedatos/blob/master/quandl/cotizaciones-dolar.ipynb)


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
