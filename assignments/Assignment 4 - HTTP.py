#References : Ruslan Pivak's Blog and Notes on Creating a Web Server (Crude Illustrations Included)
#References : Emalsha's Blog on Creating a HTTPS server using Python Socket (on wordpress.com)
#References : Vishal Sathyanarayana's Code - PES1201700183
import socket
import requests

HOST, PORT = '127.0.0.1', 8008

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HTTP on port %s ...' % PORT)
while True:
    connection,address = listen_socket.accept()
    request = connection.recv(1024).decode('utf-8')
    string_list = request.split(' ')     
    method = string_list[0]
    requesting_file = string_list[1]
    print('Client request ',requesting_file)
 
    myfile = requesting_file.split('?')[0] # After the "?" symbol not relevant here
    myfile = myfile.lstrip('/')
	# Load index file as default
    if(myfile == ''):
        myfile = 'index.html'    
 
    try:
        file = open(myfile,'rb') #Open file; r => read , b => byte format
        response = file.read()
        file.close()
 
        header = 'HTTP/1.1 200 OK\n'
 
        if(myfile.endswith(".html")):
            mimetype = 'text/html'
        else:
            print("Wrong mime type")
        header += 'Content-Type: '+str(mimetype)+'\n\n'
 
    except Exception as e:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 
    finalresponse = header.encode('utf-8')
    finalresponse += response
    connection.send(finalresponse)
    connection.close()
