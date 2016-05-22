import socket
host_ip="127.0.0.1"
host_port=700
try:
    
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host_ip,host_port))
    client.send("cleint send")
    print "[*] Send message to server"
    while True:
        send=raw_input("client:")
        client.send(send)
except:
    client.close()
    





