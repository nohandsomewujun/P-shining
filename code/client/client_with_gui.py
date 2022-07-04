import asyncio
import websockets
import deal_msg_func
from json import dumps, loads
import os
import aioconsole
import PySimpleGUI as sg
from tkinter.messagebox import showerror
from PIL import Image

username = ""

# login_layout = [
#         [sg.Text('用户名:'), sg.Text(size=(20,1),key='-username-')],
#         [sg.Text('密码:'), sg.Text(size=(20, 1), key='-password-')],
#         [sg.Submit('登录', key='-submit-')]
#     ]
# login_window = sg.Window('创新聊天室', login_layout)
# login_window.read(timeout=100)
filename = 'main.gif'
gif_file = Image.open(filename)
message = ['ewb']
sg.theme('Dark Grey 13')
chat_layout = [
    [sg.Listbox(message, key='-messages-', auto_size_text=True, size=(100, 15), enable_events=True),
     sg.Image(filename, key='-gif-')],
    [sg.Button('准备输入', key='get')],
    [sg.Quit('清空所有聊天记录', key='delete')]
]
chat_window = sg.Window('飞鸽', chat_layout, finalize=True)


# chat_window = ''

async def handout_msg_from_sever(ws):
    global chat_window
    global username
    global message
    json_msg = await ws.recv()
    msg = loads(json_msg)
    if msg["type"] == "pass":
        pass
    elif msg["type"] == "cmd_recv":
        if msg["content"]["cmd_type"] == "epidemic":
            print(msg["content"]["text"])
            message.append('疫情情况：  ')
            message.append(msg["content"]["text"])
            chat_window['-messages-'].update(message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    message = []
                    chat_window['-messages-'].update(message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)

            # TODO:read it
        elif msg["content"]["cmd_type"] == "weather":
            print(msg["content"]["text"])
            message.append('天气情况：')
            message.append(msg["content"]["text"])
            chat_window['-messages-'].update(message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    message = []
                    chat_window['-messages-'].update(message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
            # TODO:read it
        elif msg["content"]["cmd_type"] == "send_msg":
            print(msg["content"]["from_name"] + " : " + msg["content"]["text"])
            message.append(msg["content"]["from_name"] + ':  ')
            message.append(msg["content"]["text"])
            chat_window['-messages-'].update(message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    message = []
                    chat_window['-messages-'].update(message)
                elif event == '-messages-':
                    string = str(values[0])
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
            # TODO:read it
        elif msg["content"]["cmd_type"] == "joke":
            print(msg["content"]["text"])
            message.append('笑话:  ')
            message.append(msg["content"]["text"])
            chat_window['-messages-'].update(message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    message = []
                    chat_window['-messages-'].update(message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
            # TODO:read it

    # 为了实现asyncio，如果是他人发送给自己的消息，就再去接受一次
    if "content" in msg and "cmd_type" in msg["content"]:
        if msg["content"]["cmd_type"] == "send_msg":
            # 前一条消息是他人发送的
            json_msg = await ws.recv()
            msg = loads(json_msg)
            if msg["type"] == "pass":
                pass
            elif msg["type"] == "cmd_recv":
                if msg["content"]["cmd_type"] == "epidemic":
                    print(msg["content"]["text"])
                    # TODO:read it
                elif msg["content"]["cmd_type"] == "weather":
                    print(msg["content"]["text"])
                    # TODO:read it
                elif msg["content"]["cmd_type"] == "send_msg":
                    print(msg["content"]["from_name"] + " : " + msg["content"]["text"])
                    # TODO:read it
                elif msg["content"]["cmd_type"] == "joke":
                    print(msg["content"]["text"])
                    # TODO:read it

    return ""


async def handout_input_2(ws):
    sendmsg = await aioconsole.ainput()
    sendmsg_json = deal_msg_func.analyse_input(sendmsg, username)
    await ws.send(sendmsg_json)
    if loads(sendmsg_json)["type"] == "logout":
        await ws.close()
        os._exit(0)


async def main():
    global login_window
    global chat_window
    global chat_layout
    global username
    async with websockets.connect("ws://localhost:8766") as ws:
        # login
        login_msg = deal_msg_func.gen_login_msg()
        tmp = loads(login_msg)
        username = tmp["content"]["name"]
        # 更新登录页面的内容
        # login_window['-username-'].update(username)
        # login_window['-password-'].update('****')
        # login_window.read()
        await ws.send(login_msg)
        login_msg = loads(await ws.recv())
        # password错误时
        if login_msg["type"] == "shutdown":
            print("wrong password!")
            showerror('提示', '密码错误')
            login_window.close()
            logout_dict = {
                "type": "logout",
                "content": {
                    "name": username
                }
            }
            logout_json = dumps(logout_dict)
            await ws.send(logout_json)
            await ws.close()
            os._exit(0)
        else:
            # login_window.close()
            print("hello sir! I am Jarvis!")
            # chat_window = sg.Window('飞鸽', chat_layout, finalize=True)

            # Finish up by removing from the scr
        while True:
            await asyncio.gather(handout_msg_from_sever(ws), handout_input_2(ws))


asyncio.run(main())