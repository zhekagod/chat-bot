import os
import sys

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.utils import get_random_id
import datetime
import calendar
import time

from bot_for_chat.config_file import main_token

#  from bot_for_chat.config_file import id_of_chat

fullname_bot_main_file = os.path.abspath(os.path.basename(__file__))
print(fullname_bot_main_file)

path_bot_main_file = os.path.abspath(__file__)

file_of_events = 'memory_of_events.txt'

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# main_token1 = '1144bf0557959009209a3c39435cddd3ef84535600ff09259270899535e13b0960b46eb3287a5c9535592'
vk_session = vk_api.VkApi(token=main_token)

longpoll = VkBotLongPoll(vk_session, 204178882)

# CHAT_ID=vk_session.get_api().messages.searchConversations(q='Test_for_chat-bot',count=1)['items'][0]['peer']['local_id']

print(longpoll.__doc__)


def sender(id, text):
    vk_session.method('message.send', {'user_id': id, 'message': text, 'random_id': get_random_id()})


def chat_sender(id, text):
    # print('id =', id)
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def planning_event(d_1, m_1, y_1):  # + time_1
    day_of_event = d_1
    month_of_event = m_1
    year_of_event = y_1
    # time_of_event = time_1
    file = open(file_of_events, 'a+', encoding='utf-8')
    file.write(day_of_event)
    file.write(month_of_event)
    file.write(year_of_event + '\n')
    # file.write(time_1 + '\n')
    file.close()
    # print(year_of_event, month_of_event, day_of_event)
    # return day_of_event, month_of_event, year_of_event


def date_of_events(d_1, m_1, y_1):  # + time_1
    file = open(file_of_events, 'r', encoding='utf-8')
    info = d_1 + m_1 + y_1 + '\n'
    strings = file.readlines()
    # print(strings)
    # print(info)
    for line in strings:
        if line == info:
            file.close()
            return line


def check_date_of_near_event(near_date):
    file = open(file_of_events, 'r', encoding='utf-8')
    strings = file.readlines()
    # day += '\n'
    near_date += '\n'
    for line in strings:
        if line == near_date:
            file.close()
            return True
    return False


def remove_date_of_event(removing_date):
    file = open(file_of_events, 'r')
    lines = file.readlines()
    removing_date += '\n'
    if removing_date not in lines:
        file.close()
        return False
    else:
        file.close()
        file = open(file_of_events, 'w')
        for line in lines:
            if line != removing_date:
                file.write(line)
        file.close()
        return True


def rewriting_date_of_event(old_date, new_date):  # + id
    file = open(file_of_events, 'a+', encoding='utf-8')
    strings = file.readlines()
    if check_date_of_near_event(old_date):
        remove_date_of_event(old_date)
        day_of_event, month_of_event, year_of_event = new_date.split('.')
        file.write(day_of_event)
        file.write(month_of_event)
        file.write(year_of_event)
        sort_list_of_events()
        print('Перезапись должна быть выполнена')
        return True
    else:
        return False


def clear_list_of_events():
    with open(file_of_events, 'w'):
        print('Файл должен быть очищен')
        pass


def datelist_of_events(id):
    file = open(file_of_events, 'r')
    strings = file.readlines()
    if not strings:
        file.close()
        return False
    else:
        chat_sender(id, f"Список запланированных мероприятий:")
        for i in range(len(strings)):
            chat_sender(id, f"{i + 1}) {strings[i]}")
        file.close()
        return True


def show_bot_commands(id):
    file = open('help_or_commands.txt', 'r', encoding='utf-8')
    chat_sender(id, file.read())
    file.close()


def convert_date(old_date):
    tmp_date = old_date
    tmp_year, tmp_month, tmp_day = tmp_date.split('.')
    tmp_date = tmp_date.replace(tmp_day, tmp_year)
    tmp_date = tmp_date.replace(tmp_year, tmp_day, 1)
    #  print(tmp_day, tmp_month, tmp_year, tmp_date)
    new_date = str(tmp_date)
    return new_date


def convert_date_to_str_date(data):
    data = str(data).replace('-', '.')
    return data


def convert_today_date():
    tmp_today_date = datetime.date.today()
    return convert_date(convert_date_to_str_date(tmp_today_date))


def foo(info):
    try:
        d, m, y = map(int, info.split('.'))
    except:
        return False
    try:
        datetime.date(y, m, d)
        return True
    except:
        return False


def check_right_time(info):
    hour, minute = info.split(':')
    hours = [str(i) for i in range(10)]
    minutes = [str(i) for i in range(10)]
    for i in range(len(hours)):
        hours[i] += '0'
        hours[i] = hours[i][::-1]
        minutes[i] += '0'
        minutes[i] = minutes[i][::-1]
    for i in range(10, 24 + 1):
        hours.append(f"{i}")
    for i in range(10, 60 + 1):
        minutes.append(f"{i}")
    print(hours)
    print(minutes)
    if hour in hours and minute in minutes:
        return True
    else:
        return False


