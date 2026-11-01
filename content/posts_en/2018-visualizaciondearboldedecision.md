Title: Decision Tree visualization  
Date: 2018-06-17 09:00  
Category: Tutorial Python  
Tags: Python,Machine Learning, Scikit-Learn,Árbol de decisión
lang: en  
translation: true  


Last November I wrote an article about [decision trees with Python](/blog/arboldedecisionhechoenpython), which had a set of input data (height, weight and size) and an output of whether the person was a man or a woman.  This article adds the visualization of the decision tree, using two Python libraries, `pydot` and `graphviz`.

It is assumed that `scikit-learn` is already installed, so now install `pydot` and `graphviz`:
```python
#pip3 install pydot
#pip3 install graphviz
```

Now the code is shown:

![](./images/visualizaciondearboldedecision-1.png)

![](./images/visualizaciondearboldedecision-2.png)

![](./images/visualizaciondearboldedecision-3.png)


Now it is time to visualize the tree:

![](./images/visualizaciondearboldedecision-4.png)

![](./images/visualizaciondearboldedecision-5.png)

Finally, the graph of the tree is shown:

![](./images/visualizaciondearboldedecision-6.png)

This graph is generated from the instance of the class that is used to enter the data, trained, and then used to predict with new data.
The information shown by each decision node:

- Samples: The number of samples being handled.  
- gini: An index that indicates the cost of evaluating the split of the data.  
- value: A value that is being evaluated at that moment.   

You can see the code of this article in the notebook found in the [gitlab repository](https://gitlab.com/mangoosta/articulos-cienciasdedatos/blob/master/ArbolDecision.ipynb).

The next article will present another example, this time with a larger data set.

If you have any question or comment, you can leave it in the comments of the post.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from the wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)