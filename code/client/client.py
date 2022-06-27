import websocket
import threading
import os
import sys
from json import dumps
from json import loads
import deal_msg_func
import pyttsx3

username = ""

def on_open(ws):

    # login
    global username
    login_msg = deal_msg_func.gen_login_msg()
    tmp = loads(login_msg)
    username = tmp["content"]["name"]

    ws.send(login_msg)

    # 对于单个用户采用多线程的方式来实现输出输入的分隔
    def run(*args):
        while True:
            sendmsg = input()
            sendmsg_json = deal_msg_func.analyse_input(sendmsg, username)
            try:
                ws.send(sendmsg_json)
                if loads(sendmsg_json)["type"] == "logout":
                    ws.close()
                    os._exit(0)
            except:
                print('connection is already closed.')
                sys.exit(0)

    threading.Thread(target=run).start()

'''
def on_error(ws, error): 
    # 对于error发生进行处理
    print("something bad happened!")
    print("error msg:{}".format(error))
'''

def on_close(ws, close_status_code, close_msg):
    if close_status_code or close_msg:
        print('close status code:', close_status_code)
        print('close msg:', close_msg)
    try:
        print(">>>>>>CLOSED")
        os._exit(0)
    except:
        pass


def on_message(ws, json_message):
    msg = loads(json_message)
    if msg["type"] == "shutdown":
        print("wrong username or password!")
        # 客户端退出
        logoutdict = {
            "type": "logout",
            "content": {
                "name": username
            }
        }
        logoutjson = dumps(logoutdict)
        ws.send(logoutjson)
        ws.close()
        os._exit(0)
    elif msg["type"] == "pass":
        pass



ws_app = websocket.WebSocketApp("ws://localhost:8765",
                                on_open=on_open, on_message=on_message,
                                on_close=on_close)

ws_app.run_forever()