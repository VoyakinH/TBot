import telebot

bot = telebot.TeleBot("740360635:AAFoIbn-rmo3BtS4cYitmd41fMrU0hsfceE")


@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "You said help")


@bot.message_handler(commands=['note'])
def send_welcome(message):
	bot.reply_to(message, "You said note")


@bot.message_handler(commands=['shownotes'])
def send_welcome(message):
	bot.reply_to(message, "You said shownotes")


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