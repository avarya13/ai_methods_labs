from tkinter import filedialog, messagebox

def load_file(text_input):
    """Loads text from a file into the input field."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                text_input.config(state='normal')
                text_input.delete(1.0, "end")
                text_input.insert("end", text)
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading file: {e}")
