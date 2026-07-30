<h1 align="center">Enterprise AI Assistant 🤖</h1>

<p align="center">
  <strong>An intelligent RAG-powered chatbot for HR policies & IT support with 2FA, multi-language support, audio responses, and document export.</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#project-structure">Project Structure</a> •
  <a href="#security">Security</a> •
  <a href="#license">License</a>
</p>

---

## ✨ Features

| Category | Capabilities |
|----------|--------------|
| **🔐 Authentication** | User registration + login with password strength validation, **Two-Factor Authentication (2FA)** via email OTP (Outlook SMTP) |
| **📄 Document Processing** | PDF upload & text extraction (PyMuPDF), intelligent chunking (title/section/semantic), Pinecone vector indexing |
| **🧠 RAG Q&A** | Semantic search over indexed documents, Llama 3 8B Instruct (HuggingFace) for grounded answers, context-aware responses |
| **🌍 Multi-Language** | English, French, Spanish via Together AI (Llama 3 8B chat) |
| **🔊 Audio Responses** | Text-to-speech (gTTS) with downloadable MP3 for every answer |
| **📝 Conversation Export** | Auto-saves Q&A history, one-click **Word document (.docx) generation**, email delivery via Outlook SMTP |
| **🛡️ Content Moderation** | Bad-word filtering (400+ terms) on user queries |
| **💾 Persistence** | SQLite for user accounts, session state for conversation context |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Auth (2FA)  │  │ PDF Upload   │  │  Query + Language    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
└─────────┼─────────────────┼─────────────────────┼──────────────┘
          │                 │                     │
          ▼                 ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Core Python Modules                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  ragpart.py  │  │  translate.py│  │     email.py         │  │
│  │  • PDF parse │  │  • Together  │  │  • SMTP (Outlook)    │  │
│  │  • Chunking  │  │    AI trans  │  │  • Word doc gen      │  │
│  │  • Embeddings│  │  • gTTS TTS  │  │  • OTP delivery      │  │
│  │  • Pinecone  │  │              │  │  • Chat history      │  │
│  │  • Llama 3   │  │              │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │                 │                     │
          ▼                 ▼                     ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────────┐
│   Pinecone       │ │   Together AI    │ │   Outlook SMTP       │
│   (Vector DB)    │ │   (Translation)  │ │   (Email Delivery)   │
└──────────────────┘ └──────────────────┘ └──────────────────────┘
          │
          ▼
┌──────────────────┐
│   HuggingFace    │
│   (Llama 3 8B)   │
└──────────────────┘
```

**Data Flow:**
1. **Ingest**: User uploads PDFs → PyMuPDF extracts text → multi-strategy chunking → sentence-transformers embeddings → Pinecone upsert
2. **Query**: User question → embedding → Pinecone similarity search (top-k) → context + query → Llama 3 8B (HF) → answer
3. **Enhance**: Answer → Together AI (translate) → gTTS (audio) → Streamlit display + download
4. **Persist**: Q&A pairs → session state → on demand: python-docx → Word doc → SMTP email

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Pinecone account (free tier works)
- HuggingFace account + token (for Llama 3 8B)
- Together AI account + API key (for translation)
- Outlook/Office365 email for SMTP (or any SMTP provider)

### 1. Clone & Install
```bash
git clone https://github.com/pranavsurya77/Enterprise-AI-Assistant.git
cd Enterprise-AI-Assistant
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file (never commit this!):

```bash
# Pinecone
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=llama3

# HuggingFace (for Llama 3 8B Instruct)
HF_TOKEN=hf_your_huggingface_token

# Together AI (for translation)
TOGETHER_API_KEY=your_together_api_key

# SMTP (Outlook/Office365 example)
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your_email@outlook.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@outlook.com
```

