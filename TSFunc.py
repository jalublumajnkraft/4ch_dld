import requests
import json
from math import ceil

TOKEN  = '5685073154:AAFK3RgL1PhWCObZMbfeSK5bQuOwFjc8vjA'

def parse_message(message): 
    #print("message-->" , message)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        #print("chat_id-->" , chat_id)
        #print("txt-->" , txt)

        return chat_id , txt

    except:
        chat_id = message['message']['chat']['id']
        txt = 'Null'
        #print("chat_id-->" , chat_id)
        #print("txt-->" , txt)

        return chat_id , txt

def url_gen(Thread_Link_List , chat_id):

    Thread_Link = str(Thread_Link_List)
    LinkVerif1 = Thread_Link.find('4chan.org/')
    LinkVerif2 = Thread_Link.find('4channel.org/')

    start = 'https://a.4cdn.org'
    board = 0
    url = 0

    if ((LinkVerif1 != -1) or (LinkVerif2 != -1)):

        adr = str(Thread_Link[LinkVerif1 + 10:]) * (LinkVerif1 != -1) + str(Thread_Link[LinkVerif2 + 13:]) * (LinkVerif2 != -1)
        board = str(adr.partition('/thread/')[0])
        op = str(adr.partition('/thread/')[2])
        url = f'{start}/{board}/thread/{op}.json'

    return url , board

def JSA(url , board):

    r = requests.get(f'{url}')
    board = str(board + '/')
    data = json.loads(r.text)
    start = 'https://i.4cdn.org/'
    replies = data['posts'][0]['replies']

    MediaPhotoFull = []
    MediaVideoFull = []
    MediaDocumentFull = []
    MediaAnimationFull = []

    for i in range(replies + 1):
        reply = data['posts'][i]

        if reply.__contains__('ext'):
            filename = str(reply['tim'])
            ext = reply['ext']

            if (ext == '.jpg') or (ext == '.png'):
                mediaPhoto = {
                                'type': 'photo',
                                'media': f'{start}{board}{filename}{ext}'
                                }
                MediaPhotoFull.append(mediaPhoto)
            elif (ext == '.webm') or (ext == '.mp4'):
                mediaVideo = {
                                    'type': 'video',
                                    'media': f'{start}{board}{filename}{ext}'
                                    }
                MediaVideoFull.append(mediaVideo)
            elif (ext == '.gif'):
                mediaAnimation = {
                                    'type': 'animation',
                                    'media': f'{start}{board}{filename}{ext}'
                                    }
                MediaAnimationFull.append(mediaAnimation)
            else:
                mediaDocument = {
                                    'type': 'document',
                                    'media': f'{start}{board}{filename}{ext}'
                                    }
                MediaDocumentFull.append(mediaDocument)

    return MediaPhotoFull , MediaVideoFull , MediaDocumentFull , MediaAnimationFull

def parting(Media):

    length = len(Media)
    parts = ceil(length/10)
    return [Media[10*k:10*(k+1)] for k in range(parts)]

def message(chat_id , text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
    r = requests.post(url , json=payload)
    return r

def animation(chat_id , link):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAnimation'
    payload = {
                'chat_id': chat_id,
                'animation': link
                }
    r = requests.post(url, json=payload)
    return r

def document(chat_id , link):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    payload = {
                'chat_id': chat_id,
                'document': link
                }
    r = requests.post(url, json=payload)
    return r

def mediagroup(chat_id , Media):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMediaGroup'
    payload = {
                'chat_id': chat_id,
                'media': Media
                }
    r = requests.post(url, json=payload)
    return r