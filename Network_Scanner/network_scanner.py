import scapy.all as scapy
import optparse

def get_argments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='targetIP', help='Enter Target IP Range')
    options, attributes = parser.parse_args()
    if not options.targetIP:
        parser.error('Please Enter IP Range')
    return options

def scanIP_MAC(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    broadcast_arp_packet = broadcast/arp_packet
    answered, unanswered = scapy.srp(broadcast_arp_packet, timeout=1)
    return answered
def print_result(answered):
    print('IP \t\t\t MAC Address \n ---------------------------')
    for element in answered:
        receivedData = element[1]
        sourceIP = receivedData.psrc
        sourceMac = receivedData.hwsrc
        print(sourceIP + '\t\t\t '+ sourceMac + '\n')
options = get_argments()
scanned_result = scanIP_MAC(options.targetIP)
print_result(scanned_result)

