Title: Unit tests with unittest in Python using nosetests and Docker/docker-compose
Date: 2016-10-05 09:00
Category: Tutorial Python
Tags: Docker,Docker-compose,nosetests,Prueba de cobertura,Pruebas unitarias,unittest
lang: en
translation: true

The blog has already covered unit testing, and using Docker; you can find the previous articles under the tag [unittest](/blog/tags).

This article shows a calculator class that does an addition and a square root, along with the class for the unit tests.

#### File and directory structure

The file and directory structure of the repository's working directory is the following:

```
tutoriales-pruebas
├── app
│   ├── calculadora.py
│   └── __init__.py
├── docker-compose.yml
├── Dockerfile
└── test
    └── unit
        ├── calculadora_test.py
        └── __init__.py
```

`Dockerfile` and `docker-compose.yml` files

The Dockerfile defines python as the base system and passes in the dependencies needed to use nosetests and coverage.

Here is the code of the Dockerfile:

```python
FROM python


WORKDIR /code/



RUN pip3 install --upgrade pip


RUN pip3 install nose


RUN pip3 install nose-cov


RUN pip3 install rednose


RUN pip3 install pytest


RUN pip3 install pytest-cov


RUN pip3 install mock





ADD . /code/


COPY . /code/





CMD nosetests  --with-coverage

#CMD nosetests -sv --rednose 


```

You have to comment and uncomment the two CMD lines depending on whether you want to use coverage or not.

The `docker-compose.yml` file contains the following:

```
pruebas:

  build: .



  volumes:

    - ".:/code"
```

It defines the pruebas microservice, which will use the Dockerfile, and defines the volume.

#### Calculator module

This module has the calculator class with the methods for addition and square root; the code is shown below:

```python


#!/usr/bin/env python


#Se importa sqrt de math


from math import sqrt


#Clase calculadora


class Calculadora:


    #Metodo suma de x y y, se evalua si son enteros si no, devuelve error.


    def suma(self,x,y):


        if type(x) == int and type(y) == int:


            return x + y


        else:


            raise TypeError("Invalid type: {} and {}".format(type(x),type(y)))





    #Metodo raizcuadrada de X, devuelve la raiz cuadrada si es entero positivo, si no


    #devuelve mensaje de error.


    def raizCuadrada(self,x):


        if type(x) == int and x >= 0:


            return math.sqrt(x)


        else:


            raise TypeError("Invalid type: {} ".format(type(x)))



if __name__ == '__main__':


    #Se crea una instancia de la clase


    calc = Calculadora()


    #Se calcula la suma de 2 y 2, se muestra en pantalla.


    results = calc.sum(2, 2)


    print (results)

```

#### Tests module

The `calculadora_tests.py` file contains the tests for the addition and the square root. It also shows a series of methods for other tests that exist in unittest (which have nothing to do with the calculator tests, they are only there to illustrate the use of unittest).

The code is shown below:

