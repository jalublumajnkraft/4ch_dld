from flask import Flask
from flask import request
from flask import Response
import requests
import TSFunc
 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():

    if request.method == 'POST':
        msg = request.get_json()     
        chat_id , txt = TSFunc.parse_message(msg)
        try:
            r = requests.get(txt)
            if r.status_code != 200:

                TSFunc.message(chat_id , 'что то пошло не так....')

            else:

                url , board = TSFunc.url_gen(txt , chat_id)
                if url :
                    Photo , Video , Document , Animation = TSFunc.JSA(url , board)

                    pPhoto = TSFunc.parting(Photo)
                    for i in range(len(pPhoto)):
                        TSFunc.mediagroup(chat_id , pPhoto[i])

                    pVideo = TSFunc.parting(Video)
                    for i in range(len(pVideo)):
                        TSFunc.mediagroup(chat_id , pVideo[i])

                    pDocument = TSFunc.parting(Document)
                    for i in range(len(pDocument)):
                        TSFunc.mediagroup(chat_id , pDocument[i])

                    for i in range(len(Animation)):
                     TSFunc.animation(chat_id , Animation[i]['media'])

                    TSFunc.message(chat_id , 'все!')
        except:
            if txt == '/start':
                TSFunc.message(chat_id , 'привет кидай ссылку на тред')
            else:
                TSFunc.message(chat_id , 'это не ссылка на тред.....')

        return Response('ok', status=200)

    else:
        return 'vam zdes ne radi'

if __name__ == '__main__':
   app.run(debug = True)