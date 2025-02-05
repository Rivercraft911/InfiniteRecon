from flask import Flask, render_template, jsonify, request
import threading
import os
from config import Config

app = Flask(__name__)

class WebServer:
    def __init__(self):
        """Initialize the web server with shared data structures."""
        self.transcripts = []
        self.transcript_lock = threading.Lock()
        self.config = Config()

    def add_transcript(self, transcript_entry):
        """
        Add a new transcript entry to the transcript log.
        transcript_entry should be a dict with: timestamp, speaker, text, and llm_response
        """
        with self.transcript_lock:
            self.transcripts.append(transcript_entry)
            # Keep only last 20 entries
            if len(self.transcripts) > 20:
                self.transcripts.pop(0)

    def setup_routes(self):
        """Set up all the Flask routes."""
        
        @app.route('/')
        def index():
            """Serve the main dashboard page."""
            return render_template('index.html')

        @app.route('/transcripts')
        def get_transcripts():
            """Return all transcripts as JSON."""
            with self.transcript_lock:
                return jsonify(self.transcripts)

        @app.route('/config', methods=['GET', 'POST'])
        def handle_config():
            """Handle configuration get/set requests."""
            if request.method == 'GET':
                return jsonify({
                    'alert_keywords': self.config.ALERT_KEYWORDS,
                    'alerts_enabled': self.config.ALERTS_ENABLED,
                    'llm_enabled': self.config.LLM_ENABLED,
                    'llm_provider': self.config.LLM_PROVIDER
                })
            
            elif request.method == 'POST':
                data = request.get_json()
                
                # Update configuration
                if 'alert_keywords' in data:
                    self.config.ALERT_KEYWORDS = data['alert_keywords']
                if 'alerts_enabled' in data:
                    self.config.ALERTS_ENABLED = data['alerts_enabled']
                if 'llm_enabled' in data:
                    self.config.LLM_ENABLED = data['llm_enabled']
                if 'llm_provider' in data:
                    self.config.LLM_PROVIDER = data['llm_provider']
                
                return jsonify({
                    'alert_keywords': self.config.ALERT_KEYWORDS,
                    'alerts_enabled': self.config.ALERTS_ENABLED,
                    'llm_enabled': self.config.LLM_ENABLED,
                    'llm_provider': self.config.LLM_PROVIDER
                })

    def start(self, host='0.0.0.0', port=8000):
        """Start the Flask web server."""
        self.setup_routes()
        app.run(host=host, port=port, debug=False, use_reloader=False)

# Example usage:
if __name__ == "__main__":
    web_server = WebServer()
    web_server.start()