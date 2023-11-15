import os
import boto3
from config import get_config

import HTTP.const.response.status as status
import HTTP.const.request.keys as keys

CLIENT_NAME           = 'dynamodb'
REGION_NAME           = 'ap-southeast-1'
ENVIRONMENT           = os.getenv("ENVIRONMENT")

config = get_config(ENVIRONMENT)
print('ENVIRONMENT = ',ENVIRONMENT)
resource = boto3.resource(
    CLIENT_NAME,
    aws_access_key_id     = config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)
dynamodb = boto3.client(
    CLIENT_NAME, 
    region_name=REGION_NAME, 
    endpoint_url=config.DYNAMODB_ENDPOINT_URL
)

QuizTable = resource.Table('Quiz')
QuizIdIndex = keys.QUIZ_ID+"-index"

def getQuizzesByUsername(username):
    response = QuizTable.query(
        KeyConditionExpression="#username = :username",
        ExpressionAttributeNames = {"#username" : keys.USERNAME},
        ExpressionAttributeValues = {":username" : username},
    )

    if len(response["Items"]) < 1:
        return {
            status.ERROR: 'There are no quizzes found for user '+username
        }

    return response["Items"]

def getQuizByQuizId(quiz_id):
    response = QuizTable.query(
        IndexName=QuizIdIndex,
        KeyConditionExpression="#quiz_id = :quiz_id",
        ExpressionAttributeNames = {"#quiz_id" : keys.QUIZ_ID},
        ExpressionAttributeValues = {":quiz_id" : quiz_id},
    )

    if len(response["Items"]) < 1:
        return {
            status.ERROR: 'Quiz '+quiz_id+' is not found'
        }
    
    if len(response["Items"]) > 1:
        return {
            status.ERROR: 'Quiz '+quiz_id+' has duplicate records'
        }

    return response["Items"][0]

def addNewQuiz(username, quiz_id, title, questions, remark):
    return QuizTable.put_item(
        Item = {
            keys.USERNAME : username,
            keys.QUIZ_ID : quiz_id,
            keys.TITLE : title,
            keys.QUESTIONS: questions,
            keys.REMARK : remark
        }
    )

# composite primary key = username + quiz_id

def updateQuiz(username: str, quiz_id: str, inputItem: dict) -> dict:
    titleResponse = 'N/A'
    remarkResponse = 'N/A'

    try:
        if keys.TITLE in inputItem:
            titleResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET title = :title",
                ExpressionAttributeValues={':title': inputItem[keys.TITLE]},
                ConditionExpression='attribute_exists(#username) and attribute_exists(#quiz_id)',
                ExpressionAttributeNames={
                    '#username': keys.USERNAME,
                    '#quiz_id': keys.QUIZ_ID
                },
                ReturnValues="UPDATED_NEW"
            )
        
        if keys.REMARK in inputItem:
            remarkResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET remark = :remark",
                ExpressionAttributeValues={':remark': inputItem[keys.REMARK]},
                ConditionExpression='attribute_exists(#username) and attribute_exists(#quiz_id)',
                ExpressionAttributeNames={
                    '#username': keys.USERNAME,
                    '#quiz_id': keys.QUIZ_ID
                },
                ReturnValues="UPDATED_NEW"
            )
        
        return {
            'Title': titleResponse,
            'Remark': remarkResponse
        }
    
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {
            status.ERROR: 'Quiz '+quiz_id+' is not found for user '+username
        }

def deleteQuiz(username: str, quiz_id: str) -> dict:
    try:
        return QuizTable.delete_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            ConditionExpression='attribute_exists(#username) and attribute_exists(#quiz_id)',
            ExpressionAttributeNames={
                '#username': keys.USERNAME,
                '#quiz_id': keys.QUIZ_ID
            }
        )
    
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {
            status.ERROR: 'Quiz '+quiz_id+' is not found for user '+username
        }

