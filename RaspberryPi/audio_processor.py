import socket
from vosk import Model, KaldiRecognizer
from config import Config
from llm_handler import LLMHandler

class AudioProcessor:
    def __init__(self):
        self.llm_handler = LLMHandler()
        
    def process_audio_chunk(self, audio_data, config):
        text = self.recognize_speech(audio_data)
        
        if text and config['llm_enabled']:
            llm_response = self.llm_handler.process_text(
                text, 
                config['llm_provider']
            )
            return {
                'text': text,
                'llm_response': llm_response
            }
        return {'text': text}

class TCPServer:
    def __init__(self, audio_processor):
        self.audio_processor = audio_processor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):
        """Start TCP server to listen for ESP32 connections"""
        self.socket.bind((Config.TCP_HOST, Config.TCP_PORT))
        self.socket.listen(1)
        print(f"TCP Server listening on port {Config.TCP_PORT}...")

