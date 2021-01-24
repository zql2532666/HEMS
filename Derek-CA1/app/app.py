from gevent.pywsgi import WSGIServer
# from flask_mysqldb import MySQL
from flask import Flask, render_template, request, jsonify, abort, redirect, url_for, flash,send_file,session
import json
from db_new import *
from sensors import *
import threading
from rpi_lcd import LCD
from datetime import timedelta
app = Flask(__name__)


app.secret_key = 'iloveiot'



@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = DB()
    error = None
    if request.method == "POST":
        submit_email = request.form['email']
        submit_password = request.form['password']
        user_data = db.retrieve_user_by_email(submit_email)

        if user_data and submit_password == user_data["password"]:
            session["email"] = user_data["email"]
            print("\n\nUSER SUCESSFULLY AUTHENTICATED\n\n")
            return redirect(url_for('index'))
        else:
            error = "Wrong Credentials. Try Again"

    return render_template("login.html", error=error)

@app.route('/logout')
def logout():
    session.pop("email",None)
    return redirect(url_for("login"))

@app.route('/')
def index():
    if not "email" in session:
        return render_template("login.html", error=None)

    return render_template("index.html", title="Dashboard")

@app.route('/charts')
def charts():
    if not "email" in session:
        return render_template("login.html", error=None)

    return render_template("charts.html", title="Charts")

@app.route('/tables')
def tables():
    if not "email" in session:
        return render_template("login.html", error=None)
    return render_template("tables.html", title="Tables")

@app.route('/graphs')
def graphs():
    if not "email" in session:
        return render_template("login.html", error=None)
    return render_template("graphs.html", title="Tables")

@app.route('/users')
def users():
    if not "email" in session:
        return render_template("login.html", error=None)
    return render_template("users.html", title="Users")


@app.route('/api/v1/threshold',methods=['GET'])
def get_threshold():
    print("api/v1/threshold")
    db = DB()
    data = db.retrieve_threshold()
    return jsonify(data)

@app.route('/api/v1/threshold',methods=['POST'])
def modify_threshold():
    db = DB()
    print("\n\nmodify threshold\n\n")
    if not request.json:
        abort(400)
    print(request.json)
    db.change_threshold(request.json)
    return jsonify({'completed': True}), 201

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    db = DB()
    print("api/v1/users")
    data = db.retrieve_all_users_data()
    data_dict = dict()
    data_dict["data"] = data
    return jsonify(data_dict)

@app.route('/api/v1/users', methods=['POST'])
def add_user():
    db = DB()
    print("\napi/v1/users -- ADD\n")
    if not request.json:
        abort(400)
    db.insert_new_user(request.json)
    return jsonify({'completed': True}), 201


@app.route('/api/v1/users/<string:email>', methods=['GET'])
def get_user_by_email():
    db = DB()
    print("getting one user")
    return jsonify({'completed': True}), 201

@app.route('/api/v1/users/<string:email>', methods=['DELETE'])
def delete_users(email):
    db = DB()
    print("\n/api/v1/users - DELETE \n")
    db.delete_user_by_email(email)
    return jsonify({'completed': True}), 201


@app.route('/api/v1/dht11', methods=['GET'])
def get_all_dht11_data():
    db = DB()
    # print("GETTING TEMPERATURE!!")
    print("GETTING ALL DHT11 DATA")
    data = db.retrieve_all_dht11_data()
    print("/api/v1/dht11")
    # print(f"data --> {data}")
    data_dict = dict()
    data_dict["data"] = data
    return jsonify(data_dict)

@app.route('/api/v1/dht11', methods=['DELETE'])
def delete_dht11():
    db = DB()
    # print("GETTING TEMPERATURE!!")
    db.delete_all_dht11_data()
    print("/api/v1/dht11 - DELETE")
    return jsonify({'completed': True}), 201


@app.route('/api/v1/ldr', methods=['GET'])
def get_all_light_data():
    db = DB()
    print('/api/v1/ldr')
    data = db.retrieve_all_light_data()
    # print(f"light data --> {data}")
    data_dict = dict()
    data_dict["data"] = data
    return jsonify(data_dict)

@app.route('/api/v1/ldr', methods=['DELETE'])
def delete_light():
    db = DB()
    print("\n\n\n DELETING LIGHT\n\n\n")
    db.delete_all_light_data()
    print("/api/v1/light - DELETE")
    return jsonify({'completed': True}), 201

@app.route('/api/v1/dht11_last_10', methods=['GET'])
def get_last_10_rows_dht11_data():
    db = DB()
    # print("GETTING TEMPERATURE!!")
    data = db.retrieve_last_10_dht11_data()
    print("/api/v1/dht11_last_10")
    # print(f"data --> {data}")
    return jsonify(data)

@app.route('/api/v1/ldr_last_10', methods=['GET'])
def get_last_10_rows_light_data():
    db = DB()
    print('/api/v1/ldr_last_10')
    data = db.retrieve_last_10_light_data()
    # print(f"light data --> {data}")
    return jsonify(data)

@app.route('/api/v1/realtime_sensors_data', methods=['GET'])
def get_realtime_sensor_data():
    print('/api/v1/realtime_sensors_data')
    # dh11_data = db.retrieve_realtime_dht11_data()
    # light_data = db.retrieve_realtime_light_data()
    data = {}
    if len(dht11_deque) > 0 and len(light_deque) > 0:
        data["temperature"] = dht11_deque[0][0]
        data["humidity"] = dht11_deque[0][1]
        # data["temp_humidity_date"] = dh11_data["date"]
        data["light"] = light_deque[0][0]
        # data["light_date"] = light_data["date"]
        # print(data)
    return jsonify(data)


@app.route('/api/v1/lcd_display_dht11_data', methods=['GET'])
def lcd_display_dht11_data():
    print('/api/v1/lcd_display_dht11_data')
    # stop light sensor display first
    stop_lcd_display_light()
    dht11_display_thread = threading.Thread(target=start_lcd_display_dht11)
    dht11_display_thread.start()
    return jsonify({'completed': True}), 201

@app.route('/api/v1/lcd_stop_display_dht11_data', methods=['GET'])
def lcd_stop_display_dht11_data():
    print("/api/v1/lcd_stop_display_dht11_data")
    stop_lcd_display_dht11()
    return jsonify({'completed': True}), 201    

@app.route('/api/v1/lcd_display_light_data', methods=['GET'])
def lcd_display_light_data():
    # stop dht11 display first 
    stop_lcd_display_dht11()
    print('/api/v1/lcd_display_light_data')
    light_display_thread = threading.Thread(target=start_lcd_display_light)
    light_display_thread.start()
    return jsonify({'completed': True}), 201

@app.route('/api/v1/lcd_stop_display_light_data', methods=['GET'])
def lcd_stop_display_light_data():
    print("/api/v1/lcd_stop_display_light_data")
    stop_lcd_display_light()
    return jsonify({'completed': True}), 201

@app.route('/api/v1/lcd_stop_display', methods=['GET'])
def lcd_stop_display():
    print("\n\n\n/api/v1/lcd_stop_display\n\n\n\n")
    stop_lcd_display_dht11()
    stop_lcd_display_light()
    return jsonify({'completed': True}), 201


if __name__ == "__main__":
    try:
        dht11_thread = threading.Thread(target=run_dht11_sensor)
        light_sensor_thread = threading.Thread(target=run_light_sensor)
        dht11_thread.start()
        light_sensor_thread.start()

        http_server = WSGIServer(('0.0.0.0', 5000), app)
        app.debug = True
        print('Waiting for requests.. ')
        http_server.serve_forever()
    except:
        print("Exception")