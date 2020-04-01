from scapy.all import *
import subprocess
import re


class ArpSpoofDetector:
    def __init__(self):
        pass

    def get_mac_ids(self):
        arp_table_result = subprocess.check_output(["arp", "-a"])
        gateway_ip = conf.route.route("0.0.0.0")[2]
        gateway_mac_id = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(arp_table_result))
        real_mac_id = getmacbyip(gateway_ip)
        return real_mac_id, gateway_mac_id

    def print_result(self, real_mac_id, gateway_mac_id):
        if real_mac_id != gateway_mac_id.group(0):
            print("[-] You are under ArpSpoof Attack!")
            print("Real MAC\t\t\tGateway MAC" + "\n" + "-------------------------------------------------")
            print(str(real_mac_id) + "\t\t" + str(gateway_mac_id.group(0)))
            subprocess.call(["nmcli", "r", "wifi", "off"])
            print("[+] Hence your Wifi has been turned Off ;)")
        else:
            print("[+] You are not under ArpSpoof Attack :)")

    def execute_arp_spoof_detector(self):
        real_mac_id, gateway_mac_id = self.get_mac_ids()
        self.print_result(real_mac_id, gateway_mac_id)


obj = ArpSpoofDetector()
obj.execute_arp_spoof_detector()
