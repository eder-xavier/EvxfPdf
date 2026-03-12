import customtkinter as ctk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

def create_compress_frame(root):
    compress_frame = ctk.CTkFrame(root)
    compress_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(
        compress_frame,
        text="📉 Comprimir PDFs",
        font=("Arial", 24, "bold"),
        text_color="#2C5D7D"
    )
    title_label.pack(pady=(20, 20))

    folder_label = ctk.CTkLabel(
        compress_frame,
        text="📁 Pasta com PDFs:",
        font=("Arial", 12)
    )
    folder_label.pack(anchor="w", padx=15)

    folder_display = ctk.CTkLabel(
        compress_frame,
        text="Nenhuma pasta selecionada",
        font=("Arial", 10),
        text_color="#888888"
    )
    folder_display.pack(anchor="w", padx=15)

    select_btn = ctk.CTkButton(
        compress_frame,
        text="Selecionar Pasta",
        command=lambda: select_folder(folder_display),
        fg_color="#568CAD",
        hover_color="#3F789D",
        font=("Arial", 11)
    )
    select_btn.pack(fill="x", padx=15, pady=(0, 15))

    compress_btn = ctk.CTkButton(
        compress_frame,
        text="✅ Comprimir PDFs",
        command=lambda: compress_pdfs(folder_display.cget("text")),
        fg_color="#8CB5CF",
        hover_color="#3F789D",
        font=("Arial", 12)
    )
    compress_btn.pack(pady=(20, 10))

def select_folder(folder_display):
    folder = filedialog.askdirectory(title="Selecione a pasta com PDFs")
    if folder:
        folder_display.configure(text=folder)

def compress_pdfs(folder):
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Erro", "Selecione uma pasta válida com PDFs!")
        return

    for filename in sorted(os.listdir(folder)):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder, filename)
            reader = PdfReader(pdf_path)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            compressed_path = os.path.join(folder, f"compressed_{filename}")
            with open(compressed_path, "wb") as output_pdf:
                writer.write(output_pdf)

    messagebox.showinfo("Sucesso", "PDFs comprimidos com sucesso!")
