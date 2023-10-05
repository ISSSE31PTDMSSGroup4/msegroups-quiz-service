from flask import Flask
# from flask import request

from .quiz import quiz
from .question import question
from .list import list
from .detail import detail

import HTTP.utils.response as response
import HTTP.utils.request as request

app = Flask(__name__)

# Registering blueprints
app.register_blueprint(question)
app.register_blueprint(quiz)
app.register_blueprint(list)
app.register_blueprint(detail)

# def getUser():
#     return request.headers.get('X-USER')

@app.before_request
def validateRequest():
    if not request.getUser():
        return response.auth_failed()
    
    if request.isWithoutBody():
        return
    
    if not request.isBodyFormatSupported():
        return 'Content-Type not supported!'

    if request.isWithEmptyBody():
        return response.wrong_param()