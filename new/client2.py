"""
Предварительный прототип ядра клиента с различными функциями для получения и обработки сообщений
"""

import socket, threading, json, time

SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

def sendPacketAndReceive(server: tuple, data: dict, cb: callable):
    global msgFlag
    tmp = b''
    SOCKET.connect(server)
    SOCKET.send(json.dumps(data).encode('utf8'))
    res = SOCKET.recv(1024)
    while res:
        tmp += res
        res = SOCKET.recv(1024)
    SOCKET.close()
    msgFlag = True
    cb(res)

def cb1(udata: bytes):
    pass

def T1():
    sendPacketAndReceive(('192.168.1.41', 9090), dict({
        'pr': 0x00,
        'd': 'u1;p1'
    }), cb1)

# threading.Thread(target=T1).start()

msgFlag = False
SocketState = False

def main():
    while SocketState:
        if msgFlag:
            msgFlag = False

T1()
main()