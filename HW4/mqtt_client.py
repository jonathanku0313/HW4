import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time
mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

t = np.arange(0,20,1)
tilt = []
temp = 1
i = 0

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    print(float(msg.payload))
    tilt.append(float(msg.payload))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

while i <= 20:
    mqttc.loop()
    time.sleep(1)
    i+=1

if i > 20:
    plt.figure()
    plt.stem(t,tilt)
    plt.xlabel('Time')
    plt.ylabel('Tilt')
    plt.show()

#Loop forever, receiving messages
#mqttc.loop_forever()

