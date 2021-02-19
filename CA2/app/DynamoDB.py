import boto3
from boto3.dynamodb.conditions import Key,Attr
import jsonconverter as jsonc

class DynamoDBEngine:
    def __init__(self):
        # self.client = boto3.client('dynamodb',region_name='us-east-1',aws_access_key_id='ASIAWGJQJK3MLZ6KV57M',aws_secret_access_key='ft9RRzToy1hRVmdhA1ai92QEZUAT4wwwYshhWC5i')
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.dht11_table = self.dynamodb.Table('dht11_data')
        self.light_table = self.dynamodb.Table('light_data')
        self.user_table = self.dynamodb.Table('user_data')

    def retrieve_light_data_all(self):
        print("retrieve_light_data_all")
        response = self.light_table.scan()
        items = response["Items"]
        items = jsonc.data_to_json(items)
        return items
    
    def retrieve_light_data_last_10(self):
        print("retrieve_light_data_last_10")
        response = self.light_table.scan()
        items = response["Items"]
        num_of_rows = 10 #limit to last 10 rows
        # check if the len of items is more than 10, if it is take the last 10 rows
        if len(items) > 10:
            items= items[:num_of_rows]
        # perform json conversion here
        items = jsonc.data_to_json(items)
        # return value here 
        return items

    def retrieve_dht11_data_all(self):
        print("retrieve_dht11_data_all")
        response = self.dht11_table.scan()
        items = response["Items"]
        items = jsonc.data_to_json(items)
        return items
    
    def retrieve_dht11_data_last_10(self):
        print("retrieve_dht11_data_last_10")
        response = self.dht11_table.scan()
        items = response["Items"]
        num_of_rows = 10 #limit to last 10 rows
        # check if the len of items is more than 10, if it is take the last 10 rows
        if len(items) > 10:
            items= items[:num_of_rows]
        # perform json conversion here
        items = jsonc.data_to_json(items)
        return items

    def retrieve_user_by_email(self, email):
        print("retrieve_user_by_email")
        query_key = 'email'
        response = self.user_table.query(
            KeyConditionExpression=Key(query_key).eq(email)
            )
        items = response["Items"]
        items = jsonc.data_to_json(items)
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

db_engine = DynamoDBEngine()
db_engine.insert_new_user("penis@mail.com","dick suck", "fuck iot")
    
