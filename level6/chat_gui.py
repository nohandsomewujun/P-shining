# -*- coding:utf-8 -*-
import tkinter
import tkinter as tk
from PIL import Image, ImageTk

def chat_gui(root_window):
    root_window.quit()
#定义窗口的大小
width = 450
height = 300
#icon图片和背景图片的路径
ico_path = 'F:/the_end_of_2nd/multi_python/level6/ico.ico'
bg_path = 'F:/the_end_of_2nd/multi_python/level6/bg.gif'
root_window =tk.Tk()

screenwidth = root_window.winfo_screenwidth()
screenheight = root_window.winfo_screenheight()
# 设置窗口title
root_window.title('多功能聊天室')
# 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x",以及其处于桌面的位置
root_window.geometry(f'{width}x{height}+{int(screenwidth/2 - width/2)}+{int(screenheight/2 -height/2)}')
# 更改左上角窗口的的icon图标
root_window.iconbitmap(ico_path)
# 设置主窗口的背景图片
im = Image.open(bg_path).resize((width,height))
im_root = ImageTk.PhotoImage(im)
#创建画布设置所需要的图片，将画布添加至主窗口
canvas_root = tkinter.Canvas(root_window, width=width, height=height)
canvas_root.create_image(width/2, height/2, image=im_root)
canvas_root.grid()
#标题
canvas_root.create_text(140,40,text = "欢迎进入多人聊天室",fill ='#00FF7F',anchor = 'w',font =('微软雅黑',15,'bold'))

#用户名，密码和entry
canvas_root.create_text(120,100,text = "用户名:",fill ='#F8F8FF',anchor = 'w',font =('微软雅黑',10,'bold'))
entry1 = tk.Entry(root_window)
entry1.place()
canvas_root.create_window(180, 100, anchor = 'w',width=100, height=20, window=entry1)

canvas_root.create_text(132,140,text = "密码:",fill ='#F8F8FF',anchor = 'w',font =('微软雅黑',10,'bold'))
entry1 = tk.Entry(root_window, show='*')
entry1.place()
canvas_root.create_window(180, 140, anchor = 'w',width=100, height=20, window=entry1)

# # 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
button1=tk.Button(root_window,text="登录",fg="#9C9C9C",bg='#B0E2FF', command=lambda : chat_gui(root_window))
#将按钮放置在主窗口内
button1.grid()
canvas_root.create_window(300, 200, width=100, height=20,anchor = 'w',
                                       window=button1)

button2=tk.Button(root_window,text="登录",fg="#9C9C9C",bg='#B0E2FF', command=lambda : chat_gui(root_window))
#将按钮放置在主窗口内
button2.grid()
canvas_root.create_window(90, 200, width=100, height=20,anchor = 'w',
                                       window=button2)


#进入主循环，显示主窗口
root_window.mainloop()


