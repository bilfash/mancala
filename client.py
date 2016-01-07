#!/usr/bin/env python
from __future__ import print_function
import socket
import os
import time
import subprocess as sp
import pickle

server_address = ('localhost', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
buff = 1024

realpit = []
shadowpit = []
depth = []
player = 1

def changeplayer():
	global player
	if player == 1:
		player = 2
	else:
		player = 1
	return player

def choose(x, pit = []):
	if pit[x]!=0 or x!=13 or x!=6:
		hold = pit[x]
		now = x
		pit[x] = 0
		while 1:
			now += 1
			now = now%14
			#apabila turn player 1 atau 2 berjalan tapi melewati base lawan
			if player == 1 and now==13:
				pass
			elif player == 2 and now == 6:
				pass
			#apabila sisa batu di tangan = 1	
			elif (pit[now]==0 or now==player*7-1) and hold==1 :
				#apabila turn player 1 atau 2 berjalan tapi melewati base sendiri
				if now == player*7-1:
					pit[now] = pit[now]+1

				else:
					#apabila berhenti di lubang yang tidak kosong
					if (player==1 and now<6) or (player==2 and now>6):
						pit[player*7-1]+=pit[((player*7-1)+((player*7-1)-now))%14]
						pit[((player*7-1)+((player*7-1)-now))%14]=0
					pit[now]=pit[now]+1
					changeplayer()
				hold -= 1
				break
			#menembak
			elif hold==1 and pit[now]!=0:
				hold+=pit[now]
				pit[now]=0
			#increment biasa
			else:
				pit[now]+=1
				hold-=1

			sp.call('cls',shell=True)
			print ("              Room ",room)
			print ('')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('|    | ', end='')
			for y in range(5,-1,-1):
				print (pit[y],'|', end=' ')
			print ('   |')
			print ("|    |-----------------------|    |")

			print ("|",'%2s'%pit[6] , "|       Player ",player_tag,"      |" , '%2s'%pit[13],"|")

			print ("|    |-----------------------|    |")
			print ("|    | ", end='')
			for z in range(7,13):
				print (pit[z],'|', end=' ')
			print ('   |')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('')
			
			print ("Giliran Player", player)
			print ("Player", player,"memilih lubang =",x)
			print ("Sisa = " , hold)
			time.sleep(0.5)
			sp.call('cls',shell=True)

if __name__ == "__main__":
	flag_pertama = 0

	i=""

	if flag_pertama == 0:
		data = client_socket.recv(4)
		player_tag = int(data.split(" ")[0])
		temp = int(data.split(" ")[1])
		room = 1
		while temp >= 0:
			temp -=2
			if temp <= 0:
				break
			room += 1
		flag_pertama = 1

	for a in range(0,14):
		realpit.append(0)
		shadowpit.append(0)

	for i in range(0,14):
		if i==6 or i==13:
			realpit[i] = 0
		else:
			realpit[i] = 3
	sp.call('cls',shell=True)
	print ("              Room ",room)
	print ('')
	print ("-----------------------------------", end='')
	print ("  ", end='')
	print ('')
	print ('|    | ', end='')
	for y in range(5,-1,-1):
		print (realpit[y],'|', end=' ')
	print ('   |')
	print ("|    |-----------------------|    |")

	print ("|",'%2s'%realpit[6] , "|       Player ",player_tag,"      |" , '%2s'%realpit[13],"|")

	print ("|    |-----------------------|    |")
	print ("|    | ", end='')
	for z in range(7,13):
		print (realpit[z],'|', end=' ')
	print ('   |')
	print ("-----------------------------------", end='')
	print ("  ", end='')
	print ('')
	print ('')
	print ('')

	print ("            Button Index")
	print ("-----------------------------------", end='')
	print ("  ", end='')
	print ('')
	print ('|    | ', end='')
	if player_tag == 1:
		for y in range(5,-1,-1):
			print (y,'|', end=' ')
	else:
		for y in range(5,-1,-1):
			print (' ','|', end=' ')
	print ('   |')
	print ("|    |-----------------------|    |")

	print ("|",'  ' , "|       Player ",player_tag,"      |    |")

	print ("|    |-----------------------|    |")
	print ("|    | ", end='')
	if player_tag == 2:
		for z in range(7,13):
			if z < 9 or z==12:
				print (z,'|', end=' ')
			else:
				print (z,'|', end='')
	else:
		for y in range(7,13):
			print (' ','|', end=' ')
	print ('   |')
	print ("-----------------------------------", end='')
	print ("  ", end='')
	print ('')
	while 1:
		#player 1
		if player_tag == 1 :
			play1 = 0
			play2 = 0
			# print ("Player",player)
			if player == 1:
				print ("Giliran Anda Silahakan memilih lubang: ", end='')
				pilih = input()
				if (pilih <= 5):
					client_socket.send(pickle.dumps(pilih))
				while  pilih > 5:
					print ("Giliran Anda Silahakan memilih lubang: ", end='')
					pilih = input()
					if pilih <= 5:
						client_socket.send(pickle.dumps(pilih))
						break
			else:
				print ("Giliran Player 2 Silahkan Tunggu...", end='')
				data = client_socket.recv(5)
				data2 = pickle.loads(data)
				pilih = int(data2)
				print (pilih)

			time.sleep(0.5)
			sp.call('cls',shell=True)

			if realpit[pilih] == 0:
				player = changeplayer()
			else:
				choose(pilih, realpit)
			print ("              Room ",room)
			print ('')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('|    | ', end='')
			for y in range(5,-1,-1):
				print (realpit[y],'|', end=' ')
				if realpit[y] == 0:
					play1+=1
			print ('   |')
			print ("|    |-----------------------|    |")

			print ("|",'%2s'%realpit[6] , "|       Player ",player_tag,"      |" , '%2s'%realpit[13],"|")

			print ("|    |-----------------------|    |")
			print ("|    | ", end='')
			for z in range(7,13):
				print (realpit[z],'|', end=' ')
				if realpit[z] == 0:
					play2+=1
			print ('   |')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('')
			print ('')

			print ("            Button Index")
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('|    | ', end='')
			if player_tag == 1:
				for y in range(5,-1,-1):
					print (y,'|', end=' ')
			else:
				for y in range(5,-1,-1):
					print (' ','|', end=' ')
			print ('   |')
			print ("|    |-----------------------|    |")

			print ("|",'  ' , "|       Player ",player_tag,"      |    |")

			print ("|    |-----------------------|    |")
			print ("|    | ", end='')
			if player_tag == 2:
				for z in range(7,13):
					if z < 9 or z==12:
						print (z,'|', end=' ')
					else:
						print (z,'|', end='')
			else:
				for y in range(7,13):
					print (' ','|', end=' ')
			print ('   |')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			if play1 == 6 and play2 == 6:
				client_socket.send("tutup")
				if realpit[6] < realpit[13]:
					print ("Player 2 MENANG") 
				elif realpit[6] > realpit[13]:
					print ("Player 1 MENANG")
				else:
					print ("DRAW")
				time.sleep(3)
				break

		#player 2
		elif player_tag == 2 :
			play1 = 0
			play2 = 0
			# print ("Player",player)
			if player == 1:
				print ("Giliran Player 1 Silahkan Tunggu...", end='')
				data = client_socket.recv(5)
				data2 = pickle.loads(data)
				pilih = int(data2)
				# print (pilih)
			else:
				print ("Giliran Anda Silahakan memilih lubang: ", end='')
				pilih = input()
				if pilih > 6 and pilih <= 12:
					client_socket.send(pickle.dumps(pilih))
				while  pilih <= 6 or pilih > 12:
					print ("Giliran Anda Silahakan memilih lubang: ", end='')
					pilih = input()
					if pilih > 6 and pilih <= 12:
						client_socket.send(pickle.dumps(pilih))
						break
				
			time.sleep(0.5)
			sp.call('cls',shell=True)

			if realpit[pilih] == 0:
				player = changeplayer()
			else:
				choose(pilih, realpit)
			print ("              Room ",room)
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('|    | ', end='')
			for y in range(5,-1,-1):
				print (realpit[y],'|', end=' ')
				if realpit[y] == 0:
					play1+=1
			print ('   |')
			print ("|    |-----------------------|    |")

			print ("|",'%2s'%realpit[6] , "|       Player ",player_tag,"      |" , '%2s'%realpit[13],"|")

			print ("|    |-----------------------|    |")
			print ("|    | ", end='')
			for z in range(7,13):
				print (realpit[z],'|', end=' ')
				if realpit[z] == 0:
					play2+=1
			print ('   |')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('')
			print ('')

			print ("            Button Index")
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			print ('|    | ', end='')
			if player_tag == 1:
				for y in range(5,-1,-1):
					print (y,'|', end=' ')
			else:
				for y in range(5,-1,-1):
					print (' ','|', end=' ')
			print ('   |')
			print ("|    |-----------------------|    |")

			print ("|",'  ' , "|       Player ",player_tag,"      |    |")

			print ("|    |-----------------------|    |")
			print ("|    | ", end='')
			if player_tag == 2:
				for z in range(7,13):
					if z < 9 or z==12:
						print (z,'|', end=' ')
					else:
						print (z,'|', end='')
			else:
				for y in range(7,13):
					print (' ','|', end=' ')
			print ('   |')
			print ("-----------------------------------", end='')
			print ("  ", end='')
			print ('')
			if play1 == 6 and play2 == 6:
				client_socket.send("tutup")
				if realpit[6] < realpit[13]:
					print ("Player 2 MENANG") 
				elif realpit[6] > realpit[13]:
					print ("Player 1 MENANG")
				else:
					print ("DRAW")
				time.sleep(3)
				break
