"""
420-PR2-AG — Séance 5 — Squelette de départ (micro-exercice puis atelier)

Complétez les sections marquées « À FAIRE ».
Le fichier gestionnaire.py est fourni et ne doit PAS être modifié pour le
micro-exercice ; vous y ajouterez vos propres règles à l'atelier.

Exécution :  python3 fenetre_depart.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from gestionnaire import GestionnaireReservations, ReservationInvalide


class FenetreReservation(tk.Tk):
    def __init__(self, gestionnaire):
        super().__init__()
        self.gestionnaire = gestionnaire
        self.title("Réservation de salles")

        # À FAIRE (micro-exercice, étape 4)
        # Créez trois StringVar : self.salle, self.date et self.duree.
        # self.duree doit valoir "60" au départ.

        self._construire()

    def _construire(self):
        # ------------------------------------------------------------------
        # À FAIRE (micro-exercice, étapes 1 à 6)
        #
        #  ligne 0 : libellé « Salle »          + Combobox alimenté par
        #                                         self.gestionnaire.salles
        #  ligne 1 : libellé « Date »           + Entry
        #  ligne 2 : libellé « Durée (minutes)» + Entry
        #  ligne 3 : bouton « Réserver », columnspan=2, command=self.valider
        #  ligne 4 : self.liste = tk.Listbox(self, height=6, width=44)
        #
        #  Rappels :
        #   - libellés en colonne 0 avec sticky="w"
        #   - champs en colonne 1
        #   - padx=8, pady=4 sur chaque widget
        #   - un seul gestionnaire de disposition : grid partout, jamais pack
        # ------------------------------------------------------------------
        pass

    def valider(self):
        # ------------------------------------------------------------------
        # À FAIRE (atelier)
        #
        #  try:
        #      appeler self.gestionnaire.reserver(...) avec les trois champs
        #  except ReservationInvalide as e:
        #      messagebox.showwarning(...)   -> règle métier violée
        #  except ValueError:
        #      messagebox.showwarning(...)   -> la durée n'est pas un nombre
        #  else:
        #      insérer le message dans self.liste, puis vider les champs
        #
        #  AUCUNE règle métier ici : pas de if sur la durée, pas de recherche
        #  de doublon. Tout cela vit dans gestionnaire.py.
        # ------------------------------------------------------------------
        pass

    def annuler_selection(self):
        # À FAIRE (atelier, étape 5)
        # Récupérer self.liste.curselection(), appeler self.gestionnaire.annuler(),
        # puis retirer la ligne de la Listbox.
        pass


if __name__ == "__main__":
    FenetreReservation(GestionnaireReservations()).mainloop()
