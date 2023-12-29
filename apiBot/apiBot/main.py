import re
import requests
from flask import request
from flask import Flask
from flask.views import MethodView
import os


app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
API_URL = os.environ.get('API_URL')

def get_data_from_api(command):
    url = API_URL + command
    session = requests.Session()
    r = session.get(url).json()
    return r


def send_message(chat_id, msg):
    session = requests.Session()
    r = session.get(TELEGRAM_URL, params=dict(chat_id=chat_id,
                                              text=msg,
                                              parse_mode='Markdown'))
    return r.json()


def parse_text(text_msg):
    '''/start /help, /language, @python '''
    addresses = {'language': 'languages'}
    command_p = r'/\w+'
    dog_p = r'@\w+'
    message = 'Incorrect request'
    if '/' in text_msg:
        if '/start' in text_msg or '/help' in text_msg:
            message = '''
            For actual position's  based on the language please write `/language `

To save your request choose your language e.g `@python`
            '''
            return message
        else:
            command = re.search(command_p, text_msg).group().replace('/', '')
            command = addresses.get(command, None)
            return [command] if command else None
    elif '@' in text_msg:
        result = re.findall(dog_p, text_msg)
        commands = [s.replace('@','')  for s in result]
        commands += [1]
        return commands if len(commands) == 2 else None
    else:
        return message



@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        resp = request.get_json()
        print(resp)
        return '<h1> Hi Telegram! </h1>'
    return '<h1> Hi BOT!!! </h1>'

class BotAPI(MethodView):

    def get(self):
        return '<h1> Hi Class Bot!!! </h1>'

    def post(self):
        resp = request.get_json()
        text_msg = resp['message']['text']
        chat_id = resp['message']['chat']['id']
        tmp = parse_text(text_msg)
        text = 'Incorrect request'
        error_msg = 'Based on your request there is no result'
        if tmp:
            print(tmp)
            if len(tmp) > 10:
                send_message(chat_id, tmp)
            elif len(tmp) == 1:
                command = '/{}'.format(tmp[0])
                resp = get_data_from_api(command)
                if resp:
                    message = ''
                    msg = "Available positions \n"
                    for d in resp:
                        message += '#' +d['slug'] + '\n'
                    send_message(chat_id, msg + message)
                else:
                    send_message(chat_id, error_msg)
            elif len(tmp) == 2:
                command = '/vacancy/?language={}'.format(tmp[0])
                print(command)
                resp = get_data_from_api(command)
                send_message(chat_id, resp)
                if resp:
                    pices = []
                    size = len(resp)
                    extra = len(resp) % 10
                    if size < 11:
                        pices.append(resp)
                    else:
                        for i in range(size // 10):
                            y = i * 10
                            pices.append(resp[y:y + 10])
                    if extra:
                        pices.append(resp[y + 10:])

                    text_msg = "Results based on your request: \n"
                    text_msg = '- ' * 10 + '\n'
                    send_message(chat_id, text_msg)
                    for part in pices:
                        message = ''
                        for v in part:
                            message += v['title'].replace('\t','').replace('\n','') + '\n'
                            url = v['url'].split('?')
                            message += url[0] + '\n'
                            message += '-' * 5 + '\n\n'
                        send_message(chat_id, message)
                else:
                    send_message(chat_id, error_msg)
        else:
            send_message(chat_id, text)
        return '<h1> Hi Telegram! </h1>'

app.add_url_rule(f'/{TOKEN}/', view_func=BotAPI.as_view('bot'))




if __name__ == '__main__':
    app.run()