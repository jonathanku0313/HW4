import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import time
mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

t = np.arange(0,18,1)
r = np.arange(0,18,1)
i = 0

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    global i
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
    print(float(msg.payload))
    print(i)
    r[i] = float(msg.payload)
    i += 1

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

while True:
    mqttc.loop()
    if i >= 18:
        plt.figure()
        plt.plot(t,r)
        plt.xlabel('timestamp')
        plt.ylabel('number')
        plt.title("# collected data plot")
        plt.show()
        break

#Loop forever, receiving messages
#mqttc.loop_forever()

