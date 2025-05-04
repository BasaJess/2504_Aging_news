## ![](/images/pexels-googledeepmind-17484975.jpg) 

# 2504_Science_Youth
UPDATE LATEST SCIENTIFIC FINDINGS IN YOUTH EXTENSION

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

Extract the latest reliable scientific findings to extend human healthspan, using Natural Language Processing (NLP) models or any other ML methods. Extract meaningful relationships between specific kewywords, approved drugs, and interventions and filter the results from Noise and unfounded or commercial interest.​ Finaly present for Public access in the Web.

---

## Project Structure

This repo was based in a Template provided by the neuefische school and pool for digital talent as part of the capstone project for the cohort of Jan-Apr /2025

It's main parts are: 

 - [Proof of Concept](Proof_of_concept.md)
 - Milestones: As this is already a completed project on the maintenance phase, the Milestiones document are only for rerefence, they are not updated or maintained. They were presented in two forms:
   - As a list in a [markdown](Milestones.md) file
   - As a table in a [csv](Milestones.csv) file
 - [Project folders](Project_folders)
 These are the files following the milestones structure and can be used to understand the project structure
 - [scripts](scripts) (main code files)
 - [notebooks](notebooks) (used for testing code snipets)
 - [streamlit](.streamlit) (The streamlit app files)
 - [data](data) (due to the size the data are not uploaded to GitHub) 
 - [images](images) (self explanatory)
 - [modeling](modeling) (provided with the template, not used currently)
 - [models](models) (provided with the template, not used currently)


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

The `requirements.txt` and `requirements_dev.txt` files contain the libraries needed for deployment.

