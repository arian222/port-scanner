#!/usr/bin/env python3

import socket
import sys
import threading
import time
from queue import Queue
from datetime import datetime
import itertools
import threading
import json
import os
import platform

# Inițializare queue pentru thread-uri
queue = Queue()
open_ports = []
stop_loading = False

def animate_loading():
    """Funcție pentru animația de loading"""
    chars = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    global stop_loading
    while not stop_loading:
        sys.stdout.write('\r' + '\033[93m' + 'Scanare în progres ' + next(chars) + '\033[0m')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')
    sys.stdout.flush()

def print_rainbow_text(text):
    """Printează text în culorile curcubeului"""
    colors = ['\033[91m', '\033[93m', '\033[92m', '\033[94m', '\033[95m', '\033[96m']
    colored_text = ''
    for i, char in enumerate(text):
        if char != ' ':
            colored_text += colors[i % len(colors)] + char
        else:
            colored_text += char
    print(colored_text + '\033[0m')

def scan_port(target, port):
    """Scanează un singur port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
            try:
                service = socket.getservbyport(port)
                print(f"\033[92m[+] Port {port} ({service}): \033[1mDESCHIS\033[0m")
            except:
                print(f"\033[92m[+] Port {port}: \033[1mDESCHIS\033[0m")
        else:
            print(f"\033[91m[-] Port {port}: ÎNCHIS\033[0m")
        sock.close()
    except:
        print(f"\033[93m[?] Port {port}: EROARE LA SCANARE\033[0m")

def get_threads():
    """Procesează queue-ul cu thread-uri"""
    while True:
        worker = queue.get()
        if worker is None:
            break
        target, port = worker
        scan_port(target, port)
        queue.task_done()

def print_banner():
    """Afișează banner-ul animat"""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║          Port Scanner by ALECS               ║
    ║        Advanced Security Scanner             ║
    ║──────────────────────────────────────────────║
    ║  Contact:                                    ║
    ║  Telegram: @alecss12                        ║
    ║  WhatsApp: +40732159658                     ║
    ╚══════════════════════════════════════════════╝
    """
    
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    for color in colors:
        print(color + banner + '\033[0m')
        time.sleep(0.2)
        print('\033[F' * (banner.count('\n') + 1))
    print('\033[96m' + banner + '\033[0m')

