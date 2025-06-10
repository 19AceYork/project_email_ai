# 📧 Project Email AI

A Python-based Email Response Generator powered by LLMs. This tool reads guest emails, detects tone and concern, summarizes attachments, and auto-generates professional replies using GPT-4All or OpenAI API.

---

## ✨ Features

- ✅ Custom `customtkinter` GUI interface
- ✅ File summarization support (PDF, DOCX, TXT, Excel)
- ✅ Concern and tone detection
- ✅ Regenerate responses with custom tones
- ✅ Works offline with GPT4All or via OpenAI API

---

## 🧠 How It Works

1. Guest email (name, subject, body) is entered
2. Optional file attachments are summarized
3. Concern and tone are auto-detected or selected
4. Response is generated using a selected LLM
5. Response is shown and can be copied or emailed

---

## 🛠️ Requirements

- Python 3.8+
- customtkinter
- gpt4all
- openai (if using OpenAI API)
- pandas, docx, PyMuPDF, openpyxl

Install via:

```bash
pip install -r requirements.txt

Created by Allen York Viray. Powered by GPT4All + OpenAI.
