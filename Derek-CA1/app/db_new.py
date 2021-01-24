import mysql.connector as mysql

class DB:
    def __init__(self):
        self.connection = mysql.connect(
                    host = "localhost",
                    user = "iotuser",
                    passwd = "dmitiot",
                    database = "iotdatabase"
        )
    
    def retrieve_threshold(self):
        cursor = self.connection.cursor()
        query = "SELECT * FROM threshold"
        try:
            cursor.execute(query)
            threshold_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        threshold_data_dict = {
            "temperature":float(threshold_data[0][1]),
            "humidity":float(threshold_data[0][2]),
            "light":float(threshold_data[0][3])
        }
        return threshold_data_dict
        
    def change_threshold(self,data):
        cursor = self.connection.cursor()
        print("DATABASE change_threshold")
        print(data)
        update_query = "UPDATE threshold SET temperature= %s,humidity=%s,light=%s where id=0"
        try:
            cursor.execute(update_query, (data["temperature"], data["humidity"],data["light"]))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return None

    def retrieve_all_users_data(self):
        cursor = self.connection.cursor()
        query = "SELECT name, email, phone, password FROM users"
        try:
            cursor.execute(query)
            users_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        users_data_list = []
        for i in users_data:
            users_data_list.append({
                "name": i[0],
                "email": i[1],
                "phone": i[2],
                "password":i[3]
            })
        return users_data_list

    def insert_new_user(self, user_data):
        # print(f"\n\n\{user_data}\n\n")
        cursor = self.connection.cursor()
        query = "INSERT INTO users (name, email, phone,password) VALUES (%s, %s, %s , %s)"
        try:
            cursor.execute(query, (user_data["name"],user_data["email"], user_data["phone"], user_data["password"]))
            cursor.close()
            self.connection.commit()
        except Exception as e:
            print(e)
            return None


    def delete_user_by_email(self,email):
        cursor = self.connection.cursor()
        query =  f"delete from users where email='{email}'"
        try:
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return None


    def delete_all_dht11_data(self):
        cursor = self.connection.cursor()
        query =  f"DELETE FROM dht11 WHERE 1 "
        try:
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return None


    def retrieve_all_dht11_data(self):
        print("\n\nretrieve_all_dht11_data")
        cursor = self.connection.cursor()
        query = "SELECT temperature, humidity, date FROM dht11"
        try:
            cursor.execute(query)
            dht11_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        dht11_data_list = []
        for i in dht11_data:
            dht11_data_list.append({
                "temperature": float(i[0]),
                "humidity": float(i[1]),
                "date": i[2]
            })
        print(" retrieve_all_dht11_data()")
        # print(dht11_data_list)
        print("\n\n")
        # print(dht11_data)
        return dht11_data_list
    
    def delete_all_light_data(self):
        cursor = self.connection.cursor()
        query =  f"DELETE FROM light_sensor WHERE 1 "
        try:
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return None
            
    def retrieve_all_light_data(self):
        cursor = self.connection.cursor(buffered=True)
        # query = "SELECT light, date FROM light_sensor"
        query = "SELECT light, date FROM light_sensor"
        try:
            cursor.execute(query)
            self.connection.commit()
            light_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        light_data_list = []

        for row in light_data:
            light_data_list.append({
                "light": float(row[0]),
                "date": row[1]
            })
        print("retrieve_all_light_data()")
        # print(light_data_list)
        print("\n\n")
        # print(dht11_data)
        return light_data_list

    def retrieve_last_10_dht11_data(self):
        cursor = self.connection.cursor()
        # query = "SELECT temperature, humidity, date FROM dht11"
        query = "SELECT temperature, humidity, date FROM dht11 ORDER BY id DESC LIMIT 10"
        try:
            cursor.execute(query)
            dht11_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        dht11_data_list = []
        for i in dht11_data:
            dht11_data_list.append({
                "temperature": float(i[0]),
                "humidity": float(i[1]),
                "date": i[2]
            })
        print(" retrieve_all_dht11_data()")
        # print(dht11_data_list)
        print("\n\n")
        # print(dht11_data)
        return dht11_data_list


    def retrieve_last_10_light_data(self):
        cursor = self.connection.cursor(buffered=True)
        # query = "SELECT light, date FROM light_sensor"
        query = "SELECT light, date FROM light_sensor ORDER BY id DESC LIMIT 10"
        try:
            cursor.execute(query)
            light_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        
        light_data_list = []

        for row in light_data:
            light_data_list.append({
                "light": float(row[0]),
                "date": row[1]
            })
        print("retrieve_all_light_data()")
        # print(light_data_list)
        print("\n\n")
        # print(dht11_data)
        return light_data_list

    def retrieve_realtime_dht11_data(self):
        cursor = self.connection.cursor()
        print("retrive_realtime_dh11_data() is running ...")
        # cursor = connection.cursor()
        query = "SELECT * FROM dht11 ORDER BY id DESC LIMIT 1"
    
        try:
            cursor.execute(query)
            dht11_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        # [(6, Decimal('32.50'), Decimal('70.00'), '2015-4-25 15:25')]

        dht11_data_formatted = {}
        dht11_data_formatted["temperature"] = float(dht11_data[0][1])
        dht11_data_formatted["humidity"] = float(dht11_data[0][2])
        dht11_data_formatted["date"] = dht11_data[0][3]
        # print(dht11_data_formatted)
        return dht11_data_formatted

    def retrieve_realtime_light_data(self):
        print ("retrieve_realtime_light_data() is running ...")
        cursor = self.connection.cursor()
        query = "SELECT * FROM light_sensor ORDER BY id DESC LIMIT 1"
        try:
            cursor.execute(query)
            light_data = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return None
        light_data = cursor.fetchall()
        light_data_formatted = {}
        light_data_formatted["light"] = float(light_data[0][1])
        light_data_formatted["date"] = light_data[0][2]
        # print(light_data_formatted)
        return light_data_formatted


    def store_light_data_to_db(self,light_value, date):
        cursor = self.connection.cursor()
        print(f"store_light_data_to_db() --> {light_value}, {date}")
        query = "INSERT INTO light_sensor (light, date) VALUES (%s, %s)"
        try:
            cursor.execute(query, (light_value, date))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return None

    def store_dht11_data_to_db(self,temperature, humidity, date):
        print(f"store_dht11data_to_db() --> {temperature}, {humidity}, {date}")
        cursor = self.connection.cursor()
        query = "INSERT INTO dht11 (temperature, humidity, date) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (temperature, humidity, date))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return None

    def retrieve_user_by_email(self, email):
        cursor = self.connection.cursor()
        query = "SELECT * FROM users where email = %s"   
        try:
            cursor.execute(query, (email,))
   
            user_data = cursor.fetchone()

            if user_data:
                user_data_dict = {
                    "id": user_data[0],
                    "name": user_data[1],
                    "email":user_data[2],
                    "phone":user_data[3],
                    "password": user_data[4]
                }
                print("USER FOUND !!!")
                print(user_data_dict)
                return user_data_dict
            else:
                return None
        except Exception as e:
            print(e)
            return None
        

# db = DB()
# db.retrieve_all_dht11_data()
# db.retrieve_all_light_data()
# db.retrieve_realtime_dht11_data()
# db.retrieve_realtime_light_data()
