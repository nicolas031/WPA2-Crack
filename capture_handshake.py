#coding: utf-8

"""
Script to capture the eapol authentication when a client connect to the access point,
You shouldn't run wifi-scan.py at same time to avoid errors.
Author: Njörd
github: https://github.com/Njord0/
"""

import argparse
import binascii
import logging
import os
import subprocess
import sys
import typing

from collections import OrderedDict 

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="Network interface where packets will be sniffed", required=True)
parser.add_argument("-b", "--bssid", help="Access point BSSID", required=True)
parser.add_argument("-c", "--channel", help="Channel", type=int, required=True)
parser.add_argument("-o", "--output", help="Output file", required=False)

args = parser.parse_args()

def eapol_filter(packets):
    def eapol(packet):
        if packet.haslayer(EAPOL):
            if args.bssid.lower() in [packet.addr1, packet.addr2, packet.addr3]:
                packet_raw = binascii.hexlify(packet[Raw].load)
            else:
                return

            if packet_raw[2:6].decode() == "008a": #message_1
                packets["packet_1"] = packet

            elif packet_raw[2:6].decode() == "010a": #message_2
                packets["packet_2"] = packet

            elif packet_raw[2:6].decode() == "13ca": #message_3 
                packets["packet_3"] = packet

            elif packet_raw[2:6].decode() == "030a": #message_4
                packets["packet_4"] = packet

        elif packet.haslayer(Dot11Beacon):
            if args.bssid.lower() in [packet.addr1, packet.addr2, packet.addr3]:
                packets["packet_5"] = packet

        if all(list(packets.values())):
            print("\n[+] 4-Way handshake captured, now saving...")

            try:
                wrpcap("wpa_handshake01.pcap" if not args.output else args.output, 
                    list(packets.values()))
                sys.exit("[+] Done.\n")

            except Exception as e:
                print(e)

    return eapol

def main(interface, bssid, channel, output):

    conf.iface = interface
    subprocess.Popen("iwconfig {} channel {}".format(interface, channel), shell=True)

    print("[+] Writing file {}".format("wpa_handshake01.pcap" if not output else output))
    print("[+] Capturing 4-Way handshake [{}]...".format(bssid))

    packets = OrderedDict(zip(
        [f"packet_{i}" for i in range(1, 6)], 
        [False]*5))

    sniff(prn=eapol_filter(packets))

if __name__ == "__main__":

    if sys.platform.startswith("linux"):
        if os.getuid() != 0:
            sys.exit("[!] This script need to run as root to work properly")
    elif sys.platform.startswith("win"):
        sys.exit("[!] This script is for linux only!")

    if not args.channel in range(1, 14):
        sys.exit("[!] Channel must be in range 1-13")

    print("[+] Importing scapy...", end="")
    try:
        from scapy.all import *
    except ImportError:
        sys.exit("[!] Error happened while importing scapy\n")
    else:
        print("Done.\n")

    main(args.interface, args.bssid, args.channel, args.output)