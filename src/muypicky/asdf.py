import socket;
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1',4040))
print(result)
if result == 0:
   print "Port is not open"
else:
   print "Port is open"