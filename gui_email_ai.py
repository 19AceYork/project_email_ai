import customtkinter as ctk
from tkinter import filedialog

class EmailResponseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Email Generator")
        self.geometry("900x900")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.attached_files = []
        self.database_file = "database.txt"

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.input_tab = self.tabview.add("Guest Email Input")
        self.output_tab = self.tabview.add("AI Response Output")

        self.create_input_tab()
        self.create_output_tab()

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("light")
            self.theme_switch.configure(text="Dark Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_switch.configure(text="Light Mode")

    def create_input_tab(self):
    # Make grid layout responsive
        for i in range(9):  # number of rows
            self.input_tab.grid_rowconfigure(i, weight=1)
            self.input_tab.grid_columnconfigure((0, 1), weight=1)

    # Theme toggle switch
        self.theme_switch = ctk.CTkSwitch(
        self.input_tab, text="Light Mode", command=self.toggle_theme
        )
        self.theme_switch.deselect()  # Start in dark mode
        self.theme_switch.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.first_name = ctk.CTkEntry(self.input_tab, placeholder_text="First Name")
        self.first_name.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.last_name = ctk.CTkEntry(self.input_tab, placeholder_text="Last Name")
        self.last_name.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.subject = ctk.CTkEntry(self.input_tab, placeholder_text="Email Subject")
        self.subject.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.body = ctk.CTkTextbox(self.input_tab, height=200)  # Increased height
        self.input_tab.grid_rowconfigure(3, weight=2)  # Give more weight to body row
        self.body.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.body.insert("0.0", "Body of the email...")

        self.concern = ctk.CTkEntry(self.input_tab, placeholder_text="Concern")
        self.concern.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.tone_combo = ctk.CTkComboBox(self.input_tab, values=["Formal", "Friendly", "Empathetic", "Apologetic"])
        self.tone_combo.set("Select Tone")
        self.tone_combo.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.role_combo = ctk.CTkComboBox(
        self.input_tab,
        values=["Customer Service", "Loyalty Agent", "Customer Relations", "Resolutions Agent"]
        )
        self.role_combo.set("Select Role")
        self.role_combo.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.attach_button = ctk.CTkButton(self.input_tab, text="Attach Files", command=self.attach_files)
        self.attach_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

        self.generate_button = ctk.CTkButton(self.input_tab, text="Generate", command=self.generate_response)
        self.generate_button.grid(row=7, column=1, padx=10, pady=10, sticky="ew")

        self.regenerate_button = ctk.CTkButton(self.input_tab, text="Regenerate", command=self.generate_response)
        self.regenerate_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.attach_label = ctk.CTkLabel(self.input_tab, text="No files attached.")
        self.attach_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    def create_output_tab(self):
        self.output_tab.grid_rowconfigure(1, weight=1)
        self.output_tab.grid_columnconfigure(0, weight=1)

        self.generated_subject = ctk.CTkEntry(self.output_tab, placeholder_text="AI Reply Subject")
        self.generated_subject.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.generated_body = ctk.CTkTextbox(self.output_tab)
        self.generated_body.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def attach_files(self):
        files = filedialog.askopenfilenames(title="Select Files")
        if files:
            self.attached_files = files
            self.attach_label.configure(text=f"{len(files)} file(s) attached.")

    def generate_response(self):
            self.generated_body.delete("1.0", "end")
            self.generated_body.insert("end", "[Generated response will appear here...]")
if __name__ == "__main__":
    app = EmailResponseApp()
    app.mainloop()