def check_of_existing_chat_id(id):
    print(os.getcwd())
    if os.path.isfile(path_bot_main_file):
        file_id_of_chat_for_bot = open('id_of_chat_for_bot.txt', 'r')
        print('Файл есть и обрабатывается...')
        if str(id) in file_id_of_chat_for_bot.readlines():
            file_id_of_chat_for_bot.close()
            return True
        else:
            file_id_of_chat_for_bot.close()
            file_id_of_chat_for_bot = open('id_of_chat_for_bot.txt', 'w')
            file_id_of_chat_for_bot.write(f"{id}")
            file_id_of_chat_for_bot.close()
    else:
        file_id_of_chat_for_bot = open('id_of_chat_for_bot.txt', 'w')
        file_id_of_chat_for_bot.close()


def convert_date_to_python_interpretation(data):  # БАГ!!! Выдаёт ошибку, если ввести дату 20.05.2021 или 21.05.2021
    day, month, year = map(int, data.split('.'))
    print(day, month, year)
    d = datetime.datetime(year, month, day)  # Дата переводится в формат воспринимаемый Python
    return d                                 # ГГГГ/ММ/ДД


def comparison_datas_of_events(data_1, data_2):
    d1 = convert_date_to_python_interpretation(data_1)
    d2 = convert_date_to_python_interpretation(data_2)
    return d1 - d2


def comparison_days_of_events(data_1, data_2):
    d1 = convert_date_to_python_interpretation(data_1).day
    d2 = convert_date_to_python_interpretation(data_2).day
    return d1 - d2


def sort_list_of_events():
    file = open(file_of_events, 'r')
    chisla = []
    strings = ''
    for line in file.readlines():
        chisla.append(str(convert_date_to_python_interpretation(line)))
    file.close()
    #print(*chisla)
    chisla.sort()
    #print(*chisla)
    #print(chisla[0][4])
    for i in range(len(chisla)):
        strings += convert_date(convert_date_to_str_date(str(chisla[i][:10])))+'\n'
    #print(strings)
    file = open(file_of_events, 'r')
    if strings == str(file.read()):
        #print("Совпадение. Файл отсортирован")
        file.close()
        return True
    else:
        file.close()
        #print("Несовпадение. Файл неотсортирован")
        file = open(file_of_events, 'w')
        for line in strings:
            file.write(line)
        file.close()
        return False


def remembering_of_near_event():
    file = open('id_of_chat_for_bot.txt', 'r')
    while not check_of_existing_chat_id(id_of_chat):
        continue
    if id_of_chat in file:
        file.close()
        print('ID на месте')
        file = open(file_of_events, 'r')
        strings = file.readlines()
        if strings:
            if not sort_list_of_events():
                sort_list_of_events()
            else:
                for i in range(len(strings)):
                    day_of_event, month_of_event, year_of_event = map(int, strings[i].split('.'))
                    today_day, today_month, today_year = map(int, today.split('.'))
                    delta_time = datetime.datetime(year_of_event, month_of_event, day_of_event) - \
                        datetime.datetime(today_year, today_month, today_day)
                    day_delta_time = delta_time.days
                    if day_delta_time == 7:
                        chat_sender(id_of_chat, f"Напоминаю, что мероприятие состоится ровно через одну неделю.")
                    elif day_delta_time == 1:
                        chat_sender(id_of_chat, f"Напоминаю, что завтра состоится мероприятие.")
                    ...


def definition_of_weekday(weekday):
    en_python_weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ru_weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    for i in range(len(en_python_weekdays)):
        if weekday == en_python_weekdays[i]:
            return ru_weekdays[i]


