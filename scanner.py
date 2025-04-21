import socket
import argparse
import concurrent.futures

# Basic function to scan a single port
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout in seconds
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return port
    except:
        pass
    return None

# Function to scan multiple ports using threads
def scan_ports(ip, ports, max_threads):
    open_ports = []
    print(f"\n[+] Scanning {ip} with {max_threads} threads...")

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            port = futures[future]
            try:
                if future.result() is not None:
                    open_ports.append(port)
                    print(f"[+] Port {port} is open")
            except Exception as e:
                print(f"[-] Error scanning port {port}: {e}")
    
    return open_ports

# Parse CLI arguments
def main():
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
    parser.add_argument("target", help="Target IP or hostname")
    parser.add_argument("-p", "--ports", help="Ports to scan (e.g. 22,80,443 or 1-1024)", default="1-1024")
    parser.add_argument("-t", "--threads", help="Number of threads", type=int, default=100)
    args = parser.parse_args()

    # Resolve hostname to IP
    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print("[-] Could not resolve hostname.")
        return

    # Process port input
    ports = []
    if "-" in args.ports:
        start, end = args.ports.split("-")
        ports = list(range(int(start), int(end)+1))
    else:
        ports = [int(p.strip()) for p in args.ports.split(",")]

    open_ports = scan_ports(ip, ports, args.threads)

    print("\n[+] Scan complete.")
    print("[+] Open ports:", open_ports if open_ports else "None")

if __name__ == "__main__":
    main()
