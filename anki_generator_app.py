## Requirement: pip install genanki
## To run script in terminal:
## python3 anki_generator_app.py


import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import genanki

def generate_deck():
    filename = filename_entry.get().strip()
    if not filename:
        messagebox.showerror("Missing Info", "Please enter a file name.")
        return

    json_path = json_file_path.get()
    if not json_path or not os.path.isfile(json_path):
        messagebox.showerror("Missing File", "Please select a valid JSON file.")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            verbs = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read JSON file:\n{e}")
        return

    # Create Anki model and deck
    model = genanki.Model(
        1607392320,
        'Spanish Irregular Preterite Model',
        fields=[{'name': 'Front'}, {'name': 'Back'}],
        templates=[{
            'name': 'Card Template',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',
        }],
    )

    deck = genanki.Deck(
        2059400111,
        f'Spanish - Irregular Verbs (Pretérito Indefinido)'
    )

    for v in verbs:
        front = f"Conjugate: {v['infinitive']} (pretérito indefinido)"
        back = f"""
<b>Infinitive:</b> {v['infinitive']} — {v['english']}<br><br>
<b>yo</b> {v['yo']}<br>
<b>tú</b> {v['tú']}<br>
<b>él/ella/usted</b> {v['él']}<br>
<b>nosotros</b> {v['nos']}<br>
<b>vosotros</b> {v['vos']}<br>
<b>ellos/ellas/ustedes</b> {v['ellos']}<br><br>
<b>Example:</b><br>
{v['es']}<br>
<i>{v['en']}</i>
"""
        note = genanki.Note(model=model, fields=[front, back])
        deck.add_note(note)

    # Save to Desktop
    output_path = os.path.expanduser(f"~/Desktop/{filename}.apkg")
    try:
        genanki.Package(deck).write_to_file(output_path)
        messagebox.showinfo("Success", f"Anki deck saved to:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save deck:\n{e}")

def choose_json():
    path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=[("JSON files", "*.json")]
    )
    if path:
        json_file_path.set(path)

# Create the UI
root = tk.Tk()
root.title("Anki Deck Generator")
root.geometry("500x220")

tk.Label(root, text="Deck Output Filename (no extension):").pack(pady=(10, 0))
filename_entry = tk.Entry(root, width=40)
filename_entry.pack(pady=5)

tk.Label(root, text="Select JSON File:").pack(pady=(10, 0))
json_file_path = tk.StringVar()
json_entry = tk.Entry(root, textvariable=json_file_path, width=40)
json_entry.pack(side=tk.LEFT, padx=(10, 0), pady=5)
browse_button = tk.Button(root, text="Browse", command=choose_json)
browse_button.pack(side=tk.LEFT, padx=(5, 0))

# Fix layout
tk.Frame(root).pack(pady=5)

generate_button = tk.Button(root, text="Generate Anki Deck", command=generate_deck, bg='green', fg='white')
generate_button.pack(pady=20)

root.mainloop()