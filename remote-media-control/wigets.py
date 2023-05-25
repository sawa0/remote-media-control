from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import webbrowser, re

from funk import GetSetting


class UserItem:

    def __init__(self, user_group_form_layout, settings, main_parent):
        self.settings = settings
        self.cls_settings = main_parent.settings
        self.setupUi(user_group_form_layout)

    def setupUi(self, user_group_form_layout):

        self.user_item_frame = QtWidgets.QFrame()
        self.user_item_frame.setMinimumSize(QtCore.QSize(360, 62))
        self.user_item_frame.setMaximumSize(QtCore.QSize(360, 62))
        self.user_item_frame.setStyleSheet(
            "QFrame{\nfont: 9pt \"MS Shell Dlg 2\";\nbackground-color: rgb(54, 65, 72);\ncolor: rgb(240, 240, 240);\n"
            "margin-left: 6px;\nmargin-right: 16px;\npadding-left: 4px;\nborder: solid;\nborder-width: 4px;\nborder-color: rgb(29, 27, 27);\nborder-radius: 15px;}")

        self.label_user_name = QtWidgets.QLabel(self.user_item_frame)
        self.label_user_name.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_user_name.setStyleSheet(
            "color: rgb(240, 240, 240);\nfont: 14pt \"MS Shell Dlg 2\";\nbackground-color: transparent;\n"
            "margin-left: 1px;\nmargin-right: 0px;\npadding-left: 0px;\nborder-width: 0px;\nborder-radius: 0px;")

        self.frame_extendet_user_info = QtWidgets.QFrame(self.user_item_frame)
        self.frame_extendet_user_info.setStyleSheet("margin-left: 0px;\n"
                                                    "margin-right: 0px;\n"
                                                    "border-width: 0px;\n"
                                                    "border-radius: 0px;\n"
                                                    "padding-left: 0px;\n"
                                                    "background-color: transparent;")

        self.label_user_id = QtWidgets.QLabel(self.frame_extendet_user_info)
        self.label_user_id.setMaximumSize(QtCore.QSize(16777215, 18))
        self.label_user_id.setStyleSheet(
            "color: rgb(150, 170, 200);\nfont: 10pt \"MS Shell Dlg 2\";\nbackground-color: transparent;\npadding-left:4px;")

        self.btn_link_username = QtWidgets.QPushButton(self.frame_extendet_user_info)
        self.btn_link_username.setStyleSheet(
            "QPushButton{\nmargin-left: 0px;\nmargin-right: 0px;\nborder-width: 0px;\nborder-radius: 0px;\ncolor: rgb(150, 170, 200);\n"
            "font: 10pt \"MS Shell Dlg 2\";\nbackground-color: transparent;\npadding-left: 4px;\npadding-right: 4px;}QPushButton:hover{\nborder-radius: 5px;\nbackground-color: rgb(57, 91, 136);}")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.frame_update_user = QtWidgets.QFrame(self.user_item_frame)
        self.frame_update_user.setStyleSheet(
            "margin-left: 0px;\nmargin-right: 0px;\nborder-width: 0px;\nborder-radius: 0px;\nbackground-color: transparent;")

        self.comboBox = QtWidgets.QComboBox(self.frame_update_user)
        self.comboBox.setMinimumSize(QtCore.QSize(65, 26))
        self.comboBox.setMaximumSize(QtCore.QSize(65, 26))
        self.comboBox.setStyleSheet(
            "color: rgb(240, 240, 240);\nfont: 10pt \"MS Shell Dlg 2\";\nbackground-color: transparent;\nborder-radius: 5px;\nborder: solid;\n"
            "border-width: 3px;\nborder-color: rgb(29, 27, 27);\nmargin-left: 0px;\nmargin-right: 0px;\npadding-left: 3px;")
        self.comboBox.addItem("юзер")
        self.comboBox.addItem("бан")

        self.btn_uplay_user_chenge = QtWidgets.QPushButton(self.frame_update_user)
        self.btn_uplay_user_chenge.setMinimumSize(QtCore.QSize(20, 20))
        self.btn_uplay_user_chenge.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_uplay_user_chenge.setStyleSheet(
            "QPushButton{\nmargin-left: 0px;\nmargin-right: 0px;\nborder-width: 0px;\ncolor: rgb(240, 240, 240);\n"
            "border-radius: 0px;\nbackground-color: transparent;}\nQPushButton:hover{\nborder-radius: 5px;\nbackground-color: rgb(57, 91, 136);}\n")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.btn_uplay_user_chenge.setIcon(icon)
        self.btn_uplay_user_chenge.setIconSize(QtCore.QSize(18, 18))

        self.frame_update_user.layout = QtWidgets.QHBoxLayout(self.frame_update_user)
        self.frame_update_user.layout.setContentsMargins(0, 0, 0, 0)
        self.frame_update_user.layout.setSpacing(5)
        self.frame_update_user.layout.addWidget(self.comboBox)
        self.frame_update_user.layout.addWidget(self.btn_uplay_user_chenge)

        self.frame_extendet_user_info.layout = QtWidgets.QHBoxLayout(self.frame_extendet_user_info)
        self.frame_extendet_user_info.layout.setContentsMargins(0, 0, 0, 0)
        self.frame_extendet_user_info.layout.setSpacing(0)
        self.frame_extendet_user_info.layout.addWidget(self.label_user_id)
        self.frame_extendet_user_info.layout.addWidget(self.btn_link_username)
        self.frame_extendet_user_info.layout.addItem(spacerItem)

        self.user_item_frame.layout = QtWidgets.QGridLayout(self.user_item_frame)
        self.user_item_frame.layout.setContentsMargins(3, 3, 3, 3)
        self.user_item_frame.layout.setVerticalSpacing(2)
        self.user_item_frame.layout.addWidget(self.label_user_name, 0, 0, 1, 1)
        self.user_item_frame.layout.addWidget(self.frame_extendet_user_info, 1, 0, 1, 1)
        self.user_item_frame.layout.addWidget(self.frame_update_user, 1, 1, 1, 1)

        user_group_form_layout.addWidget(self.user_item_frame)

        self.label_user_name.setText(self.settings['first_name'])
        self.label_user_id.setText(str(self.settings['id']))

        username = self.settings.get("username", None)

        if username == None:
            self.btn_link_username.hide()
        else:
            self.btn_link_username.setText("@" + username if username else "")
            self.btn_link_username.clicked.connect(lambda: webbrowser.open(f"https://t.me/{self.settings['username']}"))

        self.btn_uplay_user_chenge.clicked.connect(self.uplay_user_chenge)

    def uplay_user_chenge(self):

        Index = self.comboBox.currentIndex()

        if Index == 0:
            self.settings["type"] = "user"
        elif Index == 1:
            self.settings["type"] = "baned"

        self.cls_settings.update_user(self.settings["id"], self.settings)


