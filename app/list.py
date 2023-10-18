from flask import Blueprint
from utils import dynamodb_handler

import HTTP.const.request.keys as keys
import HTTP.utils.request as request
import HTTP.const.response.status as status
import HTTP.utils.response as response

list = Blueprint('list', __name__)

@list.route('/api/quiz/list/', methods=['GET'])
def getQuizzesCreatedByUser():
    username = request.getUser()
    quizzes = dynamodb_handler.getQuizzesByUsername(username)

    if status.ERROR in quizzes: 
        return response.custom_error_message(quizzes[status.ERROR])

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