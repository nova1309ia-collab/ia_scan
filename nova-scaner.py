from scapy.all import sniff, ARP, Ether, srp, conf, IP, TCP
import ipaddress, threading, time, os, subprocess, sys, json
from datetime import datetime

# ========================
# CONFIG VERSION LIMITÉE
# ========================
SCAN_MASK        = 22
MAX_DEVICES_PER_SCAN = 7
MAX_LAUNCHES_PER_DAY = 5

mac_uniques = set()

# ========================
# Fichier de log sur le Bureau
# ========================
def get_log_file():
    try:
        username = os.environ.get('USERNAME') or os.environ.get('USER')
        desktop = os.path.join("C:\\Users", username, "Desktop")
        log_file = os.path.join(desktop, "macs_detectees.txt")
        os.makedirs(desktop, exist_ok=True)
        return log_file
    except:
        return "macs_detectees.txt"

LOG_FILE = get_log_file()

# ========================
# Limite d'utilisation
# ========================
def check_and_update_usage():
    try:
        usage_file = os.path.join(os.path.dirname(LOG_FILE), "usage_limit.json")
        today = datetime.now().date().isoformat()
        
        data = {"date": today, "count": 0}
        if os.path.exists(usage_file):
            with open(usage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        
        if data.get("date") != today:
            data = {"date": today, "count": 0}
        
        data["count"] += 1
        
        if data["count"] > MAX_LAUNCHES_PER_DAY:
            print("❌ LIMITE ATTEINTE : 5 utilisations par jour maximum.")
            input("\nAppuyez sur Entrée pour fermer...")
            sys.exit(1)
        
        with open(usage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print(f"🔢 Utilisation aujourd'hui : {data['count']}/{MAX_LAUNCHES_PER_DAY}")
    except:
        pass

# ========================
# Sauvegarde MAC
# ========================
def save_mac(mac, ip, mode):
    if len(mac_uniques) >= MAX_DEVICES_PER_SCAN:
        return
    if not mac or "??" in mac or mac in mac_uniques:
        return
    
    mac_uniques.add(mac)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{ip} | {mac} | {mode} | {datetime.now().strftime('%H:%M:%S')}\n")
        print(f"✅ [{len(mac_uniques)}/{MAX_DEVICES_PER_SCAN}] {ip} | {mac} | {mode}")
    except:
        pass

def is_windows_valid_mac(mac):
    try:
        first_byte = int(mac.split(":")[0], 16)
        return (first_byte & 1) == 0 and (first_byte & 2) != 0
    except:
        return False

# ========================
# Scan léger optimisé pour Hotspot
# ========================
def perform_scan(network_range):
    print("🔎 Lancement du scan ARP (mode Hotspot)...\n")
    
    try:
        # Scan ARP principal
        arp_req = ARP(pdst=network_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        answered, _ = srp(broadcast / arp_req, timeout=6, verbose=False, retry=2)
        
        for _, received in answered:
            mac = received.hwsrc
            ip = received.psrc
            if is_windows_valid_mac(mac):
                save_mac(mac, ip, "ARP Actif")
                if len(mac_uniques) >= MAX_DEVICES_PER_SCAN:
                    break
                    
    except Exception as e:
        print(f"⚠️ Erreur scan ARP : {e}")

    # Scan complémentaire avec ping + ARP
    try:
        print("🔎 Scan complémentaire avec Ping...")
        net = ipaddress.ip_network(network_range, strict=False)
        for ip in list(net.hosts())[:50]:   # Limite pour ne pas être trop agressif
            if len(mac_uniques) >= MAX_DEVICES_PER_SCAN:
                break
            try:
                subprocess.call(["ping", "-n", "1", "-w", "800", str(ip)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
    except:
        pass

    print(f"\n🏁 Scan terminé ! {len(mac_uniques)} appareil(s) détecté(s)")

# ========================
# MAIN
# ========================
def main():
    print("="*75)
    print("🚀 Argent Smart - Version Limitée (Hotspot CI)")
    print("="*75)
    
    check_and_update_usage()
    
    try:
        gateway = conf.route.route("0.0.0.0")[2]
        print(f"✅ Passerelle : {gateway}")
    except:
        print("❌ Impossible de détecter la passerelle.")
        input("\nAppuyez sur Entrée...")
        return

    try:
        network_range = str(ipaddress.ip_interface(f"{gateway}/{SCAN_MASK}").network)
        print(f"✅ Plage IP : {network_range}")
    except:
        network_range = "10.10.8.0/22"
        print(f"✅ Plage IP : {network_range} (par défaut)")

    print(f"📁 Log : {LOG_FILE}")
    print("🚫 Aucun contact avec http://hotspot.ci/status\n")

    perform_scan(network_range)

    print("\n" + "="*60)
    print("✅ Programme terminé.")
    print(f"📊 Total détecté : {len(mac_uniques)}/{MAX_DEVICES_PER_SCAN}")
    input("\nAppuyez sur Entrée pour fermer la fenêtre...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        input("\nAppuyez sur Entrée pour fermer...")