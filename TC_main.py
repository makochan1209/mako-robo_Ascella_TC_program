import tkinter

import time

import datetime
import subprocess

PADX_R1 = 10
PADX_R2 = 100
PADY_R1 = 10
PADY_R3 = 100
PADY_R5 = 200

def emgStop():
    print("emgStop")

def daemon():
    
    mainWindow.after(50, daemon)

# 常時実行し通信・ウィンドウを更新する関数を実行するための最初の関数
def loadDaemon():
    buttonStart.pack_forget()
    buttonEmgStop.pack(padx=10,pady=10)
    daemon()

# 以下メインルーチン

# 初期化
# ウィンドウの定義
mainWindow = tkinter.Tk()
mainWindow.title ('Main Window')
mainWindow.geometry('250x500')

labelTitle = tkinter.Label(mainWindow, text='Ascella by Team mako-robo\n管制ウィンドウ')
labelTitle.pack(padx=10,pady=10)

labelR1Title = tkinter.Label(mainWindow, text='1号機')
labelR1Title.pack(padx=PADX_R1,pady=PADY_R1)
labelR2Title = tkinter.Label(mainWindow, text='2号機')
labelR2Title.pack(padx=PADX_R2,pady=PADY_R1)
labelR3Title = tkinter.Label(mainWindow, text='3号機')
labelR3Title.pack(padx=PADX_R1,pady=PADY_R3)
labelR4Title = tkinter.Label(mainWindow, text='4号機')
labelR4Title.pack(padx=PADX_R2,pady=PADY_R3)
labelR5Title = tkinter.Label(mainWindow, text='5号機')
labelR5Title.pack(padx=PADX_R1,pady=PADY_R5)
labelR6Title = tkinter.Label(mainWindow, text='6号機')
labelR6Title.pack(padx=PADX_R2,pady=PADY_R5)

buttonStart = tkinter.Button(mainWindow, text = "開始（通信接続）", command = loadDaemon)
buttonStart.pack()

buttonEmgStop = tkinter.Button(mainWindow, text = "全ロボット緊急停止", command = emgStop)
mainWindow.mainloop()