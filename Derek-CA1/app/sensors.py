from gpiozero import MCP3008
from db_new import *
from time import sleep
import sys
from datetime import datetime
import Adafruit_DHT
import threading
from threading import Lock
from collections import deque
from rpi_lcd import LCD
from email_client import *
from twilio_client import *
import serial
import time
# db = DB()
lock = Lock()
light_deque = deque()
dht11_deque = deque()
lcd = LCD()
showDHT11DataOnLCD = False
showLightDataOnLCD = False
GMAIL_USERNAME = "spzawiot@gmail.com"
GMAIL_PASSWORD = "iloveIOT123"

TWILIO_SID = "ACc14127f85a8ba1af23949d90c04bc9a6"
TWILIO_TOKEN = "3c3c5ace80d0423990fb7de4466dc27c"
PHONE_NUM = "+12512629258"

SENSOR_DATA_COLLECTION_INTERVAL = 5
NOTIFICATION_INTERVAL_DHT11 = 300
NOTIFICATION_INTERVAL_LIGHT = 300

def run_light_sensor():
   print("run_light_sensor()")
   global light_deque
   db = DB()
   ser = serial.Serial('/dev/ttyUSB0', 9600)
   s = [0]
   old_time = 0
   noti_count = 0
   try:
      update = True
      while update:
         try:
            now = datetime.now()
            current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            # current_date_time = generate_current_date_time()
            s[0] = str(int(ser.readline(),16))          
            sensor_value = float(s[0])
            
            # print(f"storing sensor value: {sensor_value}:{current_date_time} in database")
            lock.acquire()
            db.store_light_data_to_db(sensor_value, current_date_time)
            if len(light_deque) != 0:
               light_deque.popleft()
            light_deque.append([sensor_value,current_date_time])
            lock.release()

            threshold_dict = db.retrieve_threshold()
            if sensor_value > threshold_dict["light"]:
               print("light value above threshold")
               current_time = time.time()
               if current_time - old_time >= NOTIFICATION_INTERVAL_LIGHT:
                  noti_count += 1 
                  print(f"NOTICOUNT : {noti_count}")
                  print("SENDING LIGHT NOTIFICATION")
                  msg = f"Light Value was detected to be above the threshold set!!!\nThreshold: {threshold_dict['light']}\nValue Detected: {sensor_value}\nDate: {current_date_time}"
                  print(msg)
                  send_notification_light(db,msg)
                  old_time = current_time
         except KeyboardInterrupt:
            update = False
         except:
            print("Error while inserting data...")
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
   except:
      print(sys.exc_info()[0])
      print(sys.exc_info()[1])



def generate_current_date_time():
   now = datetime.now()
   current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
   return current_date_time

def run_dht11_sensor():
   print("run_dht11_sensor()")
   db = DB()
   global dht11_deque
   pin = 4 
   update = True
   old_time = 0
   while update:
      try:
         humidity, temperature = Adafruit_DHT.read_retry(11, pin)
         now = datetime.now()
         current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
         lock.acquire()
         db.store_dht11_data_to_db(temperature, humidity, current_date_time)
         if len(dht11_deque) != 0:
            dht11_deque.popleft()
         dht11_deque.append([temperature,humidity, current_date_time])
         lock.release()
         sleep(SENSOR_DATA_COLLECTION_INTERVAL)
         # Check Threshold Here 
         threshold_dict = db.retrieve_threshold()
         send_notification = False
         msg = ""
         if temperature > threshold_dict["temperature"]:
            print("temperature above threshold")
            send_notification = True
            msg = msg + f"Temperature was detected to be above the threshold set!!!\nThreshold: {threshold_dict['temperature']} Celsius\nValue Detected: {temperature} Celcius\nDate: {current_date_time}\n\n"
         if humidity > threshold_dict["humidity"]:
            print("humidity above threshold")
            send_notification = True
            msg = msg + f"Humidity was detected to be above the threshold set!!!\nThreshold: {threshold_dict['humidity']}%\nValue Detected: {humidity}%\nDate: {current_date_time}\n\n"
         
         if send_notification:
            print("DHT11 Value over threshold")
            current_time = time.time()
            if current_time - old_time >= NOTIFICATION_INTERVAL_DHT11:
               print("\nSENDING DHT11 NOTIFICATION\n")
               print(msg)
               send_notification_dht11(db,msg)
               old_time = current_time
      except KeyboardInterrupt:
         update = False


def start_lcd_display_dht11():
    lock.acquire()
    global showDHT11DataOnLCD 
    showDHT11DataOnLCD = True
    lock.release()
    print(showDHT11DataOnLCD)
    while showDHT11DataOnLCD == True:
        # lock.acquire()
        if len(dht11_deque) > 0:
            # print(dht11_deque[0])
            # print("display temp and humidity on LCD")
            lcd.text(f"Temp: {dht11_deque[0][0]}",1)
            lcd.text(f"Humidity: {dht11_deque[0][1]}",2)
            sleep(SENSOR_DATA_COLLECTION_INTERVAL)
            lcd.clear()
        # lock.release()
    # print("stopped displaying temp humidity on lcd")

def stop_lcd_display_dht11():
    lock.acquire()
    global showDHT11DataOnLCD
    showDHT11DataOnLCD = False
    lock.release()
    lcd.clear()
    
def start_lcd_display_light():
    lock.acquire()
    global showLightDataOnLCD 
    showLightDataOnLCD = True
    lock.release()
    while showLightDataOnLCD:
        if len(light_deque) > 0:
            lcd.text(f"lights: {light_deque[0][0]}",1)
            sleep(SENSOR_DATA_COLLECTION_INTERVAL)
            lcd.clear()

def stop_lcd_display_light():
    lock.acquire()
    global showLightDataOnLCD
    showLightDataOnLCD = False
    lock.release()
    lcd.clear()

def send_notification_light(db,msg):
   # retrieve alll the users 
   users_data_list = db.retrieve_all_users_data()
   email_list = []
   phone_list = []
   for i in users_data_list:
      email_list.append(i['email'])
      phone_list.append(i['phone'])
   # perform notification here
   email_client = EmailClient(GMAIL_USERNAME,GMAIL_PASSWORD)
   email_client.notifyDetected(email_list, msg)
   twilio_client = TwilioClient(TWILIO_SID,TWILIO_TOKEN,PHONE_NUM)
   twilio_client.notifyDetected(phone_list,msg)



def send_notification_dht11(db,msg):
   # retrieve alll the users 
   users_data_list = db.retrieve_all_users_data()
   email_list = []
   phone_list = []
   for i in users_data_list:
      email_list.append(i['email'])
      phone_list.append(i['phone'])
   # perform notification here
   email_client = EmailClient(GMAIL_USERNAME,GMAIL_PASSWORD)
   email_client.notifyDetected(email_list, msg)
   twilio_client = TwilioClient(TWILIO_SID,TWILIO_TOKEN,PHONE_NUM)
   twilio_client.notifyDetected(phone_list,msg)
