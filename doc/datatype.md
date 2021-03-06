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
空消息，不作处理：
```json
{
    "type": "pass"
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
        "target_name": "",
        "send_password": "",
        "from_name": ""
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
```
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

客户端接受到的消息格式：


用户被通知关闭：
```json
{
    "type": "shutdown",
}
```
空消息，不作处理：
```json
{
    "type": "pass"
}
```

接收到疫情的回复
```json
{
    "type": "cmd_recv",
    "content": {
        "cmd_type": "epidemic",
        "text": "{...}"
    }
}
```
接收到天气的回复
```json
{
    "type": "cmd_recv",
    "content": {
        "cmd_type": "weather",
        "text": "{...}"
    }
}
```
接受某个用户的消息
```json
{
    "type": "cmd_recv",
    "content": {
        "cmd_type": "send_msg",
        "from_name": "",
        "text": ""
    }
}
```
接受到笑话
```json
{
    "type": "cmd_recv",
    "content": {
        "cmd_type": "joke",
        "text": ""
    }
}
```
接受到闲聊
```json
{
    "type": "cmd_recv",
    "content": {
        "cmd_type": "chat",
        "text": ""
    }
}
```


