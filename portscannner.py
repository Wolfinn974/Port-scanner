import socket
import threading
from queue import Queue
from datetime import datetime

# 🔹 Demander l'IP ou le domaine à scanner et la plage de ports à analyser

target = input("Entrez l'adresse IP ou le domaine à scanner : ")
start_port = int(input("Entrez le port de début : "))
end_port = int(input("Entrez le port de fin : "))

queue = Queue()
open_ports = []

# 🔹 Définir un timeout pour éviter les blocages
socket.setdefaulttimeout(0.5)

def portscan(port):
    try:
        sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((target, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "Inconnu"
            open_ports.append((port, service))
        sock.close()
    except:
        pass # Ignorer les erreurs pour éviter l'arrêt du programme
    
def fill_queue(port_list):
    """Ajoute la liste des ports à scanner dans la file d'attente."""
    for port in port_list:
        queue.put(port)

def worker():
    """Exécute les scans de ports en parallèle avec les threads."""
    while not queue.empty():
        port =  queue.get()
        portscan(port)

start_time = datetime.now()

port_list = range(start_port,end_port + 1)
fill_queue(port_list)

thread_count = 50
thread_list = []

# 🔹 Lancer les threads pour exécuter les scans
for t in range(thread_count):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)
    thread.start()

# 🔹 Attendre la fin de tous les threads
for thread in thread_list:
    thread.join()

end_time = datetime.now()
print("\nScan terminé en :", end_time - start_time)

# 🔹 Afficher les ports ouverts et les services détectés
if open_ports:
    print("\nPorts ouverts et services détectés :")
    for port, service in open_ports:
        print(f"Port {port} : {service}")
else:
    print("Aucun port ouvert trouvé.")