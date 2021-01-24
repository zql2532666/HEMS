from time import sleep, mktime
import time as t
import sys
from DbAccess import *
import serial
from threading import Thread
import Adafruit_DHT
from gpiozero import LED, Buzzer
import telepot
from rpi_lcd import LCD
from datetime import datetime as dt

serial = serial.Serial("/dev/ttyUSB0",9600)  #change ACM number as found from ls /dev/tty/ACM*
serial.baudrate=9600

# Initialise Database
db_access = DbAccess()

led = LED(17)
buzzer = Buzzer(27)

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

def get_data():
    global light_value
    error = False
    while True:
        try:
            read_serial = serial.readline() # read data sent from arduino
            light_value = read_serial.decode('ASCII').strip() # converts byte to string
            realtime_dict["light"] = light_value
            if __name__ == "__main__":
                print(light_value)
        except:
            realtime_dict["light"] = -1
            if not error:
                print("Error while getting data...")
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])
                error = True

def get_dht_data():
    pin = 23
    error = False
    while True:

        try:
            humidity, temperature = Adafruit_DHT.read_retry(11, pin)

            if humidity is not None and temperature is not None:
                realtime_dict["humidity"] = humidity
                realtime_dict["temperature"] = temperature
                if __name__ == "__main__":
                    print(f'Temp: {temperature} C')
                    print(f'Humidity: {humidity}')
            else:
                print('Failed to get DHT22 Reading, trying again in 2 seconds')

            # sleep(2)
        except:
            realtime_dict["humidity"] = -1
            if not error:
                print("Error while getting data...")
                print(sys.exc_info()[0])
                print(sys.exc_info()[1])
                error = True


def store_data():
    update = False

    sleep(2) # wait after light_value updated from thread 1 before start storing

    update = True

    while update:
        try:
            if realtime_dict["light"] == -1:
                continue

            result_value = db_access.insert_light_value(light_value)

            if __name__ == "__main__":
                if result_value == 1:
                    print(f"Light value {light_value} inserted.")
                
                print("Wait 2 secs before storing next light values..")

            sleep(2)

        except mysql.connector.Error as err:
            print(err)
        except:
            print("Error while inserting data...")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])

def lcd():
    lcd = LCD()

    dti = mktime(dt.now().timetuple())

    while 1:
        ndti = mktime(dt.now().timetuple())
        if dti < ndti:
            dti = ndti
            lcd.clear()
            lcd.text(dt.now().strftime('%b %d %Y'), 1)
            lcd.text(dt.now().strftime('%H:%M:%S'), 2)
            sleep(0.95)
        else:
            sleep(0.01)