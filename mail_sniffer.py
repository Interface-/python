# -*- coding: cp936 -*-
from scapy.all import *

#���ݰ��ص�����
def packet_callback(packet):
    print packet.show()

#������̽��
sniff(prn=packet_callback,count=1)
