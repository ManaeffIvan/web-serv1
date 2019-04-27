from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, MagazinesModel, CompaniesModel
from forms import LoginForm, RegisterForm, AddMagazineForm, SearchPriceForm, SearchCompanyForm, AddCompanyForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(db.get_connection()).init_table()
MagazinesModel(db.get_connection()).init_table()
CompaniesModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    """
    Главная страница
    :return:
    Основная страница сайта, либо редирект на авторизацю
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    # если обычный пользователь, то его на свою
    magazines = MagazinesModel(db.get_connection()).get_all()
    return render_template('magazine_user.html', username=session['username'], title='Просмотр базы', magazines=magazines)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница авторизации
    :return:
    переадресация на главную, либо вывод формы авторизации
    """
    form = LoginForm()
    if form.validate_on_submit():  # ввели логин и пароль
        user_name = form.username.data
        password = form.password.data

        user_model = UsersModel(db.get_connection())
        # проверяем наличие пользователя в БД и совпадение пароля
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name  # запоминаем в сессии имя пользователя и кидаем на главную
            return redirect('/index')
        else:
            flash('Пользователь или пароль не верны')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    """
    Выход из системы
    :return:
    """
    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Форма регистрации
    """
    form = RegisterForm()
    if form.validate_on_submit():
        # создать пользователя
        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            # редирект на главную страницу
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)


"""Работа с автомобилями"""


@app.route('/magazine_admin', methods=['GET'])
def magazine_admin():
    """
    Вывод всей информации об всех журналах
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # если обычный пользователь, то его на свою
    magazines = MagazinesModel(db.get_connection()).get_all()
    return render_template('magazine_admin.html',
                           username=session['username'],
                           title='Просмотр журналов',
                           magazines=magazines)


@app.route('/add_magazine', methods=['GET', 'POST'])
def add_magazine():
    """
    Добавление журнала
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        return redirect('index')
    form = AddMagazineForm()
    available_companies = [(i[0], i[1]) for i in CompaniesModel(db.get_connection()).get_all()]
    form.company_id.choices = available_companies
    if form.validate_on_submit():
        # создать журнал
        magazines = MagazinesModel(db.get_connection())
        magazines.insert(name=form.name.data,
                    price=form.price.data,
                    length=form.length.data,
                    theme=form.theme.data,
                    company=form.company_id.data)
        # редирект на главную страницу
        return redirect(url_for('magazine_admin'))
    return render_template("add_magazine.html", title='Добавление журнала', form=form)

#---------------------------------------------------------------------------------------------------------------------

@app.route('/magazine/<int:magazine_id>', methods=['GET'])
def magazine(magazine_id):
    """
    Вывод всей информации о журнале
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    '''if session['username'] != 'admin':
        return redirect(url_for('index'))'''
    # иначе выдаем информацию
    magazine = MagazinesModel(db.get_connection()).get(magazine_id)
    сompany = CompaniesModel(db.get_connection()).get(magazine[5])
    return render_template('magazine_info.html',
                           username=session['username'],
                           title='Просмотр журнала',
                           magazine=magazine,
                           сompany=сompany[1])


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():
    """
    Запрос журналов, удовлетворяющих определенной цене
    """
    form = SearchPriceForm()
    if form.validate_on_submit():
        # получить все журналы по определенной цене
        magazines = MagazinesModel(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)
        # редирект на страницу с результатами
        return render_template('magazine_user.html', username=session['username'], title='Просмотр базы', magazines=magazines)
    return render_template("search_price.html", title='Подбор по цене', form=form)


@app.route('/search_company', methods=['GET', 'POST'])
def search_company():
    """
    Запрос журналов, продающихся в определенной компании
    """
    form = SearchCompanyForm()
    available_companies = [(i[0], i[1]) for i in CompaniesModel(db.get_connection()).get_all()]
    form.company_id.choices = available_companies
    if form.validate_on_submit():
        #
        magazines = MagazinesModel(db.get_connection()).get_by_company(form.company_id.data)
        # редирект на главную страницу
        return render_template('magazine_user.html', username=session['username'], title='Просмотр базы', magazines=magazines)
    return render_template("search_company.html", title='Подбор по цене', form=form)


'''Работа с компанией'''


@app.route('/company_admin', methods=['GET'])
def company_admin():
    """
    Вывод всей информации об всех компаниях
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('index')
    # иначе это админ
    companies = CompaniesModel(db.get_connection()).get_all()
    return render_template('company_admin.html',
                           username=session['username'],
                           title='Просмотр Компаний',
                           companies=companies)


@app.route('/company/<int:company_id>', methods=['GET'])
def company(company_id):
    """
    Вывод всей информации о компании
    :return:
    информация для авторизованного пользователя
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если не админ, то его на главную страницу
    if session['username'] != 'admin':
        return redirect(url_for('index'))
    # иначе выдаем информацию
    company = CompaniesModel(db.get_connection()).get(company_id)
    return render_template('company_info.html',
                           username=session['username'],
                           title='Просмотр информации о компании',
                           company=company)


@app.route('/add_company', methods=['GET', 'POST'])
def add_company():
    """
    Добавление компании и вывод на экран информации о нем
    """
    # если пользователь не авторизован, кидаем его на страницу входа
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        form = AddCompanyForm()
        if form.validate_on_submit():
            # создать компанию
            companies = CompaniesModel(db.get_connection())
            companies.insert(name=form.name.data, address=form.address.data)
            # редирект на главную страницу
            return redirect(url_for('index'))
        return render_template("add_company.html", title='Добавление компании', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
