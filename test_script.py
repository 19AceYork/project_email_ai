import os
import sys
import datetime
import PyPDF2
import docx
import pandas as pd
from gpt4all import GPT4All
 
# ========== Configuration ==========
model_dir = r"C:\Users\g2943\AppData\Local\nomic.ai\GPT4All"
model_file = "Llama-3.2-1B-Instruct-Q4_0.gguf"
device = None  # or 'cpu' or 'gpu' if supported
 
input_excel = r"C:\GPTResponder\guest.xlsx"
output_excel = r"C:\GPTResponder\output_guest.xlsx"
sheet_name = "Sheet1"
 
output_subject_col = "AI_Reply_Subject"
output_body_col = "AI_Reply_Body"
error_log = r"C:\GPTResponder\Errors\test_error_log.txt"
 
# ========== Functions ==========
 
def read_guest_emails(excel_file: str, sheet_name: str = None):
    """Read guest emails from Excel."""
    return pd.read_excel(excel_file, sheet_name=sheet_name)
 
def write_responses_to_excel(df, excel_file: str, sheet_name: str = None):
    """Save the updated DataFrame to Excel."""
    with pd.ExcelWriter(excel_file, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name or 'Sheet1')
 
def generate_response(gpt4all_instance, first_name: str, last_name: str, subject: str, body: str, rag_context: str = "", additional_prompt: str ="") -> str:
    """Use GPT4All to generate a polite and helpful response."""
    prompt = (
        "You are a professional, empathetic cruise line guest relations specialist"
        "You respond clearly, politely, and with care, using advanced English at a C1 proficiency level.\n\n"
        "If the guest's concern involves calculation, refund, or policies, think through the issue step by step, "
        "then summarize the final answer in a polished reply. \n\n"
        f"Guest Name: {first_name} {last_name}\n"
        f"Subject: {subject}\n"
        f"Body of the Guest's Email:\n{body}\n"
        
    )
    if additional_prompt:
        prompt += f"\nImportant background about this case:\n{additional_prompt.strip()}\n"
    
    if rag_context:
        prompt += f"\nBackground documents relevant to this case:\n{rag_context[:3000]}\n"
        
    prompt +=(
            "\nCompose a well-structured C1-level English reply addressing the guest by their first name."
            "Always sound professional, empathetic, and solution-oriented. Avoid generic phrasing. Closed with reassurance or gratitude.\n"
            "If the guest's request cannot be fully granted, avoid saying 'we cannot' directly. "
            "Instead, suggest alternative options in a positive way. For example:\n"
            "- Instead of 'we don't have your preferred stateroom' say 'we can offer you an ocean view balcony as an alternative'.\n"
            "- Instead of 'you are subject to a penalty' say 'we can waive the change fee if you switch to a different sailing date'.\n"
            "Always focus on what *can* be done.\n"
            "Close the message with reassurance or appreciation. \n\n"
            "Reply:\n"
        )
        
    response = gpt4all_instance.generate(
        prompt,
        max_tokens=512,
        temp=0.7,
        top_k=40,
        top_p=0.9,
        repeat_penalty=1.1,
        streaming=False,
    )
 
    return "".join(response) if hasattr(response, '__iter__') else str(response)
    

 
def load_rag_documents(base_folder, concern_keyword):
    concern_folder = os.path.join(base_folder, concern_keyword)
    combined_text =""
    
    if not os.path.exists(concern_folder):
        print(f"Concern folder not found: {concern_folder}")
        return combined_text
    
    for file in os.listdir(concern_folder):
        file_path = os.path.join(concern_folder, file)
        try:
            if file.lower().endswith(".txt"):
                with open(file_path,"r", encoding="utf-8") as f:
                    combined_text += f.read() + "\n"
            elif file.lower().endswith(".pdf"):
                with open(file_path,"rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        combined_text += page.extract_text() + "\n"
            elif file.lower().endswith(".docx"):
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    combined_text += para.text + "\n"
        except Exception as e:
            print(f"Could not read file {file_path}: {e}")
            
    return combined_text.strip()
 
 
# ========== Main Workflow ==========
 
def main():
    try:
        print(f"Loading model '{model_file}' on device '{device or 'cpu'}' ...")
        gpt4all_instance = GPT4All(model_file, model_path=model_dir, device=device, allow_download=False)

        print(f"Reading guest emails from '{input_excel}' ...")
        df = read_guest_emails(input_excel, sheet_name)

        # Required columns check
        required_columns = ["First Name", "Last Name", "Email Subject", "Body"]
        for col in required_columns:
            if col not in df.columns:
                print(f"ERROR: Required column '{col}' not found in Excel.")
                sys.exit(1)

        # Initialize output columns
        df[output_subject_col] = ""
        df[output_body_col] = ""

        print(f"Processing {len(df)} guest emails...\n")

        with gpt4all_instance:
            rag_base_folder = f"C:\GPTResponder\RAG_DOCUMENTS"
            
            for i, row in df.iterrows():
                first_name = row["First Name"] if pd.notna(row["First Name"]) else ""
                last_name = row["Last Name"] if pd.notna(row["Last Name"]) else ""
                subject = row["Email Subject"] if pd.notna(row["Email Subject"]) else ""
                body = row["Body"] if pd.notna(row["Body"]) else ""
                concer = row["Concern"] if "Concern" in row and pd.notna(row["Concern"]) else ""
                
                additional_prompt = ""
                if "Additional Prompt" in df.columns:
                    additional_prompt = row["Additional Prompt"] if pd.notna(row["Additional Prompt"]) else ""
                
                print(f"[{i+1}] Generating response for: {subject[:40]}...")
                try:
                    rag_context = load_rag_documents(rag_base_folder, concer)
                    response_text = generate_response(
                        gpt4all_instance,
                        first_name,
                        last_name,
                        subject,
                        body,
                        rag_context,
                        additional_prompt
                    )
                    
                    reply_subject = "Re: " + subject if subject else "Response from the Support"
                    
                    df.at[i, output_subject_col] = reply_subject
                    df.at[i, output_body_col] = response_text.strip()

                except Exception as e:
                    print(f"  ERROR on row {i+1}: {e}")
                    df.at[i, output_subject_col] = "Error generating response"
                    df.at[i, output_body_col] = ""

        print(f"\nSaving responses to '{output_excel}' ...")
        write_responses_to_excel(df, output_excel, sheet_name)
        print("✅ Done. Responses saved.\n")

    except Exception as e:
        os.makedirs(os.path.dirname(error_log), exist_ok=True)
        with open(error_log, "a", encoding="utf-8") as f:
           f.write(f"[{datetime.datetime.now()}] {repr(e)}\n")
        print(f"\n❌ A fatal error occurred: {e}\nLogged to: {error_log}")

# ========== Run Script ==========
if __name__ == "__main__":
    main()