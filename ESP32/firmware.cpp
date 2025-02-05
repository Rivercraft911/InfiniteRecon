/***** ESP32-S3 Audio Streaming Sketch *****/
#include <WiFi.h>
#include <WiFiClient.h>
#include "driver/i2s.h"

// ======= Wi-Fi Settings =======
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ======= Raspberry Pi Server Settings =======
const char* serverIP = "192.168.1.100";  // Replace with your Pi's IP address
const uint16_t serverPort = 5000;

// ======= I2S Settings for INMP441 =======
#define I2S_SAMPLE_RATE   16000
#define I2S_SAMPLE_BITS   I2S_BITS_PER_SAMPLE_16BIT
#define I2S_CHANNEL_NUM   1

// I2S pin assignments (change as needed for your board)
#define I2S_WS  15   // Word Select (LRCLK)
#define I2S_SCK 14   // Serial Clock (SCK)
#define I2S_SD  13   // Serial Data (SD)

WiFiClient client;

void setupWiFi() {
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected!");
}

void setupI2S() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = I2S_SAMPLE_RATE,
    .bits_per_sample = I2S_SAMPLE_BITS,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = 0, 
    .dma_buf_count = 8,
    .dma_buf_len = 64,
    .use_apll = false,
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = -1,  
    .data_in_num = I2S_SD
  };

  // Install and start I2S driver
  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

void setup() {
  Serial.begin(115200);
  setupWiFi();
  setupI2S();

  // Connect to the Raspberry Pi server
  Serial.print("Connecting to server...");
  if (client.connect(serverIP, serverPort)) {
    Serial.println(" connected!");
  } else {
    Serial.println(" failed to connect!");
  }
}

void loop() {
  // Buffer to hold the audio samples
  int16_t i2sData[64];  
  size_t bytesRead = 0;

  // Read audio data from I2S
  esp_err_t result = i2s_read(I2S_NUM_0, &i2sData, sizeof(i2sData), &bytesRead, portMAX_DELAY);
  if(result == ESP_OK && bytesRead > 0) {
    // Send the raw audio bytes to the server
    client.write((uint8_t*)i2sData, bytesRead);
  }
}
