Ambev Data Challenge
==============================

A short description of the project.

## Dependencies
------------

This project needs some dependencies, the `requirements.txt` has the necessary packages to intall them automatically as we will see later. At this point you need to install Anaconda. We will use `make`too.

## Step by step
------------

This section will walk with you trhough a step by step to make this project running.


### Creating an environment:

First let's create a new environment for this project:
TODO: run make environments together with this command and test_environment
```
make create_environment
```
Then activate it with this command:
```
source activate ambev_data_challenge
```

### Getting the data - everything starts here:
The contents of `data` folder are managed by Git LFS. If you want to download the raw data and do all pre-processing stuff, just empty all folders inside `data` (but keep them) and follow the instructions bellow.

You can download the data using this command:
```
make data
```
Before it starts working with the data, this command will do 2 steps automatically:
- Install all necessary packages (command `make requirements`) based on requirements.txt
- Check the environment we just created (command `make test_environment`)
Then this will download the data into `data/raw` folder. Once the download is done, it will create a CSV file to each worksheet into the folder `data/interim`


## Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

TODO:
- Verificar scripts fora do git
- colocar datasets no git lfs
- remover partes relacionadas a s3
- limpar o diretório final
