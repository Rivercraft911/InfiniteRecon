# InfiniteRecon 

Have you ever wanted to start your ethically dubious surveillance empire? InfiniteRecon is a better Infinity transmitter than the ones old intelligence organizations used to use. This modern take on room monitoring brings high-tech features to your surveillance needs!

InfiniteRecon is a real-time audio streaming and analysis system built using an ESP32-S3 microcontroller with an INMP441 I2S MEMS microphone and a Raspberry Pi server. The system captures ambient room audio, streams it to the Raspberry Pi, and processes it for speech-to-text transcription, speaker identification, and topic-based alerting. A web dashboard running on the Raspberry Pi lets you view live transcriptions and configure alert keywords, SMS notifications, and optional LLM API integration.

## Features

- **Real-Time Audio Streaming:**  
  Streams raw 16-bit PCM audio at 16 kHz from the ESP32-S3 to the Raspberry Pi over TCP.
- **Speech-to-Text Conversion:**  
  Uses [Vosk](https://github.com/alphacep/vosk-api) for offline speech recognition.
- **Speaker Identification:**  
  (Placeholder) Identifies speakers from the audio stream.
- **Topic-Based Alerts:**  
  Monitors transcriptions for configurable keywords and sends SMS alerts via [Twilio](https://www.twilio.com/).
- **Web Dashboard:**  
  A Flask web server running on the Raspberry Pi displays live transcriptions and allows you to change configuration settings in real time.
- **LLM API Integration:**  
  Optionally integrates with LLM providers (OpenAI, DeepSeek, Anthropic) to enrich transcriptions. Easily toggle LLM usage and select the provider via the dashboard.

## Hardware Components

- **ESP32-S3 Microcontroller:**  
  Captures audio from the INMP441 microphone and streams it over Wi-Fi.
- **INMP441 I2S MEMS Microphone:**  
  Captures high-fidelity ambient audio.
- **Raspberry Pi:**  
  Receives audio, performs speech-to-text conversion, and hosts the web dashboard.

## Software Components

### Project Structure
```
infiniterecon/
├── esp32/                      # ESP32 firmware
│   └── infiniterecon.cpp       # Main ESP32 code
├── server/                     # Raspberry Pi server code
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration settings
│   ├── audio_processor.py     # Audio processing logic
│   ├── web_server.py         # Flask routes and dashboard
│   ├── alerts.py             # SMS alert functionality
│   ├── llm_handler.py        # LLM integration
│   └── templates/
│       └── index.html        # Dashboard template
├── .env.example              # Example environment variables
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Components Overview

- **ESP32-S3 Firmware:**  
  - Arduino-based firmware for audio capture and streaming
  - Located in `/esp32/infiniterecon.cpp`
  - Update with your Wi-Fi credentials and server IP

- **Raspberry Pi Server:**  
  - **TCP Listener & Audio Processing:**  
    Processes the incoming audio stream using Vosk
  - **SMS Alerts:**  
    Uses Twilio for keyword-triggered notifications
  - **Web Dashboard:**  
    Real-time monitoring and configuration interface

## Setup Instructions

### 1. Hardware Setup
- Wire the INMP441 microphone to ESP32-S3 (pinout details coming soon)
- Ensure Raspberry Pi is connected to your network

### 2. ESP32 Setup
1. Open `/esp32/infiniterecon.cpp` in Arduino IDE
2. Update Wi-Fi credentials and Raspberry Pi IP
3. Flash to ESP32-S3

### 3. Raspberry Pi Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/infiniterecon.git
   cd infiniterecon
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```

4. Required API Keys:
   - Twilio (for SMS alerts)
   - OpenAI/Anthropic/DeepSeek (for LLM features)

5. Start the server:
   ```bash
   python server/main.py
   ```

### 4. Accessing the Dashboard

- **Local Network:**  
  Access at `http://raspberry_pi_ip:8000`
  
- **Internet Access (Optional):**  
  Use ngrok for secure remote access:
  ```bash
  ngrok http 8000
  ```

## Security Notes

- Keep your `.env` file private and never commit it to repositories
- Be mindful of local privacy laws and regulations

## Future Plans

1. Integrate robust speaker diarization
2. Add support for analog microphones
3. Enhance LLM integration features
4. Optimize audio streaming for lower latency
5. Add user authentication to dashboard
6. Implement HTTPS encryption
7. Add rate limiting for API calls

## Contributing

Contributions are welcome! 

## Disclaimer

This project is for educational purposes only. Always comply with local laws and regulations regarding audio recording and surveillance. Obtain necessary permissions before deploying this system.

## 📄 License

[MIT License](LICENSE)
