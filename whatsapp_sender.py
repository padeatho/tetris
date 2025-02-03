import pywhatkit
from datetime import datetime
import time

class WhatsAppSender:
    @staticmethod
    def send_message(phone, message):
        # Remove any non-numeric characters from phone
        clean_phone = ''.join(filter(str.isdigit, phone))
        
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