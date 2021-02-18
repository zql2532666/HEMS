# Main routes of app

from flask import Blueprint, render_template, session, jsonify
from app import *
from raspberry import *
from threading import Thread
from configparser import ConfigParser
import os 

basedir = os.path.abspath(os.path.dirname(__file__))
config = ConfigParser()
config.read(os.path.join(basedir, 'config.conf'))

""" RASPBERRY PI CONFIG"""
RASPBERRY_PI_DEVICE_ID = int(config['RASPBERRY-PI']['DEVICE_ID'])
RASPBERRY_PI_DEVICE_NAME = config['RASPBERRY-PI']['DEVICE_NAME']

""" SENSORS CONFIG"""
SENSOR_DHT11_PIN = int(config['SENSOR-DHT1']['PIN'])
SENSOR_LED_PIN = int(config['SENSOR-LED']['PIN'])
SENSOR_BUZZER_PIN = int(config['SENSOR-BUZZER']['PIN'])
SENSOR_BUTTON_PIN = int(config['SENSOR-BUTTON']['PIN'])
SENSOR_LIGHT_SERIAL_PORT = config['SENSOR-LIGHT']['SERIAL_PORT']
SENSOR_LIGHT_BAUDRATE = int(config['SENSOR-LIGHT']['BAUDRATE'])

""" AWS CONFIG """ 
AWS_HOST = config['AWS']['HOST']
ROOT_CA_PATH = config['AWS']['ROOT_CA_PATH ']
CERTIFICATE_PATH =  config['AWS']['CERTIFICATE_PATH']
PRIVATE_KEY_PATH = config['AWS']['PRIVATE_KEY_PATH']
MQQT_PORT = int(config['AWS']['MQQT_PORT'])
DHT11_TOPIC = config['AWS']['DHT11_TOPIC']
LIGHT_TOPIC = config['AWS']['LIGHT_TOPIC']

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index")
@register_login
def index2():
    return render_template("index2.html", title="Dashboard", name=session['name'].title())

@main.route("/setAlarm", methods=['GET', 'POST'])
@register_login
def alarm():

    if request.method == 'POST':
        gobal_dict["rang"] = False
        gobal_dict["alarm"] = request.form.get('time')
        print(gobal_dict["alarm"])
        flash(u'Alarm Set', 'success')
        return redirect(url_for('main.alarm'))

    return render_template("alarm.html", title="Set Alarm", name=session['name'].title())

@main.route('/api/v1/alarm', methods=['GET'])
@register_login
def getAlarm():

    return str(gobal_dict["alarm"])

@main.route('/api/v1/led/status', methods=['GET'])
@register_login
def readLED():

    return ledStatus()

@main.route('/api/v1/led/<status>', methods=['GET'])
@register_login
def writeLED(status):
    
    if status == 'on':
        ledOn()
    else:
        ledOff()

    return jsonify({'success': True}), 201

@main.route('/api/v1/led/toggle', methods=['GET'])
@register_login
def writeLEDToggle():
    
    if ledStatus() == 'off':
        ledOn()
    elif ledStatus() == 'on':
        ledOff()

    return jsonify({'success': True}), 201

@main.route('/api/v1/realtimedata', methods=['GET'])
@register_login
def realtime_light_data():
    
    return jsonify(realtime_dict)

@main.route('/api/v1/lightValueForChart', methods=['GET'])
@register_login
def light_data_chart():

    light_data = json.loads(db_access.retrieve_lights_for_chart())

    table_data_dict = dict()
    table_data_dict["data"] = [i['light_value'] for i in light_data]
    table_data_dict["labels"] = [i['datetime_value'] for i in light_data]

    return str(table_data_dict)

@main.route("/api/v1/lightValueForDatatable", methods=['GET'])
@register_login
def light_data_datatable():

    datatable_dict = dict()
    datatable_dict["data"] = json.loads(db_access.retrieve_lights_for_table())

    return jsonify(datatable_dict)

    
# Threadding

t1 = Thread(target = get_data)
t2 = Thread(target = store_data)
t3 = Thread(target = get_dht_data)
t4 = Thread(target = start_tele_bot)
t5 = Thread(target = lcd)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()