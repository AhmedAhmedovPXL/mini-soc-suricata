#!/usr/bin/env python3
"""
autoblock_reset.py
------------------
Monitors Suricata fast.log for ET SCAN alerts and temporarily blocks
the attacker IP via iptables. After BLOCK_TIME seconds, the IP is
automatically unblocked.

Only processes NEW log entries since the last check — no re-blocking loop.

Usage:
    sudo python3 autoblock_reset.py

Requirements:
    - Suricata running and logging to /var/log/suricata/fast.log
    - Root privileges (for iptables)
"""

import re             # voor regex-matching van IPv4-adressen
import subprocess     # om iptables-commando's uit te voeren
import time           # voor sleep en countdown

# === Configuratie ===
LOG_FILE = "/var/log/suricata/fast.log"   # standaard locatie van Suricata fast-log
BLOCK_TIME = 60                            # blokkeerduur in seconden (kort gehouden voor testen)

# === Globale state ===
blocked_ips = set()   # houdt bij welke IPs momenteel geblokkeerd zijn (voorkomt dubbele regels)
last_line = 0         # cursor: tot welke regel we de log al gelezen hebben


def extract_new_ips():
    """Read only new lines from fast.log since last check."""
    global last_line
    ips = set()
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
        new_lines = lines[last_line:]    # enkel regels vanaf de vorige cursor-positie
        last_line = len(lines)           # cursor updaten naar het einde van het bestand
        for line in new_lines:
            if "ET SCAN" in line:                                # filter: enkel scan-alerts
                match = re.findall(r'\d+\.\d+\.\d+\.\d+', line)  # zoek alle IPv4-adressen in de regel
                if match:
                    ips.add(match[0])                            # eerste IP = source IP (de aanvaller)
    return ips


def countdown(seconds, ip):
    """Show a countdown timer in the terminal."""
    for i in range(seconds, 0, -1):
        # end="\r" zorgt dat dezelfde regel overschreven wordt (live countdown effect)
        print(f"[{ip}] Unblock in: {i}s", end="\r")
        time.sleep(1)
    print()   # nieuwe regel zodat volgende output niet over de countdown plakt


def block_ip(ip):
    """Block an IP, wait BLOCK_TIME seconds, then unblock it."""
    if ip in blocked_ips:    # IP staat al in iptables, niet opnieuw toevoegen
        return
    print(f"[+] Blocking {ip}")
    # -A INPUT = regel toevoegen aan INPUT chain (inkomend verkeer)
    # -s <ip>  = match op source IP
    # -j DROP  = pakket stilletjes droppen (geen reply naar attacker)
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
    blocked_ips.add(ip)

    countdown(BLOCK_TIME, ip)   # wacht BLOCK_TIME seconden met visuele aftelling

    print(f"[-] Unblocking {ip}")
    # -D INPUT = exact dezelfde regel weer verwijderen, IP mag terug verbinden
    subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"])
    blocked_ips.remove(ip)


def main():
    print("[*] Monitoring started...")
    while True:
        ips = extract_new_ips()       # haal nieuwe verdachte IPs op
        for ip in ips:
            block_ip(ip)              # blokkeer + auto-unblock na timer
        time.sleep(5)                 # poll-interval: elke 5 seconden opnieuw checken


if __name__ == "__main__":
    main()

