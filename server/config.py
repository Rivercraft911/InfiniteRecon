class Config:
    # Network settings
    TCP_HOST = ""  # Empty string means listen on all network interfaces
    TCP_PORT = 5000  # Port for ESP32 audio streaming
    WEB_PORT = 8000  # Port for web dashboard
    
    # Twilio (SMS) settings
    TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
    TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
    TWILIO_FROM_NUMBER = "+1234567890"
    ALERT_TO_NUMBER = "+1987654321"
    
    # Speech recognition settings
    MODEL_PATH = "/home/pi/vosk-model/vosk-model-small-en-us-0.15"
    
    # Alert settings
    ALERT_KEYWORDS = ['emergency', 'help', 'fire', 'intruder']
    ALERTS_ENABLED = True
    LLM_ENABLED = False
    LLM_PROVIDER = 'openai'