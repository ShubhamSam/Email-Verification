from flask import Flask, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('secret!')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return "<form action='/' method = 'POST'><input name = 'email'><input type='Submit'></form>"

    email = request.form['email']
    token = s.dumps(email, salt='confirm-email')

    msg = Message('Confirm email', sender='shubhamsahaabhi.sk@gmail.com', recipients=[email])
    link = url_for('confirm_email', token=token, _external=True)

    msg.body = f'Your link is {link}'
    mail.send(msg)

    return f'<h1>Email you entered is {email} and the token is {token}</h1>'

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='confirm-email', max_age = 1000)
    except SignatureExpired:
        return '<h2>The token is expired</h2>'
    except BadTimeSignature:
        return '<h2>Token Missmatch</h2>'
    return 'token works'

if __name__ == '__main__':
    app.run(debug=True)
