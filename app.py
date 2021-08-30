import telebot
from extensions import *
from config import token, keys

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message: telebot.types.Message):
    text = '''Чтобы начать работу, введите любую команду. 
Список команд вы можете получить через /help'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def commands(message: telebot.types.Message):
    text = '''Список всех комманд:
Список всех валют - /values'''
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список всех валют:\n'
    for key in keys.keys():
        text = ''.join((text, key.capitalize(), f' ({keys[key]})\n'))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        value = message.text.lower().split(' ')
        if len(value) != 3:
            raise ConvertionException('Неверное число параметров')
        quote, base, amount = value
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}.')
    else:
        text = f'Цена {amount} {keys[quote]} - {total_base} {keys[base]}'
        bot.reply_to(message, text)


bot.polling()
