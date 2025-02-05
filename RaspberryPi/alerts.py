from twilio.rest import Client
from config import Config

class AlertSystem:
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        
    def send_alert(self, message):
        """Send SMS alert"""
        if Config.ALERTS_ENABLED:
            try:
                self.client.messages.create(
                    body=message,
                    from_=Config.TWILIO_FROM_NUMBER,
                    to=Config.ALERT_TO_NUMBER
                )
            except Exception as e:
                print(f"Failed to send SMS: {e}")