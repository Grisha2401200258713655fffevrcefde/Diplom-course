from flask import Flask, render_template, request, redirect, url_for  # подключаем Flask
from flask_sqlalchemy import SQLAlchemy  # подключаем библиотеку для работы с PostgreSQL

app = Flask(__name__)  # Создаём приложение Flask

# Подключение к PostgreSQL без пароля
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://edu_user:123456@localhost/edu_site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем ненужные предупреждения

# Инициализируем объект SQLAlchemy
db = SQLAlchemy(app)

# Модель для пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    username = db.Column(db.String(50), unique=True, nullable=False)  # Имя пользователя
    password = db.Column(db.String(50), nullable=False)  # Пароль пользователя

    def __repr__(self):
        return f'<User {self.username}>'

# Модель для хранения учебных материалов
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор материала
    title = db.Column(db.String(100), nullable=False)  # Название материала
    content = db.Column(db.Text, nullable=False)  # Текст материала

    def __repr__(self):
        return f"<Material {self.title}>"

# Создание всех таблиц в базе данных
with app.app_context():
    db.create_all()

# маршоут хранения материала

@app.route('/add_material', methods=['GET',"POST"])
def add_material():
    if request.method == 'POST':
        title = request.form['title'] # получаем заголовок материала
        content = request.form['content'] # олучаем текст материала

        # создаем новый материал
        new_material = Material(title=title,content=content)
        db.session.add(new_material)
        db.session.commit() # охраняем материал в бд

        return f"материал '{title}'успешно добавлен"
    return render_template('add_material.html')

# маршрут для вывода материала
@app.route('/materials')
def materials():
    # Показываем только те материалы, где в названии есть "Теория"
    theory_materials = Material.query.filter(Material.title.ilike('%Теория%')).all()
    return render_template('materials.html', materials=theory_materials)

@app.route('/material/<int:material_id>')
def material_detail(material_id):
    material = Material.query.get_or_404(material_id)
    return render_template('material_detail.html',material=material)

# Главная страница — форма авторизации
@app.route('/')
def index():
    return render_template('login.html')  # Отображаем страницу входа

# Обработка входа пользователя
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('first')  # Получаем имя пользователя
    password = request.form.get('password')  # Получаем пароль

    # Ищем пользователя в базе данных с таким именем и паролем
    user = User.query.filter_by(username=username, password=password).first()

    # Если пользователь найден, приветствуем его
    if user:
        return redirect(url_for('materials'))
    else:
        return "Неверный логин или пароль."

# Страница регистрации нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Если форма отправлена методом POST
        username = request.form['username']  # Получаем имя пользователя
        password = request.form['password']  # Получаем пароль

        # Проверяем, есть ли уже такой пользователь в базе данных
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким логином уже существует."

        # Если пользователя нет — создаём нового
        new_user = User(username=username, password=password)
        db.session.add(new_user)  # Добавляем пользователя в сессию
        db.session.commit()  # Сохраняем изменения в базе данных

        return redirect(url_for('index'))
    return render_template('register.html')  # Если метод GET — показываем форму регистрации



# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True)