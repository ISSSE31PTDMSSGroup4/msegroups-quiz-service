from flask import Flask
from flask_cors import CORS

from .quiz import quiz
from .question import question
from .list import list
from .detail import detail

import HTTP.utils.response as response
import HTTP.utils.request as request

app = Flask(__name__)
CORS(app)

app.register_blueprint(question)
app.register_blueprint(quiz)
app.register_blueprint(list)
app.register_blueprint(detail)

@app.before_request
def validateRequest():
    if not request.getUser():
        return response.auth_failed()
    
    if request.isWithoutBody():
        return
    
    if not request.isBodyFormatSupported():
        return response.unsupported_content_type()

    if request.isWithEmptyBody():
        return response.wrong_param()