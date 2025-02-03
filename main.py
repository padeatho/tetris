import tkinter as tk
from tkinter import ttk
from database import Database
from services.whatsapp_service import WhatsAppService
from gui_tabs.registration_tab import RegistrationTab
from gui_tabs.modification_tab import ModificationTab
from gui_tabs.message_tab import MessageTab

class LoanManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gerenciador de Empréstimos")
        self.root.geometry("600x500")  # Increased height for message preview
        
        # Initialize services
        self.db = Database()
        self.whatsapp_service = WhatsAppService()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Create tabs
        self.registration_tab = RegistrationTab(self.notebook, self.db)
        self.modification_tab = ModificationTab(self.notebook, self.db)
        self.message_tab = MessageTab(self.notebook, self.db, self.whatsapp_service)
        
        # Add tabs to notebook
        self.notebook.add(self.registration_tab, text="Cadastro")
        self.notebook.add(self.modification_tab, text="Alterações")
        self.notebook.add(self.message_tab, text="Enviar Mensagem")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LoanManager()
    app.run()