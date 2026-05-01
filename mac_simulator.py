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

    def initialisation(self):
        # On programme la première arrivée de paquet pour CHAQUE station
        for i in range(self.N):
            # TIrage aléatoire selon une loi exponentielle
            temps_premiere_arrivee = random.expovariate(self.lmbda)

            # On insère l'événement dans l'écheancier
            # Format : (date, type_evenement, id_station)
            self.inserer_evenement(temps_premiere_arrivee, 'ARRIVEE', i)

    def executer(self, temps_max):
        self.initialisation() # On amorce la pompe

        # Boucle principale : on tourne tant qu'il y a des événements ET qu'on a pas dépassé le temps max
        while self.echeancier and self.horloge < temps_max:
            # Onextrait l'événement le plus proche dans le temps
            date_evt, type_evt, id_station = heapq.heappop(self.echeancier)

            # On met à jour l'horloge
            self.horloge = date_evt

            # Plus tard, on appellera les bonnes fonctions selon le type d'événement
            if type_evt == 'ARRIVEE':
                print(f"[{self.horloge:.2f}] ARRIVEE d'un paquet à la station {id_station}")
                self.traiter_arrivee(id_station)
            elif type_evt == 'DEBUT_TX':
                pass # self.traiter_debut_tx(id_station)
            elif type_evt == 'FIN_TX':
                pass # self.traiter_fin_tx(id_station)
    
    def traiter_arrivee(self, id_station):
        station = self.stations[id_station]

        # Programmer l'arrivée du PROCHAIN paquet pour cette station
        prochain_delai = random.expovariate(self.lmbda)
        self.inserer_evenement(self.horloge + prochain_delai, 'ARRIVEE', id_station)

        # Gérer la file d'attente
        if station.nb_paquets < self.K:
            # Il y a de la place, on ajoute le paquet dans le file
            station.nb_paquets += 1
            print(f" -> Paquet accepté (File : {station.nb_paquets}/{self.K})")

            # Tenter d'émettre si la station était inactive
            if station.nb_paquets == 1 and not station.en_transmission:
                print(f" -> station {id_station} tente d'émettre immédiatement.")
                self.inserer_evenement(self.horloge, 'DEBUT_TX', id_station)
        else:
            # La file est pleine, le paquet est perdu
            self.n_perdus += 1
            print(f" -> Paquet PERDU (File pleine !)")

# --- Zone de test ---
if __name__ == "__main__":
    # On crée un simulateur avec des valeurs arbitraires pour tester
    sim = Simulateur(N=5, K=10, lmbda=0.1, tau=0.5)
    print(f"Simulateur initialisé avec {sim.N} stations.")
    sim.executer(50)

"""
Ce qu'il faut retenir de ce code :

    Station : Chaque station sait combien de paquets elle a (nb_paquets), son état de backoff (etat_i) et si elle a le droit d'émettre.

    Simulateur : Il contient les paramètres globaux et crée les stations.

    heapq : C'est une bibliothèque standard très pratique en simulation. Elle permet d'insérer des événements et de toujours récupérer celui qui a la date la plus petite (donc le plus proche dans le temps).
"""