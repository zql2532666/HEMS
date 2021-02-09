from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash, session, g
from gevent.pywsgi import WSGIServer
from gpiozero import LED
import database_utils
import mysql.connector as mysql
import Adafruit_DHT
from time import sleep
from gpiozero import MCP3008
from datetime import datetime
from time import sleep
from threading import Thread
import email_utils


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

app.secret_key = 'secretkey'


RECORD_INTERVAL = 10
DHT11_PIN = 24   

adc = MCP3008(channel=0)

LED_PIN = 13
led = LED(LED_PIN)

# variables for MYSQL Database connection 
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "iot_ca1"

latest_dht11_data = {}
latest_ldr_data = {}


def ldr_main():
      global latest_ldr_data
      mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)

      while True:
            try:
                  light_value = adc.value

                  if light_value:
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        rows_affected = database_utils.insert_ldr_data(mysql_connection, mysql_cursor, light_value, current_datetime)
                        print("Light sensor reading: {}".format(light_value))
                        print("{} rows updated in the database...\n".format(rows_affected))
                  sleep(RECORD_INTERVAL)

            except Exception as err:
                  print(err)


def dht11_main():
      global latest_dht11_data
      mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)
      
      while True:
            try:
                  humidity, temperature = Adafruit_DHT.read_retry(11, DHT11_PIN)
                  print("Temp: {0} degree".format(temperature))
                  print("Humidity: {0} %".format(humidity))

                  if temperature and humidity:
                        # store the current temperature and humidity reading to database
                        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                        latest_dht11_data['temperature'] = temperature
                        latest_dht11_data['humidity'] = humidity
                        latest_dht11_data['datetime'] = current_datetime

                        print(latest_dht11_data)

                        rows_affected = database_utils.insert_dht11_data(mysql_connection, mysql_cursor, temperature, humidity, current_datetime)
                        print("{} rows updated in the database...\n".format(rows_affected))

                        # if temperature >= 30:
                        #    email_utils.send_mail("""\
                        #        Subject: High Temperature Reading

                        #        High Temperature detected by DHT11 sensor. The temperature is {0}
                        #    """.format(temperature))

                  sleep(RECORD_INTERVAL)

            except Exception as err:
                  print(err)


@app.before_request
def before_request():
    if 'user_name' in session:
        mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)
        user = database_utils.get_user_info_by_username(mysql_connection, mysql_cursor, session['user_name'])
        g.user = user


@app.route('/')
def index():
    if not g.user:
        redirect(url_for('login'))

    return render_template("index.html")


@app.route('/profile')
def profile():
    if not g.user:
        redirect(url_for('login'))

    return render_template("profile.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop('user_name', None)
        mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)
        user_info = database_utils.get_user_info_by_username(mysql_connection, mysql_cursor, request.form['username'])

        if user_info and request.form['password'] == user_info['password']:
            session['user_name'] = user_info['username']
            return redirect(url_for('profile'))
        else:
            error = 'Invalid Credentials. Plase try again.'

    return render_template("login.html", error=error)


@app.route('/api/led-status', methods=['GET'])
def get_led_status():
    if not g.user:
        redirect(url_for('login'))

    if led.is_lit:
        led_status = True
    else:
        led_status = False
 
    return jsonify({'led_status': led_status}), 201


@app.route('/api/led-on', methods=['GET'])
def turn_on_led():
    if not g.user:
        redirect(url_for('login'))

    led.on()
    return jsonify({'completed': True}), 201


@app.route('/api/led-off', methods=['GET'])
def turn_off_led():
    if not g.user:
        redirect(url_for('login'))

    led.off()
    return jsonify({'completed': True}), 201


@app.route('/api/latest-dht11-reading', methods=['GET'])
def retrieve_latest_dht11_reading():
    if not g.user:
        redirect(url_for('login'))

    if latest_dht11_data:
        return jsonify(latest_dht11_data.copy()), 201
    else:
        abort(403)


@app.route('/api/latest-ldr-reading', methods=['GET'])
def retrieve_latest_ldr_reading():
    if not g.user:
        redirect(url_for('login'))

    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)  
    latest_ldr_data = database_utils.retrieve_latest_ldr_data(mysql_connection, mysql_cursor)

    if latest_ldr_data:
        return jsonify(latest_ldr_data.copy()), 201
    else:
        abort(403)


@app.route('/api/dht11-data', methods = ['GET'])
def retrieve_dht11_data():
    if not g.user:
        redirect(url_for('login'))

    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE) 
    dht11_data = database_utils.retrieve_dht11_data(mysql_connection, mysql_cursor)

    if dht11_data:
        return jsonify(dht11_data), 201
    else:
        abort(403)

    

@app.route('/api/ldr-data', methods = ['GET'])
def retrieve_ldr_data():
    if not g.user:
        redirect(url_for('login'))
        
    mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE) 
    ldr_data = database_utils.retrieve_ldr_data(mysql_connection, mysql_cursor)

    if ldr_data:
        return jsonify(ldr_data), 201
    else:
        abort(403)

    


if __name__ == "__main__":

    try:
        t1 = Thread(target=dht11_main, args=())
        # t2 = threading.Thread(target=ldr_main, args=())
        t1.start()
        # t2.start()
        http_server = WSGIServer(('0.0.0.0', 5000), app)
        # app.debug = True
        print('Waiting for requests.. ')
        http_server.serve_forever()

    except Exception as err:
        print(err)