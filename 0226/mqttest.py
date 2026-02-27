import paho.mqtt.client as mqtt

def on_connect(client, userdara, flags, rc):
    print("Connected with result code"+str(rc))
    client.subscribe("test")

def on_message(client, userdara, msg):
    print(msg.topic+": "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)
client.loop_forever()

