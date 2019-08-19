import socket

s = socket.socket()
host = '192.168.1.41'
port = 12345

s.connect((host, port))
f = open('doc118935648_450983515', 'rb')
print('Sending...')
l = f.read(1024)
while (l):
    print('send packet')
    s.send(l)
    l = f.read(1024)

f.close()
print('End transfer')
s.shutdown(socket.SHUT_WR)
s.recv(1024)
s.close()