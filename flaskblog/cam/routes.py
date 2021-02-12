import os
from flask import render_template, url_for, flash, redirect, request, abort, Response, Blueprint
from flaskblog.cam.camera import VideoCamera
import cv2
import paho.mqtt.client as mqtt
from flask_socketio import SocketIO, emit
#from flask_cors import CORS

cam = Blueprint('cam', __name__)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/esp8266/temperature")
    client.subscribe("/esp8266/humidity")

# The callback for when a PUBLISH message is received from the ESP8266.
def on_message(client, userdata, message):
   #socketio.emit('my variable')
   print("Received message '" + str(message.payload) + "' on topic '"
      + message.topic + "' with QoS " + str(message.qos))
   if message.topic == "/esp8266/temperature":
      print("temperature update")
      socketio.emit('dht_temperature', {'data': message.payload})
   if message.topic == "/esp8266/humidity":
      print("humidity update")
      socketio.emit('dht_humidity', {'data': message.payload})

mqttc=mqtt.Client(client_id="capstone")
#mqttc=mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv31)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("localhost",1883,60)
mqttc.loop_start()

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   4 : {'name' : 'GPIO 4', 'board' : 'esp8266', 'topic' : 'esp8266/4', 'state' : 'False'},
   5 : {'name' : 'GPIO 5', 'board' : 'esp8266', 'topic' : 'esp8266/5', 'state' : 'False'}
   }

# Put the pin dictionary into the template data dictionary:
templateData = {
   'pins' : pins
   }

# to camera page
@cam.route("/")
def camera():
    return render_template('camera.html', title='Camera', **templateData)

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
