# Android RAG Starter 🚀

A minimal project demonstrating Retrieval-Augmented Generation (RAG) flow in Android apps.

## 🧠 Architecture

Android App → Backend → Retrieve Context → Generate Answer → UI

## 📱 Tech Stack

- Kotlin + Jetpack Compose
- MVVM Architecture
- Retrofit
- Python Flask Backend
- Simple RAG (keyword-based retrieval)

## ✨ Features

- Ask question from Android app
- Backend retrieves relevant data
- Generates contextual response
- Displays matched context

## 🚀 Future Improvements

- Add OpenAI LLM integration
- Replace keyword search with embeddings
- Integrate Pinecone / Weaviate
- Add Hilt DI

## 📸 Demo

(Add screenshot here)

## 🛠️ Run Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
