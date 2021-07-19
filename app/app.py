from flask import Flask, render_template, url_for, jsonify, request
from flask_ngrok import run_with_ngrok
from main import main

app = Flask(__name__)
run_with_ngrok(app)   

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/send", methods=['POST'])
def send():
    if request.method == 'POST':
        question = request.form['question']
        ans = main(question)
        print(ans)
        return jsonify({'ans': 'OK', 'text': 'helo OK'})
    return render_template('index.html')


if __name__ == "__main__":
    app.run()