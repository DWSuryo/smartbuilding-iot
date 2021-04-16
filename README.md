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
3. MQTT-based communication
4. Database driven sensor values

## Planned Features
1. Camera: human detection and counter. Counter used for device auto input (currently using dummy)
2. Add energy management (energy, power, current sensor)
## Platform
Python Flask + virtualenv
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
## Publishing MQTT (dummy)
run this file on python:
```
python mqtt_pub_test_group
```

## Create database (locally: SQLite3)
Use **python shell** ([source](https://github.com/CoreyMSchafer/code_snippets/issues/75))

```
from flask_blog import create_app
app = create_app()
app.app_context().push()
from flask_blog import db
db.create_all()
```
## Run app
Make sure add database first    
powershell:
```
python run.py
```
# Where I learn (+ code references)
- [Corey Schafer: Flask Tutorial](https://www.youtube.com/watch?v=QnDWIZuWYW0&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=2) + [Github](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)
- [Rui Santos: ESP8266 Tutorial with Flask](https://randomnerdtutorials.com/esp8266-publishing-dht22-readings-with-mqtt-to-raspberry-pi/#more-31752)
- [Shane Lynn: Simple Asynchronous Flask](https://www.shanelynn.ie/asynchronous-updates-to-a-webpage-with-flask-and-socket-io/)
