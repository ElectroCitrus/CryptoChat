"""
Предварительный прототип ядра клиента с различными функциями для получения и обработки сообщений
"""

import socket, threading, json, time

SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

f1 = False
f2 = False
a = 0

def sendPacketAndReceive(server: tuple, data: dict, cb: callable):
    tmp = b''
    SOCKET.connect(server)
    SOCKET.send(json.dumps(data).encode('utf8'))
    res = SOCKET.recv(1024)
    while res:
        tmp += res
        res = SOCKET.recv(1024)
    SOCKET.close()
    cb(res)

def cb1(udata: bytes):
    global f1
    f1 = True

def T1():
    sendPacketAndReceive(('192.168.1.41', 9090), dict({
        'pr': 0x00,
        'd': 'u1;p1'
    }), cb1)

threading.Thread(target=T1).start()

while f2:
    time.sleep(0.1)
    while f1:
        a += 1
        f1 = False
        f2 = False

print(str(a))