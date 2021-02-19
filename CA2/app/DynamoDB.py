import boto3
from boto3.dynamodb.conditions import Key,Attr

class DynamoDBEngine:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.dht11_table = self.dynamodb.Table('dht11_data')
        self.light_table = self.dynamodb.Table('light_data')
        self.user_table = self.dynamodb.Table('user_data')

    def retrieve_all_light_data(self):
        response = self.light_table.query()
        # response = self.light_table.scan()
        print(response)

db_engine = DynamoDBEngine()
print(db_engine.dht11_table.creation_date_time)
print(db_engine.light_table.creation_date_time)
print(db_engine.user_table.creation_date_time)
db_engine.retrieve_all_light_data()
    
