# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime as datetime
from time import sleep
import json
from configparser import ConfigParser
import os 


DEVICE_ID = config['RASPBERRY-PI']['DEVICE_ID']
DEVICE_NAME = config['RASPBERRY-PI']['RONGTAO_PI']
AWS_HOST = config['AWS']['HOST']
ROOT_CA_PATH = config['AWS']['ROOT_CA_PATH']
CERTIFICATE_PATH =  config['AWS']['CERTIFICATE_PATH']
PRIVATE_KEY_PATH = config['AWS']['PRIVATE_KEY_PATH']
MQQT_PORT = int(config['AWS']['MQQT_PORT'])
DHT11_TOPIC = config['AWS']['DHT11_TOPIC']
LIGHT_TOPIC = config['AWS']['LIGHT_TOPIC']


mqtt_client = AWSIoTMQTTClient(DEVICE_NAME)
mqtt_client.configureEndpoint(host, 8883)
mqtt_client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
mqtt_client.connect()


def publish_light_data(light_value):
    pass

def publish_dht11_data(temperature, humidity):
    pass



while True:
      light = random.randint(0,500)

      message = {}
      message["device_id"] = "2"
      
      now = datetime.datetime.now()
      message["date_time"] = now.isoformat()      
      message["light_value"] = light
  
      mqtt_client.publish("sensors/light", json.dumps(message), 1)
      sleep(5) 



# mqtt_client.subscribe("sensors/light", 1, customCallback)
# sleep(2)

# Publish to the same topic in a loop forever
# Custom MQTT message callback
# def customCallback(client, userdata, message):
#	print("Received a new message: ")
#	print(message.payload)
#	print("from topic: ")
#	print(message.topic)
#	print("--------------\n\n")