class user_group_form:
    def __init__(self, parent, main_parent):
        self.main_parent = main_parent
        self.widget = QtWidgets.QFrame(parent)
        self.layout = parent.layout
        self.users_items = []
        self.showe_stage = True

        self.setupUi()

    def setupUi(self):
        self.widget.setFixedSize(360, 35)
        self.widget.setStyleSheet("margin-left: 10px;\nbackground-color: rgb(37, 46, 61);\nborder-radius: 15px;")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 4)
        self.verticalLayout.setSpacing(8)

        self.user_group_summary = QtWidgets.QFrame(self.widget)
        self.user_group_summary.setMinimumSize(QtCore.QSize(0, 35))
        self.user_group_summary.setMaximumSize(QtCore.QSize(16777215, 35))
        self.user_group_summary.setStyleSheet("margin-left: 0px;\nborder-radius: 15;")

        self.btn_detais_change_state = QtWidgets.QPushButton(self.widget)
        self.btn_detais_change_state.setFixedSize(360, 35)
        self.btn_detais_change_state.setStyleSheet("""QPushButton{
font: 16pt \"MS Shell Dlg 2\";
color: rgb(230,230,230);
border-radius: 13;
background-color: rgb(55, 66, 86);}
QPushButton:hover{
background-color: rgb(64, 80, 106);
font: 75 16pt \"MS Shell Dlg 2\";
color: rgb(250,250,250);}""")

        self.layout.addWidget(self.widget)

        self.verticalLayout.addWidget(self.user_group_summary)

        self.btn_detais_change_state.clicked.connect(self.showe_stage_chenge)

    def showe_stage_chenge(self):
        if self.showe_stage:
            self.widget.setFixedSize(360, 35)
            for i in self.users_items:
                i.user_item_frame.hide()
            self.showe_stage = False
        else:
            self.widget.setFixedSize(360, 43 + (len(self.users_items) * 70))
            for i in self.users_items:
                i.user_item_frame.show()
            self.showe_stage = True

    def add_users(self, user_list):
        self.users_items = []
        for i in user_list:
            self.users_items.append(UserItem(self.verticalLayout, i, self.main_parent))


class user_group_item_form:
    def __init__(self, parent, settings, main_parent=None, do_show=False):
        self.form = user_group_form(parent, main_parent)
        self.main_parent = main_parent
        self.form.btn_detais_change_state.setText(settings[0])

        self.users = settings[1]

        self.user_list_update()

        self.form.showe_stage_chenge()
        if do_show:
            self.form.showe_stage_chenge()

    def user_list_update(self):
        #   Функция обновляет графическое наполнение страницы с пользователями
        for i in self.form.users_items:
            i.user_item_frame.deleteLater()

        self.form.add_users(self.users)

        self.form.showe_stage_chenge()
        self.form.showe_stage_chenge()

        if not self.users:
            return self.form.widget.hide()
        self.form.widget.show()


class user_group_new_form(user_group_item_form):
    def __init__(self, parent, main_parent):
        super().__init__(parent, ["Новые пользователи", main_parent.settings.new], main_parent, do_show=True)


class user_group_user_form(user_group_item_form):
    def __init__(self, parent, main_parent):
        super().__init__(parent, ["Пользователи", main_parent.settings.users], main_parent, do_show=True)


class user_group_baned_form(user_group_item_form):
    def __init__(self, parent, main_parent):
        super().__init__(parent, ["Заблокированные", main_parent.settings.baned], main_parent, do_show=False)
