import customtkinter as ctk
from tkinter import filedialog 
import os
from email_responder import ( generate_response, summarize_guest_email_and_context, )
from gpt4all import GPT4All

model_path = "C:\Users\g2943\AppData\Local\nomic.ai\GPT4All\Llama-3.2-1B-Instruct-Q4_0.gguf"


class EmailResponderGUI(ctk.CTk):
    def __init__(self): 
        super().__init__()
        self.title("AI Email Generator")
        self.geometry("900x600")

        self.gpt_model = GPT4All(model_name=model_path,
                                 allow_download= False)  # Adjust your model path/name here

        self.attached_files = []

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.input_tab = self.tabview.add("Guest Email Input")
        self.output_tab = self.tabview.add("AI Response Output")

        self.create_input_tab()
        self.create_output_tab()

def create_input_tab(self):
        self.first_name = ctk.CTkEntry(self.input_tab, placeholder_text="First Name")
        self.first_name.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.last_name = ctk.CTkEntry(self.input_tab, placeholder_text="Last Name")
        self.last_name.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.subject = ctk.CTkEntry(self.input_tab, placeholder_text="Email Subject")
        self.subject.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.body = ctk.CTkTextbox(self.input_tab, height=150)
        self.body.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.body.insert("0.0", "Body of the email...")

        self.concern = ctk.CTkEntry(self.input_tab, placeholder_text="Concern")
        self.concern.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.tone_combo = ctk.CTkComboBox(
            self.input_tab,
            values=["Formal", "Friendly", "Empathetic", "Apologetic"],
        )
        self.tone_combo.set("Select Tone")
        self.tone_combo.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    
        self.attach_button = ctk.CTkButton(
            self.input_tab, text="Attach Files", command=self.attach_files
        )
        self.attach_button.grid(row=5, column=0, padx=10, pady=10)
    
        self.attached_label = ctk.CTkLabel(self.input_tab, text="No files attached")
        self.attached_label.grid(row=5, column=1, padx=10, pady=10)
    
        self.generate_button = ctk.CTkButton(
            self.input_tab, text="Generate", command=self.generate_response_gui
        )
        self.generate_button.grid(row=6, column=0, padx=10, pady=10)
    
        self.regenerate_button = ctk.CTkButton(
            self.input_tab, text="Regenerate", command=self.generate_response_gui
        )
        self.regenerate_button.grid(row=6, column=1, padx=10, pady=10)
    
        self.input_tab.grid_rowconfigure(2, weight=1)
        self.input_tab.grid_columnconfigure((0, 1), weight=1)
 
def create_output_tab(self):
    self.generated_subject = ctk.CTkEntry(
        self.output_tab, placeholder_text="AI Reply Subject"
    )
    self.generated_subject.pack(padx=10, pady=10, fill="x")
 
    self.generated_body = ctk.CTkTextbox(self.output_tab)
    self.generated_body.pack(padx=10, pady=10, fill="both", expand=True)
 
def attach_files(self):
    file_paths = filedialog.askopenfilenames(
        title="Select Reference Documents",
        filetypes=[
            ("All Files", "*.*"),
            ("Text Files", "*.txt"),
            ("PDF Files", "*.pdf"),
            ("Word Documents", "*.docx"),
            ("Excel Files", "*.xlsx"),
        ]
    )
    self.attached_files = file_paths
    self.attached_label.configure(text=f"{len(file_paths)} file(s) attached")
 
def generate_response_gui(self):
    first = self.first_name.get()
    last = self.last_name.get()
    subject = self.subject.get()
    body_text = self.body.get("1.0", "end").strip()
    tone = self.tone_combo.get()
    concern = self.concern.get()
 
    # Summarize
    summary = summarize_guest_email_and_context(
        guest_body=body_text,
        attached_files=self.attached_files,
        input_tone=tone,
        input_concern=concern
    )
 
    # Generate response
    response = generate_response(
        gpt4all_instance=self.gpt_model,
        first_name=first,
        last_name=last,
        subject=subject,
        body=body_text,
        additional_prompt=summary
    )
 
    self.generated_subject.delete(0, "end")
    self.generated_subject.insert(0, f"RE: {subject}")
 
    self.generated_body.delete("1.0", "end")
    self.generated_body.insert("1.0", response)
if __name__ == "__main__": 
    app = EmailResponderGUI() 
    app.mainloop()