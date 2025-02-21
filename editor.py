import tkinter as tk
from tkinter import messagebox
import os
from themes import load_theme, setup_theme_menu
from file_operations import open_file, save_file
from syntax_highlighting import apply_syntax_highlighting

def quit_editor():
    if messagebox.askokcancel("Sair", "Você tem certeza que quer sair?"):
        root.destroy()

root = tk.Tk()
root.title("EmGVim")
root.iconbitmap("config/emgvim.ico")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

text_area = tk.Text(root, undo=True)
text_area.pack(expand=1, fill='both')

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Abrir", command=lambda: open_file(text_area))
file_menu.add_command(label="Salvar", command=lambda: save_file(text_area))
file_menu.add_separator()
file_menu.add_command(label="Sair", command=quit_editor)

setup_theme_menu(menu_bar, text_area)

load_theme('themes/default.json', text_area)

text_area.bind("<KeyRelease>", lambda event: apply_syntax_highlighting(text_area))

root.mainloop()