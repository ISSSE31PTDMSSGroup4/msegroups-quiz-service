from flask import Flask
import dynamodb_handler
from flask import request

import hashlib
from datetime import datetime

import HTTPConst.response.status as status
import HTTPConst.request.keys as keys
import HTTPConst.response.message as response

app = Flask(__name__)

def getUser():
    return request.headers.get('X-USER')

def genHash(value, length):
    s = str(value) + str(datetime.now().timestamp())
    return hashlib.shake_256(s.encode('utf-8')).hexdigest(length//2)

@app.before_request
def validateRequest():
    username = getUser()
    if not username:
        return response.auth_failed()
    
    if request.method == 'GET':
        return
    
    content_type = request.headers.get('Content-Type') 
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    if request.json is None:
        return response.wrong_param()

@app.route('/api/quiz/list/', methods=['GET'])
def getQuizzesCreatedByUser():
    username = getUser()

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

@app.route("/api/quiz/detail", methods=['GET'])
def getQuizDetail():
    username = getUser()

    quiz_id = request.args.get('quiz_id', None)
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

@app.route('/api/quiz', methods=['POST'])
def createQuiz():
    username = getUser()
    jsonBody = request.json 
    
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

@app.route('/api/quiz', methods=['PUT'])
def updateQuiz():
    username = getUser()
    jsonBody = request.json
    
    if keys.QUIZ_ID not in jsonBody:
        return response.wrong_key()

    dynamodb_handler.updateQuiz(
        username,
        jsonBody[keys.QUIZ_ID],
        jsonBody
    )
        
    return response.success_update()

@app.route('/api/quiz', methods=['DELETE'])
def deleteQuiz():
    username = getUser()
    jsonBody = request.json 

    if keys.QUIZ_ID not in jsonBody:
        return response.wrong_key()

    output = dynamodb_handler.deleteQuiz(
        username,
        jsonBody[keys.QUIZ_ID],
    )

    if status.ERROR in output: 
        return response.custom_error_message(output[status.ERROR])
    
    return response.success_remove()

@app.route('/api/quiz/question', methods=['POST'])
def addQuestion():
    username = getUser()
    jsonBody = request.json 

    if keys.QUIZ_ID not in jsonBody or \
        keys.QUESTION not in jsonBody or \
        keys.INDEX not in jsonBody or \
        keys.OPTIONS not in jsonBody or \
        keys.ANSWER not in jsonBody:
        return response.wrong_key()

    question_id = genHash(jsonBody[keys.INDEX], 4)

    dynamodb_handler.addQuestion(
        username,
        jsonBody.pop(keys.QUIZ_ID),
        question_id,
        jsonBody
    )

    return response.success_creation()

@app.route('/api/quiz/question', methods=['PUT'])
def updateQuestion():
    username = getUser()
    jsonBody = request.json 

    if keys.QUIZ_ID not in jsonBody or \
        keys.QUESTION_ID not in jsonBody:
        return response.wrong_key()
    
    dynamodb_handler.updateQuestion(
        username,
        jsonBody[keys.QUIZ_ID],
        jsonBody
    )

    return response.success_update()

@app.route('/api/quiz/question', methods=['DELETE'])
def deleteQuestion():
    username = getUser()
    jsonBody = request.json 

    if keys.QUIZ_ID not in jsonBody or \
        keys.QUESTION_ID not in jsonBody:
        return response.wrong_key()
    
    dynamodb_handler.deleteQuestion(
        username,
        jsonBody[keys.QUIZ_ID],
        jsonBody[keys.QUESTION_ID]
    )

    return response.success_remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)