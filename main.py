import telebot
import pandas as pd
import os
from telegram import InputMediaPhoto
from telebot import types


TOKEN = '7461237013:AAGAh1BeaqRDiQ-SY2caHHyM7iVpusmvzYs'

bot = telebot.TeleBot(TOKEN)

user_context = {}


def get_csv_path_by_mode(mode):
    mode_to_path = {
        'нокаут': 'Modes/нокаут/export.csv',
        'горячая зона': 'Modes/горячая зона/export.csv',
        'осада': 'Modes/осада/export.csv',
        'ограбление': 'Modes/ограбление/export.csv',
        'захват кристалов': 'Modes/захват кристалов/export.csv',
        'награда за поимку': 'Modes/награда за поимку/export.csv',
        'броуболл': 'Modes/броуболл/export.csv',
        'зачистка': 'Modes/зачистка/export.csv',
    }

    return mode_to_path.get(mode, None)


def get_csv_path_by_map(mode, map_name):
    mode_to_map = {
        'нокаут': {
            'живописный утёс': 'Modes/нокаут/живописный утёс/export.csv',
            'в чистом поле': 'Modes/нокаут/в чистом поле/export.csv',
            'месть луи': 'Modes/нокаут/месть луи/export.csv',
            'новые горизонты': 'Modes/нокаут/новые горизонты/export.csv',
            'омут': 'Modes/нокаут/омут/export.csv',
            'ущелье золотой руки': 'Modes/нокаут/ущелье золотой руки/export.csv',
            'четыре уровня': 'Modes/нокаут/четыре уровня/export.csv',
        },
        'горячая зона': {
            'открытая зона': 'Modes/горячая зона/открытая зона/export.csv',
            'муравьиные бега': 'Modes/горячая зона/муравьиные бега/export.csv',
            'огненное кольцо': 'Modes/горячая зона/огненное кольцо/export.csv',
            'открыто!': 'Modes/горячая зона/открыто!/export.csv',
            'параллельная игра': 'Modes/горячая зона/параллельная игра/export.csv',
            'разрыв': 'Modes/горячая зона/разрыв/export.csv',
        },
        'броуболл': {
            'в окружении': 'Modes/броуболл/в окружении/export.csv',
            'в центре внимания': 'Modes/броуболл/в центре внимания/export.csv',
            'галактическая арена': 'Modes/броуболл/галактическая арена/export.csv',
            'дворовый чемпионат': 'Modes/броуболл/дворовый чемпионат/export.csv',
            'зловредные поля': 'Modes/броуболл/зловредные поля/export.csv',
            'мечта вратаря': 'Modes/броуболл/мечта вратаря/export.csv',
            'пинбол': 'Modes/броуболл/пинбол/export.csv',
            'пляжный волейбол': 'Modes/броуболл/пляжный волейбол/export.csv',
            'сетчатка': 'Modes/броуболл/сетчатка/export.csv',
            'солнечный футбол': 'Modes/броуболл/солнечный футбол/export.csv',
            'суперпляж': 'Modes/броуболл/суперпляж/export.csv',
        },
        'захват кристалов': {
            'вжух-вжух': 'Modes/захват кристалов/вжух-вжух/export.csv',
            'затопленная шахта': 'Modes/захват кристалов/затопленная шахта/export.csv',
            'конечная станция': 'Modes/захват кристалов/конечная станция/export.csv',
            'кристальный форт': 'Modes/захват кристалов/кристальный форт/export.csv',
            'острый угол': 'Modes/захват кристалов/острый угол/export.csv',
            'открытая местность': 'Modes/захват кристалов/открытая местность/export.csv',
            'поганковая западня': 'Modes/захват кристалов/поганковая западня/export.csv',
            'подрыв': 'Modes/захват кристалов/подрыв/export.csv',
            'роковая шахта': 'Modes/захват кристалов/роковая шахта/export.csv',
            'сельский клуб': 'Modes/захват кристалов/сельский клуб/export.csv',
        },
        'зачистка': {
            'змеиные степи': 'Modes/зачистка/змеиные степи/export.csv',
            'неумолимый урок': 'Modes/зачистка/неумолимый урок/export.csv',
            'падающая звезда': 'Modes/зачистка/падающая звезда/export.csv',
            'рай для злодея': 'Modes/зачистка/рай для злодея/export.csv',
            'родные просторы': 'Modes/зачистка/родные просторы/export.csv',
            'четверной урон': 'Modes/зачистка/четверной урон/export.csv',
        },
        'награда за поимку': {
            'гранд-канал': 'Modes/награда за поимку/гранд-канал/export.csv',
            'кремовый торт': 'Modes/награда за поимку/кремовый торт/export.csv',
            'падающая звезда': 'Modes/награда за поимку/падающая звезда/export.csv',
            'укрытие': 'Modes/награда за поимку/укрытие/export.csv',
            'царь горы': 'Modes/награда за поимку/царь горы/export.csv',
        },
        'ограбление': {
            'взятие моста': 'Modes/ограбление/взятие моста/export.csv',
            'гг морг': 'Modes/ограбление/гг морг/export.csv',
            'горячая кукуруза': 'Modes/ограбление/горячая кукуруза/export.csv',
            'надёжное укрытие': 'Modes/ограбление/надёжное укрытие/export.csv',
            'пит стоп': 'Modes/ограбление/пит стоп/export.csv',
            'пороховый каньон': 'Modes/ограбление/пороховый каньон/export.csv',
        },
    }

    return mode_to_map.get(mode, {}).get(map_name)


