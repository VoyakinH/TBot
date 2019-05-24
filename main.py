import telebot
import sqlite3
import os
from datetime import datetime

# Объявление бота
bot = telebot.TeleBot("740360635:AAFoIbn-rmo3BtS4cYitmd41fMrU0hsfceE")

# Создание базы данных вопросов(если не создана)
if os.path.exists('./base_questions.db'):
	print("База данных вопросов найдена")
	# Привязка базы данных
	conn = sqlite3.connect("base_questions.db", check_same_thread=False)
	cursor = conn.cursor()
else:
	conn = sqlite3.connect("base_questions.db", check_same_thread=False)
	cursor = conn.cursor()
	cursor.execute("""CREATE TABLE notes(ind integer, author text, message text, date text)""")
	print("База данных вопросов создана")

# Создание базы данных объявлений(если не создана)
if os.path.exists('./base_announcements.db'):
	print("База данных объявлений найдена")
	# Привязка базы данных
	conn2 = sqlite3.connect("base_announcements.db", check_same_thread=False)
	cursor2 = conn.cursor()
else:
	conn2 = sqlite3.connect("base_announcements.db", check_same_thread=False)
	cursor2 = conn2.cursor()
	cursor2.execute("""CREATE TABLE notes(type integer, ind integer, author text, message text, date text)""")
	print("База данных объявлений создана")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "You said help")


@bot.message_handler(commands=['note'])
def get_one_question(message):
	bot.send_message(message.chat.id, "Введите вопрос преподавателю:")
	bot.register_next_step_handler(message, write_question_to_base)


def write_question_to_base(message):
	name = message.from_user.first_name + ' ' + message.from_user.last_name + '(' + message.from_user.username + ')'
	time = str(datetime.now().strftime('%H:%M %d-%m-%Y'))
	t = (1, name, message.text, time)
	cursor.execute('insert into notes values (?,?,?,?)', t)
	cursor.execute('select * from notes')
	kol_voprosov = 1
	for row in cursor:
		kol_voprosov += 1
	for i in range(1, kol_voprosov):
		cursor.execute("UPDATE notes SET ind=? WHERE rowid=?", (i, i))
	conn.commit()
	bot.send_message(message.chat.id, "Вопрос записан!")
	print('Записан новый вопрос в базу вопросов от ', name)


@bot.message_handler(commands=['shownotes'])
def show_all_notes(message):
	cursor.execute('select * from notes order by rowid')
	text = 'Заданные студентами вопросы:\n'
	kol_voprosov = 0
	for row in cursor:
		kol_voprosov += 1
		text += str(row[0]) + ') ' + str(row[1]) + ' ' + str(row[3]) + '\n' + str(row[2]) + '\n'
	if kol_voprosov != 0:
		bot.send_message(message.chat.id, text)
	else:
		bot.send_message(message.chat.id, 'Вопросы отсутствуют.')


@bot.message_handler(commands=['deleteask'])
def delete_question_by_pos(message):
	bot.send_message(message.chat.id, "Введите номер вопроса для удаления без ответа:")
	bot.register_next_step_handler(message, delete_question_from_base)


def delete_question_from_base(message):
	try:
		x = message.text
		cursor.execute("DELETE FROM notes WHERE ind = ?", message.text)
		conn.commit()
		bot.send_message(message.chat.id, "Вопрос удалён")
		cursor.execute('select * from notes order by rowid')
		kol_voprosov = 1
		for row in cursor:
			kol_voprosov += 1
		print(kol_voprosov)
		for i in range(1, kol_voprosov):
			cursor.execute("UPDATE notes SET ind=? WHERE rowid=?", (i, i))
		conn.commit()
	except:
		bot.send_message(message.chat.id, "Возникла ошибка.")


@bot.message_handler(commands=['clearAsks'])
def delete_all_questions(message):
	cursor.execute("DELETE FROM notes")
	bot.send_message(message.chat.id, "Все записи удалены")




@bot.message_handler(commands=['newpost'])
def send_welcome(message):
	bot.reply_to(message, "You said newpost")


@bot.message_handler(commands=['showposts'])
def send_welcome(message):
	bot.reply_to(message, "You said showposts")


@bot.message_handler(commands=['clearposts'])
def send_welcome(message):
	bot.reply_to(message, "You said clearposts")


@bot.message_handler(commands=['clearnotes'])
def send_welcome(message):
	bot.reply_to(message, "You said clearnotes")


@bot.message_handler(commands=['deletepost'])
def send_welcome(message):
	bot.reply_to(message, "You said deletepost")


@bot.message_handler(commands=['deletenote'])
def send_welcome(message):
	bot.reply_to(message, "You said deletenote")


@bot.message_handler(commands=['answer'])
def send_welcome(message):
	bot.reply_to(message, "You said answer")


bot.polling()
