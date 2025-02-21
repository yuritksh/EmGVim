import json
import os
import tkinter as tk
from syntax_highlighting import apply_syntax_highlighting

def load_theme(theme_path, text_area):
    global theme
    with open(theme_path, 'r') as file:
        theme = json.load(file)
    text_area.config(background=theme['background'], foreground=theme['foreground'], font=(theme['font'], theme['fontSize']))
    text_area.tag_configure("keyword", foreground=theme['keyword'], font=(theme['font'], theme['fontSize'], "bold"))
    text_area.tag_configure("string", foreground=theme['string'], font=(theme['font'], theme['fontSize'], "italic"))
    text_area.tag_configure("comment", foreground=theme['comment'], font=(theme['font'], theme['fontSize'], "italic"))
    apply_syntax_highlighting(text_area)

def setup_theme_menu(menu_bar, text_area):
    theme_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Tema", menu=theme_menu)

    theme_dir = 'themes'
    for theme_file in os.listdir(theme_dir):
        if theme_file.endswith('.json'):
            theme_path = os.path.join(theme_dir, theme_file)
            theme_menu.add_command(label=theme_file, command=lambda path=theme_path: load_theme(path, text_area))