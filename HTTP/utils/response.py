import flask
import HTTP.const.response.code as code
import HTTP.const.response.status as status

def allow_cors_policy(response):
    response.headers.add('Access-Control-Allow-Origin', '')
    response.headers.add('Access-Control-Allow-Headers', '')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

def auth_custom_error_message(message):
    response = flask.jsonify({
        'code': code.AUTH_ERROR,
        'status':  status.ERROR,
        'message': message
    })

    return allow_cors_policy(response)

def custom_error_message(message):
    response = flask.jsonify({
        'code': code.ERROR,
        'status':  status.ERROR,
        'message': message
    })

    return allow_cors_policy(response)

def custom_success_message(message):
    response = flask.jsonify({
        'code': code.SUCCESS,
        'status':  status.SUCCESS,
        'message': message
    })

    return allow_cors_policy(response)

def unsupported_content_type():
    return custom_error_message('Content-Type not supported!')

def auth_failed():
    return auth_custom_error_message('Authorization failed')

def wrong_param():
    return custom_error_message('Bad request due to wrong parameter')

def wrong_key():
    return custom_error_message('Bad request due to missing/wrong key')

def success_creation():
    return custom_success_message('Resource created successfully')

def success_update():
    return custom_success_message('Resource updated successfully')

def success_remove():
    return custom_success_message('Resource removed successfully')