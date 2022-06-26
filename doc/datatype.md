# 服务器与客户端之间的数据格式规定


your Jarvis

服务器和客户端之间数据通信采用json的格式。
---
client向sever传输消息：
---
用户登录信息：
```json
{
    "type": "login",
    "content": {
        "name": "",
        "password": ""
    }
}
```
用户发送消息（正常的命令消息）：
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "",
        "text": ""
    }
}
```
下面给出几种命令的消息格式：

查询天气
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "weather",
        "text": "北京"
    }
}
```
查询某地疫情情况
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "epidemic",
        "text": "北京"
    }
}
```
发送消息给某个在线用户
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "send_msg",
        "text": "",
        "target_name": ""
    }
}
```
发送邮件给某个用户
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "mail",
        "text": "",
        "target_name": ""
    }
}
```
讲故事
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "story"
    }
}
讲笑话
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "joke"
    }
}
```
闲聊
```json
{
    "type": "cmd",
    "content": {
        "cmd_type": "chat",
        "text": ""
    }
}
```
用户退出：
```json
{
    "type": "logout",
    "content": {
        "name": ""
    }
}
```