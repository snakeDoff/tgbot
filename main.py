# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
import json


def main():
    updater = Updater('1781018788:AAFlBCzDqTgbat8UpyUJHAjSPJ7YCyparRk', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add", add_number))
    dp.add_handler(CommandHandler("show", show_number))

    updater.start_polling()
    updater.idle()


reply_keyboard = [['/start', '/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Привет! Я Кибакен-Бот. Вы можете узнать как записан телефонный номер у других пользователей "
        "или добавить свой вариант записи. P.S. На данный момент бот работает только с номерами из России",
        reply_markup=markup
        )


def add_number(update, context):
    try:
        aaa = update.message.text.split()[1].split('*')
        assert len(aaa) == 2
        nomer = format(aaa[0], update)
        name = aaa[1]
        with open('numbers.json', 'r') as file:
            f = json.load(file)
            if nomer in f:
                f[nomer] = f[nomer] + [name]
            else:
                f[nomer] = [name]

        with open('numbers.json', 'w') as fil:
            json.dump(f, fil)

    except AssertionError:
        update.message.reply_text(
            "Вы задали команду неправильного формата")


def show_number(update, context):
    try:
        number = format(update.message.text.split(' ')[1], update)
        assert len(update.message.text.split()) == 2
        with open('numbers.json', 'r') as file:
            f = json.load(file)
            if number in f:
                data = ', '.join(f[number])
                update.message.reply_text(f'Номер {number} записывают как: {data}.')
            else:
                update.message.reply_text('Запрашиваемого номера нет в базе бота')
    except AssertionError:
        update.message.reply_text(
            "Вы задали команду неправильного формата")


def help(update, context):
    update.message.reply_text(
        "Активные команды:\n"
        "/start - описание программы\n"
        "/add номер*название - добавить номер в базу\n"
        "/show номер - показать как записывают номер")


def format(number, update):
    try:
        number = "".join(number.split())
        assert not (number[0] != '8' and number[:2] != '+7')
        assert "--" not in number and "-" != number[-1] and ("((" or "))") not in number
        assert number.count("(") - number.count(")") == 0
        for i in ['-', '(', ')']:
            number = number.replace(i, "")
        if number[0] != '+':
            number = '+7' + number[1:]
        if len(number) != 12:
            number[len(number) + 2]
        return number
    except AssertionError:
        update.message.reply_text('Ваш номер имеет неверный формат')
    except IndexError:
        update.message.reply_text('Ваш номер имеет неверное количество цифр')

#написано на коленке, не бейте
if __name__ == '__main__':
    main()
#1
#чтобы ровно сто строк по красоте было
