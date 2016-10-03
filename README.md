[![Build Status](https://travis-ci.com/portfoliome/foil.svg?token=79cPu78tDByfcardNKx8&branch=master)](https://travis-ci.com/portfoliome/foil)
[![codecov.io](http://codecov.io/github/portfoliome/foil/coverage.svg?branch=master)](http://codecov.io/github/portfoliome/foil?branch=master)
[![Code Climate](https://codeclimate.com/github/portfoliome/foil/badges/gpa.svg)](https://codeclimate.com/github/portfoliome/foil)

# foil

foil contains for data cleaning and ETL processing.

## Package Conventions

Contributions are welcome. Package conventions call for eliminating **IF** statements, descriptive variable names, reliance on the standard library, and priority for test driven development.

## Usage

These instructions assume Python 3.5. It is recommended that you use conda or a virtualenv. foil is fairly lightweight, but has some dependencies.

### Getting Started


#### For conda install follow:
Download the [conda installer](http://conda.pydata.org/miniconda.html).
And follow setup [instructions](http://conda.pydata.org/docs/install/quick.html#id1).

#### Conda Environment

```sh
conda create --name <environment_name> python=3.5
activate <environment_name>
conda install --file requirements.txt

python setup.py install bdist_wheel
```

#### debian installation
[Instruction](https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux)

Follow the instructions in the link provided. **DO NOT SUDO PIP INSTALL**. Alias the preferred Python installation by adding, for example:

```sh
alias python='/usr/bin/python3.5'
```

#### When using Pip
```sh
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

python setup.py install bdist_wheel
```

#### Running the Tests
```sh
py.test
```
#### Running Coverage Report
```sh
py.test --cov
```


