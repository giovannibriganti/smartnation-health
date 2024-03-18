# Instructions to run the application on Mac

# Author Details
Author: Abhishek Sakhuja
Organisation: NTT Data
Date: 13th March 2024
Location: BE

## 1. Install MongoDB

```bash
brew tap mongodb/brew
brew update
brew install mongodb-community@7.0
brew install --cask mongodb-compass
brew services start mongodb-community@7.0
brew services stop mongodb-community@7.0
```

### To run mongod manually as a background process using a config file, run

```bash
mongod --config /opt/homebrew/etc/mongod.conf --fork
```

### Start mongoDB server

```bash
uvicorn nosql.app.app.main:app
```

## 2. Web UI

### Start web ui to upload documents

```bash
streamlit run frontend/ui_feed_db.py
```

### Start web ui for chat interface

```bash
streamlit run frontend/ui_chat_db.py
```

## 3. Change the model for Mistral

### Add support for Mistral, OpenAI and AzureOpenAI

Download mistral 7B model or other model: `mistral-7b-instruct-v0.1.Q4_K_M.gguf`
Change the model_file parameter in `src/rag_loader.py` to the model

## 4. Install the requirements on your machine

```bash
pip install -r requirements.txt
```