def addQuestion(username: str, quiz_id: str, question_id: str, inputItem: dict) -> dict:
    try:
        return QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression = "SET #questions.#question_id = :question",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS,
                '#question_id': question_id
            },
            ExpressionAttributeValues={':question': inputItem},
            ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')',
            ReturnValues="UPDATED_NEW"
        )
    
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {
            status.ERROR: 'Quiz '+quiz_id+' is not found for user '+username
        }

def updateQuestion(username: str, quiz_id: str, inputItem: dict) -> dict:
    indexResponse = 'N/A'
    optionsResponse = 'N/A'
    questionResponse = 'N/A'
    answerResponse = 'N/A'
    explanationResponse = 'N/A'

    try:
        if keys.INDEX in inputItem:
            indexResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET #questions.#question_id.#question_index = :question_index",
                ExpressionAttributeNames={
                    '#questions': keys.QUESTIONS,
                    '#question_id': str(inputItem[keys.QUESTION_ID]),
                    '#question_index': str(keys.INDEX)
                },
                ExpressionAttributeValues={':question_index': inputItem[keys.INDEX]},
                ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')',
                ReturnValues="UPDATED_NEW"
            )
        
        if keys.OPTIONS in inputItem:
            optionsResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET #questions.#question_id.#options = :options",
                ExpressionAttributeNames={
                    '#questions': keys.QUESTIONS,
                    '#question_id': str(inputItem[keys.QUESTION_ID]),
                    '#options': keys.OPTIONS
                },
                ExpressionAttributeValues={':options': inputItem[keys.OPTIONS]},
                ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')',
                ReturnValues="UPDATED_NEW"
            )

        if keys.QUESTION in inputItem:
            questionResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET #questions.#question_id.#question = :question",
                ExpressionAttributeNames={
                    '#questions': keys.QUESTIONS,
                    '#question_id': str(inputItem[keys.QUESTION_ID]),
                    '#question': keys.QUESTION
                },
                ExpressionAttributeValues={':question': inputItem[keys.QUESTION]},
                ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')',
                ReturnValues="UPDATED_NEW"
            )
        
        if keys.ANSWER in inputItem:
            answerResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET #questions.#question_id.#answer = :answer",
                ExpressionAttributeNames={
                    '#questions': keys.QUESTIONS,
                    '#question_id': str(inputItem[keys.QUESTION_ID]),
                    '#answer': keys.ANSWER
                },
                ExpressionAttributeValues={':answer': inputItem[keys.ANSWER]},
                ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')',
                ReturnValues="UPDATED_NEW"
            )
        
        if keys.EXPLANATION in inputItem:
            explanationResponse = QuizTable.update_item(
                Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
                UpdateExpression="SET #questions.#question_id.#explanation = :explanation",
                ExpressionAttributeNames={
                    '#questions': keys.QUESTIONS,
                    '#question_id': str(inputItem[keys.QUESTION_ID]),
                    '#explanation': keys.EXPLANATION
                },
                ExpressionAttributeValues={':explanation': inputItem[keys.EXPLANATION]},
                ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')',
                ReturnValues="UPDATED_NEW"
            )
        
        return {
            'Index': indexResponse,
            'Options': optionsResponse,
            'Question': questionResponse,
            'Answer': answerResponse,
            'Explanation': explanationResponse
        }

    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {
            status.ERROR: 'Quiz '+quiz_id+' is not found for user '+username
        }

def deleteQuestion(username: str, quiz_id: str, question_id: dict) -> dict:
    try:
        response = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression = "REMOVE #questions.#question_id",
            ExpressionAttributeNames = {
                "#questions" : keys.QUESTIONS,
                "#question_id" : question_id,
            },
            ConditionExpression='attribute_exists('+keys.USERNAME+') and attribute_exists('+keys.QUIZ_ID+')', 
            ReturnValues="ALL_OLD" # Returns the attributes of the item as they were before the operation.
        )

        if question_id not in response["Attributes"][keys.QUESTIONS]:
            return {
                status.ERROR: 'Question '+question_id+' is not found'
            }

        return response["Attributes"]
    
    except dynamodb.exceptions.ConditionalCheckFailedException:
        return {
            status.ERROR: 'Quiz '+quiz_id+' is not found for user '+username
        }
