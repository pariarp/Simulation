import random
import heapq  # Très utile pour gérer l'échéancier (la file d'événements) par ordre chronologique

class Station:
    def __init__(self, id_station, K):
        self.id = id_station
        self.K = K              # Capacité maximale de la file d'attente
        self.nb_paquets = 0     # Nombre de paquets actuellement dans la file
        self.etat_i = 1         # État initial pour le backoff (commence à 1)
        self.en_transmission = False # Indique si la station est en train d'émettre
        self.en_backoff = False # Indique si la station est en backoff 
        
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
        self.stations_en_collision = set() # Ensemble des stations impliquées dans une collision
        
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
        """
        Boucle principale du simulateur.
        1. Initialise une première arrivée pour chaque station
        2. Extrait et traite les événements dans l'ordre chronologique
        3. S'arrête quand l'horloge dépasse temps_max
        """
        # Planifier la première arrivée pour chaque station
        for station in self.stations:
            date = random.expovariate(self.lmbda)
            self.inserer_evenement(date, "arrivee", station.id)

        # Boucle principale
        while self.echeancier:
            date, type_evt, id_station = heapq.heappop(self.echeancier)

            if date > temps_max:
                break

            # Mise à jour de la somme pour le nombre moyen de clients
            total = sum(s.nb_paquets for s in self.stations)
            self.somme_clients += total * (date - self.horloge)
            self.horloge = date

            station = self.stations[id_station]

            # Dispatcher vers la bonne fonction
            if type_evt == "arrivee":
                self._traiter_arrivee(station)
            elif type_evt == "debut_emission":
                self._traiter_debut_emission(station)
            elif type_evt == "fin_emission":
                self._traiter_fin_emission(station)
            elif type_evt == "fin_backoff":
                self._traiter_fin_backoff(station)
    
    def _traiter_arrivee(self, station):
        """
        Un paquet arrive à la station.
        - Planifie la prochaine arrivée (Exp(λ))
        - Si file pleine → paquet perdu
        - Sinon → ajout en file, et émission si station libre
        """
        # Planifier la prochaine arrivée sur cette station
        prochaine = self.horloge + random.expovariate(self.lmbda)
        self.inserer_evenement(prochaine, "arrivee", station.id)

        # Si la file est pleine → paquet perdu
        if station.nb_paquets >= self.K:
            self.n_perdus += 1
            return

        # Sinon on ajoute le paquet dans la file
        station.nb_paquets += 1

        # Si la station est libre, elle peut émettre tout de suite
        if not station.en_transmission and not station.en_backoff:
            self.inserer_evenement(self.horloge, "debut_emission", station.id)
    def _traiter_debut_emission(self, station):
        """
        La station commence à émettre.
        - Marque la station comme émettrice
        - Planifie la fin de l'émission dans 1 unité de temps
        """
        # La station commence à émettre
        station.en_transmission = True
        self.canal_occupe_par.append(station.id)

        # La fin de l'émission est dans exactement 1 unité de temps
        self.inserer_evenement(self.horloge + 1, "fin_emission", station.id)

    def _traiter_fin_emission(self, station):
        """
        L'émission se termine.
        - Si aucune autre station n'émettait en même temps → SUCCÈS
        - Sinon → COLLISION, calcul du backoff
        """
        station.en_transmission = False
        self.canal_occupe_par.remove(station.id)

        # Y avait-il d'autres stations qui émettaient en même temps ?
        # On vérifie si cette station est dans le set des stations en collision
        en_collision = len(self.canal_occupe_par) > 0 or station.id in self.stations_en_collision

        if not en_collision:
            # SUCCÈS
            self.n_succes += 1
            station.nb_paquets -= 1
            station.etat_i = 1  # Reset de l'état

            # S'il reste des paquets, on planifie la prochaine émission
            if station.nb_paquets > 0:
                self.inserer_evenement(self.horloge, "debut_emission", station.id)
        else:
            # COLLISION
            self.stations_en_collision.discard(station.id)
            
            # Marquer toutes les stations encore en train d'émettre comme en collision
            for sid in self.canal_occupe_par:
                self.stations_en_collision.add(sid)

            # Calculer le temps de backoff : Exp(1 / (2^i * tau))
            taux_backoff = 1 / ((2 ** station.etat_i) * self.tau)
            temps_backoff = random.expovariate(taux_backoff)
            station.etat_i += 1
            station.en_backoff = True

            self.inserer_evenement(self.horloge + temps_backoff, "fin_backoff", station.id)

    def _traiter_fin_backoff(self, station):
        """
        Le délai de backoff est terminé.
        - Si des paquets attendent → relancer une émission
        """
        station.en_backoff = False

        # Si la station a encore des paquets à envoyer → réessayer
        if station.nb_paquets > 0:
            self.inserer_evenement(self.horloge, "debut_emission", station.id)

# --- Zone de test ---
if __name__ == "__main__":
    sim = Simulateur(N=5, K=10, lmbda=0.3, tau=1.0)
    sim.executer(temps_max=1000)

    print(f"Simulateur initialisé avec {sim.N} stations.")
    print(f"Paquets transmis avec succès : {sim.n_succes}")
    print(f"Paquets perdus (file pleine)  : {sim.n_perdus}")
    print(f"Débit moyen n(t)/t            : {sim.n_succes / 1000:.4f}")
    print(f"Nombre moyen de clients       : {sim.somme_clients / 1000:.4f}")

"""
Ce qu'il faut retenir de ce code :

    Station : Chaque station sait combien de paquets elle a (nb_paquets), son état de backoff (etat_i) et si elle a le droit d'émettre.

    Simulateur : Il contient les paramètres globaux et crée les stations.

    heapq : C'est une bibliothèque standard très pratique en simulation. Elle permet d'insérer des événements et de toujours récupérer celui qui a la date la plus petite (donc le plus proche dans le temps).
"""