import boto3
from boto3.dynamodb.conditions import Key,Attr
import jsonconverter as jsonc
from configparser import ConfigParser
import os 

basedir = os.path.abspath(os.path.dirname(__file__))
config = ConfigParser()
config.read(os.path.join(basedir, 'config.conf'))

DHT11_TABLE = config['AWS']['DHT11_TABLE']
LIGHT_TABLE = config['AWS']['LIGHT_TABLE']
USER_TABLE = config['AWS']['USER_TABLE']
FACIAL_RECOGNITION_TABLE = config['AWS']['FACIAL_RECOGNITION_TABLE']


class DynamoDBEngine:
    def __init__(self):
        # self.client = boto3.client('dynamodb',region_name='us-east-1',aws_access_key_id='ASIAWGJQJK3MLZ6KV57M',aws_secret_access_key='ft9RRzToy1hRVmdhA1ai92QEZUAT4wwwYshhWC5i')
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.dht11_table = self.dynamodb.Table(DHT11_TABLE)
        self.light_table = self.dynamodb.Table(LIGHT_TABLE)
        self.user_table = self.dynamodb.Table(USER_TABLE)
        self.facial_recognition_table = self.dynamodb.Table(FACIAL_RECOGNITION_TABLE)

    def retrieve_light_data_all(self):
        print("retrieve_light_data_all")
        response = self.light_table.scan()
        items = response["Items"]
        items = items[::-1]
        items = jsonc.data_to_json(items)
        return items
    
    def retrieve_light_data_last_10(self):
        print("retrieve_light_data_last_10")
        response = self.light_table.scan()
        items = response["Items"]
        num_of_rows = 10 #limit to last 10 rows
        # print(items)
        # check if the len of items is more than 10, if it is take the last 10 rows
        if len(items) > 10:
            items= items[-num_of_rows:]
            # items = items[::-1]
        # perform json conversion here
        items = jsonc.data_to_json(items)
        # return value here 
        print(items)
        return items

    def retrieve_dht11_data_all(self):
        print("retrieve_dht11_data_all")
        response = self.dht11_table.scan()
        items = response["Items"]
        items = items[::-1]
        items = jsonc.data_to_json(items)
        return items
    
    def retrieve_dht11_data_last_10(self):
        print("retrieve_dht11_data_last_10")
        response = self.dht11_table.scan()
        items = response["Items"]
        num_of_rows = 10 #limit to last 10 rows
        # check if the len of items is more than 10, if it is take the last 10 rows
        # print("before slicing:")
        # print(items)
        if len(items) > 10:
            items= items[-num_of_rows:]
            # items = items[::-1]
        # perform json conversion here
        items = jsonc.data_to_json(items)
        print(items)
        return items

    def retrieve_user_by_email(self, email):
        print("retrieve_user_by_email")
        query_key = 'email'
        response = self.user_table.query(
            KeyConditionExpression=Key(query_key).eq(email)
            )
        items = response["Items"]
        items = jsonc.data_to_json(items)
        print(items)
        # items should normally just be one user unless there is an email duplicate
        return items

    def insert_new_user(self,email,name,password):
        print("insert_new_user")
        insert_data = {
            "email": email,
            "name": name,
            "password": password
        }
        response = self.user_table.put_item(
            Item=insert_data
        )
        print(response)

    def retrieve_facial_recog_data_all(self):
        print("retrieve_facial_recog_data_all")
        response = self.facial_recognition_table.scan()
        items = response["Items"]
        items = items[::-1]
        items = jsonc.data_to_json(items)
        print(items)
        return items        


def test_queries():
    db = DynamoDBEngine()
    db.retrieve_light_data_all()
    db.retrieve_light_data_last_10()
    db.retrieve_dht11_data_all()
    db.retrieve_dht11_data_last_10()
    db.retrieve_user_by_email("admin@localhost")
    # db.insert_new_user("test@mail.com","test",'test')
    db.retrieve_facial_recog_data_all()

# test_queries()
