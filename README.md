# AI Log Analyzer

![CI](https://github.com/SiverCookie/ai-log-analyzer/actions/workflows/python-tests.yml/badge.svg)

A lightweight, production-ready Python project that analyzes log files, extracts errors, and generates intelligent suggestions using an AI model.
If the AI API is unavailable (quota exceeded / no key), the system automatically falls back to a local analysis engine.

---

## 🚀 Features

- Read any `.log` file and automatically extract errors  
- AI-powered debugging suggestions  
- Automatic offline fallback (no crash if API fails)  
- Fully tested with `pytest`  
- GitHub Actions CI included  
- Modular, clean architecture  
- Beginner-friendly but industry-standard structure  

---

## 📁 Project Structure

ai-log-analyzer/
│
├── src/
│   ├── analyzer.py
│   ├── log_reader.py
│   ├── ai_suggester.py
│   └── __init__.py
│
├── tests/
│   ├── test_log_reader.py
│   ├── test_analyzer.py
│   ├── test_ai_suggester_mocked.py
│   └── __init__.py
│
├── logs/
│   └── sample.log
│
├── .github/
│   └── workflows/
│       └── python-tests.yml
│
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
└── README.md

---

## 🔧 Installation

### 1. Clone repository

git clone https://github.com/YOUR_USERNAME/ai-log-analyzer.git  
cd ai-log-analyzer

### 2. Install dependencies

pip install -r requirements.txt

### 3. Create `.env` file

Copy `.env.example` → `.env` and edit:

OPENAI_API_KEY=your_key_here  
MODEL=gpt-4o-mini

If you do not have an API key, the analyzer will use **offline fallback mode**.

---

## ▶️ Running the Project

python main.py --file logs/sample.log

Expected output:

🔍 Reading log file: logs/sample.log

📌 Extracted errors:
  - [ERROR] Failed to connect to database.
  - [CRITICAL] System temperature too high.

🤖 AI Suggestions:
⚠️ AI unavailable — using fallback engine.
Possible causes:
- Database connection issue. Check credentials or server availability.
- Critical error detected. Inspect system resources or hardware.

General steps:
- Check recent config changes.
- Inspect logs around the error timestamp.
- Reproduce issue in a controlled environment.

---

## 🧪 Running Tests

pytest

---

## 🛠 Tech Stack

- Python 3.10+
- Pytest
- GitHub Actions
- Regex-based parsing
- OpenAI API (optional)
- python-dotenv

---

## 🤖 How the AI Fallback Works

If the API key is missing or the API returns any error (`quota`, `RateLimitError`, `APIError`, etc.):

- the system switches to a heuristic-based analysis  
- does not crash  
- still produces meaningful suggestions  

This ensures reliability — just like in enterprise environments.

---

## 🧩 Skills Demonstrated

This project demonstrates:

- Clean Python architecture  
- Writing modular, testable code  
- API integration with fail-safe logic  
- Test mocking  
- CI / CD pipeline  
- CLI application design  
- Log parsing / regex  
- Professional-level README and project setup  

---

## ❤️ Author

Built by SiverCookie, showcasing Python automation + AI integration skills.

---
