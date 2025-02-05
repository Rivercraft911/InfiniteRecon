#!/usr/bin/env python3
import socket
import json
import threading
import time

from flask import Flask, request, jsonify
import numpy as np
from vosk import Model, KaldiRecognizer
from twilio.rest import Client

# ================= Global Configuration =================
# These settings can be changed via the web dashboard.
CONFIG = {
    'alert_keywords': ['emergency', 'help', 'fire', 'intruder'],
    'alerts_enabled': True,       # Toggle SMS alerts on/off
    'llm_enabled': False,         # Toggle LLM API usage on/off
    'llm_provider': 'openai'      # Options: 'openai', 'deepseek', 'anthropic'
}

# Global transcript log (holds the most recent 20 entries)
TRANSCRIPT_LOG = []
TRANSCRIPT_LOCK = threading.Lock()

# ================= Twilio Settings =================
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN  = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_FROM_NUMBER = "+1234567890"  # Your Twilio number
ALERT_TO_NUMBER    = "+1987654321"   # Destination phone number

# ================= Vosk Speech Recognition =================
MODEL_PATH = "/home/pi/vosk-model/vosk-model-small-en-us-0.15"  # Update if necessary
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)  # 16kHz sample rate

# ================= Flask App Initialization =================
app = Flask(__name__)

# ================= TCP Server Settings =================
TCP_HOST = ""       # Listen on all interfaces
TCP_PORT = 5000     # Port used by the ESP32 to stream audio

# ------------------ Utility Functions ------------------

def send_sms_alert(message):
    """Send an SMS alert via Twilio if alerts are enabled."""
    if not CONFIG['alerts_enabled']:
        print("SMS alerts are disabled. Not sending SMS.")
        return
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        sms = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=ALERT_TO_NUMBER
        )
        print(f"SMS sent: SID {sms.sid}")
    except Exception as e:
        print("Failed to send SMS:", e)

def identify_speaker(audio_chunk):
    """
    Placeholder for speaker identification.
    In production, you might integrate a diarization algorithm.
    """
    return "Speaker 1"

def call_llm_api(text):
    """
    Stub function to call an LLM API based on the provider configured.
    Replace these stubs with actual API calls and proper authentication.
    """
    if not CONFIG['llm_enabled']:
        return None
    provider = CONFIG.get('llm_provider', 'openai')
    if provider == 'openai':
        # Insert actual OpenAI API call here.
        return f"[OpenAI] Response for: {text}"
    elif provider == 'deepseek':
        # Insert actual DeepSeek API call here.
        return f"[DeepSeek] Response for: {text}"
    elif provider == 'anthropic':
        # Insert actual Anthropic API call here.
        return f"[Anthropic] Response for: {text}"
    else:
        return None

# ------------------ Audio Processing ------------------

def process_audio_stream(conn):
    """
    Process incoming audio data from the ESP32.
    Transcribe the audio with Vosk, update the transcript log,
    check for alert keywords, and (if enabled) call the LLM API.
    """
    global recognizer, TRANSCRIPT_LOG
    try:
        while True:
            # Read a chunk of data (assumed 16-bit little-endian PCM)
            data = conn.recv(1024)
            if not data:
                break

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if 'text' in result:
                    text = result['text'].strip()
                    if text:
                        speaker = identify_speaker(data)
                        llm_response = None
                        if CONFIG['llm_enabled']:
                            llm_response = call_llm_api(text)
                        transcript_entry = {
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                            'speaker': speaker,
                            'text': text,
                            'llm_response': llm_response
                        }
                        with TRANSCRIPT_LOCK:
                            TRANSCRIPT_LOG.append(transcript_entry)
                            # Keep only the last 20 entries
                            if len(TRANSCRIPT_LOG) > 20:
                                TRANSCRIPT_LOG.pop(0)
                        print(f"[{speaker}]: {text}")

                        # Check for alert keywords in the transcript text
                        for word in text.lower().split():
                            if word in [kw.lower() for kw in CONFIG['alert_keywords']]:
                                alert_msg = f"Alert: Keyword '{word}' detected from {speaker}. Transcript: {text}"
                                print(alert_msg)
                                send_sms_alert(alert_msg)
            else:
                # Optionally process partial results (ignored here)
                _ = json.loads(recognizer.PartialResult())
    except Exception as e:
        print("Error processing audio:", e)
    finally:
        conn.close()