def scan_udp_port(target, port):
    """Scanează un port UDP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b"", (target, port))
        data, addr = sock.recvfrom(1024)
        print(f"\033[92m[+] Port UDP {port}: DESCHIS\033[0m")
        return True
    except socket.timeout:
        print(f"\033[91m[-] Port UDP {port}: ÎNCHIS/FILTRAT\033[0m")
        return False
    except Exception as e:
        print(f"\033[93m[?] Port UDP {port}: EROARE ({str(e)})\033[0m")
        return False
    finally:
        sock.close()

def get_service_version(target, port):
    """Încearcă să detecteze versiunea serviciului"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((target, port))
        sock.send(b"GET / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024)
        sock.close()
        return banner.decode('utf-8', errors='ignore').strip()
    except:
        return "Versiune necunoscută"

def detect_os(target):
    """Încearcă să detecteze sistemul de operare"""
    try:
        ttl = os.popen(f"ping -c 1 {target} 2>/dev/null | grep 'ttl=' | cut -d'=' -f2 | cut -d' ' -f1").read().strip()
        if ttl:
            ttl = int(ttl)
            if ttl <= 64:
                return "Linux/Unix"
            elif ttl <= 128:
                return "Windows"
            else:
                return "Cisco/Network Device"
        return "Necunoscut"
    except:
        return "Necunoscut"

def save_results(target, results, filename="scan_results.json"):
    """Salvează rezultatele scanării în format JSON"""
    data = {
        "target": target,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "open_ports": results,
        "os_detected": detect_os(target)
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n\033[92m[+] Rezultate salvate în {filename}\033[0m")

def scan_custom_range(target, start_port, end_port):
    """Scanează un interval personalizat de porturi"""
    custom_open_ports = []
    print(f"\n\033[94mScanare porturi {start_port}-{end_port}...\033[0m")
    
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                custom_open_ports.append(port)
                try:
                    service = socket.getservbyport(port)
                    print(f"\033[92m[+] Port {port} ({service}): DESCHIS\033[0m")
                except:
                    print(f"\033[92m[+] Port {port}: DESCHIS\033[0m")
            sock.close()
        except:
            pass
    
    return custom_open_ports

def main():
    print_banner()
    time.sleep(1)

    if len(sys.argv) < 2:
        print_rainbow_text("Mod de utilizare:")
        print("\033[93mpython3 port_scanner.py <ip_address> [opțiuni]\033[0m")
        print("\nOpțiuni disponibile:")
        print("  --udp              : Scanează și porturi UDP")
        print("  --version          : Detectează versiunile serviciilor")
        print("  --range start end  : Scanează un interval specific de porturi")
        print("  --save filename    : Salvează rezultatele în fișier")
        print("  --os              : Detectează sistemul de operare")
        print("\nExemplu: python3 port_scanner.py 192.168.1.1 --udp --version --save results.json")
        sys.exit()

    target = sys.argv[1]
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("\033[91m[-] Adresa IP/hostname invalid\033[0m")
        sys.exit()

    # Procesare opțiuni
    options = sys.argv[2:] if len(sys.argv) > 2 else []
    do_udp = "--udp" in options
    do_version = "--version" in options
    do_save = "--save" in options
    do_os = "--os" in options
    custom_range = "--range" in options

    # Banner cu informații
    print("\033[94m" + "═" * 50)
    print(f"⚡ Țintă: {target_ip}")
    if do_os:
        os_detected = detect_os(target_ip)
        print(f"💻 Sistem de operare detectat: {os_detected}")
    print(f"⏰ Scanare începută la: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("═" * 50 + "\033[0m")

    print("\033[95m[i] Legendă:")
    print("   [+] Verde: Port DESCHIS")
    print("   [-] Roșu: Port ÎNCHIS")
    print("   [?] Galben: Eroare la scanare\033[0m")
    print("\033[94m" + "═" * 50 + "\033[0m\n")

    # Pornire animație loading
    global stop_loading
    loading_thread = threading.Thread(target=animate_loading)
    loading_thread.daemon = True
    loading_thread.start()

    # Scanare TCP normală
    thread_list = []
    for _ in range(100):
        t = threading.Thread(target=get_threads)
        t.daemon = True
        t.start()
        thread_list.append(t)

    if custom_range and len(options) > options.index("--range") + 2:
        range_idx = options.index("--range")
        start_port = int(options[range_idx + 1])
        end_port = int(options[range_idx + 2])
    else:
        start_port = 1
        end_port = 1024

    start_time = time.time()

    try:
        # Scanare TCP
        for port in range(start_port, end_port + 1):
            queue.put((target_ip, port))

        queue.join()

        for _ in range(100):
            queue.put(None)
        for t in thread_list:
            t.join()

        # Scanare UDP dacă este solicitată
        if do_udp:
            print("\n\033[94m" + "═" * 50)
            print("🌊 Scanare porturi UDP...")
            print("═" * 50 + "\033[0m")
            common_udp_ports = [53, 67, 68, 69, 123, 161, 162, 514, 520]
            for port in common_udp_ports:
                scan_udp_port(target_ip, port)

        # Detectare versiuni dacă este solicitată
        if do_version and open_ports:
            print("\n\033[94m" + "═" * 50)
            print("🔍 Versiuni servicii detectate:")
            print("═" * 50 + "\033[0m")
            for port in open_ports:
                version = get_service_version(target_ip, port)
                if version != "Versiune necunoscută":
                    print(f"\033[92m[+] Port {port}: {version}\033[0m")

    except KeyboardInterrupt:
        stop_loading = True
        print("\n\033[91m[-] Scanare întreruptă de utilizator\033[0m")
        sys.exit()

    stop_loading = True
    end_time = time.time()
    total_time = end_time - start_time

    # Afișare rezultate
    print("\n\033[94m" + "═" * 50)
    print_rainbow_text("🎯 Rezultate scanare:")
    print("\033[94m" + "═" * 50 + "\033[0m")
    
    if open_ports:
        print("\033[92m🔓 Porturi deschise găsite:")
        for port in sorted(open_ports):
            try:
                service = socket.getservbyport(port)
                print(f"✨ Port {port}: {service}")
            except:
                print(f"✨ Port {port}: serviciu necunoscut")
    else:
        print("\033[93m🔒 Nu au fost găsite porturi deschise în intervalul scanat\033[0m")

    print(f"\n\033[94m⚡ Scanare completă în {total_time:.2f} secunde\033[0m")

    # Salvare rezultate dacă este solicitat
    if do_save:
        save_filename = next((opt for i, opt in enumerate(options) if options[i-1] == "--save"), "scan_results.json")
        save_results(target_ip, [{"port": p, "service": socket.getservbyport(p) if p in open_ports else "necunoscut"} for p in open_ports], save_filename)
    
    print("\n\033[95m" + "═" * 50)
    print("📱 Contact ALECS pentru mai multe tools:")
    print("   • Telegram: @alecss12")
    print("   • WhatsApp: +40732159658")
    print("═" * 50 + "\033[0m")

if __name__ == "__main__":
    main() 