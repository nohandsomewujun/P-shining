import asyncio
import websockets
from json import loads
import sever_msg_func
import sys

# 添加所用到的模块路径
sys.path.append("./modules/get_epi")


import get_epi

# 存放现在连接上的所有客户
USERS = {}

async def handler(websocket):
    async for json_message in websocket:
        msg = loads(json_message)
        print(msg)
        if msg["type"] == "login":
            sendmsg_json = sever_msg_func.deal_login_msg(msg)        
            USERS[msg["content"]["name"]] = websocket
            await websocket.send(sendmsg_json)
            print("debug: send{}".format(sendmsg_json))
        elif msg["type"] == "logout":
            del USERS[msg["content"]["name"]]
            print(msg["content"]["name"] + " logout!")
        elif msg["type"] == "pass":
            pass
        elif msg["type"] == "cmd":
            if msg["content"]["cmd_type"] == "weather":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "epidemic":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "send_msg":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "mail":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "story":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "joke":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "chat":
                # TODO
                pass
        

        
        

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())