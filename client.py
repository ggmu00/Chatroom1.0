import socket
import threading
from secretpy import Playfair


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IPAddress = socket.gethostbyname(socket.gethostname())
port = 8081
server.connect((IPAddress, port))

nickname = input("Choose a nickname: ")


def receive():
    while True:
        try:
            message = server.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                server.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            server.close()
            break


def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        message = message.replace(" ", "")
        message = message.replace(",", "")
        message = message.lower()
        new_message = Playfair().encrypt(message, "blanket")
        #print(new_message)
        server.send(new_message.encode('ascii'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
