import subprocess
import optparse

def mac_change(interface, new_mac):
    print('[+] Current Configuration \n \n')
    subprocess.call(['ifconfig', interface])
    print('\n \n [+] Started changing MAC Address to ' + new_mac)
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])
    print('\n \n [+] MAC Address Changed to ' + new_mac + '\n \n')
    subprocess.call(['ifconfig', interface])

def get_options():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest='interface', help='Interface used to change MAC')
    parser.add_option('-m', '--mac', dest='new_mac', help='MAC address to change')
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error('Please provide Interface visit --help for more info')
    elif not options.new_mac:
        parser.error('Please provide MAC Address visit --help for more info')
    return options

options = get_options()
mac_change(options.interface, options.new_mac)