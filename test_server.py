import socket
import thread
host_ip="127.0.0.1"
host_port=700
accept_num=0
mylock = thread.allocate_lock()
def Accept_Thread():
     
   
   
    
    while True:
        mylock.acquire() 
    
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("127.0.0.1",700))
        server.listen(0)
        print "[*] Listening on %s:%d" % (host_ip,host_port)
        
            
        client_socket,addr=server.accept()
        server.close()
        client_socket2=client_socket
        #accept_num=accept_num +1
        thread.start_new_thread(Recv_Thread,(client_socket2,))
        #z = threading.Thread(target=Recv_Thread,args=(client_socket,accept_num))
        #z.start()

        print "[*] Accept from:%s:%d" % (addr[0],addr[1])
        mylock.release() 

        



def Recv_Thread(client_socket_1):
    
    mylock.acquire()
    while True:
        recvbuffer = client_socket_1.recv(1024)
        if not recvbuffer:
            client_socket_1.close()
            print "[*]close one socket"
            mylock.release() 
            return 
        elif recvbuffer<0:
            print "[*]error"
            return
        else:
            print "[*]recv message %s" % recvbuffer
            
           # client_socket_1.close()
        
        
    


if __name__ == "__main__":
    
     thread.start_new_thread(Accept_Thread,())
       
        
    


