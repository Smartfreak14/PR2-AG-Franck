"""
420-PR2-AG — Séance 6 — Micro-exercice 2 (12 minutes)

« Un formulaire d'inscription à un atelier reçoit quatre champs :
  - un matricule : 7 chiffres
  - un courriel  : du domaine grasset.qc.ca
  - un niveau    : débutant, intermédiaire ou avancé
  - un nombre de places : entre 1 et 4 »

Règles du jeu :
  - chaque validation est une LISTE BLANCHE : expression régulière, ensemble
    de valeurs autorisées, ou intervalle numérique ;
  - la validation a lieu DANS le constructeur : un objet ne doit jamais
    exister dans un état invalide ;
  - chaque message dit quoi corriger, sans révéler d'information interne.

Exécution :  python3 inscription_depart.py
"""

import re


class DonneeInvalide(Exception):
    """Toutes les erreurs de validation du module d'inscription."""


# À FAIRE — déclarez ici vos listes blanches
# MATRICULE = re.compile(r"...")
# COURRIEL  = re.compile(r"...")
# NIVEAUX   = {...}
# PLACES_MIN, PLACES_MAX = 1, 4


class Inscription:
    def __init__(self, matricule, courriel, niveau, places):
        # À FAIRE — étape 1
        # Validez les quatre champs AVANT d'affecter quoi que ce soit.
        # Chaque règle invalide lève une DonneeInvalide avec un message utile.
        #
        # Rappel du piège : re.match s'arrête au premier caractère non conforme.
        # Utilisez re.fullmatch pour exiger que TOUTE la chaîne corresponde.
        pass

    def resume(self):
        # À FAIRE — retournez une phrase décrivant l'inscription
        pass


# ----------------------------------------------------------------------
# Jeu de tests — complétez-le (étape 4 : 4 saisies valides, 6 invalides)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    valides = [
        ("2026001", "ana@grasset.qc.ca", "débutant", 1),
        # À FAIRE — trois autres saisies valides
    ]

    invalides = [
        ("20260", "ana@grasset.qc.ca", "débutant", 1),          # matricule court
        # À FAIRE — cinq autres saisies invalides, au moins une par champ,
        #           dont "2026001 " avec un espace final (étape bonus)
    ]

    for essai in valides + invalides:
        try:
            inscription = Inscription(*essai)
        except DonneeInvalide as e:
            print(f"Refusée  : {essai}  ->  {e}")
        else:
            print(f"Acceptée : {inscription.resume()}")
