# https://www.emqx.io/blog/how-to-use-mqtt-in-python
# You can change MQTT broker with its username and password

import paho.mqtt.client as mqttc
import random
import time
import json

broker = 'mqtt.lunar-smart.com'
# broker = 'localhost'
port = 8883
# port = 1883
# topic1 = "/esp8266/temperature"
# topic2 = "/esp8266/humidity"
# topic3 = "/esp8266/kwh"
#topic4 = "45856/esp8266/sensors"
topic5 = '45856/test/auto'
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'lunar'
password = 'smartsystem'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqttc.Client(client_id)
    client.username_pw_set(username, password)    #set user pass
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        rng1 = round(random.uniform(0,100),2)
        rng2 = round(random.uniform(0,100),2)
        rng3 = round(random.uniform(0,300),2)
        left = random.randint(0,4)
        right = random.randint(0,4)
        # JSON data
        esp_sensor={
            'temperature1' : rng1,
            'humidity1' : rng2,
            'kwh1' : rng3
        }
        cam_sensor={
            'left' : left,
            'right' : right
        }
        print(esp_sensor, type(esp_sensor))
        print(cam_sensor, type(cam_sensor))
        print("convert to JSON")
        esp_sensor_out = json.dumps(esp_sensor)
        cam_sensor_out = json.dumps(cam_sensor)
        print(esp_sensor_out, type(esp_sensor_out))
        print(cam_sensor_out, type(esp_sensor_out))

        
        msg = f"messages: {msg_count}"
        # result = client.publish(topic1, rng1)
        # result = client.publish(topic2, rng2)
        # result = client.publish(topic3, rng3)
        #result = client.publish(topic4, esp_sensor_out)
        result = client.publish(topic5, cam_sensor_out)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            # print(f"Send `{msg}` to topic `{topic1}`: {rng1}")
            # print(f"Send `{msg}` to topic `{topic2}`: {rng2}")
            # print(f"Send '{msg}' to topic '{topic3}': {rng3}")
            #print(f"Send '{msg}' to topic '{topic4}': {esp_sensor_out}")
            print(f"Send '{msg}' to topic '{topic5}': {cam_sensor_out}\n")
        else:
            # print(f"Failed to send message to topic {topic1} {topic2} {topic3}")
            print(f"Failed to send message")
        time.sleep(5)
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    print("starting program")
    run()