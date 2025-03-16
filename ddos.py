import socket
import requests as r
import random
import threading
from colorama import Fore, Style

iphosts = [
    'https://wtfismyip.com/text',
    'https://ipinfo.io/ip',
    'https://ipv4.icanhazip.com/',
    'https://myexternalip.com/raw',
    'https://ifconfig.io/ip',
    'https://ipecho.net/plain'
]


def get_my_ip():
    try:
        return r.get(random.choice(iphosts)).text.strip()
    except:
        return None


def check_proxy(proxy, server_ip, server_port):
    try:
        # Set up the proxy
        proxy_parts = proxy.split(':')
        proxy_host = proxy_parts[0]
        proxy_port = int(proxy_parts[1])

        # Create a socket and connect to the Minecraft server through the proxy
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((proxy_host, proxy_port))
        sock.sendall(bytes(f'CONNECT {server_ip}:{server_port} HTTP/1.1\r\n\r\n', 'utf-8'))
        response = sock.recv(4096).decode(errors='ignore')

        if "200 Connection established" in response:
            print(Fore.GREEN + f"[+] Working Proxy: {proxy}" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"[-] Bad Proxy: {proxy}" + Style.RESET_ALL)

        sock.close()

    except:
        print(Fore.RED + f"[-] Bad Proxy: {proxy}" + Style.RESET_ALL)



def main():
    server_ip = input("Enter Minecraft server IP: ")
    server_port = input("Enter Minecraft server port (default 25565): ") or "25565"

    # Load proxy list from a file
    proxy_file = input("Enter proxy list file: ")
    
    try:
        with open(proxy_file, 'r') as f:
            proxies = f.read().splitlines()
    except FileNotFoundError:
        print("File not found!")
        return

    # Check each proxy in a separate thread
    threads = []
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy, server_ip, server_port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
