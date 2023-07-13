import serial
import sys
import glob
import struct

import serial.tools.list_ports

def twe_serial_ports_detect():
    if sys.platform.startswith('win'):
        result = []
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if p.vid == 0x0403 and (p.pid == 0x6001 or p.pid == 0x6015): # TWE-Lite-R
                result.append(p.device)
                print(p.device)
                print(p.serial_number)
    elif sys.platform.startswith('linux'):
        result = glob.glob('/dev/serial0')  # GPIO UART
    else:
        print('Unsupported platform')
    return result

# [0xA5, 0x5A, 0x80, "Length", "Data", "CD", 0x04]の形式で受信
# "Data": 0x0*（送信元）, Command, Data
# 送信、toIDは0x78のときは全台
# tkinterから直接入力なので各引数は文字列であることに注意
def sendTWE(ser, toID, command, data):
    sendPacket = [0xA5, 0x5A, 0x80, 0x03, toID, command]
    if type(data) is complex:
        sendPacket[3] = 0x02 + len(data)
        # sendPacket.extend([int(s, 0) for s in data])
        sendPacket.extend(data)
        sendPacket.extend(["CD"])

    else:
        # sendPacket.extend([int(data, 0), "CD"])
        sendPacket.extend([data, "CD"])
    
    cdBuff = 0
    for i in range(0, len(sendPacket)):
        if (i >= 4 and i < len(sendPacket) - 1):
            cdBuff = cdBuff ^ sendPacket[i]
        elif (i == len(sendPacket) - 1):
            sendPacket[i] = cdBuff
        
        # ser.write(sendPacket[i].to_bytes(1, 'big'))
        # ser.write(struct.pack("<B", sendPacket[i]))
    ser.write(b''.join([struct.pack("<B", val) for val in sendPacket]))
        
# 1パケット受信（データは複数バイト可能の仕様）
def recvTWE(ser):
    # 値の初期化
    cdBuff = 0
    serBuffStr = []
    
    # データ受信
    
    while ser.in_waiting > 0: # データが来ているか・またはデバッグモードのとき。このループは1バイトごと、パケット受信完了でbreak
        # buff = int.from_bytes(ser.read(), 'big')   # read関数は1byteずつ読み込む、多分文字が来るまで待つはず
        buff = struct.unpack("<B", ser.read())[0]
        
        serBuffStr.append(buff)
        if len(serBuffStr) > 4:    # データの範囲
            if len(serBuffStr) <= 4 + serBuffStr[3]:    # データ終了まで
                cdBuff = cdBuff ^ buff   # CD計算
            elif len(serBuffStr) == 4 + serBuffStr[3] + 2:    # EOTまで終了
                print("Packet Received")
                print("Recieved Data:")
                print([hex(i) for i in serBuffStr])
                if serBuffStr[len(serBuffStr) - 1] == 0x04: # EOTチェック
                    print("EOT OK")
                    if cdBuff == serBuffStr[len(serBuffStr) - 2]:
                        print("CD OK")
                    else:
                        print("CD NG, Expected: " + hex(cdBuff) + ", Received: " + hex(serBuffStr[len(serBuffStr) - 2]))
                else:
                    print("EOT NG")
                break
    if serBuffStr != [] and len(serBuffStr) < 8:    # パケットが短すぎる場合は破棄
        serBuffStr = []
        print("Packet too short")
    if serBuffStr != [] and serBuffStr[4] == 0xdb:   # 応答メッセージなので省略
        serBuffStr = []
        print("Response Message")
    return serBuffStr