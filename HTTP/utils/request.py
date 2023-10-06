from flask import request

import HTTP.const.request.keys as keys
import HTTP.const.request.headers as headers
import HTTP.const.request.methods as methods
import HTTP.const.request.types as types

def getUser():
    return request.headers.get(headers.X_USER)

def getJsonBody():
    return request.json 

def getQuizId():
    return request.args.get(keys.QUIZ_ID, None)

def isWithoutBody():
    return request.method == methods.GET

def isBodyFormatSupported():
    content_type = request.headers.get(headers.CONTENT_TYPE) 
    return content_type == types.JSON

def isWithEmptyBody():
    return request.json is None