def calculate_win_probability(csv_path, characters):
    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File '{csv_path}' not found.")

        df = pd.read_csv(csv_path, encoding='cp1251')
        df_two_columns = df.iloc[:, :2]
        pairs = list(df_two_columns.itertuples(index=False, name=None))

        names_to_filter = [name.strip() for name in characters.split(',')]
        filtered_pairs = [pair for pair in pairs if pair[0] in names_to_filter]

        if not filtered_pairs:
            raise ValueError("None of the characters provided are found in the dataset.")

        second_column_values = [pair[1] for pair in filtered_pairs]
        numeric_values = list(map(float, second_column_values))

        if len(numeric_values) < 3:
            raise ValueError("Insufficient data to calculate win probability.")

        percentWin = round(sum(numeric_values) / 3 * 100, 1)

    except FileNotFoundError as e:
        print(f"File '{csv_path}' not found: {e}")
        return None, None
    except ValueError as e:
        print(f"Error calculating win probability: {e}")
        return names_to_filter, None
    except Exception as e:
        print(f"Error processing file '{csv_path}': {str(e)}")
        return None, None

    return names_to_filter, percentWin


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет дорогой бравлер!ㅤ/ᐠ - ˕ -マ  Я могу помочь тебе определить шанс выигрыша твоей команды в игре ✰BRAWL STARS✰. \n"
                                      "Для того чтобы начать, выбери режим игры (обязательно 3 на 3):")
    send_mode_keyboard(message)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    text = message.text.strip().lower()

    if text == "начать":
        bot.send_message(message.chat.id, "Привет дорогой бравлер!ㅤ/ᐠ - ˕ -マ  Я могу помочь тебе определить шанс выигрыша твоей команды в игре ✰BRAWL STARS✰. \n"
                     "Для того чтобы начать, выбери режим игры (обязательно 3 на 3):")
        send_mode_keyboard(message)
    elif text == "режим":
        send_mode_keyboard(message)
    elif text == "пики":
        send_brawler_keyboard(message)
    elif message.chat.id in user_context and 'mode' in user_context[message.chat.id] and 'map' in user_context[message.chat.id]:
        process_brawlers(message)
    else:
        bot.send_message(message.chat.id, "Прости ˙◠˙, я не понимаю твоего сообщения. Выбери 'начать'")


