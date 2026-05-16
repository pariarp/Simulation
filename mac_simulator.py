import random
import heapq

class Station:
    """
    Représente une station du réseau avec sa file d'attente et son état de transmission.
    """
    def __init__(self, id_station, K):
        self.id = id_station
        self.K = K              # Capacité maximale de la file d'attente
        self.nb_paquets = 0     # Nombre de paquets actuellement dans la file
        self.etat_i = 1         # État initial pour le backoff (commence à 1)
        self.en_transmission = False
        self.en_backoff = False
        
class Simulateur:
    """
    Moteur de simulation à événements discrets pour le protocole MAC Exponential Backoff.
    """
    def __init__(self, N, K, lmbda, tau):
        # Paramètres du système
        self.N = N
        self.K = K
        self.lmbda = lmbda
        self.tau = tau
        
        # État du système
        self.horloge = 0.0
        self.stations = [Station(i, K) for i in range(N)]
        self.canal_occupe_par = []
        self.stations_en_collision = set()
        
        # L'échéancier (file de priorité)
        self.echeancier = []    
        
        # Statistiques
        self.n_succes = 0
        self.n_perdus = 0
        self.somme_clients = 0  # Intégrale du nombre de clients (Loi de Little)

        # Listes pour les courbes
        self.temps = []
        self.debits = []
        self.clients_moyens = []
        self.taux_pertes = []

    def inserer_evenement(self, date, type_evt, id_station):
        """Insère un événement dans l'échéancier en maintenant le tri chronologique."""
        heapq.heappush(self.echeancier, (date, type_evt, id_station))

    def initialisation(self):
        """Initialise le simulateur en programment la première arrivée pour chaque station."""
        for i in range(self.N):
            temps_premiere_arrivee = random.expovariate(self.lmbda)
            self.inserer_evenement(temps_premiere_arrivee, 'arrivee', i)

    def executer(self, temps_max):
        """Boucle principale de la simulation à événements discrets."""
        self.initialisation()

        while self.echeancier:
            date, type_evt, id_station = heapq.heappop(self.echeancier)

            if date > temps_max:
                break

            # Mise à jour de l'intégrale pour le calcul du nombre moyen de clients
            total = sum(s.nb_paquets for s in self.stations)
            self.somme_clients += total * (date - self.horloge)
            self.horloge = date

            self._enregistrer_stats()

            station = self.stations[id_station]

            # Routage de l'événement vers le gestionnaire approprié
            if type_evt == "arrivee":
                self._traiter_arrivee(station)
            elif type_evt == "debut_emission":
                self._traiter_debut_emission(station)
            elif type_evt == "fin_emission":
                self._traiter_fin_emission(station)
            elif type_evt == "fin_backoff":
                self._traiter_fin_backoff(station)

    def _enregistrer_stats(self):
        """Sauvegarde l'état actuel pour la génération des courbes temporelles."""
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

    def _traiter_arrivee(self, station):
        """
        Gère l'arrivée d'un paquet, son insertion en file d'attente
        et la programmation de l'arrivée suivante.
        """
        prochain_delai = random.expovariate(self.lmbda)
        self.inserer_evenement(self.horloge + prochain_delai, 'arrivee', station.id)

        if station.nb_paquets < self.K:
            station.nb_paquets += 1
            if not station.en_transmission and not station.en_backoff:
                self.inserer_evenement(self.horloge, 'debut_emission', station.id)
        else:
            self.n_perdus += 1

    def _traiter_debut_emission(self, station):
        """
        Marque le canal comme occupé par la station et planifie
        la fin de la transmission a t+1.
        """
        station.en_transmission = True
        self.canal_occupe_par.append(station.id)
        self.inserer_evenement(self.horloge + 1, "fin_emission", station.id)

    def _traiter_fin_emission(self, station):
        """
        Evalue l'état du cnal à la fin d'une transmission (succès ou collision).
        Applique l'algorithme d'exponential backoff en cas d'échec.
        """
        station.en_transmission = False
        self.canal_occupe_par.remove(station.id)

        # Détection de collision (synchrone ou simultanée)
        en_collision = len(self.canal_occupe_par) > 0 or station.id in self.stations_en_collision

        if not en_collision:
            # Succès
            self.n_succes += 1
            station.nb_paquets -= 1
            station.etat_i = 1

            if station.nb_paquets > 0:
                self.inserer_evenement(self.horloge, "debut_emission", station.id)
        else:
            # Collision
            self.stations_en_collision.discard(station.id) 
            
            for sid in self.canal_occupe_par:
                self.stations_en_collision.add(sid)

            # Calcul du délai exponentiel : Exp(1 / (2^i * tau))
            taux_backoff = 1 / ((2 ** station.etat_i) * self.tau)
            temps_backoff = random.expovariate(taux_backoff)
            station.etat_i += 1
            station.en_backoff = True

            self.inserer_evenement(self.horloge + temps_backoff, "fin_backoff", station.id)

    def _traiter_fin_backoff(self, station):
        """
        Relance une tentative d'émission à l'issue de la période d'attente
        si la file de la station n'est pas vide.
        """
        station.en_backoff = False

        if station.nb_paquets > 0:
            self.inserer_evenement(self.horloge, "debut_emission", station.id)

    def resultats_finaux(self, temps_max):
        """Calcule et retourne les métriques globales de la simulation"""
        return {
            "debit": self.n_succes / temps_max,
            "clients_moyens": self.somme_clients / temps_max,
            "taux_pertes": self.n_perdus / (self.n_succes + self.n_perdus) if self.n_succes + self.n_perdus > 0 else 0,
            "succes": self.n_succes,
            "perdus": self.n_perdus,
        }