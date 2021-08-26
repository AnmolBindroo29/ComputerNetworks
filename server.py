
import threading
import sys
from socket import *
serverPort = int(sys.argv[1])
localhost = '127.0.0.1'
server = socket(AF_INET, SOCK_STREAM)
server.bind((localhost, serverPort))
server.listen()
print("Server Ready")
clients = []
nicknames = []
def broadcast(message):
	for client in clients:
		client.send(message)

def kick_user(name):
	if name in nicknames:
		index = nicknames.index(name)
		client_to_kick = clients[index]
		clients.remove(client_to_kick)
		client_to_kick.send("You were kicked by the admin".encode('ascii'))
		client_to_kick.close()
		nicknames.remove(name)
		broadcast(str(name) + "was kicked by admin".encode('ascii'))
def handle(client):
	while True:
		try:
			msg = client.recv(1024)
			if msg.decode('ascii').startswith('KICK'):
				if nicknames[clients.index(client) ] == 'admin':
					name_to_kick = msg.decode('ascii')[5:]
					kick_user(name_to_kick)
				else:
					client.send("Command was refused!".encode('ascii'))
			elif msg.decode('ascii').startswith('BAN'):
				if nicknames[clients.index(client)] == 'admin':
					name_to_ban = msg.decode('ascii')[4:]
					ban_user(name_to_ban)
					with open('ban.txt', 'a') as f:
						f.write(name_to_ban+'\n')
					print(name_to_ban, 'was banned!')
				else:
					client.send("Command was refused!".encode('ascii'))
			else:
				broadcast(msg)
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
		if nickname == 'admin':
			client.send('PASS'.encode('ascii'))
			msg = client.recv(1024).decode('ascii')
			if msg != 'root@kali':
				client.send('REFUSE'.encode('ascii'))
				client.close()
				continue
		nicknames.append(nickname)
		clients.append(client)
		print(f"Nickname of the client is {nickname}!")
		broadcast(f'{nickname} joined the chat!'.encode('ascii'))
		#client.send("Connected to the server!".encode('ascii'))
		thread = threading.Thread(target = handle, args = (client,))
		thread.start()
print("Server is Listening...")
recieve()
