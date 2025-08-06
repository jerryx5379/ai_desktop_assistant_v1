# 🧠 AI Desktop Assistant (PySide + Gemma 3n via Ollama)

This PySide project is an AI desktop assistant powered by **Gemma 3n** via **Ollama**.

The assistant includes:
- 💬 A chatbot interface  
- 📄 Retrieval-augmented generation (RAG) using personal documents  
- 🎙️ Audio input and output  
- 🖥️ Operating system interactivity (e.g., toggling dark/light theme)

---

## 🚀 How to Run

### 🖥️ Hardware Requirements
- **OS:** Windows 11  
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
   git clone [<your-repo-url>](https://github.com/jerryx5379/ai_desktop_assistant_v1.git)
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

