import sys
import threading
from socket import *
serverName = '127.0.0.1'
serverPort = int(sys.argv[1])
stop_thread = False
nickname = sys.argv[2]
if nickname == 'admin':
	passwrd = input("Enter password")
client = socket(AF_INET, SOCK_STREAM)
client.connect((serverName, serverPort))
def recieve():
	while True:
		global stop_thread 
		if(stop_thread):
			break
		try:
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
				next_msg  = client.recv(1024).decode('ascii')
				if next_msg == 'PASS':
					client.send(passwrd.encode('ascii'))
					if(client.recv(1024).decode('ascii') == 'REFUSE'):
						print("Connection Refused")
						stop_thread = True
				elif next_msg == 'BAN':
					print("Connection refused because of ban!")
					client.close()
					stop_thread = True

			else:
				print(message)
		except:
			print("An error occured")
			client.close()
			break
def write():
	while True:
		if(stop_thread):
			break
		message = f'{nickname}:{input("")}'
		if message[len(nickname) +2:].startswith('/') and nickname == 'admin':
			if message[len(nickname) + 2:].startswith('/kick'):
				#print("")
				client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
			elif message[len(nickname) + 2:].startswith('/ban'):
				client.send(f'BAN {message[len(nickname)+7:]}'.encode('ascii'))
			else:
				print("Invalid Operation")
		else:
			client.send(message.encode('ascii'))
recieve_thread = threading.Thread(target = recieve)
recieve_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()
 
