import socket
import threading
import select
import sys
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IPAddress = socket.gethostbyname(socket.gethostname())
port = 8081

server.bind((IPAddress, port))

server.listen(100)

userList = []
nicknameList = []


def broadcast(message):
    for user in userList:
        user.send(message)


def specific_user(name):
    i = 0
    for name in nicknameList:
        if name == nicknameList[i]:
            return name
        i += 1


def handle(user):
    while True:
        try:
            message = user.recv(1024)
            broadcast(message)
        except:
            index = userList.index(user)
            userList.remove(user)
            user.close()
            nickname = nicknameList[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknameList.remove(nickname)
            break


def receive():
    while True:
        user, address = server.accept()
        print("Connected with {}".format(str(address)))
        user.send('NICKNAME'.encode('ascii'))
        nickname = user.recv(1024).decode('ascii')
        nicknameList.append(nickname)
        userList.append(user)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        user.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()


receive()
