import sqlite3
DB_PATH = "linkedin_accounts.db"


class UserSettings:
    # класс который вытаскивает все атрибуты бота для запуска
    def __init__(self, id, user_agent, proxy, webgl_enabled, cpu_cores, memory, login, password,
                 daily_status, page_start=1, page_url=None, offer=None, message=None, oai_system_prompt=None):
        self.id = id
        self.user_agent = user_agent
        self.proxy = proxy
        self.webgl_enabled = webgl_enabled
        self.cpu_cores = cpu_cores
        self.memory = memory
        self.login = login
        self.password = password
        self.daily_status = daily_status
        self.page_start = page_start
        self.page_url = page_url
        self.offer = offer
        self.message = message
        self.oai_system_prompt = oai_system_prompt

    def save(self):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(
            '''INSERT INTO user_settings(user_agent, proxy, webgl_enabled, cpu_cores, memory, login, 
            password, daily_status, page_start, query, offer, message, oai_system_prompt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (self.user_agent, self.proxy, self.webgl_enabled, self.cpu_cores, self.memory, self.login, self.password,
             self.daily_status, self.page_start, self.page_url, self.offer, self.message, self.oai_system_prompt)
        )

        connection.commit()
        connection.close()

    @staticmethod
    def get_user_settings(id):
        # id = input("Напиши id бота: ")
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(
            '''SELECT * FROM user_settings WHERE id = ?''',
            (id,)
        )

        row = cursor.fetchone()

        if row:
            user_settings = UserSettings(
                id=row[0],
                user_agent=row[1],
                proxy=row[2],
                webgl_enabled=row[3],
                cpu_cores=row[4],
                memory=row[5],
                login=row[6],
                password=row[7],
                daily_status=row[8],
                page_start=row[9],
                page_url=row[10],
                offer=row[11],
                message=row[12],
                oai_system_prompt=row[13]
            )

            return user_settings

        connection.close()