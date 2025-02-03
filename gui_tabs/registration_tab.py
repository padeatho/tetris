import tkinter as tk
from tkinter import ttk, messagebox

class RegistrationTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        # Name
        ttk.Label(self, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Phone
        ttk.Label(self, text="Telefone:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Amount
        ttk.Label(self, text="Valor Total:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Installments
        ttk.Label(self, text="Parcelas:").grid(row=3, column=0, padx=5, pady=5)
        self.installments_entry = ttk.Entry(self)
        self.installments_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Save button
        ttk.Button(self, text="Salvar", command=self.save_loan).grid(row=4, column=0, columnspan=2, pady=20)
    
    def save_loan(self):
        try:
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            amount = float(self.amount_entry.get())
            installments = int(self.installments_entry.get())
            
            if not all([name, phone, amount, installments]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            self.db.add_loan(name, phone, amount, installments)
            messagebox.showinfo("Sucesso", "Empréstimo cadastrado com sucesso!")
            self.clear_fields()
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")
    
    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.installments_entry.delete(0, tk.END)