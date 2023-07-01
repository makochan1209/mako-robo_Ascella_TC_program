import tkinter as tk

import time

import datetime
# import subprocess

import serial
import struct
import threading
import random

# 動作モード（シリアル通信を実際に行うか）
SERIAL_MODE = False
# 動作モード（ランダムなpos、actを入れるようにするか）
RANDOM_STATUS_MODE = True

# グリッドの大きさ
GRID_WIDTH = 40
GRID_HEIGHT = 10

pos=[0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの位置（通信そのまま）
act=[0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの作業内容（通信そのまま）

serBuffStr = []
# 管制
def TCDaemon():
    if RANDOM_STATUS_MODE:
        while True:
            # ランダムにデータを生成
            for i in range(6):
                pos[i] = random.randint(0, 0xff)
                act[i] = random.randint(0, 0xff)
                time.sleep(0.2) # 1秒ごとに更新

    else:
        while True:
            # データ受信
            while True:
                if SERIAL_MODE:
                    buff = ser.read()   # read関数は1byteずつ読み込む、多分文字が来るまで待つはず
                    serBuffStr.append(buff)
                    if (buff == 0x04):
                        break
                else:
                    serBuffStr = [] # デバッグ用コマンド書く
        
            # データ解析
        

# ボタン操作からの管制への反映
def compStart():
    print("start")

def compEmgStop():
    print("emgStop")

# ウィンドウ制御（上の情報を表示する）
def windowDaemon():
    labelTime.configure(text=datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))

    configureTextBuf = ""
    for i in range(6):
        actTextBuf = ""
        if (act[i] == 0x00):
            actTextBuf = "探索中"
        else:
            actTextBuf = "待機中"

        configureTextBuf = str(i + 1) + "号機\n\n" + "場所: " + str(pos[i]) + "\n作業: " + actTextBuf

        if (i == 0):
            labelR1.configure(text=configureTextBuf)
        elif (i == 1):
            labelR2.configure(text=configureTextBuf)
        elif (i == 2):
            labelR3.configure(text=configureTextBuf)
        elif (i == 3):
            labelR4.configure(text=configureTextBuf)
        elif (i == 4):
            labelR5.configure(text=configureTextBuf)
        elif (i == 5):
            labelR6.configure(text=configureTextBuf)

    mainWindow.after(50, windowDaemon)

# 常時実行し通信・ウィンドウを更新する関数を実行するための最初の関数
def connect():
    buttonConnect.pack_forget()

def exitTCApp():
    if SERIAL_MODE:
        ser.close()
    mainWindow.destroy()

# 以下メインルーチン

# 初期化

# シリアル通信（TWE-Lite）
if SERIAL_MODE:
    use_port = '/dev/serial0'

    ser = serial.Serial(use_port)
    ser.baudrate = 115200
    ser.parity = serial.PARITY_NONE
    ser.bytesize = serial.EIGHTBITS
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = None

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

labelR1 = tk.Label(mainWindow, text='1号機', anchor=tk.N, width=GRID_WIDTH, height=GRID_HEIGHT)
labelR1.grid(row=2,column=0)
labelR2 = tk.Label(mainWindow, text='2号機', anchor=tk.N, width=GRID_WIDTH, height=GRID_HEIGHT)
labelR2.grid(row=2,column=1)
labelR3 = tk.Label(mainWindow, text='3号機', anchor=tk.N, width=GRID_WIDTH, height=GRID_HEIGHT)
labelR3.grid(row=3,column=0)
labelR4 = tk.Label(mainWindow, text='4号機', anchor=tk.N, width=GRID_WIDTH, height=GRID_HEIGHT)
labelR4.grid(row=3,column=1)
labelR5 = tk.Label(mainWindow, text='5号機', anchor=tk.N, width=GRID_WIDTH, height=GRID_HEIGHT)
labelR5.grid(row=4,column=0)
labelR6 = tk.Label(mainWindow, text='6号機', anchor=tk.N, width=GRID_WIDTH, height=GRID_HEIGHT)
labelR6.grid(row=4,column=1)

buttonConnect = tk.Button(mainWindow, text = "通信接続", command = connect)
buttonConnect.grid(row=5,column=0,columnspan=2)

buttonStart = tk.Button(mainWindow, text = "競技開始", command = compStart)
buttonEmgStop = tk.Button(mainWindow, text = "全ロボット緊急停止", command = compEmgStop)

buttonExit = tk.Button(mainWindow, text = "プログラム終了", command = exitTCApp)
buttonExit.grid(row=10,column=0,columnspan=2)

threadWindow = threading.Thread(target=windowDaemon, daemon=True)
threadTC = threading.Thread(target=TCDaemon, daemon=True)
threadWindow.start()
threadTC.start()
i = 0
mainWindow.mainloop()