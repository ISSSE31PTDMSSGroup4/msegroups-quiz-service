from flask import Blueprint
from utils import dynamodb_handler

import HTTP.const.request.keys as keys
import HTTP.utils.request as request

detail = Blueprint('detail', __name__)

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