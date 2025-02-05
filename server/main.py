import threading
from audio_processor import AudioProcessor, TCPServer
from web_server import WebServer
from alerts import AlertSystem

def main():
    # Initialize components
    audio_proc = AudioProcessor()
    tcp_server = TCPServer(audio_proc)
    web_server = WebServer()
    alert_system = AlertSystem()
    
    # Start TCP server in background thread
    tcp_thread = threading.Thread(target=tcp_server.start, daemon=True)
    tcp_thread.start()
    
    # Start web server (this will block)
    web_server.start()

if __name__ == "__main__":
    main()