#!/usr/bin/env python
import socket
import select
import sys
import time

input_socket = []
server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(8)
size = 1024
input_socket.append(server_socket)
dict={}
clients = []
clients_stream = []
i=1
flag = 0
data = ""
try:
    while True:

        read_ready, write_ready, exception = select.select(input_socket, [], [])
        for sock in read_ready:
        	
        	if sock == server_socket:
        		client_socket, client_address = server_socket.accept()
        		input_socket.append(client_socket)   
        		dict[client_socket] = i
        		print "Player " + str(i) + " Connected " + str(client_address[1])
        		clients.append(client_socket)
        		clients_stream.append(client_address)
        		if i==1:
        			flag = 1
        		elif i==2:
        			flag = 2
        		

        		if flag == 1:
        			ada = "1"
        			input_socket[1].send(ada)
        			flag = 0
        		elif flag ==2:
        			ada = "2"
        			input_socket[2].send(ada)
        			flag = 0
        		i+=1                
        	else:    
        		data = sock.recv(2)
        		# if data != "":
        		# 	for i in clients:
        		# 		if i is not server_socket:
        		# 			print i
        		# 			i.send(data)    
                if data != "":
                	print data
                	clients[0].send("ada "+data)
	            	clients[1].send("ada "+data)
                	data=""
                else:
                    if i>2:
                        print data
                        clients[0].send("non "+data)
                        clients[1].send("non "+data)
                        data=""

                # elif data=="":
                #     sock.close()
                #     input_socket.remove(sock)
                	#print temp
                	#sock.send(temp)
                	
except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        
