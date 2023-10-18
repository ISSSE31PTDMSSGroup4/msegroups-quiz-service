from flask import Blueprint
from utils import dynamodb_handler, identifier

import HTTP.const.request.keys as keys
import HTTP.utils.response as response
import HTTP.utils.request as request
import HTTP.const.response.status as status

question = Blueprint('question', __name__)

@question.route('/api/quiz/question/', methods=['POST'])
def addQuestion():
    username = request.getUser()
    jsonBody = request.getJsonBody() 

    if keys.QUIZ_ID not in jsonBody or \
        keys.QUESTION not in jsonBody or \
        keys.INDEX not in jsonBody or \
        keys.OPTIONS not in jsonBody or \
        keys.ANSWER not in jsonBody:
        return response.wrong_key()

    question_id = identifier.genHash(jsonBody[keys.INDEX], 4)

    output = dynamodb_handler.addQuestion(
        username,
        str(jsonBody.pop(keys.QUIZ_ID)),
        question_id,
        jsonBody
    )

    if status.ERROR in output: 
        return response.custom_error_message(output[status.ERROR])

    return response.success_creation()

@question.route('/api/quiz/question/', methods=['PUT'])
def updateQuestion():
    username = request.getUser()
    jsonBody = request.getJsonBody() 

    if keys.QUIZ_ID not in jsonBody or \
        keys.QUESTION_ID not in jsonBody:
        return response.wrong_key()
    
    output = dynamodb_handler.updateQuestion(
        username,
        str(jsonBody[keys.QUIZ_ID]),
        jsonBody
    )

    if status.ERROR in output: 
        return response.custom_error_message(output[status.ERROR])

    return response.success_update()

@question.route('/api/quiz/question/', methods=['DELETE'])
def deleteQuestion():
    username = request.getUser()
    jsonBody = request.getJsonBody() 

    if keys.QUIZ_ID not in jsonBody or \
        keys.QUESTION_ID not in jsonBody:
        return response.wrong_key()
    
    output = dynamodb_handler.deleteQuestion(
        username,
        jsonBody[keys.QUIZ_ID],
        jsonBody[keys.QUESTION_ID]
    )

    if status.ERROR in output: 
        return response.custom_error_message(output[status.ERROR])

    return response.success_remove()
