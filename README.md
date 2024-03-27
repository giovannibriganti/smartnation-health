# Author
_Author: Abhishek Sakhuja / Hector Lopez Perez_

_Organisation: NTT Data_

_Date: 12 to 14th March 2024_

_Location: BE_


# EaseMed
The solution presented here shows a proof of concept of how to use the high capacity of LLMs to convert (unstructured) medical texts into structured data, increasing the usefulness of this data for further research and management tasks. To accomplish this, two Retrieval-Augmented Generation (RAG) pipelines have been implemented, the first one aiming to extract key fields from the text document, saving each patient's record in MongoDB. Once this has been achieved, the second pipeline is in charge of feeding this information to a chat in which a doctor can consult the patient's information by simply using natural language.

This repository contains the necessary code as well as other dependencies to run the EaseMed application.
In this guide we will detail the different considerations and steps necessary to reproduce the final environment of the application.


## 1. Instructions to run the application

### Install the requirements on your machine

For this development, python version 3.10 was used.

### Create a python virtual environment and activate it(Optional)
```bash
python -m venv <environment name>
.\<environment name>\Scripts\activate (windows)
.\<environment name>\bin\activate (linux)
pip install -r requirements.txt
```

## 2. Install MongoDB:

### Mac/Linux
```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0
brew install --cask mongodb-compass
brew services start mongodb-community@7.0
brew services stop mongodb-community@7.0
```

### To run mongod manually as a background process using a config file, run:
```bash
mongod --config /opt/homebrew/etc/mongod.conf --fork
```

### Start mongoDB server:
```bash
uvicorn nosql.app.app.main:app
```

### Windows:
Download MongoDB Community Edition from [MongoDB Community](https://www.mongodb.com/try/download/community).

## 3. Populate ChromaDB for Snomed data.

Due to the need to carry out a purely local deployment of the solution, Chroma DB on-premises was the choice of vector data base. To load the Snomed data into this database, from the root directory of this project we will have to execute the following command (bash/cmd):
```bash
python  ./tmp/data_cleaning.py
```
For demo purposes only a subset of records/terms are processed and their embeddings stored.

## 4. Select LLM model 
### Added support for Mistral, OpenAI and AzureOpenAI
For testing purposes, also OpenAI (gpt3.5 turbo) and AzureOpenAI LLM support is implemented. To use this option, the corresponding API Key (only the key) has to be placed in a ```.secrets/azureopenapikey``` or ```.secrets/openapikey```

For dynamic control of the environment, configuration variables that modify parts of the architecture are found in the configuration file in ```pipeline_meta/prompt_meta.yaml```. From this file we can specify the LLM to be used in the application, the options being:

* OpenAI
* AzureOpenAI
* Mistral7B

If support for another model wants to be implemented, this option must be added in the load_llm function, which is located in ``` src/services/rag_loader.py ```

### Use local mistral 
Download mistral 7B model or other model: ```mistral-7b-instruct-v0.1.Q4_K_M.gguf```
Change the model_file parameter in ```src/services/rag_loader.py``` to the model

## 5. Web UI:
### Start web ui to upload documents
```bash
streamlit run frontend/ui_feed_db.py
```

### Start web ui for chat interface
```bash
streamlit run frontend/ui_chat_db.py
```
