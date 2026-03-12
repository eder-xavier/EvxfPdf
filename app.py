import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import merge
import compress
import split

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evxf PDF")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Removendo a linha que define um tema
        ctk.set_appearance_mode("dark")
        # ctk.set_default_color_theme("theme")  # Removida

        self.setup_ui()

    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(
            main_frame,
            text="Evxf PDF",
            font=("Arial", 28, "bold"),
            text_color="#2C5D7D"
        )
        title_label.pack(pady=(0, 20))

        # Menu
        menu_frame = ctk.CTkFrame(main_frame)
        menu_frame.pack(fill="x", pady=(0, 20))

        merge_btn = ctk.CTkButton(
            menu_frame,
            text="📄 Mesclar PDF",
            command=self.open_merge,
            fg_color="#568CAD",
            hover_color="#3F789D",
            font=("Arial", 12)
        )
        merge_btn.pack(side="left", fill="x", expand=True, padx=5)

        compress_btn = ctk.CTkButton(
            menu_frame,
            text="📉 Comprimir PDF",
            command=self.open_compress,
            fg_color="#8CB5CF",
            hover_color="#3F789D",
            font=("Arial", 12)
        )
        compress_btn.pack(side="left", fill="x", expand=True, padx=5)

        split_btn = ctk.CTkButton(
            menu_frame,
            text="✂️ Dividir PDF",
            command=self.open_split,
            fg_color="#6890AB",
            hover_color="#3F789D",
            font=("Arial", 12)
        )
        split_btn.pack(side="left", fill="x", expand=True, padx=5)

        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Escolha uma opção do menu acima.",
            font=("Arial", 10),
            text_color="#888888"
        )
        self.status_label.pack(anchor="w", pady=(10, 0))

    def open_merge(self):
        self.clear_frame()
        merge.create_merge_frame(self.root)

    def open_compress(self):
        self.clear_frame()
        compress.create_compress_frame(self.root)

    def open_split(self):
        self.clear_frame()
        split.create_split_frame(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.setup_ui()

def main():
    root = ctk.CTk()
    app = PDFApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
