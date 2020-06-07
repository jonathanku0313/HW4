import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import serial
import time

mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe    

t = np.arange(0,20,1)
r = np.arange(0,20,1)
x = np.arange(0,20,1)
y = np.arange(0,20,1)
z = np.arange(0,20,1)

# XBee setting

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, baudrate = 9600)

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

for i in range(0, 25):
    # send RPC to remote

    s.write("/getAcc/run\r".encode())
    time.sleep(1)
    
    if i > 5:
        line=s.readline()
        r[i-5] = float(line)
        line=s.readline() 
        x[i-5] = 1000*float(line)
        line=s.readline()  
        y[i-5] = 1000*float(line)
        line=s.readline() 
        z[i-5] = 1000*float(line)
        line=s.readline() 
        mqttc.publish(topic, line)

fig, ax = plt.subplots(2, 1)
ax[0].plot(t,r)
ax[0].set_xlabel('timestamp')
ax[0].set_ylabel('number')
ax[0].set_title("# collected data plot")
ax[1].plot(t,x/1000)
ax[1].plot(t,y/1000)
ax[1].plot(t,z/1000)
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Acc Vector')
plt.show()
s.close()
