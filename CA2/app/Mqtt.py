# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime as datetime
from time import sleep
import json
import random
from configparser import ConfigParser
import os 


basedir = os.path.abspath(os.path.dirname(__file__))
config = ConfigParser()
config.read(os.path.join(basedir, 'config.conf'))

DEVICE_ID = config['RASPBERRY-PI']['DEVICE_ID']
DEVICE_NAME = config['RASPBERRY-PI']['DEVICE_NAME']
AWS_HOST = config['AWS']['HOST']
ROOT_CA_PATH = config['AWS']['ROOT_CA_PATH']
CERTIFICATE_PATH =  config['AWS']['CERTIFICATE_PATH']
PRIVATE_KEY_PATH = config['AWS']['PRIVATE_KEY_PATH']
MQTT_PORT = int(config['AWS']['MQTT_PORT'])
DHT11_TOPIC = config['AWS']['DHT11_TOPIC']
LIGHT_TOPIC = config['AWS']['LIGHT_TOPIC']
FACIAL_RECOGNITION_TOPIC = config['AWS']['FACIAL_RECOGNITION_TOPIC']


class MQTTPublisher:

    def __init__(self):
        self.client = AWSIoTMQTTClient(DEVICE_NAME)
        self.client.configureEndpoint(AWS_HOST, 8883)
        self.client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec

        self.client.connect() # Connect to AWS IoT


    # method to publish dht 11 data to aws via mqtt protocol
    def publish_dht11_data(self, humidity, temperature):
        dht11_data = dict()
        dht11_data['device_id'] = DEVICE_ID
        dht11_data['date_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dht11_data['device_name'] = DEVICE_NAME
        dht11_data['temperature'] = temperature
        dht11_data['humidity'] = humidity
        result_value = self.client.publish(DHT11_TOPIC, json.dumps(dht11_data), 1) # Returns True if the publish request has been sent to aws broker. False if the request did not reach
        return result_value


    # method to publish light sensor data to aws via mqtt protocol
    def publish_light_data(self, light_value):
        light_data = dict()
        light_data['device_id'] = DEVICE_ID
        light_data['date_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        light_data['device_name'] = DEVICE_NAME
        light_data['light_value'] = light_value
        result_value = self.client.publish(LIGHT_TOPIC, json.dumps(light_data), 1)  # Returns True if the publish request has been sent to aws broker. False if the request did not reach
        return result_value


    def publish_facial_recognition_data(self, image_path, access):
        facial_recognition_data = dict()
        facial_recognition_data['device_id'] = DEVICE_ID
        facial_recognition_data['date_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        facial_recognition_data['device_name'] = DEVICE_NAME
        facial_recognition_data['image_path'] = image_path
        facial_recognition_data['access'] = access
        result_value = self.client.publish(FACIAL_RECOGNITION_TOPIC, json.dumps(facial_recognition_data), 1)  # Returns True if the publish request has been sent to aws broker. False if the request did not reach
        return result_value

    


image_path = "detection_images/RONGTAO_PI/2020-02-20 13:54:00.jpg"
access = "aaron"

mqtt_publisher = MQTTPublisher()
result_value = mqtt_publisher.publish_facial_recognition_data(image_path, access)
print(result_value)




    
