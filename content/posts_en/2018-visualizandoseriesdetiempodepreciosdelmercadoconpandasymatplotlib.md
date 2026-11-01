Title: Visualizing market price time series with pandas and matplotlib  
Date: 2018-06-06 09:00  
Category: Tutorial Python  
Tags: Python, Pandas,Matplotlib,Series de Tiempo, Visualización
lang: en
translation: true 


In this article the Quandl library will be used directly as the data source. The idea is to obtain the market prices of 3 airlines (Delta with code DAL, Jet Blue with code JBLU and Southwest with code LUV).  The historical closing prices, the sales volume and the moving averages of these three airlines are plotted.


Continuing with the articles on [Pandas](/blog/tags) and [Data Science](/blog/tags)[Data Science](/blog/tags), the [previous](/blog/comoobtenerdatosfinancierosdequandlconpythonypandas) article showed how to work with time series by obtaining data from Quandl.

This article is based on an English article titled [Visualizing Time Series Data of Stock Prices](http://byteacademy.co/blog/time-series-python) (that article uses the `pandas_datareader` library, but it is giving errors, so the `Quandl` library will be used).


The exercise code is shown below:

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-1.png)

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-2.png)

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-3.png)

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-4.png)

### Visualizing

#### Plotting the adjusted closing price  

The adjusted closing price of the 3 airlines will be plotted.

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-5.png)

#### Plotting the Volume

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-6.png)

You can notice that the airline Delta has a very high spike at some point in 2013.
To get the date, the idxmax method is used.

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-7.png)

#### Moving averages MA  
Moving averages are used to detect trading opportunities. 
This calculation takes the mean or average of past prices (it is called a moving average because the data is continuously moving).
Depending on the type of investor (high risk vs low risk, short term vs long term), the moving averages can be set to 10 days, 20 days, 50 days, 200 days, 1 year, 5 years, etc. 
In this case the 50-day and 200-day moving averages will be calculated.

![](./images/visualizandoseriesdetiempodepreciosdelmercadoconpandasymatplotlib-8.png)


You can download the raw notebook from the [gitlab](https://gitlab.com/mangoosta/articulos-cienciasdedatos/raw/master/quandl/VisualizandoSeriesTiempo.ipynb) repository.

If you have any suggestion or idea about how this article can be applied, you can leave it in the comments.


##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)