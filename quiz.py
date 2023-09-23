from flask import Flask, json
import dynamodb_handler
from flask import request

from keys import keys

app = Flask(__name__)


@app.route('/')
def index():
    return "This is the main page."

@app.route('/api/quiz/list/', methods=['GET'])
def getQuizzesCreatedByUser():
    # username = request.args.get('username')
    authorized = True
    username = 'Derby'

    if not authorized:
        return 'Authorization failed', 401

    quizzes = dynamodb_handler.getQuizzesByUsername(username)

    for quiz in quizzes:
        quiz.pop(keys.USERNAME.value)
        print (quiz[keys.QUESTIONS.value])
        question_list = []
        for question_id in quiz[keys.QUESTIONS.value]:
            question_list.append(
                {
                  keys.QUESTION_ID.value : question_id  
                }
            )
        quiz[keys.QUESTIONS.value] = question_list

    return quizzes, 200

@app.route("/api/quiz/detail", methods=['GET'])
def getQuizDetail():
    # username = request.args.get('username')
    authorized = True
    username = 'Derby'
    quiz_id = request.args.get('quiz_id', None)

    if not authorized:
        return 'Authorization failed', 401

    quiz = dynamodb_handler.getQuiz(username, quiz_id)

    quiz.pop(keys.USERNAME.value)

    question_list = []
    for question in quiz[keys.QUESTIONS.value]:
        question_id = {keys.QUESTION_ID.value: question}
        question_detail = quiz[keys.QUESTIONS.value][question]
        question_detail.update(question_id)

        question_list.append(question_detail)
    
    quiz[keys.QUESTIONS.value] = question_list

    return quiz, 200

@app.route('/api/quiz', methods=['POST'])
def createQuiz():
    authorized = True
    username = 'Derby'

    if not authorized:
        return 'Authorization failed', 401
    
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    jsonBody = request.json 

    if jsonBody is None:
        return 'Bad request due to wrong parameter', 400
    
    if keys.QUIZ_ID.value in jsonBody or \
        keys.TITLE.value not in jsonBody:
        return 'Bad request due to missing/wrong key', 400

    import hashlib
    from datetime import datetime
    s = jsonBody[keys.TITLE.value] + str(datetime.now().timestamp())
    uuid = hashlib.shake_256(s.encode('utf-8')).hexdigest(4)

    question_map = {}
    for question in jsonBody[keys.QUESTIONS.value]:
        s = str(question[keys.INDEX.value]) + str(datetime.now().timestamp())
        question_id = hashlib.shake_256(s.encode('utf-8')).hexdigest(2)
        question_map[question_id] = question

    dynamodb_handler.addNewQuiz(
        username,
        uuid,
        jsonBody[keys.TITLE.value],
        question_map,
        jsonBody[keys.REMARK.value] if keys.REMARK.value in jsonBody else ''
    )

    return 'Successful', 200

@app.route('/api/quiz', methods=['PUT'])
def updateQuiz():
    authorized = True
    username = 'Susan'

    if not authorized:
        return 'Authorization failed', 401
    
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    jsonBody = request.json 

    if jsonBody is None:
        return 'Bad request due to wrong parameter', 400
    
    if keys.QUIZ_ID.value not in jsonBody:
        return 'Bad request due to missing/wrong key', 400

    dynamodb_handler.updateQuiz(
        username,
        jsonBody[keys.QUIZ_ID.value],
        jsonBody
    )
        
    return 'Successful', 200

@app.route('/api/quiz/question', methods=['POST'])
def createQuestion():
    authorized = True
    username = 'Susan'

    if not authorized:
        return 'Authorization failed', 401
    
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    jsonBody = request.json 

    if jsonBody is None:
        return 'Bad request due to wrong parameter', 400
    
    if keys.QUIZ_ID.value not in jsonBody or \
        keys.INDEX.value not in jsonBody or \
        keys.OPTIONS.value not in jsonBody or \
        keys.ANSWER.value not in jsonBody:
        return 'Bad request due to missing/wrong key', 400

    import hashlib
    from datetime import datetime
    s = str(jsonBody[keys.INDEX.value]) + str(datetime.now().timestamp())
    question_id = hashlib.shake_256(s.encode('utf-8')).hexdigest(2)
    
    jsonBody[keys.QUESTION_ID.value] = question_id
    jsonBody.pop(keys.QUIZ_ID.value)
    dynamodb_handler.addQuestion(
        username,
        jsonBody[keys.QUIZ_ID.value],
        jsonBody
    )

    return 'Successful', 200

@app.route('/api/quiz/question', methods=['PUT'])
def updateQuestion():
    authorized = True
    username = 'Derby'

    if not authorized:
        return 'Authorization failed', 401
    
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    jsonBody = request.json 

    if jsonBody is None:
        return 'Bad request due to wrong parameter', 400
    
    if keys.QUIZ_ID.value not in jsonBody or \
        keys.QUESTION_ID.value not in jsonBody:
        return 'Bad request due to missing/wrong key', 400
    
    dynamodb_handler.updateQuestion(
        username,
        jsonBody[keys.QUIZ_ID.value],
        jsonBody
    )

    return 'Successful', 200

if __name__ == '__main__':
    app.run()