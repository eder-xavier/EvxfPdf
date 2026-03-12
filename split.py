import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PyPDF2 import PdfReader, PdfWriter

def create_split_frame(root):
    split_frame = ctk.CTkFrame(root)
    split_frame.pack(fill="both", expand=True)

    title_label = ctk.CTkLabel(
        split_frame,
        text="✂️ Dividir PDFs",
        font=("Arial", 24, "bold"),
        text_color="#2C5D7D"
    )
    title_label.pack(pady=(20, 20))

    folder_label = ctk.CTkLabel(
        split_frame,
        text="📁 Pasta com PDFs:",
        font=("Arial", 12)
    )
    folder_label.pack(anchor="w", padx=15)

    file_display = ctk.CTkLabel(
        split_frame,
        text="Nenhum arquivo selecionado",
        font=("Arial", 10),
        text_color="#888888"
    )
    file_display.pack(anchor="w", padx=15)

    select_btn = ctk.CTkButton(
        split_frame,
        text="Selecionar PDF",
        command=lambda: select_file(file_display),
        fg_color="#568CAD",
        hover_color="#3F789D",
        font=("Arial", 11)
    )
    select_btn.pack(fill="x", padx=15, pady=(0, 15))

    split_btn = ctk.CTkButton(
        split_frame,
        text="✅ Dividir PDF",
        command=lambda: split_pdf(file_display.cget("text")),
        fg_color="#8CB5CF",
        hover_color="#3F789D",
        font=("Arial", 12)
    )
    split_btn.pack(pady=(20, 10))

def select_file(file_display):
    file_path = filedialog.askopenfilename(title="Selecione um PDF", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        file_display.configure(text=file_path)

def split_pdf(file_path):
    if not file_path or not os.path.exists(file_path):
        messagebox.showerror("Erro", "Selecione um PDF válido!")
        return

    pdf_reader = PdfReader(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    for page_num in range(len(pdf_reader.pages)):
        writer = PdfWriter()
        writer.add_page(pdf_reader.pages[page_num])

        output_path = os.path.join(os.path.dirname(file_path), f"{base_name}_page_{page_num + 1}.pdf")
        with open(output_path, "wb") as output_pdf:
            writer.write(output_pdf)

    messagebox.showinfo("Sucesso", "PDF dividido com sucesso!")