> **⚠️ Security Note**: The current code has **hardcoded credentials** in `ragpart.py`, `translate.py`, `tokens.py`, `app_without_chat_history.py`, and `email.py`. **Replace them with environment variables before any real deployment.** See [Security](#security) section.

### 3. Run
```bash
# Main app (with chat history + Word doc export + email)
streamlit run email.py

# Alternative: simpler app without chat history persistence
streamlit run app_without_chat_history.py
```

Open `http://localhost:8501` in your browser.

---

## ⚙️ Configuration

### Pinecone Setup
1. Create a free account at [pinecone.io](https://pinecone.io)
2. Create an index: name `llama3`, dimension `384`, metric `cosine`, serverless (AWS, us-east-1)
3. Copy API key → `PINECONE_API_KEY`

### HuggingFace Setup
1. Create token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) with `read` access
2. Accept Llama 3 license at [meta-llama/Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)
3. Copy token → `HF_TOKEN`

### Together AI Setup
1. Sign up at [together.ai](https://together.ai) → get API key
2. Copy key → `TOGETHER_API_KEY`

### SMTP Setup (Outlook/Office365)
1. Enable 2FA on your Outlook account
2. Generate an **App Password**: Microsoft Account → Security → App passwords
3. Use that app password (not your login password) → `SMTP_PASSWORD`

---

## 📁 Project Structure

```
Enterprise-AI-Assistant/
├── app_without_chat_history.py   # Simpler app: auth + RAG + audio (no history/email)
├── email.py                      # Full app: auth + RAG + audio + history + Word export + email
├── ragpart.py                    # Core RAG pipeline: PDF parse, chunking, embeddings, Pinecone, Llama 3
├── translate.py                  # Translation (Together AI) + TTS (gTTS)
├── tokens.py                     # Token counting for Llama 3 (HF tokenizer)
├── bad_words.txt                 # Content moderation list (400+ terms)
├── requirements.txt              # Python dependencies
├── logo.jpg                      # App logo (sidebar/header)
├── 0__5f5jUjHU5whTiBs.webp       # Additional asset
├── HR Policy Manual 2023.pdf     # Sample HR policy document
├── IT Support Documents.pdf      # Sample IT support document
├── users.db                      # SQLite database (auto-created)
└── README.md                     # This file
```

### Module Responsibilities

| File | Purpose |
|------|---------|
| `ragpart.py` | **RAG engine**: PDF extraction (PyMuPDF), 3-tier chunking (title→section→semantic), sentence-transformers embeddings, Pinecone index management, Llama 3 8B inference via HF InferenceClient |
| `translate.py` | **Language & Audio**: Together AI chat completion for translation, gTTS for MP3 generation |
| `tokens.py` | **Token accounting**: Llama 3 tokenizer for prompt length management |
| `email.py` | **Full app**: 2FA auth (SQLite + OTP email), chat history, Word doc generation (python-docx), SMTP email delivery |
| `app_without_chat_history.py` | **Lite app**: Same auth + RAG + audio, no history persistence or email export |

---

## 🔐 Security

### ⚠️ Current Issues (Must Fix Before Production)

| Issue | Location | Fix |
|-------|----------|-----|
| **Hardcoded Pinecone API key** | `ragpart.py:15` | Use `os.getenv("PINECONE_API_KEY")` |
| **Hardcoded HF token** | `ragpart.py:167`, `tokens.py:7` | Use `os.getenv("HF_TOKEN")` |
| **Hardcoded Together AI key** | `translate.py:9` | Use `os.getenv("TOGETHER_API_KEY")` |
| **Hardcoded SMTP credentials** | `app_without_chat_history.py:52-53`, `email.py:82-83,107-108` | Use `os.getenv("SMTP_USER")`, `os.getenv("SMTP_PASSWORD")` |
| **SHA-256 password hashing** | `app_without_chat_history.py:31`, `email.py:39` | Use `bcrypt` or `argon2` (slow, salted) |
| **SQLite in plaintext** | `users.db` | Encrypt at rest or use managed DB |
| **No input sanitization** | Query handling | Add validation, rate limiting |
| **No HTTPS enforcement** | Streamlit | Deploy behind TLS proxy (nginx + certbot) |

### Recommended Hardening Checklist
- [ ] Move all secrets to `.env` + `python-dotenv`
- [ ] Replace SHA-256 with `bcrypt`/`argon2`
- [ ] Add request rate limiting (e.g., `slowapi`)
- [ ] Enable Pinecone API key rotation
- [ ] Use parameterized queries (already done ✅)
- [ ] Add CSP headers, secure cookies for session
- [ ] Run vulnerability scan: `pip-audit` / `bandit`

---

## 🧪 Testing the Sample Data

The repo includes two sample PDFs:
- `HR Policy Manual 2023.pdf` — HR policies, leave, benefits, conduct
- `IT Support Documents.pdf` — IT troubleshooting, access requests, security

Upload one or both via the sidebar → "Upload a PDF" → wait for indexing → ask questions like:
- "What is the annual leave policy?"
- "How do I request VPN access?"
- "What's the password reset procedure?"

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `sentence-transformers` | Embeddings (all-MiniLM-L6-v2, 384-dim) |
| `pinecone-client` | Vector database |
| `huggingface-hub` | Llama 3 8B Instruct inference |
| `together` | Translation via Together AI |
| `gTTS` | Text-to-speech |
| `PyMuPDF` | PDF text extraction |
| `python-docx` | Word document generation |
| `pandas` | Data handling (minor) |
| `pycryptodome` | Crypto utilities |
| `transformers` + `torch` | Tokenizer (Llama 3) |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

**Please ensure:**
- No hardcoded secrets in commits
- Code passes `bandit` and `pip-audit`
- New features include docstrings and type hints

---

## 👤 Author

**Pranav Surya R S**
- GitHub: [@pranavsurya77](https://github.com/pranavsurya77)
- Portfolio: [pranavportfolio-roan.vercel.app](https://pranavportfolio-roan.vercel.app)
- LinkedIn: [Pranav Surya](https://linkedin.com/in/Pranav Surya)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details (add one if missing).

---

## ⭐ Show Your Support

If this project helped you, give it a ⭐️ on GitHub — it helps others discover it!

---

<sub>Built for SIH / enterprise use cases. Not production-hardened — review the [Security](#security) section before deploying.</sub>