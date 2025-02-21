import tkinter as tk
from tkinter import filedialog, messagebox
from syntax_highlighting import apply_syntax_highlighting

def open_file(text_area):
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"),
                                                      ("SQL files", "*.sql"),
                                                      ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, file.read())
                apply_syntax_highlighting(text_area)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

def save_file(text_area):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"),
                                                        ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(text_area.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")