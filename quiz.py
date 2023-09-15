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

    if authorized:
        return '''
            {“Quiz_A_id”: 
                {“title”: “Solution Architect”,
                “Question_list”: [“Question1_id”, “Question2_id”]
                “remark”: “This quiz iis about testing the knowledge of the Solution Architect fundamentals”,
                },
            “Quiz_B_id”: ……
            }
        ''', 200
    
    return 'Authorization failed', 401

@app.route('/api/quiz/detail?{quiz_id}', methods=['GET'])
def getQuizDetail():
    authorized = True

    if authorized:
        return '''
            {“title”: “Solution Architect”,
            “Question1_id”: {
                “Title”: “Useful diagram”,
                “Option”: [“sequence_diagram”, “class_diagram”, “activity_diagram”, “all”],
                “Answer”: 3,
                “Explanation”: “...”
                },
            “Question2_id”: {
                “Title”: “Reference architecture design”,
                “Option”: [...],
                “Answer”: 1,
                “Explanation”: .”...”
            }
        }
        ''', 200
    
    return 'Authorization failed', 401

@app.route('/api/quiz', methods=['POST'])
def createQuiz():
    authorized = True
    badRequest = False
    username = 'Susan'

    if not authorized:
        return 'Authorization failed', 401
    
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    jsonBody = request.json 

    if jsonBody is None or badRequest:
        return '''
            Bad request due to
            1) Wrong parameter
            2) Missing/Wrong key (“title” <- write wrongly)
        ''', 400

    import hashlib
    from datetime import datetime
    s = jsonBody[keys.TITLE.value] + str(datetime.now().timestamp())
    uuid = hashlib.shake_256(s.encode('utf-8')).hexdigest(4)

    dynamodb_handler.addNewQuiz(
        username,
        uuid,
        jsonBody[keys.TITLE.value],
        jsonBody[keys.QUESTIONS.value],
        jsonBody[keys.REMARK.value]
    )

    return 'Successful', 200

@app.route('/api/quiz', methods=['PUT'])
def updateQuiz():
    authorized = True
    badRequest = False
    username = 'Susan'

    if not authorized:
        return 'Authorization failed', 401
    
    content_type = request.headers.get('Content-Type')
    
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'

    jsonBody = request.json 

    if jsonBody is None or badRequest:
        return '''
            Bad request due to
            1) Wrong parameter
            2) Missing/Wrong key (“title” <- write wrongly)
        ''', 400

    dynamodb_handler.updateQuiz(
        username,
        jsonBody[keys.QUIZ_ID.value],
        jsonBody
    )
        
    return 'Successful', 200

        


@app.route('/api/quiz/{quiz_id}/question/{question_id}', methods=['POST', 'PUT'])
def updateQuestion():
    authorized = True
    badRequest = False

    if not authorized:
        return 'Authorization failed', 401
    
    if badRequest:
        return '''
            Bad request due to
            1) Wrong parameter
            2) Missing/Wrong key (“title” <- write wrongly)
        ''', 400

    return 'Successful', 200

@app.route('/api/quiz/{quiz_id}/question', methods=['POST'])
def createQuestion():
    authorized = True
    badRequest = False

    if not authorized:
        return 'Authorization failed', 401
    
    if badRequest:
        return '''
            Bad request due to
            1) Wrong parameter
            2) Missing/Wrong key (“title” <- write wrongly)
        ''', 400

    return '''
        {“title”: “Solution Architect”,
            “Question1_id”: {
                “Title”: “Useful diagram”,
                “Option”: [“sequence_diagram”, “class_diagram”, “activity_diagram”, “all”],
                “Answer”: 3,
                “Explanation”: “...”
                },
            “Question2_id”: {
                “Title”: “Reference architecture design”,
                “Option”: [...],
                “Answer”: 1,
                “Explanation”: .”...”
            },
            “Question3_id”: {
                “Title”: “Type of Agile practice”,
                “Option”: [...],
                “Answer”: 1,
                “Explanation”: .”...”     
            }
        }
    ''', 200


if __name__ == '__main__':
    app.run()