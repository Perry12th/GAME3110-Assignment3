import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PlayerList')
    id = event["queryStringParameters"]["playerID"]
    response = table.get_item(
    Key={
        'user_id': id
    }       
)
    item = response['Item']
    
    return {
        'statusCode':200,
        'body':json.dumps(item)
    }