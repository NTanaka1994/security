import os
from dotenv import load_dotenv
from flask import Flask, render_template_string, request, session

# Load dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

FLAG = os.environ.pop('FLAG')

app = Flask(__name__)
app.secret_key = os.environ.pop('SECRET_KEY')


@app.route('/', methods=['GET'])
def index():
    session['username'] = 'guest'
    return open(__file__).read()


@app.route('/echo', methods=['GET'])
def echo():
    return render_template_string(request.args.get('q', ''))


@app.route('/admin', methods=['GET'])
def admin():
    if session.get('username') == 'admin':
        return FLAG
    else:
        return 'You are not admin!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)