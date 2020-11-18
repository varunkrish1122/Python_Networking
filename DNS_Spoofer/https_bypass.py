import subprocess
#
queue_port = 0
# try:
#     # subprocess.call(['iptables', '--flush'])
#     subprocess.call(['iptables', '-I', 'INPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
#     subprocess.call(['iptables', '-I', 'OUTPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
#     subprocess.call(['iptables', '-t', 'nat','-A', 'PREROUTING', '-p', 'tcp', '--destination-port', '80', '-j', 'REDIRECT', '--to-port', '10000'])
#
# except KeyboardInterrupt:
#     print('\n\n[+] - Pressed CTRL + C .... Quitting!! Flushing!!')
#     subprocess.call(['iptables', '--flush'])

# subprocess.call(['iptables', '-I', 'OUTPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
# subprocess.call(['iptables', '-I', 'INPUT', '-j', 'NFQUEUE', '--queue-num', str(queue_port)])
subprocess.call(['iptables', '-t', 'nat','-A', 'PREROUTING', '-p', 'tcp', '--destination-port', '80', '-j', 'REDIRECT', '--to-port', '10000'])
# subprocess.call(['iptables', '-t', 'nat','-A', 'PREROUTING', '-p', 'tcp', '--destination-port', '443', '-j', 'REDIRECT', '--to-port', '10000'])