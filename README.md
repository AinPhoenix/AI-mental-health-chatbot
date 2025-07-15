# 🧠 Mental Health Support Chatbot (RAG + Ollama)

A private and personalized mental health chatbot built using:

- 🔍 **Retrieval-Augmented Generation** (RAG)
- 🧠 **Ollama (LLaMA 3)** for local LLM inference
- 📚 FAISS for document search
- 📄 PDF knowledge base
- 💬 Real-time **streaming** chat UI with Next.js + shadcn

---

## 📖 Table of Contents

1. [Demo](#-demo)
2. [Architecture](#-architecture)
3. [Features](#-features)
4. [Getting Started](#-getting-started)
   - [Backend (Python)](#backend-python)
   - [Frontend (Next.js)](#frontend-nextjs)

---

## 📸 Demo

> Add a GIF or screenshot of your app here.

![Demo Screenshot](image.png)

---

## 🧱 Architecture

```
User → Next.js Chat UI → Flask API
                            ↑ ↓
                            Stream Ollama + FAISS
```

This architecture ensures:
- A seamless user experience with a modern chat interface.
- Local inference and document retrieval for privacy and speed.

---

## 🔧 Features

- Upload and index PDF documents locally.
- Ask mental health questions (e.g., anxiety, insomnia).
- Responses are grounded in your uploaded documents.
- LLM runs locally via Ollama (no external API required).
- Fully private with real-time streaming output.

---

## 🚀 Getting Started

### Backend (Python)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   python app.py
   ```

### Frontend (Next.js)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

> **Note:** Ollama must be running locally. Use the following command to start it:
> ```bash
> ollama run llama3
> ```

---