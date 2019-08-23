import socket, json, time

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCKET.bind(('192.168.1.41', 9090))
q = False
clients = []

while not q:
    try:
        data, addr = SOCKET.recvfrom(1024)

        if addr not in clients:
            clients.append(addr)
        
        req = json.loads(data.decode('utf8'))
        print('Req: ' + json.dumps(req))
        res = dict()
        
        """
        Строение пакета и этапы передачи
        1) Получение данных о 'весе' следующих пакетов
        ...
        """

        """
        pr - тип протокола
         0x00 - Запрос авторизации
         0x01 - Авторизация успешна
         0x02 - Авторизация отклонена
         0x03 - Сообщение
         0x0-1 - Неизвестный протокол
        """
        if req['pr'] == 0x00:
            if req['d'].split(';')[0] == 'u1' and req['d'].split(';')[1] == 'p1':
                res['pr'] = 0x01
            else:
                res['pr'] = 0x02
        else:
            res['pr'] = 0x0-1

        res['b'] = 0x00
        res['w'] = len(res.encode('utf8') + 20)

        print('Res: ' + str(res))
        SOCKET.sendto(json.dumps(res).encode('utf8'), addr)
        # print('Seconds send')
        # SOCKET.sendto(json.dumps(res).encode('utf8'), addr)

        for client in clients:
            if addr != client:
                SOCKET.sendto(data, client)
    except:
        q = True

SOCKET.close()