from flask import request

def getUser():
    return request.headers.get('X-USER')

def getJsonBody():
    return request.json 

def getQuizId():
    return request.args.get('quiz_id', None)

def isWithoutBody():
    return request.method == 'GET'

def isBodyFormatSupported():
    content_type = request.headers.get('Content-Type') 
    return content_type == 'application/json'

def isWithEmptyBody():
    return request.json is None