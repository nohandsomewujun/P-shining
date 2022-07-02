from json import dumps
from json import loads
from telnetlib import LOGOUT

# 中文分词
import jieba
import jieba.posseg as pseg #词性标注
import jieba.analyse as anls
from sqlalchemy import false #关键词提取
import time



##########
#loginmsg#
##########
def gen_login_msg():
    
    username = input("username:")
    password = input("password:")
    tmpdict = {
        "type": "login",
        "content": {
            "name": username,
            "password": password
        }
    }
    json_login_msg = dumps(tmpdict)
    return json_login_msg

'''
#############
#shutdownmsg#
#############
def deal_shutdown_msg(ws):
    print("wrong username or password!")
    ws.close()
'''

############
#deal input#
############
def analyse_input(input_msg, username):
    input_msg_cut = jieba.lcut(input_msg, cut_all=false)
    print(input_msg_cut)
    if input_msg_cut[0] == "查询":
        # 查询天气或者是疫情
        if "疫情" in input_msg_cut:
            send_msg_dict = {
                "type": "cmd",
                "content": {
                    "cmd_type": "epidemic",
                    "text": input_msg_cut[1]
                }
            }
            send_msg_json = dumps(send_msg_dict)
            return send_msg_json

        elif "天气" in input_msg_cut:
            send_msg_dict = {
                "type": "cmd",
                "content": {
                    "cmd_type": "weather",
                    "text": input_msg_cut[1]
                }
            }
            send_msg_json = dumps(send_msg_dict)
            return send_msg_json
    
    elif input_msg_cut[0] == "退出":
        send_msg_dict = {
            "type": "logout",
            "content": {
                "name": username
            }
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json

    elif input_msg_cut[0] == "和":
        target_name = input_msg_cut[1]
        text = ""
        for i in range(3, len(input_msg_cut)):
            text += input_msg_cut[i]
        send_msg_dict = {
            "type": "cmd",
            "content": {
                "cmd_type": "send_msg",
                "text": text,
                "target_name": target_name
            }
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json

    elif input_msg_cut[0] == "闲聊":
        tmp_str = ""
        for i in range(2, len(input_msg_cut)):
            tmp_str += input_msg_cut[i]
        send_msg_dict = {
            "type": "cmd",
            "content": {
                "cmd_type": "chat",
                "text": tmp_str 
            }
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json

    elif input_msg_cut[1] == "邮件":
        target_name = input_msg_cut[3]
        mail_password = input_msg_cut[len(input_msg_cut) - 1]
        text = ""
        for i in range(len(input_msg_cut)):
            if i >= 5 and i < len(input_msg_cut) - 1:
                text += input_msg_cut[i]
        send_msg_dict = {
           "type": "cmd",
           "content": {
            "cmd_type": "mail",
            "text": text,
            "target_name": target_name,
            "send_password": mail_password,
            "from_name": username
           }
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json

    elif "故事" in input_msg_cut:
        send_msg_dict = {
            "type": "cmd",
            "content": {
                "cmd_type": "story"
            }
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json

    elif "笑话" in input_msg_cut:
        send_msg_dict = {
            "type": "cmd",
            "content": {
                "cmd_type": "joke"
            }
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json

    else:
        send_msg_dict = {
            "type": "pass"
        }
        send_msg_json = dumps(send_msg_dict)
        return send_msg_json


