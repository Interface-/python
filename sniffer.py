#-*- coding: UTF-8 -*- 
import socket
import os
import struct
from ctypes import *
import threading
import time
from netaddr import IPNetwork,IPAddress

host="192.168.1.102"

subnet="192.168.1.0/24"
#IP 头定义
class IP(Structure):
    _fields_=[
        ("ihl",          c_ubyte,4),
        
        ("version",      c_ubyte,4),
        ("tos",          c_ubyte),
        ("len",          c_ushort),
        ("id",           c_ushort),
        ("offset",       c_ushort),
        ("ttl",          c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum",          c_ushort),
        ("src",          c_ulong),
        ("dst",          c_ulong)
    ]

    def __new__(self,socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    def __init__(self,socket_buffer=None):
        #协议字段与名称映射
        self.protocol_map={1:"ICMP",6:"TCP",17:"UDP"}
        #转为可读性更强的ip
        self.src_address=socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address=socket.inet_ntoa(struct.pack("<L",self.dst))
        #协议类型
        try:
            self.protocol=self.protocol_map[self.protocol_num]
        except:
            self.protocol=str(self.protocol_num)
            
        
#ICMP 定义
class ICMP(Structure):

    _fields_=[
        ("type",        c_ubyte),
        ("code",        c_ubyte),
        ("checksum",    c_ushort),
        ("unused",      c_ushort),
        ("next_hop_mtu",c_ushort)
        ]
    def __new__(self,socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    def __init__(self,socket_buffer):
        pass


#自定义的字符串，在ICMP中进行核对
magic_message="nibiru!"

#批量发送UDP包
def udp_sender(subnet,magic_message):
    time.sleep(5)
    sender=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):

        try:
            sender.sendto(magic_message,("%s" % ip,65212))
        except:
            pass
t=threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()









#创建原始套接字，并绑定在公开端口


if os.name=="nt":
    socket_protocol=socket.IPPROTO_IP
else:
    socket_protocol=socket.IPPROTO_ICMP
    
sniffer=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((host,0))

#设置在捕获的数据包中包含IP头

sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

#在windows 平台上启动网卡混杂模式

if os.name=="nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

try:
    while True:
        #读取数据包
        raw_buffer=sniffer.recvfrom(65565)[0]

        #将缓冲区前20字节按ip头进行解析
        ip_header=IP(raw_buffer[0:20])
        #输出协议和通信双方ip地址
       # print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address,ip_header.dst_address)
        if ip_header.protocol=="ICMP":
            #计算ICMP包的起始位置
            offset=ip_header.ihl * 4
            buf=raw_buffer[offset:offset+sizeof(ICMP)]

            #解析ICMP数据
            icmp_header=ICMP(buf)

          #  print "ICMP -> Type: %d Code: %d" % (icmp_header.type,icmp_header.code)
            if icmp_header.code == 3 and icmp_header.type==3:

                #确认响应主机在目标子网内
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                    #q确认ICMP数据中华包含我们发送的字符串
                    if raw_buffer[len(raw_buffer)-len(magic_message):]==magic_message:
                        print "Host Up: %s" % ip_header.src_address


        #处理CTRL—C
except KeyboardInterrupt:
    #如果运行在Windows上，关闭混杂模式
    
    if os.name=="nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
        print "RCVALL_OFF.."
                    
        


