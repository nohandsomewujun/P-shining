import asyncio
from concurrent.futures import thread
from turtle import color
import websockets
import deal_msg_func
from json import dumps, loads
import os
import aioconsole
# voice
import pyttsx3
# gui
import PySimpleGUI as sg
from tkinter.messagebox import showerror
from PIL import Image
import threading
from time import sleep

import matplotlib.pyplot as plt

username = ""

'''
layout = [[sg.Text("What's your name?")],
              [sg.Text(size=(100, 1), key='-OUTPUT-')],
              [sg.Button('Ok'), sg.Button('Quit')]]

    # Create the window
window = sg.Window('Window Title', layout, finalize=True)
'''

# gui
filename = './main.gif'
gif_file = Image.open(filename)
gui_message = []
sg.theme('Dark Grey 13')
chat_layout = [
    [sg.Listbox(gui_message, key='-messages-', auto_size_text=True, size=(100, 15), enable_events=True),
     sg.Image(filename, key='-gif-')],
    [sg.Button('已收到', key='get')],
    [sg.Quit('清空所有聊天记录', key='delete')]
]
chat_window = sg.Window('Jarvis', chat_layout, finalize=True)


async def handout_msg_from_sever(ws):
    global username
    global chat_window
    global gui_message
    json_msg = await ws.recv()
    msg = loads(json_msg)
    if msg["type"] == "pass":
        pass
    elif msg["type"] == "cmd_recv":
        if msg["content"]["cmd_type"] == "epidemic":
            print(msg["content"]["text"])
            '''
            name_list = []
            value_list = []
            for k, v in msg["content"]["text"].items():
                name_list.append(k)
                value_list.append(v)
            value_list = value_list[1:len(value_list)]
            name_list = name_list[1:len(name_list)]
            print(name_list)
            plt.bar(range(len(name_list)), value_list, color = ['red'],tick_label=name_list)

            plt.show()
            '''
            # pyttsx3.speak(str(msg["content"]["text"]))
            # def tmp1(i):
            #     pyttsx3.speak(i)
            # threading.Thread(target=tmp1, args=(str(msg["content"]["text"]),)).start()
            # gui_message.append('疫情情况：  ')
            trim_msg = ""
            for k, v in msg["content"]["text"].items():
                trim_msg += k + ':' + str(v) + ' '
            gui_message.append(trim_msg)
            chat_window['-messages-'].update(gui_message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    gui_message = []
                    chat_window['-messages-'].update(gui_message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
            

        elif msg["content"]["cmd_type"] == "weather":
            print(msg["content"]["text"])
            
            gui_message.append('天气情况：  ')
            trim_msg = ""
            for k, v in msg["content"]["text"].items():
                trim_msg += k + ':' + str(v) + ' '
            gui_message.append(trim_msg)
            chat_window['-messages-'].update(gui_message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    gui_message = []
                    chat_window['-messages-'].update(gui_message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)

        elif msg["content"]["cmd_type"] == "send_msg":
            print(msg["content"]["from_name"] + " : " + msg["content"]["text"])
            #pyttsx3.speak(msg["content"]["from_name"] + "和你说" + msg["content"]["text"])
            gui_message.append(msg["content"]["from_name"] + ':  ')
            gui_message.append(msg["content"]["text"])
            chat_window['-messages-'].update(gui_message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    gui_message = []
                    chat_window['-messages-'].update(gui_message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
            
        elif msg["content"]["cmd_type"] == "joke":
            print(msg["content"]["text"])
            #pyttsx3.speak("我要说了，听好了")
            #pyttsx3.speak(msg["content"]["text"])
            gui_message.append('笑话:  ')
            gui_message.append(msg["content"]["text"])
            chat_window['-messages-'].update(gui_message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    gui_message = []
                    chat_window['-messages-'].update(gui_message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
           
        elif msg["content"]["cmd_type"] == "chat":
            print(msg["content"]["text"])
            #pyttsx3.speak(msg["content"]["text"])
            gui_message.append('机器人:  ')
            gui_message.append(msg["content"]["text"])
            chat_window['-messages-'].update(gui_message)
            flag = 0
            while True:
                event, values = chat_window.read(timeout=100)
                if event == 'get':
                    break
                elif event == 'delete':
                    gui_message = []
                    chat_window['-messages-'].update(gui_message)
                    flag = 1
                elif flag:
                    break
                filename = 'main.gif'
                chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
        
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
                    #pyttsx3.speak(str(msg["content"]["text"]))
                    gui_message.append('疫情情况：  ')
                    trim_msg = ""
                    for k, v in msg["content"]["text"].items():
                        trim_msg += k + ':' + str(v) + ' '
                    gui_message.append(trim_msg)
                    chat_window['-messages-'].update(gui_message)
                    flag = 0
                    while True:
                        event, values = chat_window.read(timeout=100)
                        if event == 'get':
                            break
                        elif event == 'delete':
                            gui_message = []
                            chat_window['-messages-'].update(gui_message)
                            flag = 1
                        elif flag:
                            break
                        filename = 'main.gif'
                        chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)

                elif msg["content"]["cmd_type"] == "weather":
                    print(msg["content"]["text"])
                    '''
                    pyttsx3.speak("当前温度" + msg["content"]["text"]["当前温度"][0:2] + "度")
                    pyttsx3.speak("当前湿度" + "百分之" + msg["content"]["text"]["当前湿度"][0:2])
                    pyttsx3.speak("当前风向" + msg["content"]["text"]["当前风向"])
                    pyttsx3.speak("今日最高温度" + msg["content"]["text"]["今日最高温度"][0:2] + "度")
                    pyttsx3.speak("今日最低温度" + msg["content"]["text"]["今日最低温度"][0:2] + "度")
                    '''
                    gui_message.append('天气情况：  ')
                    trim_msg = ""
                    for k, v in msg["content"]["text"].items():
                        trim_msg += k + ':' + str(v) + ' '
                    gui_message.append(trim_msg)
                    chat_window['-messages-'].update(gui_message)
                    flag = 0
                    while True:
                        event, values = chat_window.read(timeout=100)
                        if event == 'get':
                            break
                        elif event == 'delete':
                            gui_message = []
                            chat_window['-messages-'].update(gui_message)
                            flag = 1
                        elif flag:
                            break
                        filename = 'main.gif'
                        chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)

                elif msg["content"]["cmd_type"] == "send_msg":
                    print(msg["content"]["from_name"] + " : " + msg["content"]["text"])
                    #pyttsx3.speak(msg["content"]["from_name"] + "和你说" + msg["content"]["text"])
                    gui_message.append(msg["content"]["from_name"] + ':  ')
                    gui_message.append(msg["content"]["text"])
                    chat_window['-messages-'].update(gui_message)
                    flag = 0
                    while True:
                        event, values = chat_window.read(timeout=100)
                        if event == 'get':
                            break
                        elif event == 'delete':
                            gui_message = []
                            chat_window['-messages-'].update(gui_message)
                            flag = 1
                        elif flag:
                            break
                        filename = 'main.gif'
                        chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
            
                elif msg["content"]["cmd_type"] == "joke":
                    print(msg["content"]["text"])
                    #pyttsx3.speak("我要说了，听好了")
                    #pyttsx3.speak(msg["content"]["text"])
                    gui_message.append('笑话:  ')
                    gui_message.append(msg["content"]["text"])
                    chat_window['-messages-'].update(gui_message)
                    flag = 0
                    while True:
                        event, values = chat_window.read(timeout=100)
                        if event == 'get':
                            break
                        elif event == 'delete':
                            gui_message = []
                            chat_window['-messages-'].update(gui_message)
                            flag = 1
                        elif flag:
                            break
                        filename = 'main.gif'
                        chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
           
                elif msg["content"]["cmd_type"] == "chat":
                    print(msg["content"]["text"])
                    #pyttsx3.speak(msg["content"]["text"])
                    gui_message.append('机器人:  ')
                    gui_message.append(msg["content"]["text"])
                    chat_window['-messages-'].update(gui_message)
                    flag = 0
                    while True:
                        event, values = chat_window.read(timeout=100)
                        if event == 'get':
                            break
                        elif event == 'delete':
                            gui_message = []
                            chat_window['-messages-'].update(gui_message)
                            flag = 1
                        elif flag:
                            break
                        filename = 'main.gif'
                        chat_window['-gif-'].UpdateAnimation(filename, time_between_frames=10)
        

    return ""

async def handout_input_2(ws):
    sendmsg = await aioconsole.ainput()
    sendmsg_json = deal_msg_func.analyse_input(sendmsg, username)
    await ws.send(sendmsg_json)
    if loads(sendmsg_json)["type"] == "logout":
        await ws.close()
        os._exit(0)


async def main():
    global username
    global chat_window
    global gui_message
    global filename
    async with websockets.connect("ws://localhost:8765") as ws:
        # login
        login_msg = deal_msg_func.gen_login_msg()
        tmp = loads(login_msg)
        username = tmp["content"]["name"]
        await ws.send(login_msg)
        login_msg = loads(await ws.recv())
        # password错误时
        if login_msg["type"] == "shutdown":
            print("wrong password!")
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
            print("hello sir! I am Jarvis!")
            
        while True:
            await asyncio.gather(handout_msg_from_sever(ws), handout_input_2(ws))

        


asyncio.run(main())
