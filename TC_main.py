import tkinter as tk

import time

import datetime
import subprocess

PADX_R1 = 10
PADX_R2 = 10
PADY_R1 = 10
PADY_R3 = 10
PADY_R5 = 10

def compStart():
    print("start")

def compEmgStop():
    print("emgStop")

def daemon():
    labelTime.configure(text=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    mainWindow.after(50, daemon)

# 常時実行し通信・ウィンドウを更新する関数を実行するための最初の関数
def connect():
    buttonStart.pack_forget()

# 以下メインルーチン

# 初期化
# ウィンドウの定義
mainWindow = tk.Tk()
mainWindow.title ('Main Window')
mainWindow.geometry('800x800')

# グリッドの定義
mainFrame = tk.Frame(mainWindow)
mainFrame.grid(column=0, row=0)

# タイトル
labelTitle = tk.Label(mainWindow, text='Ascella by Team mako-robo\n管制ウィンドウ')
labelTitle.grid(row=0,column=0,columnspan=2)
labelTime = tk.Label(mainWindow, text='')
labelTime.grid(row=1,column=0,columnspan=2)

labelR1Title = tk.Label(mainWindow, text='1号機')
labelR1Title.grid(row=2,column=0)
labelR2Title = tk.Label(mainWindow, text='2号機')
labelR2Title.grid(row=2,column=1)
labelR3Title = tk.Label(mainWindow, text='3号機')
labelR3Title.grid(row=3,column=0)
labelR4Title = tk.Label(mainWindow, text='4号機')
labelR4Title.grid(row=3,column=1)
labelR5Title = tk.Label(mainWindow, text='5号機')
labelR5Title.grid(row=4,column=0)
labelR6Title = tk.Label(mainWindow, text='6号機')
labelR6Title.grid(row=4,column=1)

buttonStart = tk.Button(mainWindow, text = "通信接続", command = connect)
buttonStart.grid(row=5,column=0,columnspan=2)

buttonStart = tk.Button(mainWindow, text = "競技開始", command = compStart)
buttonEmgStop = tk.Button(mainWindow, text = "全ロボット緊急停止", command = compEmgStop)

daemon()
mainWindow.mainloop()