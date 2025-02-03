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

class ModificationTab(ttk.Frame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.setup_ui()
    
    def setup_ui(self):
        # Loan selection
        ttk.Label(self, text="Selecione o empréstimo:").grid(row=0, column=0, padx=5, pady=5)
        self.loan_var = tk.StringVar()
        self.loan_combo = ttk.Combobox(self, textvariable=self.loan_var)
        self.loan_combo.grid(row=0, column=1, padx=5, pady=5)
        self.loan_combo.bind('<<ComboboxSelected>>', self.load_loan_data)
        
        # Fields
        ttk.Label(self, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Telefone:").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Valor Total:").grid(row=3, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(self, text="Parcelas:").grid(row=4, column=0, padx=5, pady=5)
        self.installments_entry = ttk.Entry(self)
        self.installments_entry.grid(row=4, column=1, padx=5, pady=5)
        
        # Update button
        ttk.Button(self, text="Atualizar", command=self.update_loan).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Refresh loan list
        ttk.Button(self, text="Atualizar Lista", command=self.refresh_loans).grid(row=6, column=0, columnspan=2, pady=5)
        
        self.refresh_loans()
    
    def refresh_loans(self):
        loans = self.db.get_all_loans()
        self.loan_combo['values'] = [f"{loan[0]} - {loan[1]}" for loan in loans]
    
    def load_loan_data(self, event=None):
        if not self.loan_var.get():
            return
            
        loan_id = int(self.loan_var.get().split('-')[0].strip())
        loan = self.db.get_loan(loan_id)
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, loan[1])
        
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, loan[2])
        
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, str(loan[3]))
        
        self.installments_entry.delete(0, tk.END)
        self.installments_entry.insert(0, str(loan[4]))
    
    def update_loan(self):
        try:
            loan_id = int(self.loan_var.get().split('-')[0].strip())
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            amount = float(self.amount_entry.get())
            installments = int(self.installments_entry.get())
            
            if not all([name, phone, amount, installments]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            self.db.update_loan(loan_id, name, phone, amount, installments)
            messagebox.showinfo("Sucesso", "Empréstimo atualizado com sucesso!")
            self.refresh_loans()
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos!")

class MessageTab(ttk.Frame):
    def __init__(self, parent, db, whatsapp_sender):
        super().__init__(parent)
        self.db = db
        self.whatsapp_sender = whatsapp_sender
        self.setup_ui()
    
    def setup_ui(self):
        # Loan selection
        ttk.Label(self, text="Selecione o empréstimo:").grid(row=0, column=0, padx=5, pady=5)
        self.loan_var = tk.StringVar()
        self.loan_combo = ttk.Combobox(self, textvariable=self.loan_var)
        self.loan_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Message
        ttk.Label(self, text="Mensagem:").grid(row=1, column=0, padx=5, pady=5)
        self.message_text = tk.Text(self, height=5, width=40)
        self.message_text.grid(row=1, column=1, padx=5, pady=5)
        
        # Send button
        ttk.Button(self, text="Enviar Mensagem", command=self.send_message).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Refresh button
        ttk.Button(self, text="Atualizar Lista", command=self.refresh_loans).grid(row=3, column=0, columnspan=2, pady=5)
        
        self.refresh_loans()
    
    def refresh_loans(self):
        loans = self.db.get_all_loans()
        self.loan_combo['values'] = [f"{loan[0]} - {loan[1]}" for loan in loans]
    
    def send_message(self):
        if not self.loan_var.get():
            messagebox.showerror("Erro", "Selecione um empréstimo!")
            return
            
        loan_id = int(self.loan_var.get().split('-')[0].strip())
        loan = self.db.get_loan(loan_id)
        message = self.message_text.get("1.0", tk.END).strip()
        
        if not message:
            messagebox.showerror("Erro", "Digite uma mensagem!")
            return
        
        success, msg = self.whatsapp_sender.send_message(loan[2], message)
        if success:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)