```python
#!/usr/bin/env python3


import unittest


from app.calculadora import Calculadora




class TestCalculadora(unittest.TestCase):


    def setUp(self):


        self.calc = Calculadora()



    def test_suma_retorna_resultado_correcto(self):


        ##Asegura que sea igual la operacion de suma 2+2 a 4


        self.assertEqual(4, self.calc.suma(2,2))



    def test_suma_devuelve_error_si_el_tipo_no_es_entero(self):


        #Asegura error, si es de tipo, cuando se le pasa dos string.


        self.assertRaises(TypeError, self.calc.suma, "Hello", "World")



    def test_asegura_que_sea_verdadero(self):


        #Se asegura que el valor 1 es true y un string.


        self.assertTrue(1)


        self.assertTrue("Hello, World")



    def test_aseura_que_sea_falso(self):


        #Se asegura que el string vacio y cero son falso.


        self.assertFalse(0)


        self.assertFalse("")




    def test_asegura_que_es_mayor(self):


        #Se asegura que 2>1


        self.assertGreater(2, 1)



    def test_asegura_que_es_mayor_e_igual(self):


        #Se asegura que 2>=2


        self.assertGreaterEqual(2, 2)



    def test_asegura_que_es_casi_igual_a_delta_0_5(self):


        #Se asegura que sea casi igual 1 y 1.2 con delta de 0.5


        self.assertAlmostEqual(1, 1.2, delta=0.5)



    def test_asegura_lugares_casi_igual(self):


        #Se asegura que es casi igual 1 y 1.00001 por 4 lugares.


        self.assertAlmostEqual(1, 1.00001, places=4)




    def test_asegura_diccionario_contiene_subconjunto(self):


        esperado = {'a': 'b'}


        actual = {'a': 'b', 'c': 'd', 'e': 'f'}


        #Se asegura que el diccionario actual contiene lo esperado.


        self.assertDictContainsSubset(esperado, actual)



    def test_asegura_diccionarios_iguales(self):


        esperado = {'a': 'b', 'c': 'd'}


        actual = {'c': 'd', 'a': 'b'}


        #Se asegra que el diccionario esperado sea igual al actual.


        self.assertDictEqual(esperado, actual)



    def test_asegura_que_esta_en(self):


        #Se asegura que 1 este en la lista


        self.assertIn(1, [1,2,3,4,5])



    def test_asegura_expresiones_iguales(self):


        #Se asegura que las expresiones son iguales expre1 y expre2


        self.assertIs("a", "a")



    def test_asegura_objeto_es_instancia_de_una_clase(self):


        #Se asegura que el objeto 2 sea de la clase entero


        self.assertIsInstance(2, int)



    def test_asegura_objeto_no_es_instancia_de_una_clase(self):


        #Se asegura que el objeto 2 no sea una clase str


        self.assertNotIsInstance(2, str)



    def test_asegura_que_es_none(self):


        #Se asegura que es None.


        self.assertIsNone(None)



    def test_asegura_expresiones_no_sean_iguales(self):


        self.assertIsNot([], [])



    def test_asegura_que_no_sea_none(self):


        #Se asegura que 1 no es None.


        self.assertIsNotNone(1)



    def test_asegura_que_es_menor(self):


        #Se asegura que 3 es menor que 5


        self.assertLess(3, 5)



    def test_asegura_que_es_menor_e_igual(self):


        #Se asegura que 7 es menor o igual que 7.


        self.assertLessEqual(7, 7)




if __name__ =




= '__main__':



  unittest.main()
```

### Running the tests

#### Running unit tests

To run the tests, leave uncommented the line in the Dockerfile that says:

```
#CMD nosetests  --with-coverage
CMD nosetests -sv --rednose
```

Build the image:

```
docker-compose build
```

Run the container:

```
docker-compose up
```

The result of the run is shown below:

```
Recreating tutorialespruebas_pruebas_1
Attaching to tutorialespruebas_pruebas_1
pruebas_1 | test_asegura_diccionario_contiene_subconjunto (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_diccionarios_iguales (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_expresiones_iguales (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_expresiones_no_sean_iguales (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_lugares_casi_igual (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_objeto_es_instancia_de_una_clase (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_objeto_no_es_instancia_de_una_clase (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_es_casi_igual_a_delta_0_5 (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_es_mayor (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_es_mayor_e_igual (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_es_menor (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_es_menor_e_igual (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_es_none (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_esta_en (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_no_sea_none (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_asegura_que_sea_verdadero (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_aseura_que_sea_falso (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_suma_devuelve_error_si_el_tipo_no_es_entero (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | test_suma_retorna_resultado_correcto (unit.calculadora_test.TestCalculadora) ... passed
pruebas_1 | 
pruebas_1 | -----------------------------------------------------------------------------
pruebas_1 | 19 tests run in 0.072 seconds (19 tests passed)
tutorialespruebas_pruebas_1 exited with code 0
```

19 tests were run and all of them passed; the run took 0.072 seconds.

Running coverage tests
Code coverage makes it possible to measure the quality of the tests ( more information on wikipedia).

To run the test, you need to modify the Dockerfile so that it uses coverage:

```
CMD nosetests  --with-coverage
#CMD nosetests -sv --rednose
```

Build the Docker image:

```
docker-compose build 
```

Run the test container:

```
docker-compose up
```

The result is shown below:

```
Recreating tutorialespruebas_pruebas_1
Attaching to tutorialespruebas_pruebas_1
pruebas_1 | ...................
pruebas_1 | Name                 Stmts   Miss  Cover
pruebas_1 | ----------------------------------------
pruebas_1 | app.py                   0      0   100%
pruebas_1 | app/calculadora.py      14      6    57%
pruebas_1 | unit.py                  0      0   100%
pruebas_1 | ----------------------------------------
pruebas_1 | TOTAL                   14      6    57%
pruebas_1 | ----------------------------------------------------------------------
pruebas_1 | Ran 19 tests in 0.019s
pruebas_1 | 
pruebas_1 | OK
tutorialespruebas_pruebas_1 exited with code 0
```

As you can see, the calculator module has 57% coverage.

The code of this project is in the [tutorial tests repo on the nosetests branch](https://gitlab.com/ecrespo/tutoriales-pruebas/tree/nosetests).

## ##

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)
