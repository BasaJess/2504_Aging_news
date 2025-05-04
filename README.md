## ![](/images/pexels-googledeepmind-17484975.jpg) 

# 2504_Science_Youth
FIND THE LATEST SCIENTIFIC FINDINGS IN YOUTH EXTENSION AND HEALTH SPAN

---

*Jesus Gonzalez  
Data Science and IT Support   
Am Lindenbaum 71  
Frankfurt am Main, GE*

--- 
## **Overview**

There’s growing interest in longevity research, but manually sifting through vast amounts of scientific papers is time-consuming. According to experts in the field, nowadays there is a scientific paper on regards to this topic published every 20 min. Additionally there are many commercial interests and more and more Dietary Supplements Companies claim to have found the fountain of youth to sell their products. Finally there are news outlets publishing stories related to this topic but without providing new or fundamented information.

Thus a quick Broswer or ChatGPT search does not give good results, an automated system that retrieves and analyzes scientific articles on human longevity and extracts relevant insights using NLP is of great help for the people interested.

## **Goal**

Extract the latest reliable scientific findings to extend human healthspan, using Natural Language Processing (NLP) models, Artificial Intelligence or any other ML methods. Extract meaningful relationships between specific kewywords, approved drugs, and interventions and filter the results from Noise and unfounded or commercial interest.​ Finaly present for Public access in the Web.

---

## Project Structure

This repo was based in a Template provided by the neuefische school and pool for digital talent as part of the capstone project for the cohort of Jan-Apr /2025

It's main parts are: 

 - [Proof of Concept](Proof_of_concept.md)
 - Milestones are presented in two forms:
   - As a list in a [markdown](Milestones.md) file
   - As a table in a [csv](Milestones.csv) file
 - [Project folders](Project_folders)
 This are the main files and it follows the milestones structure
 - [images](images) (self explanatory)
 - [modeling](modeling) (provided with the template), includes python working files
 - [models](models) (provided with the template)
 - [notebooks](notebooks) (provided with the template)

---

## Requirements:

- pyenv with Python: 3.11.3

## Environment

Use the requirements file to create a new environment for this task. 

```BASH
make setup

#or

pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### **`WindowsOS`** type the following commands :

- Install the virtual environment and the required packages by following commands.

    For `PowerShell` CLI :

    ```PowerShell
    pyenv local 3.11.3
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

    For `Git-Bash` CLI :
    ```
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/Scripts/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
--- 

## ds-modeling-pipeline

Here you find a Skeleton project for building a simple model in a python script or notebook and log the results on MLFlow.

There are two ways to do it: 
* In Jupyter Notebooks:
    We train a simple model in the [jupyter notebook](notebooks/EDA-and-modeling.ipynb), where we select only some features and do minimal cleaning. The hyperparameters of feature engineering and modeling will be logged with MLflow

* With Python scripts:
    The [main script](modeling/train.py) will go through exactly the same process as the jupyter notebook and also log the hyperparameters with MLflow

Data used is the [coffee quality dataset](https://github.com/jldbc/coffee-quality-database).

--- 

The `requirements.txt` file contains the libraries needed for deployment.. of model or dashboard .. thus no jupyter or other libs used during development.

The MLFLOW URI should **not be stored on git**, you have two options, to save it locally in the `.mlflow_uri` file:

```BASH
echo http://127.0.0.1:5000/ > .mlflow_uri
```

This will create a local file where the uri is stored which will not be added on github (`.mlflow_uri` is in the `.gitignore` file). Alternatively you can export it as an environment variable with

```bash
export MLFLOW_URI=http://127.0.0.1:5000/
```

This links to your local mlflow, if you want to use a different one, then change the set uri.

The code in the [config.py](modeling/config.py) will try to read it locally and if the file doesn't exist will look in the env var.. IF that is not set the URI will be empty in your code.

## Usage

### Creating an MLFlow experiment

You can do it via the GUI or via [command line](https://www.mlflow.org/docs/latest/tracking.html#managing-experiments-and-runs-with-the-tracking-service-api) if you use the local mlflow:

```bash
mlflow experiments create --experiment-name 0-template-ds-modeling
```

Check your local mlflow

```bash
mlflow ui
```

and open the link [http://127.0.0.1:5000](http://127.0.0.1:5000)

This will throw an error if the experiment already exists. **Save the experiment name in the [config file](modeling/config.py).**

In order to train the model and store test data in the data folder and the model in models run:

```bash
#activate env
source .venv/bin/activate

python -m modeling.train
```

In order to test that predict works on a test set you created run:

```bash
python modeling/predict.py models/linear data/X_test.csv data/y_test.csv
```

## About MLFLOW -- delete this when using the template

MLFlow is a tool for tracking ML experiments. You can run it locally or remotely. It stores all the information about experiments in a database.
And you can see the overview via the GUI or access it via APIs. Sending data to mlflow is done via APIs. And with mlflow you can also store models on S3 where you version them and tag them as production for serving them in production.
![mlflow workflow](images/0_general_tracking_mlflow.png)

### MLFlow GUI

You can group model trainings in experiments. The granularity of what an experiment is up to your usecase. Recommended is to have an experiment per data product, as for all the runs in an experiment you can compare the results.
![gui](images/1_gui.png)

### Code to send data to MLFlow

In order to send data about your model you need to set the connection information, via the tracking uri and also the experiment name (otherwise the default one is used). One run represents a model, and all the rest is metadata. For example if you want to save train MSE, test MSE and validation MSE you need to name them as 3 different metrics.
If you are doing CV you can set the tracking as nested.
![mlflow code](images/2_code.png)

### MLFlow metadata

There is no constraint between runs to have the same metadata tracked. I.e. for one run you can track different tags, different metrics, and different parameters (in cv some parameters might not exist for some runs so this .. makes sense to be flexible).

- tags can be anything you want.. like if you do CV you might want to tag the best model as "best"
- params are perfect for hypermeters and also for information about the data pipeline you use, if you scaling vs normalization and so on
- metrics.. should be numeric values as these can get plotted

![mlflow metadata](images/3_metadata.png)
