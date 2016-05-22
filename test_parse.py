# -*- coding: cp936 -*-
import re
import zlib
import os

from scapy.all import *
num=1
a=rdpcap("pcap1.pcap")
while True:
    try:
        num+=1
        file_name="pcap%d.pcap" % num
        b=rdpcap(file_name)
        a=a+b
    except:
        break
        print "[*] Read pcap file ok"
    
  

print "[*] Begin to parse pcapfile..."

try:
 
    print "[*] OPen new pcap_file %s" % pcap_file
    sessions=a.sessions()
    for session in sessions:
        print "[*]New session %s" % session
        data_payload=""
        for packet in sessions[session]:
            try:
                data_payload +=str(packet[TCP].payload)
                print "[**] Data:%s" % data_payload
            except:
                pass
except:
    print "[*]no pcapfile..."

       
