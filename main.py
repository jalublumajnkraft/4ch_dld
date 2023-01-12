from flask import Flask
from flask import request
from flask import Response
import requests
import TSFunc
 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        msg = request.get_json() #Сообщение пользователя в формате json.
        chat_id , txt = TSFunc.parse_message(msg) #id чата и текст сообщение из msg.
        try:
            r = requests.get(txt)

            #Проверяет сообщение пользователя, 
            #Если пользователь отправил ссылку, но нерабочую, то информируем об ошибке.
            if r.status_code != 200:  

                TSFunc.message(chat_id , 'Что то пошло не так....')

            else:
                #Генерируем ссылку на json файл, если ссылка рабочая.
                url , board = TSFunc.url_gen(txt)
                if url :
                    Photo , Video , Document , Animation = TSFunc.JSA(url , board)

                    #Отправляем файлы:
                    pPhoto = TSFunc.parting(Photo)
                    for i in range(len(pPhoto)):
                        TSFunc.mediagroup(chat_id , pPhoto[i])

                    pVideo = TSFunc.parting(Video)
                    for i in range(len(pVideo)):
                        TSFunc.mediagroup(chat_id , pVideo[i])

                    pDocument = TSFunc.parting(Document)
                    for i in range(len(pDocument)):
                        TSFunc.mediagroup(chat_id , pDocument[i])

                    #Анимации отправляем по одной, т.к. метод sendMediaGroup не поддерживает их.
                    for i in range(len(Animation)):
                        TSFunc.animation(chat_id , Animation[i]['media'])

                    TSFunc.message(chat_id , 'Все!') #Сообщаем пользователю что все файлы отправлены.

                else: #Если пользователь отправил рабочую ссылку, но не на тред.
                    TSFunc.message(chat_id , 'Это не ссылка на тред.....')
        except:
            if txt == '/start': #Начало общения с ботом.
                TSFunc.message(chat_id , 'Привет, кидай ссылку на тред.....')
            else: #Если пользователь отправил не ссылку на тред.
                TSFunc.message(chat_id , 'Это не ссылка на тред.....')

        return Response('ok', status=200)

    else:
        return 'vam zdes ne radi'

if __name__ == '__main__':
   app.run(debug = True)