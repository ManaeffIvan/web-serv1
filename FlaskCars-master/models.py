class UsersModel:
    """Сущность пользователей"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(20) UNIQUE,
                             password_hash VARCHAR(128),
                             email VARCHAR(20),
                             is_admin INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, email, is_admin=False):
        """Вставка новой записи"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, email, is_admin) 
                          VALUES (?,?,?,?)''',
                       (user_name, password_hash, email, int(is_admin)))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        """Проверка, есть ли пользователь в системе"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?", [user_name])
        row = cursor.fetchone()
        return (True, row[2], row[0]) if row else (False,)

    def get(self, user_id):
        """Возврат пользователя по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех пользователей"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows


class CompaniesModel:
    """Сущность компаний"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS сompanies 
                            (company_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20) UNIQUE,
                             address VARCHAR(128)
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, address):
        """Добавление компании"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO сompanies 
                          (name, address) 
                          VALUES (?,?)''',
                       (name, address))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск компании по названию"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM сompanies WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, company_id):
        """Запрос компании по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM сompanies WHERE company_id = ?", (str(company_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех компаний"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM сompanies")
        rows = cursor.fetchall()
        return rows

    def delete(self, company_id):
        """Удаление компании"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM сompanies WHERE company_id = ?''', (str(company_id)))
        cursor.close()
        self.connection.commit()


class MagazinesModel:
    """Сущность журналов"""
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        """Инициализация таблицы"""
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS magazines 
                            (magazine_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             name VARCHAR(20),
                             price INTEGER,
                             length INTEGER,
                             theme VARCHAR(20),
                             company INTEGER
                        )''')
        cursor.close()
        self.connection.commit()

    def insert(self, name, price, length, theme, company):
        """Добавление журнала"""
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO magazines 
                          (name, price, length, theme, company) 
                          VALUES (?,?,?,?,?)''',
                       (name, str(price), str(length), theme, str(company)))
        cursor.close()
        self.connection.commit()

    def exists(self, name):
        """Поиск журнала по имени"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?",
                       name)
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, magazine_id):
        """Поиск журналов по id"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM magazines WHERE magazine_id = ?", (str(magazine_id)))
        row = cursor.fetchone()
        return row

    def get_all(self):
        """Запрос всех журналов"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, price, magazine_id FROM magazines")
        rows = cursor.fetchall()
        return rows

    def delete(self, magazine_id):
        """Удаление журнала"""
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM magazines WHERE magazine_id = ?''', (str(magazine_id)))
        cursor.close()
        self.connection.commit()

    def get_by_price(self, start_price, end_price):
        """Запрос журналов по цене"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, price, magazine_id FROM magazines WHERE price >= ? AND price <= ?", (str(start_price), str(end_price)))
        row = cursor.fetchall()
        return row

    def get_by_company(self, company_id):
        """Запрос журналов по компании"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, price, magazine_id FROM magazines WHERE company = ?", (str(company_id)))
        row = cursor.fetchall()
        return row
