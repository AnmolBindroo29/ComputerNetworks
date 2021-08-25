import threading
from socket import *
serverName = '127.0.0.1'
serverPort = 12000
nickname = input("Choose a nickname: ")
client = socket(AF_INET, SOCK_STREAM)
client.connect((serverName, serverPort))
def recieve():
	while True:
		try:
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
			else:
				print(message)
		except:
			print("An error occured")
			client.close()
			break
def write():
	while True:
		message = f'{nickname}:{input("")}'
		client.send(message.encode('ascii'))
recieve_thread = threading.Thread(target = recieve)
recieve_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()
