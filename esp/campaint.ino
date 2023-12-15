/*
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com/esp32-cam-post-image-photo-server/
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*/

#include <Arduino.h>
#include <WiFi.h>
#define LOGGING
#include <HTTPClient.h>
#include <ArduinoJson.h> // Validacao de erros da API
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"
#include "esp_camera.h"

// ============
//  OUTROS
// ===============
//#define CAMERA_MODEL_AT_THINKER // Has PSRAM
//#include "camera_pins.h"

// ============
//   CONSTS PINAGEM
// ==============
const int botao = 2;
const int ledWifi = 13;
const int ledOpen = 12;
const int ledFlash = 4;


// ==============
//   WIFI CONSTANTES
// ================

const char* ssid = "2.4GEGV";
const char* password = "8H2F-6h8w00**!";


const String serverName = "192.168.0.35";   // Contem o endpoint para envio das fotos (deve ser o IP do local na rede)
const char* serverComp = "192.168.0.35";
const int serverPort = 5000;
const char* serverRoute = "/upload";     // ENDPOINT UPLOAD



WiFiClient client;


#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define PART_BOUNDARY "123456789000000000000987654321"

// CAMERA_MODEL_AI_THINKER
/*#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22*/

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); 
  Serial.begin(115200);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  // init with high specs to pre-allocate larger buffers
  if(psramFound()){
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 10;  //0-63 lower number means higher quality
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_CIF;
    config.jpeg_quality = 12;  //0-63 lower number means higher quality
    config.fb_count = 1;
  }
  
  // Inicia a câmera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // initial sensors are flipped vertically and colors are a bit saturated
  if (s->id.PID == OV3660_PID) {
    s->set_vflip(s, 1); // flip it back
    s->set_brightness(s, 1); // up the brightness just a bit
    s->set_saturation(s, -2); // lower the saturation
  }
  // drop down frame size for higher initial frame rate
  if(config.pixel_format == PIXFORMAT_JPEG){
    s->set_framesize(s, FRAMESIZE_QVGA);
  }

  pinMode(ledOpen, OUTPUT);
  pinMode(ledWifi, OUTPUT);
  pinMode(botao, INPUT_PULLUP);
  pinMode(ledFlash, OUTPUT);

  // =========
  //   INICIALIZA WIFI
  // =========

  //WiFi.mode(WIFI_STA);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);  
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(ledWifi, HIGH);
    delay(500);
    Serial.print(".");
    digitalWrite(ledWifi, LOW);
  }
  digitalWrite(ledWifi, HIGH); // Se conectado LED em HIGH
  Serial.println();
  Serial.print("ESP32-CAM IP Address: ");
  Serial.println(WiFi.localIP());

  sendPhoto(); 
}

void loop() {
  int leitura = digitalRead(botao);
  //Serial.println(leitura);
  if(leitura == HIGH){
    //pull up
  }else{
    //digitalWrite(campainhaPin, HIGH);
    //delay(440);
    //digitalWrite(campainhaPin, LOW);
    
    //um intervalo de 1,2 segundos para distancia
    for(int i = 0; i < 2; i++){
    	digitalWrite(ledOpen,HIGH);
      	delay(600);
      	digitalWrite(ledOpen,LOW);
    }
    //rotina da camera do esp
    sendPhoto();
  }
}

String sendPhoto() {
  String getAll;
  String getBody;

  // Inicializa pointer e tenta obter a foto
  camera_fb_t * fb = NULL;
  digitalWrite(ledFlash, HIGH);
  fb = esp_camera_fb_get();
  delay(140);
  digitalWrite(ledFlash, LOW);
  if(!fb) {
    Serial.println("Falhou na captura da foto");
    delay(1000);
    ESP.restart();
  }
  Serial.println("sucesso!");
  // Obtem o horario do evento
  //String horario = WiFi.getTime();

  // Enviar HTTP request
  HTTPClient http;
  http.begin("http://" + String(serverComp) + ":" + String(serverPort) + "/uploadesp");
  http.addHeader("Content-Type", "multipart/form-data");
  //http.addHeader("DateTime", horario);
  http.addHeader("Content-Disposition", "form-data; name=\"imagem\"");
  Serial.printf("Tentando enviar para %s", serverComp);
  // Enviar pacote
  int httpResponseCode = http.POST((uint8_t*)fb->buf, fb->len);
  // Se o codigo de resposta for 200 alguma coisa entao sucesso
  if (httpResponseCode / 100 == 2) {
    Serial.printf("Envio com sucesso, codigo: %d\n", httpResponseCode);
  } else if (httpResponseCode > 0){
    DynamicJsonDocument jsonDoc(1024); // Adjust the size according to your expected JSON response size
    deserializeJson(jsonDoc, http.getString());
    
    // Access the message field in the JSON response
    const char* message = jsonDoc["msg"];
    
    Serial.println("Erro: JSON Response Message: " + String(message));
  } else {

    Serial.printf("Envio com erro, codigo: %d\n", httpResponseCode);
  }

  // Libera conexao HTTP e libera o buffer da Camera do esp
  http.end();
  esp_camera_fb_return(fb);
  return "true";
}