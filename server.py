import socket, threading
import sys

# open socket to connect with the clients with port from the usr
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip ='0.0.0.0'
dest_port = int(sys.argv[1])
server.bind((server_ip, dest_port))
server.listen(5)

# dictionary of client ports and list of files
clients = {}
# dictionary of client poer and ip
info = {}

# wait for client to connect
while True:
	client_socket, client_address = server.accept()
	data = client_socket.recv(1024).decode()
	#  if client send '1' add the client to the client dictionary and save the files	
	if data[0] == '1':
		data = data.split(' ')
		files_list = data[2].split(',')
		port = data[1]
		clients[port] = files_list 	
		info[port] = client_address[0]
	# if client send '2' search for the containing the string
	elif data[0] == '2':
		result = ""
		name_of_file = data[2]
		for client in clients:
			for f in clients[client]:
				if name_of_file in f:
					# add all the file information to the string
					result = result + str(f) + " " + str(info[client]) +" " + str(client) + ","
		result = result + "\n"
		# send the list to the client
		client_socket.send(result)
	# close the socket
	client_socket.close()
