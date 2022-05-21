from __main__ import app 
from flask import request
from objects.token import Token
from objects.user import User
from flask_cors import cross_origin

@app.route("/api/login", methods = ['POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        data = request.get_json(force=True)

        secret_key = app.config.get('SECRET_KEY')

        auth = User.authenticate(data['username'], data['password'], secret_key)
        
        return {'access_token': auth[2], 'payload': auth[1] if not auth[0] else None}

@app.route("/api/user/token/decode/<token>", methods = ['GET'])
@cross_origin()
def decode_token(token):
    secret_key = app.config.get('SECRET_KEY')

    decoded = User.decode_auth_token(token, secret_key)

    if type(decoded) == dict:
        return {
            'error': decoded['error'],
            'code': 'TOKEN_FAIL'
        }
    else:
        if Token(token).is_expired:
            return {
                'error': 'Token is already expired.',
                'code': 'TOKEN_FAIL'
            }

        u = User(decoded)

        if not u.is_registered:
            return {
                "code": "TOKEN_FAIL",
                "error": "Tokenized user does not exist [anymore]."
            }

        return {
            'user': u.get_user(),
            'code': 'TOKEN_SUCCESS'
        }

@app.route("/api/user/token/expire/<token>")
@cross_origin()
def expire_token(token):
    try:
        secret_key = app.config.get('SECRET_KEY')

        decoded = User.decode_auth_token(token, secret_key)

        if type(decoded) == dict:
            return {
                'error': decoded['error'],
                'code': 'TOKEN_FAIL'
            }
        else:
            if Token(token).is_expired:
                return {
                    'error': 'Token is already expired.',
                    'code': 'TOKEN_FAIL'
                }

            Token().expire_token(token)

            return {'code': 'TOKEN_EXPIRE_SUCCESS'}
    except Exception as e:
        return {'code': 'TOKEN_EXPIRE_FAILURE', 'error': str(e)}