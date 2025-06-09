import json
import os
import tkinter as tk
from tkinter import filedialog
from gpt4all import GPT4All
import pandas as pd
from PIL import Image
import pytesseract

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("PyPDF2 not installed. Install with: pip install PyPDF2")
    exit()

def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf_file(file_path):
    text = []
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df.to_string(index=False)

def read_image_file(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def detect_title_or_topic(text: str) -> str:
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        if len(line.split()) > 3 and line[0].isupper():
            return line
    return "Untitled Document"

def local_model_summarize(text, model):
    prompt = (
        "You are an AI assistant summarizing documents for a knowledge base.\n"
        "Summarize the following content clearly in 5-7 sentences:\n\n"
        f"{text}\n\nSummary:"
    )
    response = model.generate(prompt, max_tokens=300)
    return response.strip()

def append_to_jsonl(jsonl_path, details, content):
    entry = {
        "details": details,
        "content": content
    }
    with open(jsonl_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title="Select one or more files to summarize",
        filetypes=[
            ("All supported", "*.txt *.pdf *.xlsx *.xls *.xlsm *.png *.jpg *.jpeg"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Excel files", "*.xlsx *.xls *.xlsm"),
            ("Image files", "*.png *.jpg *.jpeg"),
        ]
    )
    root.destroy()
    return list(file_paths)

if __name__ == "__main__":
    model_path = r"C:\Users\Allen York\Project\nomic.ai\GPT4All\Llama-3.2-1B-Instruct-Q4_0.gguf"
    jsonl_path = r"C:\Users\Allen York\Project\project_email_ai\data\knowledge_base.jsonl"

    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        exit()

    jsonl_folder = os.path.dirname(jsonl_path)
    if not os.path.exists(jsonl_folder):
        os.makedirs(jsonl_folder)

    print("Loading GPT4All model...")
    gpt4all_model = GPT4All(model_path)

    selected_files = select_files()
    if not selected_files:
        print("No files selected, exiting.")
        exit()

    for file_path in selected_files:
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == ".txt":
                raw_text = read_txt_file(file_path)
            elif ext == ".pdf":
                raw_text = read_pdf_file(file_path)
            elif ext in [".xlsx", ".xls", ".xlsm"]:
                raw_text = read_excel_file(file_path)
            elif ext in [".png", ".jpg", ".jpeg"]:
                raw_text = read_image_file(file_path)
            else:
                print(f"❌ Unsupported file type: {ext}")
                continue
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            continue

        title_or_topic = detect_title_or_topic(raw_text)

        print(f"\n🧠 Summarizing: {os.path.basename(file_path)} ...")
        summary = local_model_summarize(raw_text, gpt4all_model)

        details = f"Summary of {title_or_topic}"
        append_to_jsonl(jsonl_path, details, summary)

        print(f"✅ Appended summary for: {os.path.basename(file_path)}")

    print(f"\n🎉 All done! Summaries added to: {jsonl_path}")
