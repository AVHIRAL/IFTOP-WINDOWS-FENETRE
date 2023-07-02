import psutil
import tkinter as tk
from tkinter import ttk

def get_network_connections():
    connections = psutil.net_connections()
    filtered_connections = []

    for conn in connections:
        if conn.status == 'ESTABLISHED':
            local_address = conn.laddr
            foreign_address = conn.raddr
            filtered_connections.append((local_address, foreign_address))

    return filtered_connections

def get_mac_address(ip_address):
    try:
        import getmac
        return getmac.get_mac_address(ip=ip_address)
    except ImportError:
        return 'Unknown'

def refresh():
    connections = get_network_connections()

    # Effacer les anciennes données
    tree.delete(*tree.get_children())

    for local_address, foreign_address in connections:
        local_ip, local_port = local_address
        foreign_ip, foreign_port = foreign_address

        local_mac = get_mac_address(local_ip)
        foreign_mac = get_mac_address(foreign_ip)

        tree.insert('', tk.END, values=(local_ip, local_port, local_mac, foreign_ip, foreign_port, foreign_mac))

    # Définir la largeur fixe pour chaque colonne
    tree.column('#0', width=100)  # colonne vide
    tree.column('Local IP', width=120)
    tree.column('Local Port', width=100)
    tree.column('Local MAC', width=150)
    tree.column('Foreign IP', width=120)
    tree.column('Foreign Port', width=100)
    tree.column('Foreign MAC', width=150)

    # Redimensionner les colonnes pour s'adapter au contenu
    for column in columns:
        tree.heading(column, text=column)

# Création de la fenêtre principale
window = tk.Tk()
window.title('IFTOP pour Windows')
window.geometry('800x600')

# Création d'un widget Treeview pour afficher les connexions
tree = ttk.Treeview(window, columns=('Local IP', 'Local Port', 'Local MAC', 'Foreign IP', 'Foreign Port', 'Foreign MAC'))
tree.pack(fill=tk.BOTH, expand=True)

# Définir les en-têtes de colonnes
columns = ('Local IP', 'Local Port', 'Local MAC', 'Foreign IP', 'Foreign Port', 'Foreign MAC')

# Définir les options de colonnes
for column in columns:
    tree.heading(column, text=column)

# Rafraîchir les connexions initiales
refresh()

# Fonction de rafraîchissement automatique
def auto_refresh():
    refresh()
    window.after(1000, auto_refresh)

# Lancer le rafraîchissement automatique
auto_refresh()

# Boucle principale de l'interface graphique
window.mainloop()
