Title: Back to basics, how to handle queues in python.
Date: 2017-02-24 09:00
Category: Tutorial Python
Tags: Python
lang: en
translation: true

Queue data structures are FIFO (first in, first out).

The article is based on the [official Python documentation in English](http://docs.python.org/3/tutorial/datastructures.html#using-lists-as-queues) .
Lists can be used as a queue.

Lists support the following methods:

- `list.append(x)`: adds an element to the end of the list, equivalent to a[len(a):] =[x].
- `list.extend(L)`: extends a list by adding all the elements of another list, equivalent to a[len(a):] = L.
- `list.insert(i,x)`: Inserts an element into the list at a given position. 
- `list.remove(x)`: Removes the first item x from the list.
- `list.pop([i])`:Removes the item at the given position in the list, and returns it.
- `list.clear()`: Removes all the elements from the list.
- `list.count(x)`: Returns the number of times x appears in the list.
- `list.sort(key=None,reverse=False)`: Sorts the elements of the list.
- `list.reverse()`: Reverses the order of the list.
- `list.index(x)`: Returns the index of the first element of the list that is x.
- `list.copy()`: Returns a copy of the list.


To emulate a queue with a list, here is the following example:
```python
>>> cola = [3,5,6]

>>> cola.append(8)

>>> cola

[3, 5, 6, 8]

>>> cola.pop()

8

>>> cola.append(8)

>>> cola.pop(0)

3

>>> cola.append(9)

>>> cola.pop(0)

5

>>> cola.pop(0)

6

>>> cola = [3,5,6]

>>> cola

[3, 5, 6]

>>> cola.append(9)

>>> cola

[3, 5, 6, 9]

>>> cola.append(19)

>>> cola

[3, 5, 6, 9, 19]

>>> cola.pop(0)

3

>>> cola.pop(0)

5

>>> cola

[6, 9, 19]

>>> cola.pop(0)

6

>>> cola

[9, 19]

>>> cola.pop(0)

9

>>> cola

[19]

>>> cola.pop(0)

19

>>> cola

[]

```

The `pop` method is used, telling it to always take the first element of the list.

This is not efficient, so the best option is to implement a queue with `collection.deque`:

```python

>>> from collections import deque


>>> cola = deque([1,2,3,4,5])


>>> cola


deque([1, 2, 3, 4, 5])


>>> cola.append(19) #Llega 19


>>> cola


deque([1, 2, 3, 4, 5, 19])


>>> cola.append(39) #Llega 39


>>> cola


deque([1, 2, 3, 4, 5, 19, 39])


>>> cola.popleft() #Sale 1


1


>>> cola.popleft() #Sale 2


2


>>> cola


deque([3, 4, 5, 19, 39])


>>> cola.append(51) #Llega 51


>>> cola


deque([3, 4, 5, 19, 39, 51])


>>> cola.popleft() #Sale 3


3


>>> cola


deque([4, 5, 19, 39, 51])

```

This article showed how to handle queues using only lists or `collections.deque`.

##  ##
Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)