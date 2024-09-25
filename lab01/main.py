import tkinter as tk
from tkinter import scrolledtext, ttk
from file_utils import load_file
from translation import process_text
from env_setup import load_environment

# Load environment variables
google_headers, fast_translate_headers = load_environment()


# Set up the GUI
def swap_languages():
    """Swaps the selected source and target languages in the comboboxes."""
    source_language = source_language_selection.get()
    target_language = language_selection.get()
    source_language_selection.set(target_language)
    language_selection.set(source_language)


# GUI setup
font_style = ("Arial", 14) 
background_color = "#F0F2F5"  
button_color = "#007bff"
button_text_color = "#ffffff"
entry_font = ("Arial", 14)
dropdown_font = ("Arial", 14)

root = tk.Tk()
root.title("Translation App")
root.state('zoomed')  
root.configure(bg=background_color)

tk.Label(root, text="Введите или загрузите текст:", font=font_style, bg=background_color).grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="n")

tk.Button(root, text="Загрузить файл", command=lambda: load_file(text_input), font=font_style, bg=button_color, fg=button_text_color).grid(row=1, column=0, padx=10, pady=5, sticky="w")

text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10, font=entry_font, bg="#ffffff", fg="#000000")
text_input.grid(row=1, column=1, padx=10, pady=5, columnspan=2, sticky="ew")

tk.Label(root, text="Выбор языка:", font=font_style, bg=background_color).grid(row=2, column=0, padx=10, pady=5, sticky="w")
source_language_selection = ttk.Combobox(root, values=['en', 'ru'], font=dropdown_font, state='readonly')  
source_language_selection.grid(row=2, column=1, padx=10, pady=5, sticky="w")
source_language_selection.set('en')  

tk.Button(root, text="Изменить порядок языков", command=swap_languages, font=font_style, bg=button_color, fg=button_text_color).grid(row=2, column=2, padx=10, pady=5, sticky="w")

tk.Label(root, text="Выбор языка для перевода:", font=font_style, bg=background_color).grid(row=3, column=0, padx=10, pady=5, sticky="w")
language_selection = ttk.Combobox(root, values=['en', 'ru'], font=dropdown_font, state='readonly')  
language_selection.grid(row=3, column=1, padx=10, pady=5, sticky="w")
language_selection.set('ru') 

tk.Label(root, text="Выбор API для перевода:", font=font_style, bg=background_color).grid(row=4, column=0, padx=10, pady=5, sticky="w")
translate_api_selection = ttk.Combobox(root, values=['Google Translate', 'Fast-Translate-API'], font=dropdown_font, state='readonly')  # Добавлена Fast-Translate-API
translate_api_selection.grid(row=4, column=1, padx=10, pady=5, sticky="w")
translate_api_selection.set('Google Translate')  

tk.Button(root, text="Перевести текст", command=lambda: process_text(
    text_input=text_input, 
    result_text_input=result_text_input, 
    source_language_selection=source_language_selection, 
    language_selection=language_selection, 
    translate_api_selection=translate_api_selection, 
    google_headers=google_headers, 
    fast_translate_headers=fast_translate_headers), 
    font=font_style, bg=button_color, fg=button_text_color).grid(row=4, column=2, padx=10, pady=5, sticky="w")

tk.Label(root, text="Результат перевода:", font=font_style, bg=background_color).grid(row=5, column=0, padx=10, pady=5, columnspan=3, sticky="w")

result_text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=10, font=entry_font, bg="#ffffff", fg="#000000", state=tk.DISABLED)
result_text_input.grid(row=6, column=0, padx=10, pady=5, columnspan=3, sticky="ew")

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(6, weight=1)  

root.mainloop()
