import board
import neopixel
import paho.mqtt.client as paho

# callback executed when a new MQTT message is received
# Check the msg object and take a corresponding action
def on_message(mosq, obj, msg):
    receivedPayload = str(msg.payload)
    print("%s" % receivedPayload)
    mosq.publish('home/office/LED/state', 'msg.payload', 0)

    if "ON" in receivedPayload:
        pixels.fill((0, 0, 255))
    else:
        pixels.fill((0, 0, 0))

# callback executed when a new MQTT message is send
def on_publish(mosq, obj, mid):
    pass

# define neopixel object. It is connected to 
# D12 pin and the size of the strip is 30 pixels
# TODO make the arguments configurable
pixels = neopixel.NeoPixel(board.D12, 30)

# define MQTT client object and corresponding callbacks
client = paho.Client()
client.on_message = on_message
client.on_publish = on_publish

# connect to the broker
# used broker is Mosquitto. More information on the following link:
# https://mosquitto.org
# It is currently installed on a linux server
# TODO make the following arguments configurable
client.connect("192.168.0.102", 1883, 60)

# subscribe to the topic for controlling the LEDs state
# possible states are ON and OFF
client.subscribe("home/office/LED", 0)

# endless loop to wait for MQTT messages
while client.loop() == 0:
    pass
