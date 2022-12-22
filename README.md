# Description
Python project for controlling WS2812B LEDs using Raspberry Pi and MQTT protocol.

# Prerequisitives
1. MQTT broker installed on a local machine. If the broker is installed on a Linux server,
check the firewall permissions: https://mosquitto.org
2. MQTT client configured as a publisher, in order to be able to control the LEDs - for example
Home Assistant: https://www.home-assistant.io

# Configuration
1. After cloning, create a virtual environment using venv:
<b>python -m venv .venv</b>

2. Activate the newly created virtual environment:
<b>source .venv/bin/activate (for MAC and Linux users)</b>
<b>.venv/bin/activate.bat (for Windows users)</b>

3. Install packages locally in the environment:
<b>pip install -r requirements.txt</b>

3. If you install other project dependencies using pip, update the requirements.txt file:
<b>pip freeze > requirements.txt</b>

# Running the script
In order to work correctly, the script must be executed using sudo