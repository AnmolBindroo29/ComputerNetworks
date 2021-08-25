from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Server Ready")
while True:
	connectionSocket , addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024).decode()
	capitalized = sentence.upper()
	connectionSocket.send(capitalized.encode())
	connectionSocket.close()
