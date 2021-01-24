import json, yaml, mysql.connector, os
import datetime
from datetime import datetime as dt
import time 

class DbAccess:

    def __init__(self):

        basedir = os.path.abspath(os.path.dirname(__file__))

        # Configure DB
        db = yaml.load(open(os.path.join(basedir, 'db.yaml')), Loader=yaml.SafeLoader)
        self.host = db['mysql_host']
        self.user = db['mysql_user']
        self.password = db['mysql_password']
        self.database = db['mysql_db']

        # self.connection = mysql.connector.connect(user=user,password=password,host=host,database=database)

    def query_db_in_json(self, cursor):
        r = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        return r

    def myconverter(self,obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

    def retrieve_lights_for_chart(self):
    
        json_data = {}

        # Mysql connection
        connection = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cur = connection.cursor()
        sql = "SELECT * FROM (select * from lights ORDER BY id DESC LIMIT 10) as foo ORDER BY foo.id ASC;"
        cur.execute(sql)

        try:
            my_query = self.query_db_in_json(cur)
            json_data = json.dumps(my_query, default=self.myconverter)
        except Exception as err:
            json_data = {}
            print(err)

        cur.close()
        connection.close()

        return json_data

    def retrieve_lights_for_table(self):
        
        json_data = {}

        # Mysql connection
        connection = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cur = connection.cursor()
        sql = "SELECT * from lights;"
        cur.execute(sql)

        try:
            my_query = self.query_db_in_json(cur)
            json_data = json.dumps(my_query, default=self.myconverter)
        except Exception as err:
            print(err)
            json_data = {}

        cur.close()
        connection.close()

        return json_data

    def check_user_exists(self, email):

        json_data = {}

        # Mysql connection
        connection = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cur = connection.cursor()

        sql = f"select * from user where email='{email}'"
        cur.execute(sql)
        
        try:
            my_query = self.query_db_in_json(cur)
            json_data = json.dumps(my_query, default=self.myconverter)
        except:
            json_data = {}

        cur.close()
        connection.close()

        return json_data

    def insert_user(self, email, name, password):
    
        #Mysql connection
        connection = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cur = connection.cursor()

        sql = f"insert into user(email, name, password) \
            values('%s', '%s', '%s')" % (email, name, password)
        
        result_value = 0

        try:
            cur.execute(sql)
            result_value = cur.rowcount
            connection.commit()
            cur.close()
        except Exception as err:
            print(err)

        cur.close()
        connection.close()

        return result_value

    def insert_light_value(self, light_value):

        #Mysql connection
        connection = mysql.connector.connect(user=self.user,password=self.password,host=self.host,database=self.database)
        cur = connection.cursor()

        sql = f"insert into lights(light_value) \
            values('%d')" % (int(light_value))
        
        result_value = 0

        try:
            cur.execute(sql)
            result_value = cur.rowcount
            connection.commit()
        except Exception as err:
            print("INSERT LIGHT ERROR", err)

        cur.close()
        connection.close()

        return result_value