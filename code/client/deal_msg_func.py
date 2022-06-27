from json import dumps
from json import loads


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


#############
#shutdownmsg#
#############
def deal_shutdown_msg(ws):
    print("wrong username or password!")
    ws.close()
