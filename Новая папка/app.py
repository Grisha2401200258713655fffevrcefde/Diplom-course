from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://edu_user:123456@localhost/edu_site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('first')
    password = request.form.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return f"Добро пожаловать, {username}!"
    else:
        return "Неверный логин или пароль."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким логином уже существует."
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return f"Пользователь {username} зарегистрирован!"
    return render_template('register.html')
if __name__ == '__main__':
    app.run(debug=True)
