import getpass, socket, threading, json, sys

serverIp = ('192.168.1.41', 9090)
username = input('Username: ')
password = getpass.getpass('Password: ')

socketState = False

def flags():
	flags.inChat = False

flags()

def receving(name, sock):
	"""
	Ожидание сообщение с сервера (для потока)
	"""
	while not socketState:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				print(data.decode('utf8'))
				res = json.loads(data.decode("utf-8"))
				if res['pr'] == 0x01:
					flags.inChat = True
				time.sleep(0.2)
		except:
			pass

host = socket.gethostbyname(socket.gethostname())

SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
SOCKET.bind((serverIp[0], 0))
SOCKET.setblocking(0)

socketState = True

T_receiveMsg = threading.Thread(target=receving, args=('RecvThread', SOCKET))
T_receiveMsg.start()

def c2cr(SOCKET: socket.socket, username: str, password: str, serverIp: tuple):
	"""
	Подключение к чат-комнате
	"""
	data = dict()
	data['pr'] = 0x00
	data['d'] = username + ';' + password
	packet = json.dumps(data).encode('utf-8')
	SOCKET.sendto(packet, serverIp)
    # data, addr = SOCKET.recvfrom(1024)
    # print(data.decode('utf8'))

c2cr(SOCKET, username, password, serverIp)

def createPacket(protocol: int, data: dict):
	"""
	Формирование пакета, шифрование, кодировка в utf-8
	"""
	packet = dict()
	packet['pr'] = protocol
	packet['d'] = data
	return json.dumps(packet).encode('utf-8')

def sendPacket(SOCKET: socket.socket, serverIp: tuple, s: bytes):
	"""
	Отправка сообщения на авторизованный сервер
	"""
	SOCKET.sendto(s, serverIp)
	# if authorize:
	# 	return True
	# else:
	# 	return False

while socketState:
    if flags.inChat:
        # print('Send packet ' + str(flags.inChat))
        # # inChat = True
        # # res = dict(json.loads(SOCKET.recv(1024)))
        # # if res['status'] == 1:
        # #     inChat = True
        # # else:
        # #     print('Status: ' + str(res['status']))
        # #     SOCKET.close()
        # #     sys.exit(0)
        try:
            msg = input('> ')
            if msg != '':
				sendPacket(SOCKET, serverIp, createPacket(0x03, msg))
				# SOCKET.sendto((msg), serverIp)
        except Exception as e:
            SOCKET.sendto('У меня возникла ошибка: ' + (str(e)))
            flags.inChat = False
            socketState = False

T_receiveMsg.join()
SOCKET.close()