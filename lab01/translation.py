import requests
import tkinter as tk
from tkinter import messagebox

def translate_text(text, source_language, target_language, api_choice, google_headers, fast_translate_headers):
    """Translates text using the selected API (Google or Fast-Translate)."""
    if api_choice == 'Google Translate':
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        payload = {
            'q': text,
            'source': source_language,
            'target': target_language,
            'format': 'text'
        }
        headers = google_headers
    elif api_choice == 'Fast-Translate-API':
        url = "https://fast-translate-api1.p.rapidapi.com/translate"
        payload = {
            'from_lang': source_language,
            'to_lang': target_language,
            'text': text
        }
        headers = fast_translate_headers
    else:
        return {'error': 'Unsupported API selection'}

    try:
        if api_choice == 'Fast-Translate-API':
            response = requests.post(url, json=payload, headers=headers)
        else:
            response = requests.post(url, data=payload, headers=headers)

        print(f"Selected API: {api_choice}")
        print(f"URL: {url}")
        print(f"Payload: {payload}")
        print(f"Headers: {headers}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}


def process_text(text_input, result_text_input, source_language_selection, language_selection, translate_api_selection, google_headers, fast_translate_headers):
    """Handles the translation process and updates the result."""
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter or load some text.")
        return

    source_language = source_language_selection.get()
    target_language = language_selection.get()
    if source_language and target_language:
        selected_api = translate_api_selection.get()

        translation_result = translate_text(text, source_language, target_language, selected_api, google_headers, fast_translate_headers)

        # Handle errors in the translation process
        if 'error' in translation_result:
            messagebox.showerror("Translation Error", f"Error: {translation_result['error']}")
            print(f"Error: {translation_result['error']}")  # Print error to console
            return

        # Extract the translated text based on the selected API
        if selected_api == 'Google Translate':
            translated_text = translation_result.get('data', {}).get('translations', [{}])[0].get('translatedText', text)
        elif selected_api == 'Fast-Translate-API':
            translated_text = translation_result.get('result', text)
        else:
            translated_text = text

        print(f"Translated Text: {translated_text}")

        # Update the result text input with the translated text
        result_text_input.config(state=tk.NORMAL)  
        result_text_input.delete(1.0, tk.END)
        result_text_input.insert(tk.END, translated_text)
        result_text_input.config(state=tk.DISABLED)  
    else:
        result_text_input.config(state=tk.NORMAL)
        result_text_input.delete(1.0, tk.END)
        result_text_input.insert(tk.END, text)
        result_text_input.config(state=tk.DISABLED)
