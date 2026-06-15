# AI Video Assistant

An AI-powered Video Question Answering System that allows users to upload a video file or provide a YouTube URL and ask questions about the video content.

## Features

* Upload local video/audio files
* Process YouTube video URLs
* Automatic speech-to-text transcription using Whisper
* Audio chunking for large videos
* Vector database storage using ChromaDB
* Semantic search with Sentence Transformers
* Retrieval-Augmented Generation (RAG)
* Question Answering using Mistral AI
* Streamlit-based user interface
* PDF export support

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & NLP

* OpenAI Whisper
* Sentence Transformers
* Mistral AI
* LangChain

### Vector Database

* ChromaDB

### Media Processing

* yt-dlp
* FFmpeg
* Pydub

## Project Workflow

1. User uploads a video file or provides a YouTube URL.
2. Audio is extracted from the video.
3. Whisper converts audio into text.
4. The transcript is divided into chunks.
5. Embeddings are generated using Sentence Transformers.
6. Embeddings are stored in ChromaDB.
7. User asks questions about the video.
8. Relevant chunks are retrieved using RAG.
9. Mistral AI generates accurate answers based on retrieved context.

## Installation

```bash
git clone <repository-url>
cd ai-video-assistant
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
MISTRAL_API_KEY=your_api_key
```

## Run Locally

```bash
streamlit run app.py
```

## Future Improvements

* Multi-language support
* Speaker identification
* Video summarization
* Meeting minutes generation
* Cloud deployment optimization

## Author

Kubra Siraj and Zoha kamil
BS Computer Science Student
AI & Data Science Enthusiast
