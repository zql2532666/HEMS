import boto3
from boto3.dynamodb.conditions import Key,Attr

class DynamoDBPuller:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.dht11_table = self.dynamodb.Table('dht11_data')
        self.light_table = self.dynamodb.Table('light_data')
        self.user_table = self.dynamodb.Table('user_data')


db_puller = DynamoDBPuller()
print(db_puller.dht11_table.creation_date_time)
print(db_puller.light_table.creation_date_time)
print(db_puller.user_table.creation_date_time)
    
