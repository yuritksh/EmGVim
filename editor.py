import tkinter as tk
from tkinter import filedialog, messagebox
import re
import json

with open('config/theme.json', 'r') as file:
    theme = json.load(file)

# Função para abrir um arquivo
def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text Files", "*.txt"),
                                                      ("SQL files", "*.sql"),
                                                      ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_area.delete(1.0, tk.END)  # Limpa o editor antes de abrir um novo arquivo
                text_area.insert(tk.END, file.read())  # Insere o conteúdo do arquivo no editor
                apply_syntax_highlighting()
        # except UnicodeDecodeError as e:
        #     messagebox.showerror("Erro na codificação", f"Erro ao abrir arquivo: {e}")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

# Função para salvar um arquivo
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"),
                                                        ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(text_area.get(1.0, tk.END))  # Salva o conteúdo do editor no arquivo
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

def apply_syntax_highlighting(event=None):
    text = text_area.get("1.0", tk.END)
    
    # Remove estilos anteriores
    text_area.tag_remove("keyword", "1.0", tk.END)
    text_area.tag_remove("string", "1.0", tk.END)
    text_area.tag_remove("comment", "1.0", tk.END)
    
    # Definindo padrões para as keywords SQL
    keywords = r"\b(SELECT|FROM|INSERT|INTO|VALUES|UPDATE|DELETE|WHERE|JOIN|INNER|LEFT|RIGHT|OUTER|CREATE|TABLE|ALTER|DROP|INDEX)\b"
    strings = r"'.*?'"  # Strings simples entre aspas simples
    comments = r"--.*?$"  # Comentários de linha única
    
    # Highlight para palavras-chave
    for match in re.finditer(keywords, text, re.IGNORECASE):
        start, end = match.span()
        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"
        text_area.tag_add("keyword", start_index, end_index)

    # Highlight para strings
    for match in re.finditer(strings, text):
        start, end = match.span()
        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"
        text_area.tag_add("string", start_index, end_index)

    # Highlight para comentários
    for match in re.finditer(comments, text, re.MULTILINE):
        start, end = match.span()
        start_index = f"1.0+{start}c"
        end_index = f"1.0+{end}c"
        text_area.tag_add("comment", start_index, end_index)

# Função para sair do editor
def quit_editor():
    if messagebox.askokcancel("Sair", "Você tem certeza que quer sair?"):
        root.destroy()

# Criando a janela principal
root = tk.Tk()
root.title("Editor de Texto Simples")

# Criando o menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Adicionando as opções no menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=quit_editor)

# Criando a área de texto
text_area = tk.Text(root, undo=True, background=theme['background'], foreground=theme['foreground'], font=(theme['font'], theme['fontSize']))
text_area.pack(expand=1, fill='both')

# Configurando tags para syntax highlighting
text_area.tag_configure("keyword", foreground=theme['keyword'], font=(theme['font'], theme['fontSize'], "bold"))
text_area.tag_configure("string", foreground=theme['string'], font=(theme['font'], theme['fontSize'], "italic"))
text_area.tag_configure("comment", foreground=theme['comment'], font=(theme['font'], theme['fontSize'], "italic"))

# Vinculando evento de modificação de texto para aplicar syntax highlighting
text_area.bind("<KeyRelease>", apply_syntax_highlighting)

# Iniciar o loop da interface gráfica
root.mainloop()
