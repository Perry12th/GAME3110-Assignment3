import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PlayerList')
    id = event["queryStringParameters"]["playerID"]
    newRank = event["queryStringParameters"]["newRank"]
    
    response = table.update_item(
        Key={
            'user_id' : id
        },
        UpdateExpression='SET #Rank=:r',
        ExpressionAttributeValues={
            ':r': newRank
        },
        ExpressionAttributeNames={
            '#Rank': 'rank'
        },
        ReturnValues='UPDATED_NEW'
    )
    
    return json.dumps('Updated Player')
