import telebot
from extensions import APIException, CurConverter
from config import TOKEN, keys

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Change It бот приветствует Вас! \n Для конвертации введите через пробел: \n ' \
           '=валюта= =в какую перевести= =количество= \n Список доступных валют /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Список доступных для конвертации валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    values = message.text.split(" ")

    try:
        if len(values) != 3:
            raise APIException('Введите валюты и их количество по образцу: \n евро доллар 20')

        quote, base, amount = values

        total_base = CurConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)