def main_program():
    # reminder = False
    wait_for_data_add_request = False
    # wait_for_time_add_request = False
    wait_for_data_remove_request = False
    for event in longpoll.listen():
        id = event.chat_id
        #  print(type(id))
        while not check_of_existing_chat_id(id):
            chat_sender(id, f"ID не на месте")
            continue
        else:
            chat_sender(id, f"ID на месте")
        if check_date_of_near_event(today):
            chat_sender(id, f"Напоминаю всем, что сегодня состоится мероприятие")
            # reminder = True
            remove_date_of_event(today)
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message['text'].lower()
            chat_sender(id, f"Вроде работает")

            if event.from_chat:

                if wait_for_data_add_request == True:
                    if msg in ['отмена']:
                        wait_for_data_add_request = False
                        #wait_for_time_add_request = False
                        continue
                    if foo(msg) == False:
                        chat_sender(id, f"@id{event.object.message['from_id']} "
                                        f"(Дата введена некорректно. Повторите попытку или введите «отмена».)")
                        continue
                    elif foo(msg) == True:
                        d_1, m_1, y_1 = map(str, msg.split('.'))
                        d_1 += '.'
                        m_1 += '.'
                        date_1 = d_1 + m_1 + y_1
                        if comparison_days_of_events(today, date_1) > 0:  # Пока не ясно, разрешать или запрещать
                            #  равнятся нулю (сегодняшней дате (дню сегодняшней даты))
                            chat_sender(id, f"Событие не может быть запланировано на уже прошедшую дату."
                                        f"Повторите попытку или введите «отмена».")
                            continue
                        else:
                            if check_date_of_near_event(date_1) == True:
                                chat_sender(id, f"На этот день уже запланировано мероприятие. Попробуйте снова или "
                                                f"введите «отмена»")
                            elif check_date_of_near_event(date_1) == False:
                                #wait_for_time_add_request = True
                                #if wait_for_time_add_request == True:
                                    #chat_sender(id, f"Введите время")
                                    #if check_right_time(msg) == False:
                                        #chat_sender(id, f"Время введено неверно. Попробуйте снова или "
                                                #f"введите «отмена»")
                                        #continue
                                    #else:
                                #time_1 = msg.split(':')
                                planning_event(d_1, m_1, y_1) # + time_1
                                date_1 = date_of_events(d_1, m_1, y_1) # + time_1
                                date_1 = str(date_1)
                                chat_sender(id, f"Мероприятие успешно запланировано на " + date_1)
                                wait_for_data_add_request = False
                                #wait_for_time_add_request = False
                if wait_for_data_remove_request == True:
                    if msg in ['отмена']:
                        wait_for_data_remove_request = False
                        continue
                    if foo(msg) == False:
                        chat_sender(id, f"@id{event.object.message['from_id']} "
                                        f"(Дата введена некорректно. Повторите попытку или введите «отмена».)")
                        continue
                    elif foo(msg) == True:
                        d_1, m_1, y_1 = map(str, msg.split('.'))
                        d_1 += '.'
                        m_1 += '.'
                        date_1 = d_1 + m_1 + y_1
                        if remove_date_of_event(date_1) == False:
                            chat_sender(id, f"В списке запланированных мероприятий отсутствует введённая дата."
                                            f"Проверьте правильность вводимых данных или введите «отмена».")
                            continue
                        else:
                            chat_sender(id, f"Введённая дата найдена и успешно удалена.")
                            wait_for_data_remove_request = False




                elif msg in ['привет!']:
                    chat_sender(id, f"@id{event.object.message['from_id']}" + "(Хай)")
                elif msg in ['хочу запланировать мероприятие']:
                    chat_sender(id, f"@id{event.object.message['from_id']} "
                                    f"(Когда состоится мероприятие? Введите дату.)")
                    wait_for_data_add_request = True
                    # planning_event()
                elif msg in ['сегодняшняя дата']:
                    chat_sender(id, f"Сегодняшняя дата: {today}\n"
                                f"День недели: {weekday}")
                    print(today)
                    """if msg != '':
                        
                        chat_sender(id, f"@id{event.object.message['from_id']} "
                                    f"(Мероприятие успешно запланировано!)")"""
                elif msg in ['очистить список запланированных мероприятий']:
                    clear_list_of_events()
                    chat_sender(id, f"Список запланированных мероприятий успешно очищен.")
                elif msg in ['показать список запланированных мероприятий']:
                    if datelist_of_events(id) == False:
                        chat_sender(id, f"Список запланированных мероприятий пуст")

                elif msg in [f"хочу удалить запланированное мероприятие"]:
                    chat_sender(id, f"@id{event.object.message['from_id']} "
                                    f"(Введите дату мероприятия, которую нужно удалить.)")
                    wait_for_data_remove_request = True
                elif (msg in ['помощь']) or (msg in ['команды']):
                    show_bot_commands(id)
                elif msg in ['sort_list_of_events']:
                    sort_list_of_events()
                elif msg in ['хочу перезаписать событие']:
                    chat_sender(id, 'Введите дату, которую хотите заменить')
                    ...
            else:
                id = event.object.message['from_id']
                sender(id, f"@{event.user_id}, (Хай)")


while True:
    global today
    global reminder
    global q_reminder
    global id_of_chat
    global weekday
    global workdate
    today = convert_today_date()
    workdate = datetime.datetime.strptime(today, "%d.%m.%Y")
    weekday = definition_of_weekday(calendar.day_name[workdate.date().weekday()])
    sort_list_of_events()
    with open('id_of_chat_for_bot.txt', 'r') as f_id:
        id_of_chat = f_id.readline()
    print(today)
    remembering_of_near_event()  # Сбрабатывает лишь при старте бота
    # if check_date_of_near_event():
    # reminder = True
    # q_reminder += 1
    main_program()
