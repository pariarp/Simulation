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

        # Listes pour les courbes
        self.temps = []          # Liste des temps pour les courbes
        self.debits = []         # Liste des débits pour les courbes
        self.clients_moyens = [] # Liste du nombre moyen de clients pour les courbes
        self.taux_pertes = []    # Liste des taux de pertes pour les courbes

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
            self.inserer_evenement(temps_premiere_arrivee, 'arrivee', i)

    def executer(self, temps_max):
        self.initialisation() # On amorce la pompe

        # Boucle principale
        while self.echeancier:
            date, type_evt, id_station = heapq.heappop(self.echeancier)

            if date > temps_max:
                break

            # Mise à jour de la somme pour le nombre moyen de clients
            total = sum(s.nb_paquets for s in self.stations)
            self.somme_clients += total * (date - self.horloge) # Intégration du nombre de clients sur le temps, pour calculer la moyenne à la fin, aire sous la courbe 
            self.horloge = date # Avance l'horloge au moment de l'événement

            self._enregistrer_stats() # Enregistre les statistiques pour les courbes à chaque événement

            station = self.stations[id_station]

            # Dispatcher vers la bonne fonction
            if type_evt == "arrivee":
                self._traiter_arrivee(station) # Traite l'arrivée d'un paquet à la station
            elif type_evt == "debut_emission":
                self._traiter_debut_emission(station) #la station commence à envoyer son paquet
            elif type_evt == "fin_emission":
                self._traiter_fin_emission(station) # la station termine d'envoyer son paquet, on vérifie s'il y a eu collision ou pas
            elif type_evt == "fin_backoff":
                self._traiter_fin_backoff(station) # le délai de backoff est terminé, on peut réessayer d'envoyer le paquet s'il en reste

    def _enregistrer_stats(self):
        if self.horloge == 0:
            return  # Éviter la division par zéro
        
        self.temps.append(self.horloge)
        self.debits.append(self.n_succes / self.horloge)
        self.clients_moyens.append(self.somme_clients / self.horloge)

        total_observe = self.n_succes + self.n_perdus
        if total_observe > 0:
            self.taux_pertes.append(self.n_perdus / total_observe)
        else:
            self.taux_pertes.append(0)
    
    # --- Fonctions de traitement des événements ---
    # Le préfixe _ indique qu’une méthode est interne à la classe et ne doit pas être utilisée en dehors du simulateur.
    def _traiter_arrivee(self, station):
        """
        Traite l'arrivée d'un paquet à la station.
         - Programme l'arrivée du prochain paquet pour cette station
         - Si la file n'est pas pleine, ajoute le paquet et tente d'émettre
         - Sinon, le paquet est perdu
        """
        # Programmer l'arrivée du PROCHAIN paquet pour cette station
        prochain_delai = random.expovariate(self.lmbda)
        self.inserer_evenement(self.horloge + prochain_delai, 'arrivee', station.id)

        # Gérer la file d'attente
        if station.nb_paquets < self.K:
            # Il y a de la place, on ajoute le paquet dans la file
            station.nb_paquets += 1

            # Tenter d'émettre si la station était inactive
            if not station.en_transmission and not station.en_backoff:
                self.inserer_evenement(self.horloge, 'debut_emission', station.id)
        else:
            # La file est pleine, le paquet est perdu
            self.n_perdus += 1

    def _traiter_debut_emission(self, station):
        """
        La station commence à émettre.
        - Marque la station comme émettrice
        - Ajoute la station à la liste des stations en transmission, pour détecter les collisions
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
            self.stations_en_collision.discard(station.id) # Retire la station de l'ensemble des stations en collision 
            
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


    def resultats_finaux(self, temps_max):
        return {
            "debit": self.n_succes / temps_max,
            "clients_moyens": self.somme_clients / temps_max,
            "taux_pertes": self.n_perdus / (self.n_succes + self.n_perdus) if self.n_succes + self.n_perdus > 0 else 0,
            "succes": self.n_succes,
            "perdus": self.n_perdus,
        }

"""
Ce qu'il faut retenir de ce code :

    Station : Chaque station sait combien de paquets elle a (nb_paquets), son état de backoff (etat_i) et si elle a le droit d'émettre.

    Simulateur : Il contient les paramètres globaux et crée les stations.

    heapq : C'est une bibliothèque standard très pratique en simulation. Elle permet d'insérer des événements et de toujours récupérer celui qui a la date la plus petite (donc le plus proche dans le temps).
"""