import requests
import json
from math import ceil

#https://api.telegram.org/bot{token}/setWebhook?url={url}
#Токен
TOKEN  = '5685073154:AAFK3RgL1PhWCObZMbfeSK5bQuOwFjc8vjA'

#Функция считывает сообщение пользователя.
def parse_message(message): 
    try:
        chat_id = message['message']['chat']['id'] #id чата
        txt = message['message']['text'] #Текст сообщения

        return chat_id , txt

    except:
        chat_id = message['message']['chat']['id']
        txt = 'Null'

        return chat_id , txt

#Функция принимает ссылку на тред, возврашает: ссылку на json файл треда, название доски(сокращенное).
def url_gen(Thread_Link_List):

    #Проверяем ссылку:
    Thread_Link = str(Thread_Link_List)
    LinkVerif1 = Thread_Link.find('4chan.org/') 
    LinkVerif2 = Thread_Link.find('4channel.org/')

    start = 'https://a.4cdn.org'
    board = 0
    url = 0

    if ((LinkVerif1 != -1) or (LinkVerif2 != -1)): #Если ссылка на тред подходит, возвращаем ссылку на json и название доски.

        adr = str(Thread_Link[LinkVerif1 + 10:]) * (LinkVerif1 != -1) + str(Thread_Link[LinkVerif2 + 13:]) * (LinkVerif2 != -1)
        board = str(adr.partition('/thread/')[0])
        op = str(adr.partition('/thread/')[2])
        url = f'{start}/{board}/thread/{op}.json'

    return url , board

#Функция принимает ссылку на json файл треда, название доски(соеращенное), возвращает: списки ссылок на файлы треда.
def JSA(url , board):

    r = requests.get(f'{url}')
    board = str(board + '/')
    data = json.loads(r.text)
    start = 'https://i.4cdn.org/'
    replies = data['posts'][0]['replies'] #Количество сообщений в треде.

    MediaPhotoFull = [] #Список ссылок на фото.
    MediaVideoFull = [] #Список ссылок на видео.
    MediaDocumentFull = [] #Список ссылок на прочие файлы.
    MediaAnimationFull = [] #Список ссылок на анимации.

    for i in range(replies + 1):
        reply = data['posts'][i] #Сообщение с номером i.

        if reply.__contains__('ext'): #Проверяем наличие файла в сообщении.
            filename = str(reply['tim']) #Имя файла.
            ext = reply['ext'] #Расширение файла.

            if (ext == '.jpg') or (ext == '.png'): #Если расширения файла .jpg или .png, то ссылку в MediaPhotoFull.
                mediaPhoto = {
                                'type': 'photo',
                                'media': f'{start}{board}{filename}{ext}'
                                }
                MediaPhotoFull.append(mediaPhoto)
            elif (ext == '.webm') or (ext == '.mp4'): #Если расширения файла .webm или .mp4, то ссылку в MediaVideoFull.
                mediaVideo = {
                                    'type': 'video',
                                    'media': f'{start}{board}{filename}{ext}'
                                    }
                MediaVideoFull.append(mediaVideo)
            elif (ext == '.gif'): #Если расширения файла .gif, то ссылку в MediaAnimationFull.
                mediaAnimation = {
                                    'type': 'animation',
                                    'media': f'{start}{board}{filename}{ext}'
                                    }
                MediaAnimationFull.append(mediaAnimation)
            else: #Если расширения файла не из из перечисленных выше, то ссылку  в MediaDocumentFull.
                mediaDocument = {
                                    'type': 'document',
                                    'media': f'{start}{board}{filename}{ext}'
                                    }
                MediaDocumentFull.append(mediaDocument)

    return MediaPhotoFull , MediaVideoFull , MediaDocumentFull , MediaAnimationFull

#Функция разделяет список на несколько подсписков по 10 элементов в каждом, возвращает: список из подсписков. 
def parting(Media):

    length = len(Media)
    parts = ceil(length/10) #Количество частей.
    return [Media[10*k:10*(k+1)] for k in range(parts)]

#Бот отправляет текстовое сообщение.
def message(chat_id , text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
    r = requests.post(url , json=payload)
    return r

#Бот отправляет одну анимацию.
def animation(chat_id , link):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAnimation'
    payload = {
                'chat_id': chat_id,
                'animation': link
                }
    r = requests.post(url, json=payload)
    return r

#Бот отправляет один документ.
def document(chat_id , link):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    payload = {
                'chat_id': chat_id,
                'document': link
                }
    r = requests.post(url, json=payload)
    return r

#Бот отправляет несколько файлов в одном сообщении (кроме анимаций).
def mediagroup(chat_id , Media):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMediaGroup'
    payload = {
                'chat_id': chat_id,
                'media': Media
                }
    r = requests.post(url, json=payload)
    return r
