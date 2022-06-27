import asyncio
import websockets
from json import loads
import sever_msg_func


# 存放现在连接上的所有客户
USERS = {}

async def handler(websocket):
    async for json_message in websocket:
        msg = loads(json_message)
        print(msg)
        if msg["type"] == "login":
            sendmsg_json = sever_msg_func.deal_login_msg(msg)
            tmp_dict = loads(sendmsg_json)
            
            USERS[msg["content"]["name"]] = websocket
            await websocket.send(sendmsg_json)
            print("debug: send{}".format(sendmsg_json))

        
        

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())