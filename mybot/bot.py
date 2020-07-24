import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler)
import settings
#import ephem
from read_citys import collect_citys
from glob import glob
from random import choice
from gtts import gTTS


logging.basicConfig(filename='bot.log', level=logging.INFO)
GAME = range(1)
PROXY = {'proxy_url' : settings.PROXY_URL, 
    'urllib3_proxy_kwargs' : {'username' : settings.PROXY_USERNAME, 'password' : settings.PROXY_PASSWORD}}


#for_planet = []
city_list = collect_citys() # Список формируется из city.csv
if_bot_dont_know = [] # Если бот не знает город. Реальные города можно добавить в пул

#def where_this_planet():
#    planets = {
#        "Mars" : ephem.Mars(),
#        "Uranus" : ephem.Uranus(),
#    }
#    if for_planet[0] in planets:
#        p = planets[for_planet[0]]
#        p.compute(for_planet[1])
#        return ephem.constellation(p)

#def planets(update, context):
#    print("Вызван /planets")
#    reply_keyboard = [["Mars", "Uranus"]]

#    answer = update.message.reply_text("Выбери планету, о которой хочешь узнать",
#        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

#def write_planet(update, context):
#    for_planet.append(update.message.text)
#    update.message.reply_text("Теперь введи дату в формате ГГГГ/ММ/ДД")

#def write_date(update,context):
#    for_planet.append(update.message.text)
#    answer = where_this_planet()
#    update.message.reply_text(f'{answer[0]} -> {answer[1]}')

#def wordcount_start(update, context):
#    words = len(context.args)
#    if words:
#        if words % 10 == 1 and words != 11:
#            update.message.reply_text(f'Ты написал {words} слово!')
#        elif words % 10 in range(2, 5) and words not in range(12, 15):
#            update.message.reply_text(f'Ты написал {words} слова!')
#        else:
#            update.message.reply_text(f'Ты написал {words} слов!')     
#    else:
#        update.message.reply_text(f'Мне нечего считать =(')
#        update.message.reply_text(f'Пример использования /wordcount фраза')

#    return ConversationHandler.End

def start_citys(update, context):
    update.message.reply_text("""Привет, сейчас будем играть в города!
Ты начинаешь - введи город с большой буквы.
Если захочешь закончить игру, введи /cancel""")
    print(update.message.from_user)
    context.user_data["city_list"] = list(city_list)
    context.user_data["refresh_list"] = []

    
    return GAME

def check_user_city(context, user_city):
    first_letter = user_city[0].lower()
    if len(context.user_data['refresh_list']) != 0:
        prev_city = context.user_data['refresh_list'][-1]
        if prev_city[-1] != first_letter:
            return 0
        return 1

def citys(update, context):
    user_city = update.message.text
    last_letter = user_city[-1].upper()
    if user_city not in context.user_data['city_list']:
        update.message.reply_text("Я знаю 11 тысяч городов, а такого не знаю, значит его нет или ты его уже называл. Попробуй еще")
        if_bot_dont_know.append(user_city)
        return GAME
    if check_user_city(context, user_city) == 0:
        update.message.reply_text("Кожанный мешок, ты меня пытаешься обмануть?")
        return GAME
    context.user_data['refresh_list'].append(user_city)
    context.user_data['city_list'].remove(user_city)
    for city in context.user_data['city_list']:
        if city[0] == last_letter:
            update.message.reply_text(update.message.from_user['first_name'] + ' : ' + city)
            context.user_data['refresh_list'].append(city)
            context.user_data['city_list'].remove(city)
            return GAME
    update.message.reply_text("Похоже я проиграл, больше не знаю городов(((")
    return ConversationHandler.END

def cancel(update, context):
    username = update.message.from_user['first_name']
    update.message.reply_text(f'Че, {username}, потрачено? Заходи еще')
    
    return ConversationHandler.END

def send_friend_picture(update, context):
    chat_id = update.effective_chat.id
    friends = {
        "Слава": 'friends_photos/slava*',
        "Маша": 'friends_photos/masha*',
        "Саша": 'friends_photos/sasha*',
        "Ира": 'friends_photos/ira*',
        "Рома": 'friends_photos/roma*',
        "Антон": 'friends_photos/anton*',
        "Настя":'friends_photos/nastya*',
    }
    if context.args:
        photo_of = context.args[0]
        if photo_of in friends:
            photo_list = glob(friends[photo_of])
            to_send_photo = choice(photo_list)
            #string_to_tts = f'Это твой братан {photo_of}'
            #tts = gTTS(string_to_tts, lang='ru') # sound part
            #tts.save('bratan.mp3') #sound part
            context.bot.send_photo(chat_id=chat_id, photo=open(
                to_send_photo, 'rb')) 
            context.bot.send_audio(chat_id=chat_id, audio=open(
                'bratan.mp3', 'rb'))
        else:
            message = "Тут не такого братана"
    else:
        message = "Ты не выбрал братана!"
    if message:
        update.message.reply_text(message)

def aleksey(update, context):
    chat_id = update.effective_chat.id
    if context.args:
        string_to_tts = ''.join(context.args)
        tts = gTTS(string_to_tts, lang='ru') # sound part
        tts.save('leha_bratan.mp3') #sound part
        print(context.chat_data)
        context.bot.send_message(chat_id=chat_id, text="@simplycosmos")
        context.bot.send_audio(chat_id=chat_id, audio=open(
            'leha_bratan.mp3', 'rb'))
    else:
        context.bot.send_message(chat_id=chat_id, text="@simplycosmos Возвращайся скорее")


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher

    citys_game = ConversationHandler(
        entry_points=[CommandHandler('citys', start_citys)],
    
        states={
            GAME : [MessageHandler(Filters.text & (~Filters.command), citys)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]    
    )

    dp.add_handler(citys_game)
    dp.add_handler(CommandHandler('bratan', send_friend_picture))
    dp.add_handler(CommandHandler('aleksey', aleksey))
#    dp.add_handler(CommandHandler("planets", planets))
#    dp.add_handler(MessageHandler(Filters.regex('^(Mars|Uranus)$'), write_planet))
#    dp.add_handler(MessageHandler(Filters.regex('^\d\d\d\d/\d\d/\d\d$'), write_date))
#    dp.add_handler(wordcount_hd)
    

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()