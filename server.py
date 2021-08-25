import threading
from socket import *
serverPort = 12000
localhost = '127.0.0.1'
server = socket(AF_INET, SOCK_STREAM)
server.bind((localhost, serverPort))
server.listen(1)
print("Server Ready")
clients = []
nicknames = []
def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = clients.index(client)
			clients.remove(client)
			clients.close()
			nickname = nicknames[index]
			broadcast(f'{nickname} left the chat!'.encode('ascii'))
			nicknames.remove(nickname)
			break

def recieve():
	while True:
		client, addr = server.accept()
		print(f"Connected with {str(addr)}")
		client.send('NICK'.encode('ascii'))
		nickname = client.recv(1024).decode('ascii')
		nicknames.append(nickname)
		clients.append(client)
		print(f"Nickname of the client is {nickname}!")
		broadcast(f'{nickname} joined the chat!'.encode('ascii'))
		client.send("Connected to the server!".encode('ascii'))
		thread = threading.Thread(target = handle, args = (client,))
		thread.start()
print("Server is Listening...")
recieve()
