import telebot
from telebot import types

bot = telebot.TeleBot('1507860102:AAH3y4nFwQgnYJCFP49PMRRqQVEvhIGrLmw')

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Tak', 'Nie')
    msg = bot.reply_to(message,
        """\
            Cześć witam w quize.
            Kontynujemy?
        """,
        reply_markup=markup)
    bot.register_next_step_handler(msg, start_quiz_step)


def start_quiz_step(message):
    try:
        chat_id = message.chat.id
        answer = message.text
        if answer == "Tak":
            msg = bot.reply_to(message, 'Jak masz na imię?')
            bot.register_next_step_handler(msg, process_name_step)
        elif answer == "Nie":
            bot.send_message(chat_id, 'Miło było cię poznać')
        else:
            raise Exception("Unknown answer")
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Ile masz lat?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_name_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == 'Male') or (sex == 'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')



# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

bot.polling(none_stop=True)