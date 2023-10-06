import boto3
from decouple import config
import HTTP.const.response.status as status
import HTTP.const.request.keys as keys

AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
REGION_NAME           = config("REGION_NAME")

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id     = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    region_name           = REGION_NAME,
)

dynamodb = boto3.client('dynamodb', region_name=REGION_NAME)
QuizTable = resource.Table('Quiz')

def getQuizzesByUsername(username):
    response = QuizTable.query(
        KeyConditionExpression="#username = :username",
        ExpressionAttributeNames = {"#username" : keys.USERNAME},
        ExpressionAttributeValues = {":username" : username},
    )
    return response["Items"]

def getQuiz(username, quiz_id):
    response = QuizTable.get_item(
        Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id}
    )
    return response["Item"]

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

    if keys.TITLE in inputItem:
        titleResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET title = :title",
            ExpressionAttributeValues={':title': inputItem[keys.TITLE]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.REMARK in inputItem:
        remarkResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET remark = :remark",
            ExpressionAttributeValues={':remark': inputItem[keys.REMARK]},
            ReturnValues="UPDATED_NEW"
        )
    
    return {
        'Title': titleResponse,
        'Remark': remarkResponse
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
    return QuizTable.update_item(
        Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
        UpdateExpression = "SET #questions.#question_id = :question",
        ExpressionAttributeNames={
            '#questions': keys.QUESTIONS,
            '#question_id': question_id
        },
        ExpressionAttributeValues={':question': inputItem},
        ReturnValues="UPDATED_NEW"
    )

def updateQuestion(username: str, quiz_id: str, inputItem: dict) -> dict:
    indexResponse = 'N/A'
    optionsResponse = 'N/A'
    questionResponse = 'N/A'
    answerResponse = 'N/A'
    explanationResponse = 'N/A'

    if keys.INDEX in inputItem:
        indexResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET #questions.#question_id.#question_index = :question_index",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS,
                '#question_id': inputItem[keys.QUESTION_ID],
                '#question_index': keys.INDEX
            },
            ExpressionAttributeValues={':question_index': inputItem[keys.INDEX]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.OPTIONS in inputItem:
        optionsResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET #questions.#question_id.#options = :options",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS,
                '#question_id': inputItem[keys.QUESTION_ID],
                '#options': keys.OPTIONS
            },
            ExpressionAttributeValues={':options': inputItem[keys.OPTIONS]},
            ReturnValues="UPDATED_NEW"
        )

    if keys.QUESTION in inputItem:
        questionResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET #questions.#question_id.#answer = :answer",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS,
                '#question_id': inputItem[keys.QUESTION_ID],
                '#question': keys.QUESTION
            },
            ExpressionAttributeValues={':question': inputItem[keys.QUESTION]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.ANSWER in inputItem:
        answerResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET #questions.#question_id.#answer = :answer",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS,
                '#question_id': inputItem[keys.QUESTION_ID],
                '#answer': keys.ANSWER
            },
            ExpressionAttributeValues={':answer': inputItem[keys.ANSWER]},
            ReturnValues="UPDATED_NEW"
        )
    
    if keys.EXPLANATION in inputItem:
        explanationResponse = QuizTable.update_item(
            Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
            UpdateExpression="SET #questions.#question_id.#explanation = :explanation",
            ExpressionAttributeNames={
                '#questions': keys.QUESTIONS,
                '#question_id': inputItem[keys.QUESTION_ID],
                '#explanation': keys.EXPLANATION
            },
            ExpressionAttributeValues={':explanation': inputItem[keys.EXPLANATION]},
            ReturnValues="UPDATED_NEW"
        )
    
    return {
        'Index': indexResponse,
        'Options': optionsResponse,
        'Question': questionResponse,
        'Answer': answerResponse,
        'Explanation': explanationResponse
    }

def deleteQuestion(username: str, quiz_id: str, question_id: dict) -> dict:
    return QuizTable.update_item(
        Key={keys.USERNAME: username, keys.QUIZ_ID: quiz_id},
        UpdateExpression = "REMOVE #questions.#question_id",
        ExpressionAttributeNames = {
            "#questions" : keys.QUESTIONS,
            "#question_id" : question_id,
        },
        ReturnValues="UPDATED_NEW"
    )