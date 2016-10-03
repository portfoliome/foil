# foil

foil contains for data cleaning and ETL processing.

# Usage

These instructions assume Python 3.5. It is recommended that you use conda or a virtualenv. foil is fairly lightweight, but has some dependencies.

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

#### When using Pip

```sh
pip install --upgrade pip
pip install wheel
pip install -r requirements.txt

python setup.py install bdist_wheel
```

## Running the Tests

```sh
py.test
```

### Running Coverage Report
```sh
py.test --cov
```


