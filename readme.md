# 🧠 AI Desktop Assistant (PySide + Gemma 3n via Ollama)

This PySide project is an AI desktop assistant powered by **Gemma 3n** via **Ollama**.
📌 Submission to the **Gemma 3n Kaggle Competition**  
📽️ [Video Demo](https://www.youtube.com/watch?v=z-EgM4D8SoM)

The assistant includes:
- 💬 A chatbot interface  
- 📄 Retrieval-augmented generation (RAG) using personal documents  
- 🎙️ Audio input and output  
- 🖥️ Operating system interactivity (e.g., toggling dark/light theme)

---

## 💡 Inspiration

Many people lack easy access to advanced tools like **RAG architectures** for their personal documents.  
This gap especially affects students struggling with dense textbooks and professionals managing complex legal files.

Another motivation behind this project is the **limited interaction between smart language models and personal computers**.  
Imagine if LLMs could directly access and control your computer — you could simply prompt,  
“Do my homework,” and the application would handle file management, research, and submission automatically.  

Currently, users must manually upload files and perform tasks step-by-step, which is inefficient and disconnected from true AI assistance.

---

## 🚀 How to Run

### 🖥️ Hardware Requirements
- **OS:** Windows 11 (python 3.12.8)
- **RAM:** 16 GB (uses ~8 GB during runtime)

---

### 📦 Setup Instructions

1. **Install Ollama**  
   👉 [Download Ollama](https://ollama.com/download)

2. **In Git Bash**, run the following:
   ```bash
   ollama pull gemma3n:e2b
   ollama run gemma3n:e2b
   ollama serve
   ```

3. **Clone this repository**
   ```bash
   git clone https://github.com/jerryx5379/ai_desktop_assistant_v1.git
   cd <project-folder>
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download AI models** (audio-to-text, vector embeddings, TTS, etc.)
   ```bash
   python download_models.py
   ```

6. **Start the assistant**
   ```bash
   python main.py
   ```
---

## 📘 Technical Writeup

### 📁 Project Structure

```
├── assets/         # Icons, fonts, and images
├── core/           # Core functions and OS interactions
├── logic/          # Chat window logic and widget controllers
├── rag_window/     # RAG file window with its own UI and embedding pipeline
├── style/          # Application-wide QSS styles
├── threads/        # Threaded functions to avoid UI blocking
├── user_data/      # Stores user-generated data (e.g., embeddings)
├── util/           # Utility functions and classes
├── widgets/        # Chat window components and UI widgets
├── app.py          # Creates QApplication, applies styles/icons
└── main.py         # Runs the app and starts the event loop
```

---

### ⚙️ Functionality

#### 💬 Regular Chatting
Messages are sent to the **Gemma 3n** model with the context of the previous 2 messages to reduce inference time (prompt size scales linearly with latency).

---

#### 📄 RAG Architecture (`rag_window/`)
- Embedding model: `msmarco-MiniLM-L6-cos-v5` (384d, Sentence Transformers)
- Workflow:
  1. Accepts PDFs from user.
  2. Parses with **PyMuPDF** and splits on `\n\n` (paragraphs).
  3. Generates text chunks → embeds them → saves as `.npy` files.
  4. Constructs:
     - `embeddings.npy`
     - `index.faiss`
     - `text_chunks.npy`
  5. On inference, retrieves top-k chunks and adds to prompt as context.

---

#### 🖥️ OS Interaction (`os_button`)
- Allows the assistant to control the OS.
- Currently supports **toggling dark/light mode** using Python’s `subprocess`.
- Custom prompt sent to gemma3n which responds with structured **JSON object**, which map to predefined functions.

---

#### 🎙️ Microphone Input
- Uses **`faster_whisper` (base)** to transcribe voice input.
- Detects end of speech based on ongoing sound level variables
- Transcribed text is automatically sent to the chat window.

---

#### 🔊 Speaker Output
- Converts responses to speech using **coqui-tts**:  
  `tts_models/en/ljspeech/tacotron2-DDC`
- Audio is played automatically after the response is generated.

---

#### 💡 Conversation Mode
- Toggles a concise mode by changing system instructions sent to the model.

---

## ⚠️ Challenges

- A major challenge was creating the **basic chatbox UI**.  
  Formatting the chat bubbles was difficult due to the many widgets that needed to be controlled.  
  The current solution calculates the chatbox height dynamically based on the chat bubble heights,  
  but this approach could likely be improved for better performance and maintainability.

- Another major challenge was designing the **RAG pipeline**.  
  The multi-step process—from file preprocessing, parsing, to generating embeddings and merging them—  
  was complex and required careful orchestration to work smoothly.

---

## 🛠️ Improvements & Future Work

- **RAG Parsing:**  
  Replace paragraph splitting with DL-based text chunking for better semantic understanding.
  
- **OS Interaction:**  
  Extend to **mouse/keyboard control**. Enables richer interactions but raises security concerns.

- **Speaker Optimization:**  
  Analyze and synthesize **sentence-by-sentence** to improve latency.  
  Optionally move TTS to the cloud (tradeoff: local privacy vs speed).

- **Microphone Optimization:**  
  Cloud-based transcription could reduce local compute load.

- **General Usability:**  
  - Persist conversations  
  - File-based embedding database

---

## 📚 What I Learned

- My **first PySide project**: learned about widgets, layouts, signals/slots, threading, and UI modularity.
- Gained insight into the **feasibility of local LLMs**: performance, tradeoffs, and architecture.
- Developed practical knowledge of **RAG**, audio models, and OS automation with AI.


