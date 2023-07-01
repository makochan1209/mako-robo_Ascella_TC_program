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

pos = [0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの位置（通信そのまま）
destPos = [0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの行き先（通信そのまま）
act = [0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの作業内容（通信そのまま）
recvCom = [0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの受信通信内容（通信そのまま）
transCom = [0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6] # ロボットの送信通信内容（通信そのまま）
connectStatus = [False, False, False, False, False, False]  # 接続できているか

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
            actTextBuf = "待機中"
        elif (act[i] == 0x01):
            actTextBuf = "走行中"
        elif (act[i] == 0x02):
            actTextBuf = "探索中"
        else:
            actTextBuf = "不明"

        if (recvCom[i] == 0x00):
            recvCommandBuf = "探索結果報告："
        elif (recvCom[i] == 0x01):
            recvCommandBuf = "位置到達報告："
        elif (recvCom[i] == 0x02):
            recvCommandBuf = "ボールシュート報告"
        elif (recvCom[i] == 0x20):
            recvCommandBuf = "行動指示要求"
        elif (recvCom[i] == 0x21):
            recvCommandBuf = "許可要求"
        elif (recvCom[i] == 0x30):
            recvCommandBuf = "通信可否報告"
        else:
            recvCommandBuf = "なし"

        if (transCom[i] == 0x50):
            transCommandBuf = "移動許可：" + destPos[i]
        elif (transCom[i] == 0x51):
            transCommandBuf = "行動許可："
        else:
            transCommandBuf = "なし"

        if connectStatus[i]:
            configureTextBuf = str(i + 1) + "号機\n\n" + "接続状態: " + "接続済\n\n" + "場所: " + str(pos[i]) + "\n状態: " + actTextBuf + "\n最終通信内容（受信）: " + recvCommandBuf + "\n最終通信内容（送信）: " + transCommandBuf
        else:
            configureTextBuf = str(i + 1) + "号機\n\n" + "接続状態: " + "未接続"

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

# ロボット本体との接続
def connect():
    buttonConnect.grid_forget()
    for i in range(6):
        connectStatus[i] = True
    buttonStart.grid(row=5,column=0,columnspan=2)

def exitTCApp():
    if SERIAL_MODE:
        ser.close()
    mainWindow.destroy()

def keyPress(event):
    # Enterのとき
    if event.keycode == 13:
        compStart()
    # Numkey 1のとき
    elif event.keycode == 49:
        connect()
    # Numkey 2のとき
    elif event.keycode == 50:
        compEmgStop()
    # Numkey 9のとき
    elif event.keycode == 57:
        exitTCApp()

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

buttonConnect = tk.Button(mainWindow, text = "通信接続 (Num 1)", command = connect)
buttonConnect.grid(row=5,column=0,columnspan=2)

buttonStart = tk.Button(mainWindow, text = "競技開始 (Enter)", command = compStart)
buttonEmgStop = tk.Button(mainWindow, text = "全ロボット緊急停止 (Num 2)", command = compEmgStop)

buttonExit = tk.Button(mainWindow, text = "プログラム終了 (Num 9)", command = exitTCApp)
buttonExit.grid(row=10,column=0,columnspan=2)

mainWindow.bind("<KeyPress>", keyPress)

threadWindow = threading.Thread(target=windowDaemon, daemon=True)
threadTC = threading.Thread(target=TCDaemon, daemon=True)
threadWindow.start()
threadTC.start()
i = 0
mainWindow.mainloop()