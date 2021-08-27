from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zEP5%K97^$F9mDSC'
auth = HTTPBasicAuth()

@app.route('/unprotected')
def unprotected():
    return jsonify({"message": "unprotected access given"}), 200

users = {
    "karan": "12345"
}

@auth.verify_password
def userVerification(username, password):
    if username in users and users.get(username) == password:
        return username
    return None

@app.route('/getToken')
@auth.login_required
def getToken():
    token = jwt.encode({'username': auth.current_user(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return jsonify({"token": token})


def verifyToken(func):
    @wraps(func)
    def verification(*args, **kwargs):
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')
            except:
                return jsonify({"message": "Invalid token"})
        else:
             return jsonify({"message": "token missing"})
        return func(data['username'],*args, **kwargs)
    return verification


@app.route('/protected')
@verifyToken
def protected(current_user):
    return jsonify({"massage":f"protected access given to {current_user}"})


if __name__ == "__main__":
    print("running the new version")
    app.run(debug = True, port=80, host='0.0.0.0') #5000