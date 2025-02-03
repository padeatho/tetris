import tkinter as tk
from tkinter import ttk, messagebox
from models.loan import Loan

class MessageTab(ttk.Frame):
    def __init__(self, parent, db, whatsapp_service):
        super().__init__(parent)
        self.db = db
        self.whatsapp_service = whatsapp_service
        self.setup_ui()
    
    def setup_ui(self):
        # Loan selection
        ttk.Label(self, text="Selecione o empréstimo:").grid(row=0, column=0, padx=5, pady=5)
        self.loan_var = tk.StringVar()
        self.loan_combo = ttk.Combobox(self, textvariable=self.loan_var)
        self.loan_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Preview message
        ttk.Label(self, text="Prévia da mensagem:").grid(row=1, column=0, padx=5, pady=5)
        self.message_preview = tk.Text(self, height=10, width=40)
        self.message_preview.grid(row=1, column=1, padx=5, pady=5)
        self.loan_combo.bind('<<ComboboxSelected>>', self.update_message_preview)
        
        # Send button
        ttk.Button(self, text="Enviar Mensagem", command=self.send_message).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Refresh button
        ttk.Button(self, text="Atualizar Lista", command=self.refresh_loans).grid(row=3, column=0, columnspan=2, pady=5)
        
        self.refresh_loans()
    
    def refresh_loans(self):
        loans = self.db.get_all_loans()
        self.loan_combo['values'] = [f"{loan[0]} - {loan[1]}" for loan in loans]
    
    def update_message_preview(self, event=None):
        if not self.loan_var.get():
            return
            
        loan_id = int(self.loan_var.get().split('-')[0].strip())
        loan_data = self.db.get_loan(loan_id)
        loan = Loan(
            id=loan_data[0],
            name=loan_data[1],
            phone=loan_data[2],
            total_amount=loan_data[3],
            installments=loan_data[4],
            created_at=loan_data[5]
        )
        
        message = MessageFormatter.format_loan_message(
            (loan.name, loan.total_amount, loan.installments)
        )
        
        self.message_preview.delete("1.0", tk.END)
        self.message_preview.insert("1.0", message)
    
    def send_message(self):
        if not self.loan_var.get():
            messagebox.showerror("Erro", "Selecione um empréstimo!")
            return
            
        loan_id = int(self.loan_var.get().split('-')[0].strip())
        loan_data = self.db.get_loan(loan_id)
        loan = Loan(
            id=loan_data[0],
            name=loan_data[1],
            phone=loan_data[2],
            total_amount=loan_data[3],
            installments=loan_data[4],
            created_at=loan_data[5]
        )
        
        success, msg = self.whatsapp_service.send_message(loan)
        if success:
            messagebox.showinfo("Sucesso", msg)
        else:
            messagebox.showerror("Erro", msg)