import os
from flask import render_template, url_for, flash, redirect, request, abort, Response, Blueprint
from flaskblog.cam.camera import VideoCamera
from flaskblog import socketio
import cv2
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit
#from flask_cors import CORS
from datetime import datetime, date
import time, csv, json
import configparser

# import eventlet
# eventlet.monkey_patch()

cam = Blueprint('cam', __name__)
#socketio = SocketIO(cam, ping_interval=5, ping_timeout=10)
print("YOU ARE WOKRING ON:", os.getcwd())
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("/esp8266/temperature")
    # client.subscribe("/esp8266/humidity")
    # client.subscribe("/esp8266/kwh")
    client.subscribe("45856/esp8266/sensors")

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
    if not hasattr(on_message,'energy'):
        on_message.energy = 0
    if not hasattr(on_message,'tgl_temp'):
        on_message.tgl_temp = 0
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))
    # plain text receive
    '''
    if message.topic == "/esp8266/temperature":
        print("temperature update")
        socketio.emit('dht_temperature', {'data': message.payload})
    if message.topic == "/esp8266/humidity":
        print("humidity update")
        socketio.emit('dht_humidity', {'data': message.payload})
    if message.topic == "/esp8266/kwh":
        print("energy update")
        socketio.emit('energy_kwh', {'data': message.payload})
    '''
    # JSON receive and csv write
    if message.topic == "45856/esp8266/sensors":
        esp1 = str(message.payload.decode('utf-8'))
        print('received esp1 ', type(esp1))
        esp1_conv = json.loads(esp1)
        print('convert esp1 ', type(esp1_conv))
        print(f'esp1_conv: temp1 {esp1_conv["temperature1"]} --- hum1 {esp1_conv["humidity1"]} --- power1 {esp1_conv["power1"]}')
        print(type(esp1_conv['temperature1']), type(esp1_conv['humidity1']), type(esp1_conv['power1']))
        # socketio.emit('sensor1', {'data': message.payload})
        # csv write
        with open('./sensor_room1.csv', mode='a') as file:
            with open('./sensor_room1.csv', mode='r+', newline='') as file:
                reader = csv.reader(file, delimiter=",")
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                
                # set the date and compare
                tgl = datetime.now().replace(microsecond=0)
                print(f"{tgl.day} --- {on_message.tgl_temp}")
                if tgl.day != on_message.tgl_temp:
                    print("energy reset")
                    on_message.energy = 0
                on_message.tgl_temp = tgl.day

                power = float(esp1_conv["power1"])
                step = 5 # time step
                on_message.energy = round((on_message.energy + power/(3600/step)),2)

                # socketio emits energy
                # socketio.emit('esp_energy', {'data': on_message.energy})
                mqttc.publish("45856/esp8266/sensors/energy",on_message.energy)

                header = ['tgl','temp','hum','power','energy']
                row = [tgl,
                        # tgl.strftime("%x"),
                        # tgl.strftime("%X"),
                        esp1_conv["temperature1"],
                        esp1_conv["humidity1"],
                        esp1_conv["power1"],
                        #esp1_conv["energy1"],
                        on_message.energy
                        ]
                
                print(f'file opened: {esp1_conv["temperature1"]} --- {esp1_conv["humidity1"]} --- {esp1_conv["power1"]} --- {tgl}')
                #way to write to csv file
                #if temperature1 and humidity1 and power1:
                print(enumerate(reader))
                rowcount = sum(1 for num in reader)     #row count
                if rowcount == 0:
                    writer.writerow(header)
                    print('header written')
                writer.writerow(row)
                print("row written", rowcount)

cred=configparser.ConfigParser()
cred.read("credential.ini")
#print(cred.sections())         # test if file exists
mqttc=mqtt.Client(client_id="capstone")

broker = cred["MQTT-python"]["broker"]
port = int(cred["MQTT-python"]["port"])
username = cred["MQTT-python"]["user"]
password = cred["MQTT-python"]["pass"]

mqttc.username_pw_set(username, password)
#mqttc=mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(broker,port,60)
mqttc.loop_start()
'''
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : 'False'},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins
   }
'''
# to camera page
@cam.route("/")
@cam.route("/capstone")
@cam.route("/capstone/room1")
def camera():
    return render_template('room1_new.html', async_mode=socketio.async_mode, title='Room 1')

@cam.route("/capstone/room2")
def room2():
    return render_template('room2_new.html', async_mode=socketio.async_mode, title='Room 2')

@cam.route("/capstone/room3")
def room3():
    return render_template('room3_new.html', async_mode=socketio.async_mode, title='Room 3')

# stream camera
camera = cv2.VideoCapture(0)

# for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' 
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
'''
def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               '''
@cam.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#http request code page
'''
@app.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404
@app.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403
@app.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
'''
'''
#shutdown
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
'''
'''
@cam.route("/")
def main():
   # Pass the template data into the template main.html and return it to the user
   return render_template('camera.html', **templateData)
'''

# The function below is executed when someone requests a URL with the pin number and action in it:
# change to paho javascript later
'''
@cam.route("/<board>/<changePin>/<action>")
def action(board, changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   devicePin = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "1" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"1")
      pins[changePin]['state'] = 'True'

   if action == "0" and board == 'esp8266':
      mqttc.publish(pins[changePin]['topic'],"0")
      pins[changePin]['state'] = 'False'

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('camera.html', **templateData)
'''
# socketio response
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json data here: ' + str(json))
'''
@socketio.on('my event1')
def handle_my_temperature(json):
    print('received json temperature here: ' + str(json))

@socketio.on('my event2')
def handle_my_humidity(json):
    print('received json humidity here: ' + str(json))

@socketio.on('my event3')
def handle_my_energy(json):
    print('received json kwh here: ' + str(json))

@socketio.on('my sensor')
def handle_my_kwh(json):
   print('received json sensor here: ' + str(json))
'''