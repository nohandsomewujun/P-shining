import websocket
import threading
import os
import sys
from json import dumps
from json import loads
import deal_msg_func


def on_open(ws):

    # login
    login_msg = deal_msg_func.gen_login_msg()
    ws.send(login_msg)

    # 对于单个用户采用多线程的方式来实现输出输入的分隔
    def run(*args):
        while True:
            sendmsg = input()
            try:
                ws.send(sendmsg)
            except:
                print('connection is already closed.')
                sys.exit(0)

    threading.Thread(target=run).start()


def on_error(ws, error): 
    # 对于error发生进行处理
    print("something bad happened!")
    print("error msg:{}".format(error))


def on_close(ws, close_status_code, close_msg):
    # 客户端退出
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
        deal_msg_func.deal_shutdown_msg(ws)
    elif msg["type"] == "pass":
        print("connect success!")


ws_app = websocket.WebSocketApp("ws://localhost:8765",
                                on_open=on_open, on_message=on_message,
                                on_close=on_close, on_error=on_error)

ws_app.run_forever()