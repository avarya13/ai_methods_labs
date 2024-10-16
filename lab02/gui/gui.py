import tkinter as tk
from tkinter import scrolledtext
from model.model import TextGenerator

class TextGeneratorApp:
    def __init__(self, root):
        """Initialize the graphical interface of the application."""
        self.root = root
        self.root.title("Text Generation with ruGPT-3.x")
        
        # Set the window size
        self.root.geometry("600x500") 

        # Set background color
        self.root.configure(bg="#f0f0f0")

        # Initialize the text generator
        self.text_generator = TextGenerator()

        # Input label
        self.input_label = tk.Label(root, text="Enter text:", bg="#f0f0f0", font=("Arial", 12))
        self.input_label.pack(pady=(10, 5))  # Add vertical padding

        # Input text area
        self.input_text = tk.Text(root, height=8, width=70, font=("Arial", 12), wrap=tk.WORD)
        self.input_text.pack(pady=(0, 10))  # Add vertical padding

        # Generate button
        self.generate_button = tk.Button(root, text="Generate Text", command=self.generate_text, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.generate_button.pack(pady=(5, 10))  

        # Output label
        self.output_label = tk.Label(root, text="Generated text:", bg="#f0f0f0", font=("Arial", 12))
        self.output_label.pack(pady=(10, 5))  

        # Output text area
        self.output_text = scrolledtext.ScrolledText(root, height=15, width=70, font=("Arial", 12), wrap=tk.WORD)
        self.output_text.pack(pady=(0, 10))  

    def generate_text(self):
        """Generate text and display it in the output text field."""
        input_text = self.input_text.get("1.0", tk.END).strip()
        generated = self.text_generator.generate_text(input_text)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, generated)

def run_app():
    """Run the main loop of the application."""
    root = tk.Tk()
    app = TextGeneratorApp(root)
    root.mainloop()
