#!/usr/bin/env python
import socket
import select
import sys
import time
import thread
import pickle

input_socket = []
server_address = ('localhost', 5000)
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

def player_tag(threadName, z):
    print z
    if z%2 == 1:
        flag = 1
    else:
        flag = 2
    

    if flag == 1:
        ada = "1"
        input_socket[z].send(ada)
        flag = 0
    elif flag ==2 and z>1:
        ada = "2"
        input_socket[z].send(ada)
        flag = 0

def gameplay(data, y):
    print y
    print data
    if y%2 == 0:
        clients[y].send(data)
        clients[y+1].send(data)
    else:
        clients[y-1].send(data)
        clients[y].send(data)

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
                thread.start_new_thread(player_tag,("player"+str(i), i))
                i+=1
            else:
                data = sock.recv(36)
                a=0
                b=1
                for sock_temp in clients:
                    if sock_temp == sock:
                        break
                    a+=1
                    b+=1
                
                if "tutup" in data:
                    if b%2 == 0:
                        time.sleep(5)
                        input_socket[b].close()
                        input_socket[b-1].close()
                        input_socket.remove(input_socket[b-1])
                        input_socket.remove(input_socket[b-1])
                        clients.remove(clients[b-2])
                        clients.remove(clients[b-2])
                        i-=2
                    else:
                        time.sleep(5)
                        input_socket[b].close()
                        input_socket[b+1].close()
                        input_socket.remove(input_socket[b])
                        input_socket.remove(input_socket[b])
                        clients.remove(clients[b-1])
                        clients.remove(clients[b-1])
                        i-=2
                elif data != "":
                    print pickle.loads(data)
                    thread.start_new_thread( gameplay, (data, a) )
                
                	
except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)        
