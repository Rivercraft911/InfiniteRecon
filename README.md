# InfiniteRecon
Have you ever wanted so start your ethically dubious survelence empire? Infinite Recon is A better Infinity transmitter than ones the old intelligence organizations used to use.

InfiniteRecon is a real-time audio streaming and analysis system built using an ESP32-S3 microcontroller with an INMP441 I2S MEMS microphone and a Raspberry Pi server. The system captures ambient room audio, streams it to the Raspberry Pi, and processes it for speech-to-text transcription, speaker identification, and topic-based alerting. A web dashboard running on the Raspberry Pi lets you view live transcriptions and configure alert keywords, SMS notifications, and optional LLM API integration using either OpenAI, DeepSeek, or Anthropic.

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

- **ESP32-S3 Firmware (Arduino):**  
  Configured to stream raw audio data over TCP to the Raspberry Pi. *(Update the code with your Wi-Fi credentials and server IP as needed.)*

- **Raspberry Pi Server (Python):**  
  - **TCP Listener & Audio Processing:**  
    Processes the incoming audio stream using Vosk, checks for alert keywords, and optionally calls an LLM API.
  - **SMS Alerts:**  
    Uses Twilio to send SMS alerts when a configured keyword is detected.
  - **Web Dashboard:**  
    A Flask web application provides a live transcript view and configuration controls (alert keywords, SMS alerts toggle, and LLM API options).

## Setup Instructions
TODO


### Future Plans

1. Integrate a robust speaker diarization system.
2. Update the hardware and software for support for analog microphones.
3. Implement actual API calls to the LLM providers with proper API key management and error handling.
4. Optimize the audio streaming protocol for even lower latency.
5. Enhance the web dashboard with user authentication for added security.


