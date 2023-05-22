import sys, time, os, requests, webbrowser
from   PyQt5 import QtCore, QtGui, QtWidgets, Qt
from   PyQt5.QtWidgets import *

from   funk import settings as settings

import funk, bot_ui, wigets
import bot_stream as Bot


class bot_stream(Bot.bot_stream):
    def __init__(self, ui):
        super().__init__(ui)
        self.start()

    def restart(self):
        self.terminate()
        self.start()



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = bot_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.gui_config()

        self.tray_config()          #   Создание и настройка системного трея
        self.settings_bakcup()      #   Восстановление настроек из файла
        self.page_users_filling()   #   Заполнение страницы с пользователями
        
        #settings.page_users_update.connect(self.page_users_update)

        settings.page_users_update = self.page_users_update
        settings.notification = self.tray_icon.showMessage

    def page_users_update(self):
        self.ui.page_users_frame_neve.user_list_update()
        self.ui.page_users_frame_users.user_list_update()
        self.ui.page_users_frame_banned.user_list_update()

        settings.update_user_file()

    def page_users_filling(self):
         
        self.ui.scrollAreaWidgetContents.layout = self.ui.verticalLayout_6

        self.ui.page_users_frame_neve = wigets.user_group_new_form(self.ui.scrollAreaWidgetContents)
        self.ui.page_users_frame_users = wigets.user_group_user_form(self.ui.scrollAreaWidgetContents)
        self.ui.page_users_frame_banned = wigets.user_group_baned_form(self.ui.scrollAreaWidgetContents)

        self.ui.scrollAreaWidgetContents.layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def bot_start(self):
        self.bot_stream = Bot.bot_stream(settings.bot_token)

    def tray_config(self):

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def settings_bakcup(self):
        #######   Восстановление сохраненых настроек   ############
        if settings.bot_token != "":
            self.ui.lineEdit_2.setPlaceholderText(settings.bot_token)
            self.bot_start()

        if settings.do_autorun != "":
            if settings.do_autorun == "True":
                self.ui.checkBox.setChecked(True)
            else:
                self.ui.checkBox.setChecked(False)

    def gui_config(self):

        ########    Настройки MainWindow    ########
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True )
        #self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        ############################################

        #######   Верхняя панель навигации   #######
        def cange_page(newe_page):
            active_style = """QPushButton{
font: 12pt "Segoe UI Black";
background-color: rgb(9, 114, 194);
color: rgb(240, 240, 240);
border-radius: 5px;}"""
            passive_style = """QPushButton{font: 12pt "Segoe UI Black";
background-color: rgb(143, 143, 143);
color: rgb(240, 240, 240);
border-radius: 5px;}
QPushButton:hover{font: 13pt "Segoe UI Black";
background-color: rgb(11, 153, 255);}
QPushButton:focus:pressed{font: 12pt "Segoe UI Black";}"""
            if newe_page:
                self.ui.btn_users.setStyleSheet(passive_style)
                self.ui.btn_bot_settings.setStyleSheet(active_style)
            else:
                self.ui.btn_users.setStyleSheet(active_style)
                self.ui.btn_bot_settings.setStyleSheet(passive_style)
            self.ui.stackedWidget.setCurrentIndex(newe_page)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btn_users.clicked.connect(lambda: cange_page(0))
        self.ui.btn_bot_settings.clicked.connect(lambda: cange_page(1))
        #######
        self.ui.frame_top_bar.mouseMoveEvent = self.moveWindow          #   Обработка события
        self.ui.frame_top_bar.mousePressEvent = self.mouse_header_press #   перетягивания окна
        ############################################

        self.ui.btn_close_window.clicked.connect(lambda: self.hide())
        self.ui.btn_close_window.clicked.connect(lambda: settings.notification("Remote media control", "Application is steel runing"))

        self.ui.checkBox.stateChanged.connect(lambda: self.update_do_autorun())
        self.ui.btn_save.clicked.connect(lambda: self.update_bot_token(self.ui.lineEdit_2.text()))
        self.ui.btn_bf_link.clicked.connect(lambda: webbrowser.open('https://t.me/BotFather'))

    def update_bot_token(self, token):
        def cheak_token(token):
            res = requests.get(f"https://api.telegram.org/bot{token}/getMe")
            if res.status_code == 200:
                return True
            elif res.status_code == 401:
                return False
            print(res.status_code)
            return False

        if cheak_token(token):
            settings.update_settings("bot_token", token)
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_2.setPlaceholderText(token)
            self.bot_start()
        else:
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_2.setPlaceholderText("Неправильный токен")    #   обновление

    def update_do_autorun(self):
        if self.ui.checkBox.isChecked():
            settings.update_settings("do_autorun", "True")
        else:
            settings.update_settings("do_autorun", "False")    #   настроек

    def moveWindow(self, e):
        try:
            if self.isMaximized() == False:
                if e.buttons() == QtCore.Qt.LeftButton:
                    self.move(e.globalPos()-(self.start_click_pos - self.start_window_pos))
                    e.accept ()
        except AttributeError:
            pass    #   событие перетягивания

    def mouse_header_press(self, e):
        self.start_click_pos = e.globalPos()
        self.start_window_pos = self.pos()    #   фиксация первоночальных значений при перетаскивании окна


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())



    


#from pynput.keyboard import Key, Listener

#def on_press(key):
#    print('{0} pressed'.format(key))

#def on_release(key):
#    print('{0} release'.format(key))
#    if key == Key.esc:
#        # Stop listener
#        return False

## Collect events until released
#with Listener(on_press=on_press, on_release=on_release) as listener:
#    listener.join()
