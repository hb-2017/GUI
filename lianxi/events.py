#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)


# from tkinter import *
# def hello(event):
#     print("Single Click, Button-l")
# def quit(event):
#     print("Double Click, so let's stop")
#     import sys; sys.exit()
#
# widget = Button(None, text='Mouse Clicks')
# widget.pack()
# widget.bind('<Button-1>', hello)
# widget.bind('<Double-1>', quit)
# widget.mainloop()


from tkinter import *

def motion(event):
  print("Mouse position: (%s %s)" % (event.x, event.y))
  return

master = Tk()
whatever_you_do = "Whatever you do will be insignificant, but it is very important that you doit.\n(Mahatma Gandhi)"
msg = Message(master, text = whatever_you_do)
msg.config(bg='lightgreen', font=('times', 24, 'italic'))
msg.bind('<Motion>',motion)
msg.pack()
mainloop()