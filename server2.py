#!/usr/bin/env python
import socket
import select
import sys
import time
import thread

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

def player_tag(z):
    if z%2 == 1:
        flag = 1
    else:
        flag = 2
    

    if flag == 1:
        ada = "1"
        input_socket[z].send(ada)
        flag = 0
    elif flag ==2:
        ada = "2"
        input_socket[z+1].send(ada)
        flag = 0

def gameplay(y):
    if y%2 == 1:
        clients[y-1].send(data)
        clients[y].send(data)
    else:
        clients[y-2].send(data)
        clients[y-1].send(data)

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
                thread.start_new_thread(player_tag,(i))
                i+=1
            
            else:
                data = ""
                data = sock.recv(2)
                a=1
                for sock_temp in read_ready:
                    if sock_temp == sock:
                        break
                    a++
                if data != "":
                    #print data
                    thread.start_new_thread( gameplay, (a) )
                    data=""
                	
except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        
