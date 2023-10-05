from flask import Blueprint
import utils.dynamodb_handler as dynamodb_handler
# from flask import request

import hashlib
from datetime import datetime

import HTTP.const.response.status as status
import HTTP.const.request.keys as keys
import HTTP.utils.response as response
import HTTP.utils.request as request

# Defining a blueprint
quiz = Blueprint('quiz', __name__)

# def getUser():
#     return request.headers.get('X-USER')

def genHash(value, length):
    s = str(value) + str(datetime.now().timestamp())
    return hashlib.shake_256(s.encode('utf-8')).hexdigest(length//2)

@quiz.route('/api/quiz', methods=['POST'])
def createQuiz():
    username = request.getUser()
    jsonBody = request.getJsonBody() 
    
    if keys.QUIZ_ID in jsonBody or \
        keys.TITLE not in jsonBody:
        return response.wrong_key()

    uuid = genHash(jsonBody[keys.TITLE], 8)

    question_map = {}
    for question in jsonBody[keys.QUESTIONS]:
        question_id = genHash(question[keys.INDEX], 4)
        question_map[question_id] = question

    dynamodb_handler.addNewQuiz(
        username,
        uuid,
        jsonBody[keys.TITLE],
        question_map,
        jsonBody[keys.REMARK] if keys.REMARK in jsonBody else ''
    )

    return response.success_creation()

@quiz.route('/api/quiz', methods=['PUT'])
def updateQuiz():
    username = request.getUser()
    jsonBody = request.getJsonBody() 

    if keys.QUIZ_ID not in jsonBody:
        return response.wrong_key()

    dynamodb_handler.updateQuiz(
        username,
        jsonBody[keys.QUIZ_ID],
        jsonBody
    )
        
    return response.success_update()

@quiz.route('/api/quiz', methods=['DELETE'])
def deleteQuiz():
    username = request.getUser()
    jsonBody = request.getJsonBody() 

    if keys.QUIZ_ID not in jsonBody:
        return response.wrong_key()

    output = dynamodb_handler.deleteQuiz(
        username,
        jsonBody[keys.QUIZ_ID],
    )

    if status.ERROR in output: 
        return response.custom_error_message(output[status.ERROR])
    
    return response.success_remove()