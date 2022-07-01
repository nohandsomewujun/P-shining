import asyncio
import websockets
import deal_msg_func
from json import dumps, loads
import os
import aioconsole

username = ""


async def handout_msg_from_sever(ws):
    global username
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
    global username
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
