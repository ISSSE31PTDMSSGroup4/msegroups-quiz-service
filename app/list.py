from flask import Blueprint
# from flask import request
import utils.dynamodb_handler as dynamodb_handler

import HTTP.const.request.keys as keys
import HTTP.utils.request as request

# Defining a blueprint
list = Blueprint('list', __name__)

# def getUser():
#     return request.headers.get('X-USER')

@list.route('/api/quiz/list/', methods=['GET'])
def getQuizzesCreatedByUser():
    username = request.getUser()
    quizzes = dynamodb_handler.getQuizzesByUsername(username)

    for quiz in quizzes:
        quiz.pop(keys.USERNAME)
        print (quiz[keys.QUESTIONS])
        question_list = []
        for question_id in quiz[keys.QUESTIONS]:
            question_list.append(
                {
                  keys.QUESTION_ID : question_id  
                }
            )
        quiz[keys.QUESTIONS] = question_list

    return quizzes