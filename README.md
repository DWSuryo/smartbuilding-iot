# smartbuilding-iot
Project for making Smart building IoT. Contains Show camera, temperature sensor, led auto/manual input

## Goal
- Make a full functioning dashboard for IoT command center:

## Device Nodes
- IP Camera (RTSP-based)
- NodeMCU ESP8266 (sensor/actuator)
  - LED
  - DHT11 Temperature sensor

## Main Features
1. Dashboard for each room
   - Camera
   - Node indicator and control
   - Room Info
   - Graphs: temperature and energy
2. Account system
   - For full authorization in dashboard
3. MQTT-based communication (Paho MQTT)
4. csv-stored sensor values and visualization (amcharts 4)

## Planned Features
1. Camera: person detection and counter. Counter used for device auto input (currently using dummy)
## Platform
Python Flask + virtualenv. Code based on [[1](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog),[3](https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/)]
# Setup 
## Virtualenv (venv) and python libraries
Use powershell:
```
virtualenv <folder>
cd <folder>
.\Scripts\activate
pip install -r requirements.txt
```
for example, i use `dashboard` as venv folder (without <>)

## MQTT Setup
go to ```credential.ini``` in root, Fill your MQTT broker. Besides fill the SECRET_KEY. For basic secret key, you can do (python shell):
```
import secrets
secrets.token_hex(16)
```
Copy and paste the token to SECRET_KEY
## Publishing MQTT (dummy)
run this file on python:
```
python mqtt_pub_test_group
```
## Publishing MQTT (ESP8266)
The code uses Arduino IDE. For schematic, refer to this page [[2](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-with-mqtt-to-raspberry-pi/#more-31752)]. Then, upload .ino file to ESP

## Create database (locally: SQLite3)
Use **python shell** ([source](https://github.com/CoreyMSchafer/code_snippets/issues/75))

```
from flaskblog import create_app
app = create_app()
app.app_context().push()
from flaskblog import db
db.create_all()
```
## Run app
Make sure add database first    
powershell:
```
python run.py
```
# References + code
1. [Corey Schafer: Flask Tutorial](https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2) + [Github](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)
2. [Rui Santos: ESP8266 Tutorial with Flask](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-with-mqtt-to-raspberry-pi/#more-31752)
3. [Shane Lynn: Simple Asynchronous Flask](https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/)
