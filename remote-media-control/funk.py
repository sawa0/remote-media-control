import os, json
from PyQt5.QtCore import pyqtSignal

class settings_file():
    page_users_update = pyqtSignal()
    def __init__(self):
        from win32com.shell import shell, shellcon
        self.pach = shell.SHGetKnownFolderPath(shellcon.FOLDERID_LocalAppData) + "\\remote_video_control"

        if os.path.exists(self.pach) != True:
            os.mkdir(self.pach)
        if os.path.exists(self.pach + "\\bot_settings") != True:
            open(self.pach + "\\bot_settings", "w").close()
        if os.path.exists(self.pach + "\\users") != True: 
            open(self.pach + "\\users", "w", encoding='utf-8').close()

        #############################################################
        #    Достаём настройки из файла сохранений.                 #
        with open(self.pach + "\\bot_settings") as file:
            self.__settings_data = file.read()
        self.__settings_data = self.__settings_data.split("\n")
        #############################################################
        #   Настройки, хранящиеся в файле переношу в переменные     #
        self.bot_token = ""
        self.do_autorun = ""

        for i in self.__settings_data:
            if i[0:6] == "TOKEN=":
                self.bot_token = i[6:]
            elif i[0:8] == "AUTORUN=":
                self.do_autorun =  i[8:]
        #############################################################

        #################################################################
        #      Достаём списки пользователей из файла сохранений.        #
        with open(self.pach + "\\users", encoding='utf-8') as file:
            self.__users_data = file.read()
        self.__users_data = self.__users_data.split("\n")
        #################################################################
        #     Переношу в переменные восстановленных пользователей       #
        self.users = []
        self.baned = []
        self.new = []

        for i in self.__users_data:
            try:
                i = eval(i)
                if i['type'] == "user":
                    self.users.append(i)
                elif i['type'] == "baned":
                    self.baned.append(i)
                elif i['type'] == "new":
                    self.new.append(i)
            except:
                ...
        #################################################################


    def update_user(self, id, user):
        for item in self.users:
            if item.get("id") == id:
                self.users.remove(item)
        for item in self.baned:
            if item.get("id") == id:
                self.baned.remove(item)
        for item in self.new:
            if item.get("id") == id:
                self.new.remove(item)

        if user["type"] == "user":
            self.users.append(user)
        elif user["type"] == "baned":
            self.baned.append(user)
        elif user["type"] == "new":
            self.new.append(user)
        
        #self.update_user_file()
        self.settings.emit()
        self.page_users_update()

    #   Обновление файла с пользователями
    def update_user_file(self):
        result = ""
        for i in self.users + self.baned + self.new:
            result += f"{i}\n"
        with open(self.pach + "\\users", "w", encoding='utf-8') as file:
            file.write(result)

    #   Обновление файла с настройками
    def update_settings(self, parametr, newe_value):

        if parametr == "bot_token":
            self.bot_token = newe_value
        elif parametr == "do_autorun":
            self.do_autorun = newe_value

        with open(self.pach + "\\bot_settings", "w") as file:
            file.write("TOKEN=" + self.bot_token + "\n" + "AUTORUN=" + self.do_autorun)

    #   Проверка наличия, и прав пользователя
    def check_user(self, user):
        for i in self.users:
            if user['id'] == i['id']:
                return "user"
        for i in self.baned:
            if user['id'] == i['id']:
                return "baned"
        for i in self.new:
            if user['id'] == i['id']:
                return "new"

        self.new.append({'id': user['id'], 'first_name': user['first_name'], 'username': user['username'], 'type': 'new'})
        #self.update_user_file()
        self.settings.emit()
        return "new"

settings = settings_file()