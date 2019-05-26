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
	cursor.execute("""CREATE TABLE notes(author text, message text, date text)""")
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
	cursor2.execute("""CREATE TABLE notes(ind integer, author text, message text, date text)""")
	print("База данных объявлений создана")


# Семён сделай это!
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "You said help")


# Получение нового вопроса и запись в базу данных (DONE)
@bot.message_handler(commands=['note'])
def get_one_question(message):
	bot.send_message(message.chat.id, "Введите вопрос преподавателю:")
	bot.register_next_step_handler(message, write_question_to_base)


def write_question_to_base(message):
	name = message.from_user.first_name + ' ' + message.from_user.last_name + ' (' + message.from_user.username + ')'
	time = str(datetime.now().strftime('%H:%M %d-%m'))
	if len(message.text) <= 501:
		t = (name, message.text, time)
		cursor.execute('insert into notes values (?,?,?)', t)
		conn.commit()
		bot.send_message(message.chat.id, "Вопрос записан!")
	else:
		bot.send_message(message.chat.id, "Максимальная длина вопроса - 500 символов.")


# Вывод вопросов от студентов (DONE)
@bot.message_handler(commands=['shownotes'])
def show_all_notes(message):
	cursor.execute('select * from notes order by rowid')
	text = 'Заданные студентами вопросы:\n'
	kol_voprosov = 0
	for row in cursor:
		kol_voprosov += 1
		text += str(kol_voprosov) + ') ' + str(row[0]) + ' ' + str(row[2]) + '\n' + str(row[1]) + '\n'
	if kol_voprosov != 0:
		bot.send_message(message.chat.id, text)
	else:
		bot.send_message(message.chat.id, 'Вопросы отсутствуют.')


# Команда для ответа преподавателем на вопросы студентов (NOT DONE)
@bot.message_handler(commands=['answer'])
def send_welcome(message):
	bot.reply_to(message, "You said answer")


# Удаление вопроса из базы данных (DONE)
@bot.message_handler(commands=['deletenote'])
def delete_question_by_pos(message):
	bot.send_message(message.chat.id, "Введите номер вопроса для удаления без ответа:")
	bot.register_next_step_handler(message, delete_question_from_base)


def delete_question_from_base(message):
	try:
		x = int(message.text)
		sel = cursor.execute('SELECT count() from notes')
		num_quest = str(sel.fetchone())[1:-2]
		if 0 < x <= int(num_quest):
			cursor.execute("DELETE FROM notes WHERE rowid = ?", (x,))
			conn.commit()
			bot.send_message(message.chat.id, "Вопрос удалён")
			conn.commit()
			conn.execute("VACUUM")
			conn.commit()
		else:
			bot.send_message(message.chat.id, "Вопроса с таким номером нет.")
	except:
		bot.send_message(message.chat.id, "Некорректный ввод.")


# Очистка всех вопросов (DONE)
@bot.message_handler(commands=['clearnotes'])
def delete_all_questions(message):
	cursor.execute("DELETE FROM notes")
	bot.send_message(message.chat.id, "Все записи удалены")
	conn.commit()


# Запись нового объявления преподователя в базу данных (NOT DONE)
@bot.message_handler(commands=['newpost'])
def send_welcome(message):
	bot.reply_to(message, "You said newpost")


# Вывод объявлений из базы данных на экран (NOT DONE)
@bot.message_handler(commands=['showposts'])
def send_welcome(message):
	bot.reply_to(message, "You said showposts")


# Очистка всех объявлений в базе данных (NOT DONE)
@bot.message_handler(commands=['clearposts'])
def send_welcome(message):
	bot.reply_to(message, "You said clearposts")


# Удаление одного объявдения по его номеру (NOT DONE)
@bot.message_handler(commands=['deletepost'])
def send_welcome(message):
	bot.reply_to(message, "You said deletepost")


bot.polling()