def tcp_listener():
    """
    Listen for incoming TCP connections on the specified port.
    Each connection (from the ESP32) is handled in its own thread.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_HOST, TCP_PORT))
    s.listen(1)
    print(f"TCP Server listening on port {TCP_PORT}...")
    try:
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            threading.Thread(target=process_audio_stream, args=(conn,), daemon=True).start()
    except Exception as e:
        print("TCP listener error:", e)
    finally:
        s.close()

# ------------------ Flask Web Endpoints ------------------

@app.route('/')
def index():
    """
    Serve a simple dashboard that displays the live transcription log and
    provides a form to update configuration (alert keywords, toggles, and LLM settings).
    """
    return '''
    <html>
    <head>
      <title>InfiniteRecon Dashboard</title>
      <script>
      async function fetchTranscripts() {
          const response = await fetch('/transcripts');
          const data = await response.json();
          let content = "";
          data.forEach(function(entry) {
              content += `<p><strong>${entry.timestamp} - ${entry.speaker}:</strong> ${entry.text}`;
              if(entry.llm_response) {
                  content += `<br><em>LLM:</em> ${entry.llm_response}`;
              }
              content += `</p>`;
          });
          document.getElementById("transcripts").innerHTML = content;
      }
      async function fetchConfig() {
          const response = await fetch('/config');
          const data = await response.json();
          document.getElementById("alert_keywords").value = data.alert_keywords.join(", ");
          document.getElementById("alerts_enabled").checked = data.alerts_enabled;
          document.getElementById("llm_enabled").checked = data.llm_enabled;
          document.getElementById("llm_provider").value = data.llm_provider;
      }
      async function updateConfig() {
          const alert_keywords = document.getElementById("alert_keywords").value.split(",").map(s => s.trim());
          const alerts_enabled = document.getElementById("alerts_enabled").checked;
          const llm_enabled = document.getElementById("llm_enabled").checked;
          const llm_provider = document.getElementById("llm_provider").value;
          const response = await fetch('/config', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  alert_keywords: alert_keywords,
                  alerts_enabled: alerts_enabled,
                  llm_enabled: llm_enabled,
                  llm_provider: llm_provider
              })
          });
          const data = await response.json();
          alert("Configuration updated!");
      }
      setInterval(fetchTranscripts, 2000);
      window.onload = function() {
          fetchTranscripts();
          fetchConfig();
      }
      </script>
    </head>
    <body>
      <h1>InfiniteRecon Dashboard</h1>
      <div id="transcripts">
        <p>Loading transcripts...</p>
      </div>
      <hr>
      <h2>Configuration</h2>
      <label for="alert_keywords">Alert Keywords (comma-separated):</label><br>
      <input type="text" id="alert_keywords" size="50"><br><br>
      <label for="alerts_enabled">SMS Alerts Enabled:</label>
      <input type="checkbox" id="alerts_enabled"><br><br>
      <label for="llm_enabled">LLM API Enabled:</label>
      <input type="checkbox" id="llm_enabled"><br><br>
      <label for="llm_provider">LLM Provider:</label>
      <select id="llm_provider">
        <option value="openai">OpenAI</option>
        <option value="deepseek">DeepSeek</option>
        <option value="anthropic">Anthropic</option>
      </select><br><br>
      <button onclick="updateConfig()">Update Configuration</button>
    </body>
    </html>
    '''

@app.route('/transcripts')
def transcripts():
    """Return the current transcript log as JSON."""
    with TRANSCRIPT_LOCK:
        return jsonify(TRANSCRIPT_LOG)

@app.route('/config', methods=['GET', 'POST'])
def config():
    """
    GET: Return the current configuration as JSON.
    POST: Update configuration settings (alert keywords, toggles, LLM provider) using JSON payload.
    """
    global CONFIG
    if request.method == 'GET':
        return jsonify(CONFIG)
    elif request.method == 'POST':
        data = request.get_json()
        if 'alert_keywords' in data:
            CONFIG['alert_keywords'] = data['alert_keywords']
        if 'alerts_enabled' in data:
            CONFIG['alerts_enabled'] = data['alerts_enabled']
        if 'llm_enabled' in data:
            CONFIG['llm_enabled'] = data['llm_enabled']
        if 'llm_provider' in data:
            CONFIG['llm_provider'] = data['llm_provider']
        return jsonify(CONFIG)

def start_flask():
    """Start the Flask web server on all interfaces at port 8000."""
    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

# ------------------ Main Entry Point ------------------

if __name__ == "__main__":
    # Start the TCP listener (for audio streaming) in a separate background thread.
    threading.Thread(target=tcp_listener, daemon=True).start()
    # Start the Flask web dashboard.
    start_flask()
