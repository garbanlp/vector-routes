# Mnemosine app

App to store and retrieve your notes.

Stack used:
- [obsidian](https://obsidian.md) for create notes
- fastapi to run backend
- sentence-transformers to vectorize text
- qdrant to store vectors
- streamlit as a frontend

## Setup

```
poetry install
```
Once you have your obsidian notes, populate qdrant database using:

```
poetry run python populate_qdrant_db.py
```

## Run the app

Start your backend 
```
uvicorn main:app --reload
```

Start you frontend
```
streamlit run frontend.py
```