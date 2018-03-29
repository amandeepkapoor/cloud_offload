import socket
import datetime

host = '199.60.17.11'
port = 23000                   # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
for i in range(1):
	t1_network = datetime.datetime.now()
	s.sendall(b'H'*640*480)
	data = s.recv(640*480)
	t2_network = datetime.datetime.now()
	tdif_network = t2_network - t1_network
	print('Total network time =' + str(tdif_network.seconds + tdif_network.microseconds/1e6) + ' seconds')
	#print('Received', str(data,'utf-8'))

s.close()