import asyncio
import websockets
from json import dumps, loads
import sever_msg_func
from sever_module_get_epi import get_epi
from sever_module_get_weather import get_Weather
from sever_module_joke import load_one_joke

# 存放现在连接上的所有客户
USERS = {}

async def handler(websocket):
    async for json_message in websocket:
        msg = loads(json_message)
        print(msg)
        if msg["type"] == "login":
            send_msg_json = sever_msg_func.deal_login_msg(msg)        
            USERS[msg["content"]["name"]] = websocket
            await websocket.send(send_msg_json)
            print("debug: send{}".format(send_msg_json))

        elif msg["type"] == "logout":
            del USERS[msg["content"]["name"]]
            print(msg["content"]["name"] + " logout!")

        elif msg["type"] == "pass":
            pass

        elif msg["type"] == "cmd":
            if msg["content"]["cmd_type"] == "weather":
                city = msg["content"]["text"]
                info = get_Weather(city)
                send_msg_dict = {
                    "type": "cmd_recv",
                    "content": {
                        "cmd_type": "weather",
                        "text": info
                    }
                }
                send_msg_json = dumps(send_msg_dict)
                await websocket.send(send_msg_json)
                print("debug: send{}".format(send_msg_json))


            elif msg["content"]["cmd_type"] == "epidemic":
                city = msg["content"]["text"]
                info = get_epi(city)
                send_msg_dict = {
                    "type": "cmd_recv",
                    "content": {
                        "cmd_type": "epidemic",
                        "text": info
                    }
                }
                send_msg_json = dumps(send_msg_dict)
                await websocket.send(send_msg_json)
                print("debug: send{}".format(send_msg_json))
            

            elif msg["content"]["cmd_type"] == "send_msg":
                target_name = msg["content"]["target_name"]
                text = msg["content"]["text"]
                for k, v in USERS.items():
                    if v == websocket:
                        name = k
                    if k == target_name:
                        target_websocket = v
                send_msg_dict = {
                    "type": "cmd_recv",
                    "content": {
                        "cmd_type": "send_msg",
                        "from_name": name,
                        "text": text
                    }
                }
                send_msg_json = dumps(send_msg_dict)
                await target_websocket.send(send_msg_json)
                print("debug: send{}".format(send_msg_json))
                
                
            elif msg["content"]["cmd_type"] == "mail":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "story":
                # TODO
                pass
            elif msg["content"]["cmd_type"] == "joke":
                joke = load_one_joke()
                send_msg_dict = {
                    "type": "cmd_recv",
                    "content": {
                        "cmd_type": "joke",
                        "text": joke
                    }
                }
                send_msg_json = dumps(send_msg_dict)
                await websocket.send(send_msg_json)
                print("debug: send{}".format(send_msg_json))

            elif msg["content"]["cmd_type"] == "chat":
                # TODO
                pass
        

        
        

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())