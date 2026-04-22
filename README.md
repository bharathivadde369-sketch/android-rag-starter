# Android RAG Starter

A minimal starter project demonstrating a simple Retrieval-Augmented Generation (RAG) flow for Android apps.

## Architecture

Android App → Backend API → Retrieve Context → Generate Answer → Response to UI

## Tech Stack

- Android: Kotlin, Jetpack Compose, ViewModel, Retrofit
- Backend: Python, Flask
- Retrieval: Simple keyword-based matching
- Next step: Embeddings + Vector DB

## Why this project?

This project is a lightweight prototype to validate the end-to-end RAG flow before moving to more advanced retrieval approaches like embeddings and vector databases.

## Features

- Ask a question from Android UI
- Send query to backend
- Retrieve relevant knowledge
- Return grounded answer
- Display matched context in app

## Future Improvements

- Integrate OpenAI or other LLM APIs
- Replace keyword search with embeddings
- Add Pinecone / Weaviate vector DB
- Add Hilt dependency injection
- Add loading/error design improvements

## Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Run Android App

1. Open `android-app` in Android Studio
2. Start backend locally on port 5000
3. Run app on emulator
4. Use `10.0.2.2` as backend host for Android emulator

## Sample Questions

- What is Android lifecycle?
- What is Jetpack Compose?
- Explain MVVM
