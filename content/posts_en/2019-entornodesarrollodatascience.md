Title: Creating a development environment for Data Science with Anaconda, Jupyter, git and cookiecutter
Date:  2019-07-28 12:20
Category: Tutorial de Data Science
Tags: Debian,Ubuntu,Linux,Python,Data Science,Ciencia de Datos,Entorno Desarrollo
lang: en
translation: true
Slug: entorno_desarrollo_datascience
Authors: Ernesto Crespo
Summary: Development environment with anaconda, Jupyter, git, black and cookiecutter for Data Science

![https://imgs.xkcd.com/comics/python_environment.png](./images/20190728-python_environment.png)


For some time now I have been working with data, and it is a mess to keep the data files organized: the input data, the intermediate data files and the final data, besides keeping the jupyter notebooks under version control. The idea of this article is to give a guide to organizing the data and the notebooks, as well as the necessary tools; later articles will cover the topic of continuous integration and Data Pipeline management.

The first thing to do is create a repository on github ([article on how to create a repository (broken link)](https://towardsdatascience.com/introduction-to-github-for-data-scientists-2cf8b9b25fba)).

Creating the datadev repository:

![Creating the datadev repository](./images/20190728-creandorepositorio.png)

datadev repository created:

![datadev repository created](./images/20190728-repositorio_datadev.png)

Clone the repository (this step is skipped when using cookiecutter):

```bash
git clone git@github.com:ecrespo/datadev.git
```



### Installing Anaconda

[Anaconda](https://www.anaconda.com/) is a Python distribution dedicated to scientific computing or data science. For Linux it
can be downloaded from the following link [Python 3.7](https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh).


To install, run the following command:

```bash
bash Anaconda3-2019.07-Linux-x86_64.sh
```

### Creating the anaconda working environment


Create an environment called datadev:

```bash
conda create -n datadev
```

To activate the environment, run:

```bash
conda activate datadev
```

To deactivate it:

```bash
conda deactivate
```

When it is activated you get the following prompt:

```bash
(datadev) ernesto@jewel:~/proyectos/datadev$
```

Add the conda-forge channel:

```bash
conda config --env --add channels conda-forge
```

Verify that the channel has been added:

```bash
conda config --show channels
channels:
  - conda-forge
  - defaults

```

Install basic packages:

```bash
conda install pandas scikit-learn matplotlib notebook jupyter numpy
```

![Anaconda package installer](./images/20190728_paquetes.png)


Install packages that are not in conda-forge:

```bash
conda install -c plotly plotly_express
```


Start jupyter notebook:

```bash
jupyter notebook
```

This opens the browser on the jupyter notebook:

![jupyter notebook](./images/20190728_jupyternotebook.png)

### Installing cookiecutter

Run the anaconda installer to install cookiecutter.

```
 conda install cookiecutter
```

 Create the data science project:

Run it outside the datadev repository, with the name datadev.

```  
 cookiecutter https://github.com/drivendata/cookiecutter-data-science
```

This asks a few questions in order to create the directories:

![cookiecutter](./images/20190728_datadev.png)

This creates the following structure of directories and files:

```
.
├── data
│   ├── external                          <- Data de fuentes de 3eras partes
│   ├── interim                           <- Datos intermedios que han sido transformados
│   ├── processed                         <- Datos procesados, que serán usados para el modelo
│   └── raw                               <- Data cruda, datos descargados sin modificar
├── docs                                  <- Default proyecto sphinx
│   ├── commands.rst
│   ├── conf.py
│   ├── getting-started.rst
│   ├── index.rst
│   ├── make.bat
│   └── Makefile
├── LICENSE                               
├── Makefile                              <- Archivo makefile con comandos como make data o make train
├── models                                <- Modelos entrados o serializados, predicciones
├── notebooks                             <- Notebooks de jupyter
├── README.md         
├── references                            <- Diccionario de datos, manuales, y cualquier otro material explicativo
├── reports                               <- análisis generados como pdf, html, latex, etc
│   └── figures                           <- Gráficas generadas a hacer usados en los reportes
├── requirements.txt                      <- lista de paquetes requeridos para reproducir el entorno, pip freeze > requirements.txt
├── setup.py                              <- Hace este proyecto instalable con pip install -e
├── src                                   <- Código fuente de este proyecto
│   ├── data                              <-Scripts para descargar o generar datos
│   │   ├── __init__.py
│   │   └── make_dataset.py
│   ├── features                          <- Scripts para convertir la data cruda a datos para el modelo
│   │   ├── build_features.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── models                            <- Scripts para entrenar el modelo y luego hacer predicciones
│   │   ├── __init__.py
│   │   ├── predict_model.py
│   │   └── train_model.py
│   └── visualization                     <- Scripts para crear exploración y resultados orientados a la visualización
│       ├── __init__.py
│       └── visualize.py
├── test_environment.py
└── tox.ini                               <- Archivo tox con configuraciones para correr tox
```

Install additional requirements:

```bash
pip install -r requirements.txt
```

### Creating the Anaconda environment yml file

To create the yml file, run the following command:

```bash
conda env export > environment.yml
```

This generates a yml file with the contents of the datadev environment:

```
name: datadev
channels:
  - plotly
  - conda-forge
  - defaults
dependencies:
  - _libgcc_mutex=0.1=main
  - arrow=0.14.3=py37_0
  - asn1crypto=0.24.0=py37_1003
  - attrs=19.1.0=py_0
  - backcall=0.1.0=py_0
  - binaryornot=0.4.4=py_1
  - bleach=3.1.0=py_0
  - bzip2=1.0.8=h516909a_0
  - ca-certificates=2019.6.16=hecc5488_0
  - certifi=2019.6.16=py37_1
  - cffi=1.12.3=py37h8022711_0
  - chardet=3.0.4=py37_1003
  - click=7.0=py_0
  - cookiecutter=1.6.0=py37_1000
  - cryptography=2.7=py37h72c5cf5_0
  - cycler=0.10.0=py_1
  - dbus=1.13.6=he372182_0
  - decorator=4.4.0=py_0
  - defusedxml=0.5.0=py_1
  - entrypoints=0.3=py37_1000
  - expat=2.2.5=he1b5a44_1003
  - fontconfig=2.13.1=h86ecdb6_1001
  - freetype=2.10.0=he983fc9_0
  - future=0.17.1=py37_1000
  - gettext=0.19.8.1=hc5be6a0_1002
  - glib=2.58.3=h6f030ca_1002
  - gst-plugins-base=1.14.5=h0935bb2_0
  - gstreamer=1.14.5=h36ae1b5_0
  - icu=64.2=he1b5a44_0
  - idna=2.8=py37_1000
  - ipykernel=5.1.1=py37h5ca1d4c_0
  - ipython=7.7.0=py37h5ca1d4c_0
  - ipython_genutils=0.2.0=py_1
  - ipywidgets=7.5.0=py_0
  - jedi=0.14.1=py37_0
  - jinja2=2.10.1=py_0
  - jinja2-time=0.2.0=py_2
  - joblib=0.13.2=py_0
  - jpeg=9c=h14c3975_1001
  - json5=0.8.5=py_0
  - jsonschema=3.0.1=py37_0
  - jupyter=1.0.0=py_2
  - jupyter_client=5.3.1=py_0
  - jupyter_console=6.0.0=py_0
  - jupyter_core=4.4.0=py_0
  - jupyterlab=1.0.4=py37_0
  - jupyterlab_server=1.0.0=py_1
  - kiwisolver=1.1.0=py37hc9558a2_0
  - libblas=3.8.0=10_openblas
  - libcblas=3.8.0=10_openblas
  - libffi=3.2.1=he1b5a44_1006
  - libgcc-ng=9.1.0=hdf63c60_0
  - libgfortran-ng=7.3.0=hdf63c60_0
  - libiconv=1.15=h516909a_1005
  - liblapack=3.8.0=10_openblas
  - libopenblas=0.3.6=h6e990d7_5
  - libpng=1.6.37=hed695b0_0
  - libsodium=1.0.17=h516909a_0
  - libstdcxx-ng=9.1.0=hdf63c60_0
  - libuuid=2.32.1=h14c3975_1000
  - libxcb=1.13=h14c3975_1002
  - libxml2=2.9.9=hee79883_2
  - markupsafe=1.1.1=py37h14c3975_0
  - matplotlib=3.1.1=py37_1
  - matplotlib-base=3.1.1=py37he7580a8_1
  - mistune=0.8.4=py37h14c3975_1000
  - nbconvert=5.5.0=py_0
  - nbformat=4.4.0=py_1
  - ncurses=6.1=hf484d3e_1002
  - notebook=6.0.0=py37_0
  - numpy=1.16.4=py37h95a1406_0
  - openblas=0.3.6=h6e990d7_5
  - openssl=1.1.1c=h516909a_0
  - pandas=0.25.0=py37hb3f55d8_0
  - pandoc=2.7.3=0
  - pandocfilters=1.4.2=py_1
  - parso=0.5.1=py_0
  - patsy=0.5.1=py_0
  - pcre=8.41=hf484d3e_1003
  - pexpect=4.7.0=py37_0
  - pickleshare=0.7.5=py37_1000
  - pip=19.2.1=py37_0
  - plotly=4.0.0=py_0
  - plotly_express=0.4.0=py_0
  - poyo=0.5.0=py_0
  - prometheus_client=0.7.1=py_0
  - prompt_toolkit=2.0.9=py_0
  - pthread-stubs=0.4=h14c3975_1001
  - ptyprocess=0.6.0=py_1001
  - pycparser=2.19=py37_1
  - pygments=2.4.2=py_0
  - pyopenssl=19.0.0=py37_0
  - pyparsing=2.4.1.1=py_0
  - pyqt=5.9.2=py37hcca6a23_0
  - pyrsistent=0.15.4=py37h516909a_0
  - pysocks=1.7.0=py37_0
  - python=3.7.3=h33d41f4_1
  - python-dateutil=2.8.0=py_0
  - pytz=2019.1=py_0
  - pyzmq=18.0.2=py37h1768529_2
  - qt=5.9.7=h0c104cb_3
  - qtconsole=4.5.2=py_0
  - readline=8.0=hf8c457e_0
  - requests=2.22.0=py37_1
  - retrying=1.3.3=py_2
  - scikit-learn=0.21.2=py37hcdab131_1
  - scipy=1.3.0=py37h921218d_1
  - send2trash=1.5.0=py_0
  - setuptools=41.0.1=py37_0
  - sip=4.19.8=py37hf484d3e_1000
  - six=1.12.0=py37_1000
  - sqlite=3.29.0=hcee41ef_0
  - statsmodels=0.10.1=py37hc1659b7_0
  - terminado=0.8.2=py37_0
  - testpath=0.4.2=py_1001
  - tk=8.6.9=hed695b0_1002
  - tornado=6.0.3=py37h516909a_0
  - traitlets=4.3.2=py37_1000
  - urllib3=1.25.3=py37_0
  - wcwidth=0.1.7=py_1
  - webencodings=0.5.1=py_1
  - wheel=0.33.4=py37_0
  - whichcraft=0.6.0=py_0
  - widgetsnbextension=3.5.0=py37_0
  - xorg-libxau=1.0.9=h14c3975_0
  - xorg-libxdmcp=1.1.3=h516909a_0
  - xz=5.2.4=h14c3975_1001
  - zeromq=4.3.2=he1b5a44_2
  - zlib=1.2.11=h516909a_1005
  - pip:
    - alabaster==0.7.12
    - awscli==1.16.207
    - babel==2.7.0
    - botocore==1.12.197
    - colorama==0.3.9
    - coverage==4.5.3
    - docutils==0.15.1
    - flake8==3.7.8
    - imagesize==1.1.0
    - jmespath==0.9.4
    - mccabe==0.6.1
    - packaging==19.0
    - pyasn1==0.4.5
    - pycodestyle==2.5.0
    - pyflakes==2.1.1
    - python-dotenv==0.10.3
    - pyyaml==5.1
    - rsa==3.4.2
    - s3transfer==0.2.1
    - snowballstemmer==1.9.0
    - sphinx==2.1.2
    - sphinxcontrib-applehelp==1.0.1
    - sphinxcontrib-devhelp==1.0.1
    - sphinxcontrib-htmlhelp==1.0.2
    - sphinxcontrib-jsmath==1.0.1
    - sphinxcontrib-qthelp==1.0.2
    - sphinxcontrib-serializinghtml==1.1.3
prefix: /home/ernesto/anaconda3/envs/datadev
```
The good thing is that this file handles the packages installed by anaconda as well as by pip.

To use the yml file, run:

```bash
conda env create -f environment.yml -p /home/user/anaconda3/envs/env_name
```

Where the -p option defines the path where the environment is installed.


### Git

To finish the article, the datadev directory is associated with the repository that was created on github or gitlab.

Run git init inside the datadev directory:

```bash
git init
```

Add the repository to the local repo:

```bash
 git remote add origin  https://github.com/ecrespo/datadev.git
 ```

Define the master branch and the origin repository to push to:

```bash
 git push --set-upstream origin master
 ```

 With this you have a working environment; later articles will show other tools to use in the environment.


 At the end, the repository on github looks as shown below:

 ![Github repository](./images/20190728_repo_datadev.png)



References:

* [Introduction to Github for Data Scientists (broken link)](https://towardsdatascience.com/introduction-to-github-for-data-scientists-2cf8b9b25fba)
* [Creating Reproducible Data Science Projects (broken link)](https://towardsdatascience.com/creating-reproducible-data-science-projects-1fa446369386)
* [How to Start a Data Science Project in Python (broken link)](https://blog.godatadriven.com/how-to-start-a-data-science-project-in-python)
* [Managing Data Science Projects with Git (broken link)](http://www.brycemcdonald.net/powershell/automation/exchange/2018/04/09/Using-Cookiecutter-for-data-science.html)
* [Cookiecutter Data Science — Organize your Projects — Atom and Jupyter (broken link)](https://medium.com/@rrfd/cookiecutter-data-science-organize-your-projects-atom-and-jupyter-2be7862f487e)
* [Setup a python data analysis environment](https://tutorials.technology/tutorials/18-Setup-a-python-data-analysis-environment.html)
* [Set up a lean, robust data science environment with Miniconda and Conda-Forge (broken link)](https://medium.com/dunder-data/anaconda-is-bloated-set-up-a-lean-robust-data-science-environment-with-miniconda-and-conda-forge-b48e1ac11646)
* [cookiecutter data science repository](https://github.com/drivendata/cookiecutter-data-science)
* [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/?source=post_page---------------------------#opinions)


####

Make a donation!
If you liked the article you can make a donation with Bitcoin (BTC)
using the digital wallet of your choice to the following
address: 17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV

Or by scanning the QR code from your wallet:

![17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV](./images/17MtNybhdkA9GV3UNS6BTwPcuhjXoPrSzV.png)