import socket

s = socket.socket()
s.bind(('192.168.1.41', 12345))
f = open('file.txt', 'wb')
flag = True
s.listen(5)
while flag:
    c, addr = s.accept()
    l = c.recv(1024)
    while (l):
        print('Receive packet')
        f.write(l)
        l = c.recv(1024)
    f.close()
    c.send('Done')
    print('file has been completed')
    c.close()
    flag = False