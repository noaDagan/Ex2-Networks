import socket
import os
import sys

# class file info contain the name of the file, ip and port of the client
class file_info :
	def __init__(self, name=None ,ip=None ,port=None):
		self.name=name
		self.ip=ip
		self.port=port
	def __lt__(self,other):
		return self.name < other.name
	


# client sever mode
def client_mode_0(dest_ip,dest_port,socket_port):
	# open a socket and connect to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((dest_ip, dest_port))
	# run over all the files in the directory and send to server
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	str_files = ""
	for f in files:
		str_files = str_files + f 
		str_files = str_files + ","
		msg = "1 " + str(socket_port) + " " + str_files 
	s.send(msg)
	s.close()
	# open new socket
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.bind(('0.0.0.0', socket_port))
	client.listen(5)
	while True:
		# wait for client connect
		client_socket, client_address = client.accept()
		file_to_find = client_socket.recv(1024)
		file_to_read = open(file_to_find,'rb')  
		line = file_to_read.read(1024)
		# read the file and send
		while line:
			client_socket.send(line)
			line = file_to_read.read(1024)
		client_socket.send(line)
		# close the file and socket
		file_to_read.close()
		client_socket.close()



# client mode
def client_mode_1():
	sort_files_list = []
	files_dic = {}
	# get the file name from the user
	msg = raw_input("Search: ")
	# connect to server, send the file name and wait to the files list
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((dest_ip, dest_port))
	s.send("2 " + msg)
	data = s.recv(1024).decode()	
	# close the socket
	s.close()
	# go over the list and print the list for the user
	if data != "\n":
		list_from_usr = data.split(',')
		i = 0
		while list_from_usr[i] != "\n":	
			user_list = list_from_usr[i]
			user_list =  user_list.split(' ')
			newFile=file_info(user_list[0],user_list[1],user_list[2])
			sort_files_list.append(newFile)
			sort_files_list.sort()
	 		i = i + 1
		i = 1
		# print the sorted list
		for f in sort_files_list:
			print(str(i) + " " + f.name)
			i = i + 1			
		msg = raw_input("Choose: ")
		msg = int(msg)
		files_send = sort_files_list[msg - 1]			
		dest_ip_c = files_send.ip
		dest_port_c = int(files_send.port)
		# connect to client and wait for the file
		s_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s_c.connect((dest_ip_c, dest_port_c))
		s_c.send(files_send.name)
		new_file = open(files_send.name,'wb')
		while True:
			data = s_c.recv(1024)
			if data == '':
				break
			new_file.write(str(data))
		# close the file and socket
		new_file.close()
		s_c.close()
	



if __name__ == "__main__":
	# check if argument is valid
	if len(sys.argv) < 4:
		raise Exception("Illegal arguments")
	dest_ip =sys.argv[2]
	dest_port = int(sys.argv[3])
	mode = int(sys.argv[1])
	files = {}
	while True:
		# user choose mode 0
		if mode == 0:
			if len(sys.argv) != 5:
				raise Exception("Illegal arguments")
			socket_port = int(sys.argv[4])
			client_mode_0(dest_ip,dest_port,socket_port)
		# user choose mode 1	
		elif mode == 1:
			while True:
				client_mode_1()
	


