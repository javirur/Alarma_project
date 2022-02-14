#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#define DHTTYPE DHT11 
#define DHTPin D4
DHT dht(DHTPin, DHTTYPE);

 
const char* ssid = "wifi";
const char* password = "yayaya";
const char* mqtt_server = "ip";
  String hstr;
  String tempstr;
  boolean comphum=true;
  boolean comptemp=true;
float temp;
float h;
int comptemp2;
int comphum2;
 
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
String puertoin_str;
char ppuertoin[5];
int value = 0;
String puertoin,puertoin2;
float aux=0;


 
void setup() {

  Serial.begin(9600);
  setup_wifi();
  dht.begin();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  //Pin digital 3 para el echo del sensor
  pinMode(D1, OUTPUT); //pin como salida
  pinMode(D2, INPUT);  //pin como entrada
  digitalWrite(D1, LOW);//Inicializamos el pin con 0
}
 
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
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
 
void callback(char* topic, byte* message, unsigned int length) {
  String messageTemp;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];}

   if (String(topic) == "m1/subtemp") {
    if(messageTemp == "on"){
        comptemp2=15;
  }}
  if (String(topic) == "m1/subhum") {
    if(messageTemp == "on"){
        comphum2=15;
  }}
 
}
 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client","javierruiz","Javier14")) {
      Serial.println("connected");
      client.subscribe("m1/subtemp");
      client.subscribe("m1/subhum");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
 
void loop() {
  long t; //timepo que demora en llegar el eco
  long d;
  long d2;
  long d3;//distancia en centimetros

  digitalWrite(D1, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(D1, LOW);
  
  t = pulseIn(D2, HIGH); //obtenemos el ancho del pulso
  d = d2;
  d2 = d3;
  d3 = t/59;             //escalamos el tiempo a una distancia en cm
  h = dht.readHumidity();
  temp= dht.readTemperature();
  String strtemp = String(temp);
  String strhum = String(h);
   
 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  if(comptemp2==15){
  client.publish("m1/temperatura",strtemp.c_str());
  comptemp2=0;
  }
  if(comphum2==15){
  client.publish("m1/humedad", strhum.c_str());
  comphum2=0;}
  
  if (d<=20 && d2<=20 && d3<=20) {
    //  puertoin=Serial.readString() ;
   // puertoin.toCharArray(ppuertoin, 5);
    client.publish("m1/lampara","puertaabierta");
    
    delay(20000);}
}
