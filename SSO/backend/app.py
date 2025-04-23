from utils.sso import SSO
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

service = SSO('some app')
service.database.verbose = True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<username>/dashboard')
def dashboard(username):
    return render_template('dashboard.html')

@app.route('/profile_info')
def profile_info():
    global service
    return jsonify({'message': service.profile_info, 'status': 200})

@app.route('/login', methods=['POST'])
def sign_in():
    global service
    data = request.json
    try:
        username, password = data['username'], data['password']
        response = service.verify_user(username, password)
        service.save()
        return jsonify(response)
    except Exception as err:
        return jsonify({'message': f'Failed to verify user\nResponse: {response}\n{type(err).__name__}: {err}', 'status': 500})
    
@app.route('/create', methods=['POST'])
def create_user():
    global service
    data = request.json
    try:
        username, password = data['username'], data['password']
        response = service.create_user(username, password)
        service.save()
        return jsonify(response)
    except Exception as err:
        return jsonify({'message': f'Failed to create user\nResponse: {response}\n{type(err).__name__}: {err}', 'status': 500})
    
if __name__ == '__main__':
    app.run()