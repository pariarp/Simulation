import random
import heapq  # Très utile pour gérer l'échéancier (la file d'événements) par ordre chronologique

class Station:
    def __init__(self, id_station, K):
        self.id = id_station
        self.K = K              # Capacité maximale de la file d'attente
        self.nb_paquets = 0     # Nombre de paquets actuellement dans la file
        self.etat_i = 1         # État initial pour le backoff (commence à 1)
        self.en_transmission = False # Indique si la station est en train d'émettre
        
class Simulateur:
    def __init__(self, N, K, lmbda, tau):
        # Paramètres du système
        self.N = N              # Nombre de stations
        self.K = K              # Capacité de la file
        self.lmbda = lmbda      # Taux d'arrivée des paquets (lambda)
        self.tau = tau          # Paramètre de base pour le backoff (tau)
        
        # État du système
        self.horloge = 0.0      # Temps t de la simulation
        self.stations = [Station(i, K) for i in range(N)] # Création des N stations
        self.canal_occupe_par = [] # Liste des IDs des stations en train d'émettre (pour détecter les collisions)
        
        # L'échéancier (file de priorité)
        self.echeancier = []    
        
        # Statistiques pour les courbes demandées à la fin
        self.n_succes = 0       # Nombre de paquets transmis avec succès
        self.n_perdus = 0       # Nombre de paquets rejetés (file pleine)
        self.somme_clients = 0  # Pour calculer le nombre moyen de clients

    def inserer_evenement(self, date, type_evt, id_station):
        # heapq permet de garder la liste triée par date automatiquement
        heapq.heappush(self.echeancier, (date, type_evt, id_station))

    def executer(self, temps_max):
        # C'est ici qu'on mettra la boucle principale du simulateur plus tard !
        pass

# --- Zone de test ---
if __name__ == "__main__":
    # On crée un simulateur avec des valeurs arbitraires pour tester
    sim = Simulateur(N=5, K=10, lmbda=0.1, tau=0.5)
    print(f"Simulateur initialisé avec {sim.N} stations.")

"""
Ce qu'il faut retenir de ce code :

    Station : Chaque station sait combien de paquets elle a (nb_paquets), son état de backoff (etat_i) et si elle a le droit d'émettre.

    Simulateur : Il contient les paramètres globaux et crée les stations.

    heapq : C'est une bibliothèque standard très pratique en simulation. Elle permet d'insérer des événements et de toujours récupérer celui qui a la date la plus petite (donc le plus proche dans le temps).
"""