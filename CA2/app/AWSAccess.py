# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import datetime as datetime
from time import sleep
import json
import random
from configparser import ConfigParser
import os 

# test imports for sensors, will remove
import Adafruit_DHT
import serial


class MQTTPublisher:

    def __init__(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        config = ConfigParser()
        config.read(os.path.join(basedir, 'config.conf'))

        self.DEVICE_ID = config['RASPBERRY-PI']['DEVICE_ID']
        self.DEVICE_NAME = config['RASPBERRY-PI']['DEVICE_NAME']
        self.AWS_HOST = config['AWS']['HOST']
        self.ROOT_CA_PATH = config['AWS']['ROOT_CA_PATH']
        self.CERTIFICATE_PATH =  config['AWS']['CERTIFICATE_PATH']
        self.PRIVATE_KEY_PATH = config['AWS']['PRIVATE_KEY_PATH']
        self.MQTT_PORT = int(config['AWS']['MQTT_PORT'])
        self.DHT11_TOPIC = config['AWS']['DHT11_TOPIC']
        self.LIGHT_TOPIC = config['AWS']['LIGHT_TOPIC']

        self.client = AWSIoTMQTTClient(self.DEVICE_NAME)
        self.client.configureEndpoint(self.AWS_HOST, 8883)
        self.client.configureCredentials(self.ROOT_CA_PATH, self.PRIVATE_KEY_PATH, self.CERTIFICATE_PATH)

        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec

        self.client.connect() # Connect to AWS IoT


    # method to publish dht 11 data to aws via mqtt protocol
    def publish_dht11_data(self, humidity, temperature):
        dht11_data = dict()
        dht11_data['device_id'] = self.DEVICE_ID
        dht11_data['date_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dht11_data['device_name'] = self.DEVICE_NAME
        dht11_data['temperature'] = temperature
        dht11_data['humidity'] = humidity
        self.client.publish(self.DHT11_TOPIC, json.dumps(dht11_data), 1)


    # method to publish light sensor data to aws via mqtt protocol
    def publish_light_data(self, light_value):
        light_data = dict()
        light_data['device_id'] = self.DEVICE_ID
        light_data['date_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        light_data['device_name'] = self.DEVICE_NAME
        light_data['light_value'] = light_value
        self.client.publish(self.LIGHT_TOPIC, json.dumps(light_data), 1)
        


pin = 23
serial = serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
serial.baudrate = 9600
mqtt_publisher = MQTTPublisher()

while True:
    try:
        read_serial = serial.readline() # read data sent from arduino
        light_value = read_serial.decode('ASCII').strip() # converts byte to string

        if light_value is not None:
            print(f"light value: {light_value}")
            mqtt_publisher.publish_light_data(light_value)
            sleep(5)
        else:
            print('Failed to get light sensor Reading, trying again in 2 seconds')
    except:
        if not error:
            print("Error while getting data...")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            error = True