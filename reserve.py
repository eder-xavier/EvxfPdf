import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from pathlib import Path
import PyPDF2

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger - Mesclar PDFs")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.folder_path = None
        self.pdf_files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface gráfica"""
        
        # Frame principal com scrolling
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="🔀 Mesclar PDFs",
            font=("Arial", 28, "bold"),
            text_color="#00A8FF"
        )
        title_label.pack(pady=(0, 20))
        
        # Seção de seleção de pasta
        folder_frame = ctk.CTkFrame(main_frame, fg_color="#1E1E1E", corner_radius=10)
        folder_frame.pack(fill="x", pady=(0, 20))
        
        folder_label = ctk.CTkLabel(
            folder_frame,
            text="📁 Pasta com PDFs:",
            font=("Arial", 12, "bold")
        )
        folder_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.folder_display = ctk.CTkLabel(
            folder_frame,
            text="Nenhuma pasta selecionada",
            font=("Arial", 10),
            text_color="#888888"
        )
        self.folder_display.pack(anchor="w", padx=15, pady=(0, 10))
        
        select_btn = ctk.CTkButton(
            folder_frame,
            text="Selecionar Pasta",
            command=self.select_folder,
            fg_color="#00A8FF",
            hover_color="#0088CC",
            font=("Arial", 11, "bold"),
            height=35,
            corner_radius=8
        )
        select_btn.pack(fill="x", padx=15, pady=(0, 15))
        
        # Seção de lista de PDFs
        list_frame = ctk.CTkFrame(main_frame, fg_color="#1E1E1E", corner_radius=10)
        list_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        list_label = ctk.CTkLabel(
            list_frame,
            text="📄 PDFs encontrados:",
            font=("Arial", 12, "bold")
        )
        list_label.pack(anchor="w", padx=15, pady=(10, 10))
        
        # Textbox com scrollbar manual
        self.pdf_listbox = ctk.CTkTextbox(
            list_frame,
            font=("Arial", 10),
            height=150,
            corner_radius=8
        )
        self.pdf_listbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.pdf_listbox.configure(state="disabled")
        
        # Seção de nome do arquivo de saída
        output_frame = ctk.CTkFrame(main_frame, fg_color="#1E1E1E", corner_radius=10)
        output_frame.pack(fill="x", pady=(0, 20))
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="💾 Nome do arquivo de saída:",
            font=("Arial", 12, "bold")
        )
        output_label.pack(anchor="w", padx=15, pady=(10, 8))
        
        self.output_name = ctk.CTkEntry(
            output_frame,
            placeholder_text="merged_pdfs.pdf",
            font=("Arial", 11),
            height=35,
            corner_radius=8
        )
        self.output_name.pack(fill="x", padx=15, pady=(0, 15))
        self.output_name.insert(0, "merged_pdfs.pdf")
        
        # Seção de botões - CORRIGIDO
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 10))
        
        # Criar frame para cada botão com peso igual
        merge_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        merge_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        merge_btn = ctk.CTkButton(
            merge_frame,
            text="✅ Mesclar PDFs",
            command=self.merge_pdfs,
            fg_color="#00CC00",
            hover_color="#00AA00",
            text_color="#000000",
            font=("Arial", 12, "bold"),
            height=45,
            corner_radius=8
        )
        merge_btn.pack(fill="both", expand=True)
        
        clear_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        clear_frame.pack(side="left", fill="both", expand=True)
        
        clear_btn = ctk.CTkButton(
            clear_frame,
            text="🔄 Limpar",
            command=self.clear_all,
            fg_color="#FF6B6B",
            hover_color="#CC5555",
            text_color="#FFFFFF",
            font=("Arial", 12, "bold"),
            height=45,
            corner_radius=8
        )
        clear_btn.pack(fill="both", expand=True)
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Pronto para começar",
            font=("Arial", 10),
            text_color="#888888"
        )
        self.status_label.pack(anchor="w", pady=(10, 0))
    
    def select_folder(self):
        """Abre diálogo para selecionar pasta"""
        folder = filedialog.askdirectory(title="Selecione a pasta com PDFs")
        
        if folder:
            self.folder_path = folder
            self.folder_display.configure(text=folder)
            self.load_pdfs()
    
    def load_pdfs(self):
        """Carrega lista de PDFs da pasta selecionada"""
        if not self.folder_path:
            return
        
        self.pdf_files = []
        
        # Procurar por arquivos PDF
        for file in sorted(os.listdir(self.folder_path)):
            if file.lower().endswith('.pdf'):
                self.pdf_files.append(file)
        
        # Atualizar listbox
        self.pdf_listbox.configure(state="normal")
        self.pdf_listbox.delete("1.0", "end")
        
        if self.pdf_files:
            for i, pdf in enumerate(self.pdf_files, 1):
                self.pdf_listbox.insert("end", f"{i}. {pdf}\n")
            self.status_label.configure(
                text=f"✓ {len(self.pdf_files)} PDF(s) encontrado(s)",
                text_color="#00CC00"
            )
        else:
            self.pdf_listbox.insert("end", "Nenhum arquivo PDF encontrado nesta pasta.")
            self.status_label.configure(
                text="⚠ Nenhum PDF encontrado",
                text_color="#FF9900"
            )
        
        self.pdf_listbox.configure(state="disabled")
    
    def merge_pdfs(self):
        """Mescla os PDFs em thread separada"""
        if not self.pdf_files:
            messagebox.showwarning("Aviso", "Selecione uma pasta com PDFs!")
            return
        
        output_name = self.output_name.get().strip()
        if not output_name.endswith('.pdf'):
            output_name += '.pdf'
        
        # Executar merge em thread para não travar a UI
        thread = threading.Thread(
            target=self._perform_merge,
            args=(output_name,),
            daemon=True
        )
        thread.start()
    
    def _perform_merge(self, output_name):
        """Executa a mesclagem de PDFs"""
        try:
            self.status_label.configure(
                text="⏳ Mesclando PDFs...",
                text_color="#FFB700"
            )
            self.root.update()
            
            output_path = os.path.join(self.folder_path, output_name)
            
            # Verificar se arquivo já existe
            if os.path.exists(output_path):
                response = messagebox.askyesno(
                    "Arquivo Existe",
                    f"O arquivo '{output_name}' já existe. Deseja sobrescrever?"
                )
                if not response:
                    self.status_label.configure(
                        text="❌ Operação cancelada",
                        text_color="#FF6B6B"
                    )
                    return
            
            # Criar merger
            merger = PyPDF2.PdfMerger()
            
            # Adicionar PDFs
            for pdf_file in self.pdf_files:
                pdf_path = os.path.join(self.folder_path, pdf_file)
                merger.append(pdf_path)
            
            # Escrever arquivo de saída
            merger.write(output_path)
            merger.close()
            
            self.status_label.configure(
                text=f"✅ PDFs mesclados com sucesso! Arquivo: {output_name}",
                text_color="#00CC00"
            )
            
            messagebox.showinfo(
                "Sucesso!",
                f"PDFs mesclados com sucesso!\n\nArquivo: {output_name}\nLocalização: {self.folder_path}"
            )
            
        except Exception as e:
            self.status_label.configure(
                text=f"❌ Erro: {str(e)}",
                text_color="#FF6B6B"
            )
            messagebox.showerror("Erro", f"Erro ao mesclar PDFs:\n{str(e)}")
    
    def clear_all(self):
        """Limpa todos os dados"""
        self.folder_path = None
        self.pdf_files = []
        self.folder_display.configure(text="Nenhuma pasta selecionada")
        self.pdf_listbox.configure(state="normal")
        self.pdf_listbox.delete("1.0", "end")
        self.pdf_listbox.configure(state="disabled")
        self.output_name.delete(0, "end")
        self.output_name.insert(0, "merged_pdfs.pdf")
        self.status_label.configure(
            text="Pronto para começar",
            text_color="#888888"
        )

def main():
    root = ctk.CTk()
    app = PDFMergerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
