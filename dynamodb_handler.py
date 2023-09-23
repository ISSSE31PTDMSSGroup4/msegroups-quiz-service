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

def getQuizzesByUsername(username):
    response = QuizTable.query(
        KeyConditionExpression="#username = :username",
        ExpressionAttributeNames = {"#username" : keys.USERNAME.value},
        ExpressionAttributeValues = {":username" : username},
    )
    return response["Items"]

def getQuiz(username, quiz_id):
    response = QuizTable.get_item(
        Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id}
    )
    return response["Item"]

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

def deleteQuiz(username: str, quiz_id: str) -> dict:
    response = QuizTable.delete_item(
        Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
    )

    return response

def addQuestion(username: str, quiz_id: str, question_id: str, inputItem: dict) -> dict:
    response = QuizTable.update_item(
        Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
        UpdateExpression = "SET #attrName = list_append(#attrName, :attrValue)",
        ExpressionAttributeNames = {"#attrName" : keys.QUESTIONS.value},
        ExpressionAttributeValues = {":attrValue" : [inputItem]},
        ReturnValues="UPDATED_NEW"
    )

    return response

def updateQuestion(username: str, quiz_id: str, inputItem: dict) -> dict:
    indexResponse = 'N/A'
    optionsResponse = 'N/A'
    answerResponse = 'N/A'
    explanationResponse = 'N/A'

    if keys.INDEX.value in inputItem:
        indexResponse = QuizTable.update_item(
            Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
            UpdateExpression="SET #questions.#question_id.#question_index = :question_index",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS.value,
                '#question_id': inputItem[keys.QUESTION_ID.value],
                '#question_index': keys.INDEX.value
            },
            ExpressionAttributeValues={':question_index': inputItem[keys.INDEX.value]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.OPTIONS.value in inputItem:
        optionsResponse = QuizTable.update_item(
            Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
            UpdateExpression="SET #questions.#question_id.#options = :options",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS.value,
                '#question_id': inputItem[keys.QUESTION_ID.value],
                '#options': keys.OPTIONS.value
            },
            ExpressionAttributeValues={':options': inputItem[keys.OPTIONS.value]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.ANSWER.value in inputItem:
        answerResponse = QuizTable.update_item(
            Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
            UpdateExpression="SET #questions.#question_id.#answer = :answer",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS.value,
                '#question_id': inputItem[keys.QUESTION_ID.value],
                '#answer': keys.ANSWER.value
            },
            ExpressionAttributeValues={':answer': inputItem[keys.ANSWER.value]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.EXPLANATION.value in inputItem:
        explanationResponse = QuizTable.update_item(
            Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
            UpdateExpression="SET #questions.#question_id.#explanation = :explanation",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS.value,
                '#question_id': inputItem[keys.QUESTION_ID.value],
                '#explanation': keys.EXPLANATION.value
            },
            ExpressionAttributeValues={':explanation': inputItem[keys.EXPLANATION.value]},
            ReturnValues="UPDATED_NEW"
        )
    
    return {
        'Index': indexResponse,
        'Options': optionsResponse,
        'Answer': answerResponse,
        'Explanation': explanationResponse
    }

def deleteQuestion(username: str, quiz_id: str, question_id: dict) -> dict:
    response = QuizTable.update_item(
        Key={keys.USERNAME.value: username, keys.QUIZ_ID.value: quiz_id},
        UpdateExpression = "REMOVE #questions.#question_id",
        ExpressionAttributeNames = {
            "#questions" : keys.QUESTIONS.value,
            "#question_id" : question_id,
        },
        ReturnValues="UPDATED_NEW"
    )

    return response