class MessageFormatter:
    @staticmethod
    def format_loan_message(loan_data):
        """Format loan message with emojis and line breaks"""
        name, total_amount, installments = loan_data
        installment_value = total_amount / installments

        message = (
            f"Olá, tudo bem? ☺️\n\n"
            f"Sua parcela do último mês ainda está em aberto. 😱😱\n\n"
            f"⚠️  Valores  ⚠️\n\n"
            f"💰 Parcela: R$ {installment_value:.2f}\n"
            f"🧨 Restante: R$ {total_amount:.2f}"
        )
        return message