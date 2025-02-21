import re
import tkinter as tk

def apply_syntax_highlighting(text_area):
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