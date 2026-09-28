"""
420-PR2-AG — Séance 5 — La vue (solution de référence de l'atelier)

La fenêtre ne fait que trois choses :
  1. lire les champs,
  2. appeler le gestionnaire,
  3. afficher le résultat ou l'erreur.

Aucune règle métier ici. Toutes les règles sont dans gestionnaire.py.

Exécution :  python3 fenetre.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from gestionnaire import GestionnaireReservations, ReservationInvalide


class FenetreReservation(tk.Tk):
    def __init__(self, gestionnaire):
        super().__init__()                        # héritage (séance 3)
        self.gestionnaire = gestionnaire          # association (séance 3)
        self.title("Réservation de salles")
        self.resizable(False, False)

        self.salle = tk.StringVar()
        self.date = tk.StringVar(value="2026-09-21")
        self.duree = tk.StringVar(value="60")

        self._construire()                        # méthode privée (séance 1)

    # ------------------------------------------------------------------
    # Construction de l'interface
    # ------------------------------------------------------------------
    def _construire(self):
        ttk.Label(self, text="Salle").grid(
            row=0, column=0, sticky="w", padx=8, pady=4)
        ttk.Combobox(
            self,
            textvariable=self.salle,
            state="readonly",
            values=[s.get_numero() for s in self.gestionnaire.salles]
        ).grid(row=0, column=1, sticky="we", padx=8, pady=4)

        ttk.Label(self, text="Date (AAAA-MM-JJ)").grid(
            row=1, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.date, width=24).grid(
            row=1, column=1, sticky="we", padx=8, pady=4)

        ttk.Label(self, text="Durée (minutes)").grid(
            row=2, column=0, sticky="w", padx=8, pady=4)
        ttk.Entry(self, textvariable=self.duree, width=24).grid(
            row=2, column=1, sticky="we", padx=8, pady=4)

        ttk.Button(self, text="Réserver", command=self.valider).grid(
            row=3, column=0, columnspan=2, sticky="we", padx=8, pady=8)

        self.liste = tk.Listbox(self, height=6, width=44)
        self.liste.grid(row=4, column=0, columnspan=2, padx=8, pady=4)

        ttk.Button(self, text="Annuler la sélection",
                   command=self.annuler_selection).grid(
            row=5, column=0, columnspan=2, sticky="we", padx=8, pady=(4, 12))

        self.columnconfigure(1, weight=1)

    # ------------------------------------------------------------------
    # Réactions aux actions de l'utilisateur
    # ------------------------------------------------------------------
    def valider(self):
        try:
            message = self.gestionnaire.reserver(
                self.salle.get(),
                self.date.get().strip(),
                int(self.duree.get()))
        except ReservationInvalide as e:           # règle métier violée
            messagebox.showwarning("Réservation refusée", str(e))
        except ValueError:                         # « soixante » au lieu de 60
            messagebox.showwarning("Réservation refusée",
                                   "La durée doit être un nombre entier.")
        else:                                      # aucun problème
            self.liste.insert(tk.END, message)
            self._vider_champs()

    def annuler_selection(self):
        selection = self.liste.curselection()
        try:
            if not selection:
                raise ReservationInvalide("Aucune réservation sélectionnée.")
            indice = selection[0]
            self.gestionnaire.annuler(indice)
        except ReservationInvalide as e:
            messagebox.showwarning("Annulation impossible", str(e))
        else:
            self.liste.delete(indice)

    def _vider_champs(self):
        self.salle.set("")
        self.duree.set("60")


if __name__ == "__main__":
    # Le gestionnaire est créé à l'extérieur, puis injecté dans la fenêtre.
    FenetreReservation(GestionnaireReservations()).mainloop()
