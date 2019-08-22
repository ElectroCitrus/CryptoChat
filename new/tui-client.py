import npyscreen, time, socket, json

ip = '192.168.1.41'
port = 9090

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCKET.bind((ip, 0))

msgs = list()
neMsg = False

def receving(name: str, sock: socket.socket):
	"""
	Ожидание сообщение с серверов (для потока)
	"""
    global msgs
	while True:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				print('DEBUG: ' + data.decode('utf8'))
				msgs.append(data.decode('utf8'))
                neMsg = True
                # res = json.loads(data.decode("utf-8"))
				time.sleep(0.2)
		except:
			pass

def sendPacket(server: tuple, data: dict):
    SOCKET.connect((ip, port))
    SOCKET.send(json.dumps(
        data
    ).encode('utf8'), (ip, port))
    SOCKET.close()

def sendAndRecvPacket(server: tuple, data: dict, cb: callable):
    SOCKET.connect((ip, port))
    SOCKET.send(json.dumps(
        data
    ).encode('utf8'), (ip, port))
    SOCKET.close()
    SOCKET.bind((ip, 0))

class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Авторизация")

class MainForm(npyscreen.ActionForm):
    # Конструктор
    def create(self):
        # Добавляем виджет TitleText на форму
        x, y = self.useable_space()
        self.username = self.add(npyscreen.TitleText, name="Логин", value="u1")
        self.password = self.add(npyscreen.TitleText, name="Пароль", value="p1")
    # переопределенный метод, срабатывающий при нажатии на кнопку «ok»
    def on_ok(self):
        sendPacket((ip, port), dict({
            'pr': 0x00,
            'd': 'u1;p1'
        }))
        self.parentApp.setNextForm(None)
    # переопределенный метод, срабатывающий при нажатии на кнопку «cancel»
    def on_cancel(self):
        self.username.value = "..."
        self.password.value = "..."

T_receiveMsg = threading.Thread(target=receving, args=('RecvThread'))
T_receiveMsg.start()

MyApp = App()
MyApp.run()