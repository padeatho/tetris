import pywhatkit
from datetime import datetime
from utils.message_formatter import MessageFormatter

class WhatsAppService:
    def __init__(self):
        self.message_formatter = MessageFormatter()

    def send_message(self, loan):
        # Remove any non-numeric characters from phone
        clean_phone = ''.join(filter(str.isdigit, loan.phone))
        
        # Format the message
        message = self.message_formatter.format_loan_message(
            (loan.name, loan.total_amount, loan.installments)
        )
        
        # Get current time
        now = datetime.now()
        
        try:
            # Send message (2 minutes from now to ensure WhatsApp Web is ready)
            pywhatkit.sendwhatmsg(
                f"+{clean_phone}",
                message,
                now.hour,
                now.minute + 2
            )
            return True, "Mensagem agendada com sucesso!"
        except Exception as e:
            return False, f"Erro ao enviar mensagem: {str(e)}"