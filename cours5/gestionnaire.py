"""
420-PR2-AG — Séance 5 — La logique métier

Règle absolue de l'atelier : AUCUN import tkinter dans ce fichier.
Ce module doit fonctionner, et se tester, sans la moindre interface.

Exécution directe :  python3 gestionnaire.py
(le bloc de test en bas de fichier vérifie les règles sans ouvrir de fenêtre)
"""


class ReservationInvalide(Exception):
    """Erreur métier : la réservation demandée ne peut pas être acceptée."""


class Salle:
    def __init__(self, numero, capacite, pavillon):
        self.__numero = numero
        self.__capacite = capacite
        self.__pavillon = pavillon

    def get_numero(self):
        return self.__numero

    def get_capacite(self):
        return self.__capacite

    def __str__(self):
        return f"{self.__numero} ({self.__capacite} places, {self.__pavillon})"


class Reservation:
    def __init__(self, salle, date, duree):
        self.salle = salle
        self.date = date
        self.duree = duree
        self.statut = "confirmée"

    def resume(self):
        return f"{self.salle.get_numero()} — {self.date} — {self.duree} min"


class GestionnaireReservations:
    """Contient les règles, les données et les exceptions. Ignore l'interface."""

    DUREE_MIN = 1
    DUREE_MAX = 240

    def __init__(self):
        self.salles = [
            Salle("A-101", 30, "Pavillon A"),
            Salle("B-204", 12, "Pavillon B"),
            Salle("C-010", 60, "Pavillon C"),
        ]
        self.reservations = []

    # ------------------------------------------------------------------
    # Règles métier
    # ------------------------------------------------------------------
    def trouver_salle(self, numero):
        for salle in self.salles:
            if salle.get_numero() == numero:
                return salle
        raise ReservationInvalide(f"Salle inconnue : {numero}")

    def est_libre(self, numero, date):
        return not any(r.salle.get_numero() == numero and r.date == date
                       for r in self.reservations)

    def reserver(self, numero, date, duree):
        """Retourne un message de confirmation, ou lève ReservationInvalide."""
        if not numero or not date:
            raise ReservationInvalide("La salle et la date sont obligatoires.")

        if not (self.DUREE_MIN <= duree <= self.DUREE_MAX):
            raise ReservationInvalide(
                f"La durée doit être comprise entre {self.DUREE_MIN} "
                f"et {self.DUREE_MAX} minutes.")

        salle = self.trouver_salle(numero)

        if not self.est_libre(numero, date):
            raise ReservationInvalide(
                f"La salle {numero} est déjà réservée le {date}.")

        reservation = Reservation(salle, date, duree)
        self.reservations.append(reservation)
        return reservation.resume()

    def annuler(self, indice):
        """Annule la réservation d'indice donné dans la liste."""
        if not 0 <= indice < len(self.reservations):
            raise ReservationInvalide("Aucune réservation sélectionnée.")
        return self.reservations.pop(indice)


# ----------------------------------------------------------------------
# Tests — aucune fenêtre n'est nécessaire, c'est tout l'intérêt
# ----------------------------------------------------------------------
if __name__ == "__main__":
    g = GestionnaireReservations()

    essais = [
        ("A-101", "2026-09-21", 60),    # correct
        ("", "2026-09-21", 60),         # salle manquante
        ("A-101", "2026-09-21", 300),   # durée trop longue
        ("Z-999", "2026-09-21", 60),    # salle inconnue
        ("A-101", "2026-09-21", 90),    # salle déjà réservée ce jour-là
        ("B-204", "2026-09-21", 45),    # correct
    ]

    for numero, date, duree in essais:
        try:
            message = g.reserver(numero, date, duree)
        except ReservationInvalide as e:
            print(f"Refusée  : {e}")
        else:
            print(f"Confirmée: {message}")

    print()
    print(f"{len(g.reservations)} réservation(s) enregistrée(s)")
