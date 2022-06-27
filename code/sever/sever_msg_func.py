from json import dumps
from json import load

from itsdangerous import json

def deal_login_msg(msg):
    username = msg["content"]["name"]
    password = msg["content"]["password"]

    # 读入username和password的json文件
    # 实现身份检验
    with open("./user.json", "r") as f:
        user_dict = load(f)
    
    # 检验
    if username in user_dict["username"]:
        if user_dict["username"][username] == password:
            # 成功校验
            pass_dict = {
                "type": "pass"
            }
            pass_json = dumps(pass_dict)
            return pass_json
    shutdown_dict = {
        "type": "shutdown"
    }
    shutdown_json = dumps(shutdown_dict)
    return shutdown_json

    

