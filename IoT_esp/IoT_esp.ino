/*****
 
 All the resources for this project:
 https://randomnerdtutorials.com/
 
*****/

// Loading the ESP8266WiFi library and the PubSubClient library
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// Change the credentials below, so your ESP8266 connects to your router
const char* ssid = "ssid_user";
const char* password = "ssid_pass";

// Change the variable to your Raspberry Pi IP address, so it connects to your MQTT broker
const char* mqtt_server = "192.168.X.X";

// MQTT Username & Password
const char* mq_username = "mq_user";
const char* mq_password = "mq_pass";
int port = 8883;

// Initializes the espClient
WiFiClient espClient;
PubSubClient client(espClient);

// Connect an LED to each GPIO of your ESP8266
const int ledGPIO5 = 5;
const int ledGPIO4 = 4;

//DHT11 setup
const int DHTPin = 14;
DHT dht(DHTPin, DHT11);

// Timers auxiliar variables
long now = millis();
long lastMeasure = 0;
// Don't change the function below. This functions connects your ESP8266 to your router
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

// This functions is executed when some device publishes a message to a topic that your ESP8266 is subscribed to
// Change the function below to add logic to your program, so when a device publishes a message to a topic that 
// your ESP8266 is subscribed you can actually do something
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic home/office/esp1/gpio2, you check if the message is either 1 or 0. Turns the ESP GPIO according to the message
  
  //receives trigger for activating auto/manual mode in ESP
  if(topic=="45856/test/trigger"){
    StaticJsonDocument<16> doc_trig;
    deserializeJson(doc_trig, message, length);
    int trigger = doc_trig["trigger"]; // 1
    Serial.print("Trigger received: ");
    Serial.print(trigger);
    if(trigger==1){
      Serial.print(" MANUAL MODE");
      client.unsubscribe("45856/test/auto");
      client.subscribe("45856/test/manual");
    }
    else if(trigger==0){
      Serial.print(" AUTO MODE");
      client.subscribe("45856/test/auto");
      client.unsubscribe("45856/test/manual");
    }
  }

  //manual mode logic
  if(topic=="45856/test/manual"){
    Serial.print("received manual: ");
    StaticJsonDocument<32> msg_manual;
    deserializeJson(msg_manual, message, length);
    int m_left = msg_manual["left"]; // 1
    int m_right = msg_manual["right"]; // 1
    //left logic
    if (m_left==1){
      digitalWrite(ledGPIO4, HIGH);
      Serial.print("GPIO4 1");
    }
    else if (m_left==0){
      digitalWrite(ledGPIO4, LOW);
      Serial.print("GPIO4 0");
    }
    Serial.print(" | ");
    
    //right logic
    if (m_right==1){
      digitalWrite(ledGPIO5, HIGH);
      Serial.print("GPIO4 1");
    }
    else if (m_right==0){
      digitalWrite(ledGPIO5, LOW);
      Serial.print("GPIO4 0");
    }
  }

  //auto mode logic
  if(topic=="45856/test/auto"){
    Serial.print("received auto: ");
    StaticJsonDocument<32> msg_auto;
    deserializeJson(msg_auto, message, length);
    /*
    DeserializationError error = deserializeJson(msg_auto, message);
    if (error) {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
    }
    */
    
    int left = msg_auto["left"]; // 1
    int right = msg_auto["right"]; // 1
    
    //left logic
    if (left>=1){
      digitalWrite(ledGPIO4, HIGH);
      Serial.print("GPIO4 ");
      Serial.print(left);
      Serial.print(" (ON)");
    }
    else if (left==0){
      digitalWrite(ledGPIO4, LOW);
      Serial.print("GPIO4 0 (OFF)");
    }
    Serial.print(" | ");
    
    //right logic
    if (right>=1){
      digitalWrite(ledGPIO5, HIGH);
      Serial.print("GPIO5 ");
      Serial.print(right);
      Serial.print(" (ON)");
    }
    else if (right==0){
      digitalWrite(ledGPIO5, LOW);
      Serial.print("GPIO5 0 (OFF)");
    }
  }
  Serial.println();
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
     /*
     YOU  NEED TO CHANGE THIS NEXT LINE, IF YOU'RE HAVING PROBLEMS WITH MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, you will have to give a unique name to the ESP8266.
     Here's how it looks like now:
       if (client.connect("ESP8266Client")) {
     If you want more devices connected to the MQTT broker, you can do it like this:
       if (client.connect("ESPOffice")) {
     Then, for the other ESP:
       if (client.connect("ESPGarage")) {
      That should solve your MQTT multiple connections problem

     THE SECTION IN loop() function should match your device name
    */
    if (client.connect("ESP8266Client", mq_username,mq_password)) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more LEDs in this example)
      client.subscribe("45856/test/auto");
      client.subscribe("45856/test/trigger");
      //client.subscribe("esp8266/5");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// synthetic RNG