def send_mode_keyboard(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    modes = ['нокаут', 'горячая зона', 'ограбление', 'захват кристалов', 'награда за поимку', 'броуболл', 'зачистка']
    for mode in modes:
        keyboard.add(types.InlineKeyboardButton(mode, callback_data=f'mode_{mode}'))

    bot.send_message(message.chat.id, "❕ Выбери режим игры:", reply_markup=keyboard)


def send_map_keyboard(message, mode):
    maps = get_maps_for_mode(mode)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for map_name in maps:
        keyboard.add(types.InlineKeyboardButton(map_name, callback_data=f'map_{map_name}'))

    bot.send_message(message.chat.id, f"❕ Выбери карту для режима '{mode}':", reply_markup=keyboard)


def get_maps_for_mode(mode):
    if mode == 'нокаут':
        return ['живописный утёс', 'омут', 'в чистом поле', 'ущелье золотой руки', 'месть луи', 'новые горизонты', 'четыре уровня']
    elif mode == 'горячая зона':
        return ['открытая зона', 'муравьиные бега', 'огненное кольцо', 'открыто!', 'параллельная игра', 'разрыв']
    elif mode == 'броуболл':
        return ['в окружении', 'в центре внимания', 'галактическая арена', 'дворовый чемпионат', 'зловредные поля','мечта вратаря', 'пинбол', 'пляжный волейбол', 'сетчатка', 'солнечный футбол', 'суперпляж']
    elif mode == 'захват кристалов':
        return ['вжух-вжух', 'затопленная шахта', 'конечная станция', 'кристальный форт', 'острый угол', 'открытая местность','поганковая западня', 'подрыв', 'роковая шахта', 'сельский клуб']
    elif mode == 'зачистка':
        return ['змеиные степи', 'неумолимый урок', 'падающая звезда', 'рай для злодея', 'родные просторы', 'четверной урон']
    elif mode == 'награда за поимку':
        return ['гранд-канал', 'кремовый торт', 'падающая звезда', 'укрытие', 'царь горы']
    elif mode == 'ограбление':
        return ['взятие моста', 'гг морг', 'горячая кукуруза', 'надёжное укрытие', 'пит стоп', 'пороховый каньон']
    return []


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.message:
        chat_id = call.message.chat.id

        if call.data.startswith('mode_'):
            mode = call.data.split('_')[1]
            if chat_id not in user_context:
                user_context[chat_id] = {}
            user_context[chat_id]['mode'] = mode
            bot.send_message(chat_id, f"Отлично! ^._.^ฅ Теперь выбери карту для режима '{mode}'.")
            send_map_keyboard(call.message, mode)

        elif call.data.startswith('map_'):
            map_name = call.data.split('_')[1]
            if chat_id in user_context and 'mode' in user_context[chat_id]:
                mode = user_context[chat_id]['mode']
                user_context[chat_id]['map'] = map_name
                photo_paths = [
                    'картинки/помощь с персонажами/персы1.jpg',
                    'картинки/помощь с персонажами/персы2.jpg',
                    'картинки/помощь с персонажами/персы3.jpg',
                    'картинки/помощь с персонажами/персы4.jpg',
                    'картинки/помощь с персонажами/персы5.jpg',
                    'картинки/помощь с персонажами/персы6.jpg',
                    'картинки/помощь с персонажами/персы7.jpg',
                    'картинки/помощь с персонажами/персы8.jpg'
                ]

                media = [types.InputMediaPhoto(media=open(photo_path, 'rb')) for photo_path in photo_paths]

                bot.send_media_group(chat_id, media)

                caption = f"Отлично! Теперь введи список персонажей, разделенных запятой, для режима '{mode}' и карты '{map_name}'." \
                          f" Для этого перепиши имя нужного персонажа с картинки, чтобы я не ошибся (напиши их КАПСОМ)"
                bot.send_message(chat_id, caption)
            else:
                bot.send_message(chat_id, "Произошла ошибка⚠️. Пожалуйста, начни сначала выбрав режим и карту.")


@bot.message_handler(content_types=['text'])
def talk(message):
    text = message.text.strip().lower()

    if text == "режим":
        send_mode_keyboard(message)
    elif text == "пики":
        send_brawler_keyboard(message)
    else:
        process_brawlers(message)


def send_brawler_keyboard(message):
    bot.send_message(message.chat.id, "Мне нужно чтобы ты ввел список персонажей, разделенных запятой, после выбора режима и карты.ㅤᵕ̈")


@bot.message_handler(content_types=['text'])
def process_brawlers(message):
    if message.chat.id in user_context and 'mode' in user_context[message.chat.id] and 'map' in user_context[message.chat.id]:
        mode = user_context[message.chat.id]['mode']
        map_name = user_context[message.chat.id]['map']
        characters = message.text.strip()
        path = get_csv_path_by_map(mode, map_name)

        if path is None:
            bot.send_message(message.chat.id, f"Файл для режима '{mode}' и карты '{map_name}' не найден.")
            return

        names, win_probability = calculate_win_probability(path, characters)
        if win_probability is not None:
            bot.send_message(message.chat.id, f"Список твоей команды: {', '.join(names)}")
            bot.send_message(message.chat.id, f"Шанс на победу 🏆๋࣭: {win_probability} %")
        else:
            bot.send_message(message.chat.id, "Я ошибся при вычислении выигрыша, ты наверное неправильно написал имена персонажей, попробуй исправить это или нажми 'Начать' :с")
    else:
        bot.send_message(message.chat.id, "Произошла ошибка⚠️. Пожалуйста, начни сначала выбрав режим и карту")


bot.polling(none_stop=True)
