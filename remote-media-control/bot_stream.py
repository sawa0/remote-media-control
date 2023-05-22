from os import name

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from pynput.keyboard import Key, Controller

import telebot, time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from funk import GetSetting


class TextHandler:
    def text_command(self, message):
        user_type = GetSetting().check_user(message.json['chat'])

        if user_type == "baned":
            self.bot.send_message(chat_id=message.chat.id, text=f"id {message.json['chat']['id']} заблокирован",
                                  reply_markup=ReplyKeyboardRemove(selective=False))
            return
        elif user_type == "user":
            self.bot.send_message(chat_id=message.chat.id, text=f"{message.json['chat']['first_name']} ✌️",
                                  reply_markup=self.inline_media_kb)
            return
        elif user_type == "new":
            self.bot.send_message(chat_id=message.chat.id,
                                  text=f"{message.json['chat']['first_name']} ✌️\nЗапрос отправлен")
        return


class CallbackHandler:
    def callback_command(self, call):
        user_type = GetSetting().check_user(call.json['from'])

        if user_type == "baned":
            self.bot.send_message(chat_id=call.from_user.id, text=f"id {call.from_user.id} заблокирован",
                                  reply_markup=ReplyKeyboardRemove(selective=False))
            return

        if user_type == "user":

            if call.data == 'btn_previous':
                self.keyboard.press(Key.media_previous)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_pause':
                self.keyboard.press(Key.media_play_pause)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_next':
                self.keyboard.press(Key.media_next)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_up_volume':
                for i in range(3):
                    self.keyboard.press(Key.media_volume_up)
                    time.sleep(0.05)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_mute':
                self.keyboard.press(Key.media_volume_mute)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_down_volume':
                for i in range(3):
                    self.keyboard.press(Key.media_volume_down)
                    time.sleep(0.05)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_right':
                for i in range(2):
                    self.keyboard.press(Key.right)
                    time.sleep(0.05)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return

            elif call.data == 'btn_left':
                for i in range(2):
                    self.keyboard.press(Key.left)
                    time.sleep(0.05)
                self.bot.answer_callback_query(callback_query_id=call.id, text='✅')
                return
        return


class BotStreamThread(
    QtCore.QThread,
    TextHandler,
    CallbackHandler
):
    def __init__(self, bot_id):
        QtCore.QThread.__init__(self)
        TextHandler.__init__(self)
        CallbackHandler.__init__(self)

        self.inline_media_kb = None
        self.bot_id = bot_id
        self.init_keyboard()
        self.keyboard = Controller()

        self.bot = telebot.TeleBot(self.bot_id, parse_mode=None)
        self.start()

    def run(self):

        @self.bot.message_handler(content_types=['text'])
        def start(message):
            return self.text_command(message)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            return self.callback_command(call)

        self.bot.polling()

    def init_keyboard(self):
        self.inline_media_kb = InlineKeyboardMarkup(row_width=2)

        inline_btn_previous = InlineKeyboardButton('⏮', callback_data='btn_previous')
        inline_btn_pause = InlineKeyboardButton('⏯', callback_data='btn_pause')
        inline_btn_next = InlineKeyboardButton('⏭', callback_data='btn_next')
        inline_btn_right = InlineKeyboardButton('◀️', callback_data='btn_left')
        inline_btn_left = InlineKeyboardButton('▶️', callback_data='btn_right')

        inline_btn_up_volume = InlineKeyboardButton('-6 🔈', callback_data='btn_down_volume')
        inline_btn_mute = InlineKeyboardButton('🔇', callback_data='btn_mute')
        inline_btn_down_volume = InlineKeyboardButton('+6 🔊', callback_data='btn_up_volume')

        self.inline_media_kb.row(inline_btn_previous, inline_btn_next)
        self.inline_media_kb.row(inline_btn_right, inline_btn_pause, inline_btn_left)
        self.inline_media_kb.row(inline_btn_up_volume, inline_btn_mute, inline_btn_down_volume)
