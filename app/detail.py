from flask import Blueprint
# from flask import request
import utils.dynamodb_handler as dynamodb_handler

import HTTP.const.request.keys as keys
import HTTP.utils.request as request

# Defining a blueprint
detail = Blueprint('detail', __name__)

# def getUser():
#     return request.headers.get('X-USER')

@detail.route("/api/quiz/detail", methods=['GET'])
def getQuizDetail():
    username = request.getUser()
    quiz_id = request.getQuizId()
    
    quiz = dynamodb_handler.getQuiz(username, quiz_id)

    quiz.pop(keys.USERNAME)

    question_list = []
    for question in quiz[keys.QUESTIONS]:
        question_id = {keys.QUESTION_ID: question}
        question_detail = quiz[keys.QUESTIONS][question]
        question_detail.update(question_id)

        question_list.append(question_detail)
    
    quiz[keys.QUESTIONS] = question_list

    return quiz