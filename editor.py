import tkinter as tk
from tkinter import filedialog, messagebox
import re
import json
import os

def load_theme(theme_path):
    global theme
    with open(theme_path, 'r') as file:
        theme = json.load(file)
    text_area.config(background=theme['background'], foreground=theme['foreground'], font=(theme['font'], theme['fontSize']))
    text_area.tag_configure("keyword", foreground=theme['keyword'], font=(theme['font'], theme['fontSize'], "bold"))
    text_area.tag_configure("string", foreground=theme['string'], font=(theme['font'], theme['fontSize'], "italic"))
    text_area.tag_configure("comment", foreground=theme['comment'], font=(theme['font'], theme['fontSize'], "italic"))
    apply_syntax_highlighting()

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"),
                                                      ("SQL files", "*.sql"),
                                                      ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
                apply_syntax_highlighting()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"),
                                                        ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(text_area.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

def apply_syntax_highlighting(event=None):
    text = text_area.get("1.0", tk.END)
    text_area.tag_remove("keyword", "1.0", tk.END)
    text_area.tag_remove("string", "1.0", tk.END)
    text_area.tag_remove("comment", "1.0", tk.END)
    keywords = r"\b(SELECT|FROM|INSERT|INTO|VALUES|UPDATE|DELETE|WHERE|JOIN|INNER|LEFT|RIGHT|OUTER|CREATE|TABLE|ALTER|DROP|INDEX)\b"
    strings = r"'.*?'"
    comments = r"--.*?$"
    for match in re.finditer(keywords, text, re.IGNORECASE):
        start, end = match.span()
        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"
        text_area.tag_add("keyword", start_index, end_index)
    for match in re.finditer(strings, text):
        start, end = match.span()
        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"
        text_area.tag_add("string", start_index, end_index)
    for match in re.finditer(comments, text, re.MULTILINE):
        start, end = match.span()
        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"
        text_area.tag_add("comment", start_index, end_index)

def quit_editor():
    if messagebox.askokcancel("Sair", "Você tem certeza que quer sair?"):
        root.destroy()

root = tk.Tk()
root.title("EmGVim")
root.iconbitmap("config/emgvim.ico")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=quit_editor)

theme_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tema", menu=theme_menu)

theme_dir = 'themes'
for theme_file in os.listdir(theme_dir):
    if theme_file.endswith('.json'):
        theme_path = os.path.join(theme_dir, theme_file)
        theme_menu.add_command(label=theme_file, command=lambda path=theme_path: load_theme(path))

text_area = tk.Text(root, undo=True)
text_area.pack(expand=1, fill='both')

load_theme('themes/default.json')

text_area.bind("<KeyRelease>", apply_syntax_highlighting)

root.mainloop()
