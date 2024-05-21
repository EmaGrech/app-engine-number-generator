from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('http://api-service-url/results')
    data = response.json()
    return render_template('display.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
