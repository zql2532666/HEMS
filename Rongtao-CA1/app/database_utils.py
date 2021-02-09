import mysql.connector as mysql
import sys


def get_mysql_connection(host, username, password, database):
    connection = mysql.connect(
            host = host,
            user = username,
            passwd = password,
            database = database
    )
    cursor = connection.cursor() 

    return connection, cursor


def insert_dht11_data(connection, cursor, temperature, humidity, date_time):      
    query = "INSERT INTO dht11data (temperature, humidity, datetime) VALUES (%s, %s, %s)"
    values = (temperature, humidity, date_time)

    try:
        cursor.execute(query, values)
        connection.commit()
    except mysql.Error as err:
         print(err)
    except KeyboardInterrupt:
         cursor.close()
         connection.close()
    except:
        print("Error while inserting data...")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])

    return cursor.rowcount


def retrieve_dht11_data(connection, cursor):     
    query = "SELECT * FROM dht11data ORDER BY id DESC LIMIT 10"

    try:
        cursor.execute(query)
        dht11_data = cursor.fetchall()
        connection.close()
        dht11_data_list = []

        for row in dht11_data[::-1]:
            dht11_data_list.append({
                "temperature": float(row[1]),
                "humidity": float(row[2]),
                "datetime": row[3]
            })

        return dht11_data_list

    except Exception as err:
        print(err)
        return None

    
def retrieve_latest_dht11_data(connection, cursor):      
    query = "SELECT * FROM dht11data ORDER BY id DESC LIMIT 1"

    try:
        cursor.execute(query)
        dht11_data = cursor.fetchall()
        connection.close()

        dht11_data_dict = {}

    
        dht11_data_dict = {
                "temperature": float(dht11_data[0][1]),
                "humidity": float(dht11_data[0][2]),
                "datetime": dht11_data[0][3]
        }

        return dht11_data_dict

    except Exception as err:
        print(err)
        return None

    

def insert_ldr_data(connection, cursor, light_intensity, date_time):       
    query = "INSERT INTO LDRdata (light_intensity, datetime) VALUES (%s, %s)"
    values = (light_intensity, date_time)

    try:
        cursor.execute(query, values)
        connection.commit()
    except mysql.Error as err:
         print(err)
    except KeyboardInterrupt:
         cursor.close()
         connection.close()
    except:
        print("Error while inserting data...")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


    return cursor.rowcount


def retrieve_ldr_data(connection, cursor):     
    query = "SELECT * FROM LDRdata ORDER BY id DESC LIMIT 10"

    try:
        cursor.execute(query)
        ldr_data = cursor.fetchall()
        connection.close()

        ldr_data_list = []

        for row in ldr_data[::-1]:
            ldr_data_list.append({
            "light_intensity": float(row[1]),
            "datetime": row[2]
        })

        return ldr_data_list

    except Exception as err:
        print(err)
        return None

    
def retrieve_latest_ldr_data(connection, cursor):      
    query = "SELECT * FROM LDRdata ORDER BY id DESC LIMIT 1"

    try:
        cursor.execute(query)
        ldr_data = cursor.fetchall()
        connection.close()

        ldr_data_dict = {
            "light_intensity": float(ldr_data[0][1]),
            "datetime": ldr_data[0][2]
        }
        print(ldr_data_dict)
        return ldr_data_dict

    except Exception as err:
        print(err)
        return None


def get_user_info_by_username(connection, cursor, username):
    query = "SELECT * FROM user where username = %s"

    try:
        cursor.execute(query, (username,))
        user_info = cursor.fetchone()
        connection.close()

        if user_info:
            user_info_dict = {
                "username": user_info[1],
                "password": user_info[2]
            }
            
            return user_info_dict
        else:
            return None

    except Exception as err:
        print(err)
        return None

