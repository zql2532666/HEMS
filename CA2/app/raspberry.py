from time import sleep, mktime
import time as t
import sys
import os
from DbAccess import *
from Mqtt import *
import serial
from threading import Thread
import Adafruit_DHT
from gpiozero import LED, Buzzer
import telepot
from rpi_lcd import LCD
from threading import Lock
from datetime import datetime as dt


basedir = os.path.abspath(os.path.dirname(__file__))
config = ConfigParser()
config.read(os.path.join(basedir, 'config.conf'))

""" SENSORS CONFIG"""
SENSOR_DHT11_PIN = int(config['SENSOR-DHT11']['PIN'])
SENSOR_LED_PIN = int(config['SENSOR-LED']['PIN'])
SENSOR_BUZZER_PIN = int(config['SENSOR-BUZZER']['PIN'])
SENSOR_BUTTON_PIN = int(config['SENSOR-BUTTON']['PIN'])
SENSOR_LIGHT_SERIAL_PORT = config['SENSOR-LIGHT']['SERIAL_PORT']
SENSOR_LIGHT_BAUDRATE = int(config['SENSOR-LIGHT']['BAUDRATE'])


serial = serial.Serial(SENSOR_LIGHT_SERIAL_PORT, SENSOR_LIGHT_BAUDRATE)  #change ACM number as found from ls /dev/tty/ACM*
serial.baudrate=SENSOR_LIGHT_BAUDRATE


# Initialise AWS MQTT Publisher 
mqtt_publisher = MQTTPublisher()

led = LED(SENSOR_LED_PIN)
buzzer = Buzzer(SENSOR_BUZZER_PIN)

lock = Lock()

my_bot_token = '1478147032:AAHHhcMUfsMvt5JkK9jLmQL_k1zubcYlJkY'
chat_id = 961348895 # own chat id from bot

realtime_dict = {
                    'light': 0,
                    'temperature': 0,
                    'humidity': 0
                }

gobal_dict = { "alarm": None, "rang": False }

def ledOn():
    led.on()
    return "LED turned on"

def ledOff():
    led.off()
    return "LED turned off"

def ledStatus():
    if led.is_lit:
        return 'on'
    else:
        return 'off'



def run_light_sensor():
    print("run_light_sensor()")
    try:
        update = True
        while update:
            try:
                read_serial = serial.readline() # read data sent from arduino
                light_value = read_serial.decode('ASCII').strip() # converts byte to string

                if light_value is not None:
                    lock.acquire()
                    result_value = mqtt_publisher.publish_light_data(light_value) # publish the light value to aws via mqtt and store in dynamodb

                    if result_value == True:
                        print(f"stored light value: {light_value}")

                    realtime_dict["light"] = light_value  # update realtime_dict
                    lock.release()
                    sleep(5)

            except KeyboardInterrupt:
                update = False

            except:
                print("Error while inserting light data...")
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])

    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])




def run_dht11_sensor():
    print("run_dht11_sensor()")
    try:
        update = True
        while update:
            try:
                humidity, temperature = Adafruit_DHT.read_retry(11, SENSOR_DHT11_PIN)

                if humidity is not None and temperature is not None:
                    lock.acquire()
                    result_value = mqtt_publisher.publish_dht11_data(humidity, temperature)  # publish the dht 11 values to aws via mqtt and store in dynamodb

                    if result_value == True:
                        print("\n")
                        print(f"stored humidity: {humidity}")
                        print(f"stored temperature: {temperature}")
                        print("\n")

                    realtime_dict["humidity"] = humidity  # update realtime_dict
                    realtime_dict["temperature"] = temperature  # update realtime_dict
                    lock.release()
                    sleep(2)

            except KeyboardInterrupt:
                update = False

            except:
                print("Error while inserting dht11 data...")
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])



# def lcd():
#    lcd = LCD()

#    dti = mktime(dt.now().timetuple())

#    while 1:
#        ndti = mktime(dt.now().timetuple())
#        if dti < ndti:
#            dti = ndti
#            lcd.clear()
#            lcd.text(dt.now().strftime('%b %d %Y'), 1)
#            lcd.text(dt.now().strftime('%H:%M:%S'), 2)
#            sleep(0.95)
#        else:
#            sleep(0.01)



'''
TELEGRAM BOT CODE 

def start_tele_bot():

    send_alert = False # prevent sending alert the first loop

    # Bot commands
    def respondToMsg(msg):
        command = msg['text']

        print('Got command: {}'.format(command))

        if command == 'onLED':
            bot.sendMessage(chat_id, ledOn())
        elif command =='offLED':
            bot.sendMessage(chat_id, ledOff())

    bot = telepot.Bot(my_bot_token)
    bot.message_loop(respondToMsg)
    print('Listening for RPi commands...')

    while True:
        # Unusual data alerts
        if int(realtime_dict["light"]) < 60 and send_alert:
            bot.sendMessage(chat_id, "Unusual light value detected. Current light value: {}".format(realtime_dict["light"]))
            # trigger buzzer for 5s if unusual data recorded
            buzzer.on()

        now = dt.now() # get current time

        ###### ALARM SYSTEM ##########
        # get time of set alarm (if alarm is set)
        if gobal_dict["alarm"] is not None:
            alarm_array = gobal_dict["alarm"].split(":")
            alarm_set = now.replace(hour=int(alarm_array[0]), minute=int(alarm_array[1]), second=int(alarm_array[2]), microsecond=0) 

            # if current time equal or exceed alarm time start actions
            if alarm_set <= now:
                start_time = time.time()
                seconds = 10

                # if alarm has not rang and light sensor value within threshold
                while not gobal_dict["rang"] and int(realtime_dict["light"]) < 100:

                    current_time = time.time()
                    elapsed_time = current_time - start_time

                    buzzer.on()
                    bot.sendMessage(chat_id, "Wake up! Alarm set for {} ringing".format(gobal_dict["alarm"]))
                    sleep(0.5)
                    buzzer.off()
                    buzzer.on()
                    bot.sendMessage(chat_id, "Wake up! Alarm set for {} ringing".format(gobal_dict["alarm"]))
                    sleep(0.5)
                    buzzer.off()

                    if elapsed_time > seconds:
                        gobal_dict["rang"] = True
                        gobal_dict["alarm"] = None
                        break

                gobal_dict["rang"] = True # disable alarm after alarm set exceed current time
                gobal_dict["alarm"] = None

        send_alert = True

        sleep(2)

        buzzer.off()
'''