import tkinter as tk
import tkinter.font as tkfont
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename, asksaveasfilename


current_filepath = ""

def set_filepath(filepath):
    global current_filepath
    current_filepath = filepath
    window.title(f"Aikoja – {filepath}")

def open_file():
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
        return
    textarea.delete("1.0", tk.END)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()
        textarea.insert(tk.END, text)
    set_filepath(filepath)

def save_file(ask_filepath):
    filepath = current_filepath
    if ask_filepath or not filepath:
        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
    if not filepath:
        return
    with open(filepath, "w", encoding="utf-8") as output_file:
        text = textarea.get("1.0", tk.END)
        output_file.write(text)
    set_filepath(filepath)

window = tk.Tk()
window.title("Aikoja")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

textarea = ScrolledText(window, undo=True, autoseparators=True)

font = tkfont.Font(font=textarea["font"])
tab_size = font.measure("        ")
# Configure tabs. The default tabstyle of "tabular" creates an undesired alignment.  
textarea.config(tabs=(tab_size, tk.LEFT), tabstyle="wordprocessor")

textarea.grid(row=0, column=0, sticky="nsew")

# Override the default menu style.
window.option_add("*tearOff", False)

menubar = tk.Menu(window)

menu_file = tk.Menu(menubar)
menu_file.add_command(label="Open...", accelerator="Control+O", command=open_file)
window.bind("<Control_L>o", lambda _: open_file())
menu_file.add_command(label="Save", accelerator="Control+S", command=lambda _: save_file(False))
window.bind("<Control_L>s", lambda _: save_file(False))
menu_file.add_command(label="Save As...", accelerator="Control+Shift+S", command=lambda _: save_file(True))
window.bind("<Control_L>S", lambda _: save_file(True))
menubar.add_cascade(label="File", menu=menu_file)

window.config(menu=menubar)

window.mainloop()