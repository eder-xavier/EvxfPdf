import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import PyPDF2

def create_merge_frame(root):
    merge_frame = ctk.CTkFrame(root)
    merge_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(
        merge_frame,
        text="🔀 Mesclar PDFs",
        font=("Arial", 24, "bold"),
        text_color="#2C5D7D"
    )
    title_label.pack(pady=(20, 20))

    folder_label = ctk.CTkLabel(
        merge_frame,
        text="📁 Pasta com PDFs:",
        font=("Arial", 12)
    )
    folder_label.pack(anchor="w", padx=15)

    folder_display = ctk.CTkLabel(
        merge_frame,
        text="Nenhuma pasta selecionada",
        font=("Arial", 10),
        text_color="#888888"
    )
    folder_display.pack(anchor="w", padx=15)

    select_btn = ctk.CTkButton(
        merge_frame,
        text="Selecionar Pasta",
        command=lambda: select_folder(folder_display),
        fg_color="#568CAD",
        hover_color="#3F789D",
        font=("Arial", 11)
    )
    select_btn.pack(fill="x", padx=15, pady=(0, 15))

    output_name_label = ctk.CTkLabel(
        merge_frame,
        text="💾 Nome do arquivo de saída:",
        font=("Arial", 12)
    )
    output_name_label.pack(anchor="w", padx=15)

    output_entry = ctk.CTkEntry(
        merge_frame,
        placeholder_text="merged_pdfs.pdf",
        font=("Arial", 11)
    )
    output_entry.pack(fill="x", padx=15)

    merge_btn = ctk.CTkButton(
        merge_frame,
        text="✅ Mesclar PDFs",
        command=lambda: merge_pdfs(folder_display, output_entry.get()),
        fg_color="#8CB5CF",
        hover_color="#3F789D",
        font=("Arial", 12)
    )
    merge_btn.pack(pady=(20, 10))

def select_folder(folder_display):
    folder = filedialog.askdirectory(title="Selecione a pasta com PDFs")
    if folder:
        folder_display.configure(text=folder)

def merge_pdfs(folder_display, output_name):
    folder = folder_display.cget("text")
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Erro", "Selecione uma pasta válida com PDFs!")
        return

    output_path = os.path.join(folder, output_name)
    if not output_name.endswith('.pdf'):
        output_name += '.pdf'

    merger = PyPDF2.PdfMerger()
    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith('.pdf'):
            merger.append(os.path.join(folder, filename))

    merger.write(output_path)
    merger.close()
    messagebox.showinfo("Sucesso", f"PDFs mesclados em: {output_path}")