float float_rand( float min, float max ){
  float scale = rand() / (float) RAND_MAX;  /* [0, 1.0] */
  float val = min + scale * ( max - min );  /* [min, max] */
  float val_dec = roundf(val * 100) / 100;  // 2 decimals
  return val_dec;
}

// The setup function sets your ESP GPIOs to Outputs, starts the serial communication at a baud rate of 115200
// Sets your mqtt broker and sets the callback function
// The callback function is what receives messages and actually controls the LEDs
void setup() {

  dht.begin();
  pinMode(ledGPIO4, OUTPUT);
  pinMode(ledGPIO5, OUTPUT);
  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, port);
  client.setCallback(callback);
}

// For this project, you don't need to change anything in the loop function. 
// Basically it ensures that you ESP is connected to your broker
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
     /*
     YOU  NEED TO CHANGE THIS NEXT LINE, IF YOU'RE HAVING PROBLEMS WITH MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, you will have to give a unique name to the ESP8266.
     Here's how it looks like now:
       client.connect("ESP8266Client");
     If you want more devices connected to the MQTT broker, you can do it like this:
       client.connect("ESPOffice");
     Then, for the other ESP:
       client.connect("ESPGarage");
      That should solve your MQTT multiple connections problem

     THE SECTION IN recionnect() function should match your device name
    */
    client.connect("ESP8266Client", mq_username,mq_password);
  now = millis();
  // Publishes new temperature and humidity every 5 seconds
  if (now - lastMeasure > 5000) {
    lastMeasure = now;
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float h = dht.readHumidity();
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();
    // Read temperature as Fahrenheit (isFahrenheit = true)
    float f = dht.readTemperature(true);
    // generate random number for kwh
    float kwh = float_rand(0,300);
    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t) || isnan(f) || isnan(kwh)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    // Computes temperature values in Celsius
    float hic = dht.computeHeatIndex(t, h, false);
    static char temperatureTemp[7];
    dtostrf(hic, 6, 2, temperatureTemp);
    
    // Uncomment to compute temperature values in Fahrenheit 
    // float hif = dht.computeHeatIndex(f, h);
    // static char temperatureTemp[7];
    // dtostrf(hic, 6, 2, temperatureTemp);
    
    static char humidityTemp[7];
    dtostrf(h, 6, 2, humidityTemp);

    // setup message encoding to json
    const int capacity = JSON_OBJECT_SIZE(3); // json object size
    StaticJsonDocument<capacity> doc;         // create doc json object
    doc["temperature1"] = t;
    doc["humidity1"] = h;
    doc["kwh1"] = kwh;
    char output[200];
    //serializeJson(doc,output);
    //const char* pub_msg = serializeJson(doc,output,measureJson(doc));  // to string
    serializeJson(doc,output,measureJson(doc)+1);  // to string
    //Serial.println(pub_msg);
    
    // publishes json message
    client.publish("45856/esp8266/sensors", output);

    Serial.print("Hum1: ");
    Serial.print(h);
    Serial.print(" | Temp1: ");
    Serial.print(t);
    Serial.print(" *C ");
    Serial.print(f);
    Serial.print(" *F ");
    Serial.print("| kWh1: ");
    Serial.print(kwh);
    Serial.print(" kWh");
    Serial.println();
    /*
    Serial.print("| Heat index: ");
    Serial.print(hic);
    Serial.println(" *C ");
    */
    // Serial.print(hif);
    // Serial.println(" *F");
  }
}
