import board
import neopixel
import paho.mqtt.client as paho
import mqttData
import atexit
import json

# Callback executed when a new MQTT message is received
# Check the msg object and take a corresponding action
def on_message(mosq, obj, msg):
    # received payload is in json format, so it needs to be
    # converted to a python specific format (dict.)
    receivedPayload = json.loads(msg.payload)
    receivedTopic = str(msg.topic)
    print("%s - %s" % (receivedTopic, receivedPayload))

    # Check if received topic is Turn On/Off request
    if receivedTopic == mqttData.commandTopic:
        # Publish the newly set state
        client.publish(mqttData.stateTopic, msg.payload, 0, True)

        if len(receivedPayload) == 1:
            if 'state' in receivedPayload.keys():
                if receivedPayload['state'] == 'ON':
                    pixels.fill((mqttData.defaultRedValue, mqttData.defaultGreenValue, mqttData.defaultBlueValue))
                else:
                    pixels.fill((0, 0, 0))
        elif len(receivedPayload) == 2:
            if 'color' in receivedPayload.keys():
                print("change color")
                colorDictionary = receivedPayload['color']
                mqttData.redValue = colorDictionary['r']
                mqttData.greenValue = colorDictionary['g']
                mqttData.blueValue = colorDictionary['b']
                newRedValue = (mqttData.redValue * mqttData.brightnessValue) / 100
                newGreenValue = (mqttData.greenValue * mqttData.brightnessValue) / 100
                newBlueValue = (mqttData.blueValue * mqttData.brightnessValue) / 100
                pixels.fill((newRedValue, newGreenValue, newBlueValue))
            elif 'brightness' in receivedPayload.keys():
                print("change brightness")
                mqttData.brightnessValue = receivedPayload['brightness']
                newRedValue = (mqttData.redValue * mqttData.brightnessValue) / 100
                newGreenValue = (mqttData.greenValue * mqttData.brightnessValue) / 100
                newBlueValue = (mqttData.blueValue * mqttData.brightnessValue) / 100
                pixels.fill((newRedValue, newGreenValue, newBlueValue))
            else:
                print("unknown data!")
        else:
            print("Received data size is too big!")


# callback executed when a new MQTT message is send
def on_publish(mosq, obj, mid):
    print("topic published!")

def on_connect(client, userdata, flags, rc):
    # Notify clients that the LEDs are available
    client.publish(mqttData.availability_topics, "online")

# This callback will be executed when the script execution is interrupted
def exit_handler():
    pixels.fill((0, 0, 0))
    # Notify clients that the LEDs are not available anymore
    topicPayload = {'state': 'OFF'}
    topicPayloadEncoded = json.dumps(topicPayload).encode('utf-8')
    client.publish(mqttData.stateTopic, topicPayloadEncoded, 0, True)
    client.publish(mqttData.availability_topics, "offline")

# register handler to be executed on exit
atexit.register(exit_handler)

# define neopixel object. It is connected to 
# D12 pin and the size of the strip is 30 pixels
pixels = neopixel.NeoPixel(board.D12, 30)

# define MQTT client object and corresponding callbacks
client = paho.Client()
client.on_message = on_message
client.on_publish = on_publish
client.on_connect = on_connect

# connect to the broker
# used broker is Mosquitto. More information on the following link:
# https://mosquitto.org
# It is currently installed on a linux server
# TODO make the following arguments configurable
client.connect(mqttData.host, 1883, 60)

# subscribe to the topic for controlling the LEDs state
client.subscribe("home/office/LED", 0)

# endless loop to wait for MQTT messages
client.loop_forever()
