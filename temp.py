# Импортируем необходимые классы.
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import json







def main():
    updater = Updater('1781018788:AAFlBCzDqTgbat8UpyUJHAjSPJ7YCyparRk', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("add_number", add_number))

    updater.start_polling()
    updater.idle()


def start(update, context):
    update.message.reply_text(
        "Привет! Я Кибакен-Бот. Вы можете узнать как записан телефонный номер у других пользователей "
        "или добавить свой вариант записи. P.S. На данный момент бот работает только с номерами из России")


def add_number(update, context):
    try:
        aaa = update.message.text.split()[1].split('*')
        assert len(aaa) == 2
        nomer = format(aaa[1], update)
        name = aaa[2]
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
            "Я пока не умею помогать... Я только ваше эхо.")
        






def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")



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



# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
