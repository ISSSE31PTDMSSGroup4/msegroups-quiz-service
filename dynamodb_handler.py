import boto3
from decouple import config
from keys import keys
import json

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

client = boto3.client(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)
resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

QuizTable = resource.Table('Quiz')

def addNewQuiz(username, quiz_id, title, questions, remark):
    response = QuizTable.put_item(
        Item = {
            keys.USERNAME.value : username,
            keys.QUIZ_ID.value : quiz_id,
            keys.TITLE.value : title,
            keys.QUESTIONS.value: questions,
            keys.REMARK.value : remark
        }
    )
    return response

# composite primary key = username + quiz_id

def updateQuiz(username: str, quiz_id: str, inputItem: dict) -> dict:
    titleResponse = 'N/A'
    remarkResponse = 'N/A'

    if keys.TITLE.value in inputItem:
        titleResponse = QuizTable.update_item(
            Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
            UpdateExpression="SET title = :title",
            ExpressionAttributeValues={':title': inputItem[keys.TITLE.value]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.REMARK.value in inputItem:
        remarkResponse = QuizTable.update_item(
            Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
            UpdateExpression="SET remark = :remark",
            ExpressionAttributeValues={':remark': inputItem[keys.REMARK.value]},
            ReturnValues="UPDATED_NEW"
        )
    
    return {
        'Title': titleResponse,
        'Remark': remarkResponse
    }