"""
420-PR2-AG — Séance 6 — Micro-exercice 2 : CORRIGÉ

Quatre validations, quatre listes blanches. Aucune liste noire.

Point clé de l'étape bonus :
  re.match(r"\\d{7}", "2026001 ")      -> correspond (l'espace est ignoré)
  re.fullmatch(r"\\d{7}", "2026001 ")  -> ne correspond pas
Utiliser match au lieu de fullmatch est une source classique de validation
contournée : la donnée passe le contrôle, puis un espace ou un caractère
supplémentaire se retrouve dans la base ou dans une requête.

Exécution :  python3 inscription_corrige.py
"""

import re


class DonneeInvalide(Exception):
    """Toutes les erreurs de validation du module d'inscription."""


# --- Listes blanches : on décrit ce qui est permis, jamais ce qui est interdit
MATRICULE = re.compile(r"\d{7}")
COURRIEL = re.compile(r"[a-z0-9._-]+@grasset\.qc\.ca", re.IGNORECASE)
NIVEAUX = {"débutant", "intermédiaire", "avancé"}
PLACES_MIN, PLACES_MAX = 1, 4


class Inscription:
    def __init__(self, matricule, courriel, niveau, places):
        # 1. Matricule
        if not isinstance(matricule, str) or not MATRICULE.fullmatch(matricule):
            raise DonneeInvalide("Matricule : 7 chiffres attendus.")

        # 2. Courriel
        if not isinstance(courriel, str) or not COURRIEL.fullmatch(courriel):
            raise DonneeInvalide(
                "Courriel : une adresse du domaine grasset.qc.ca est attendue.")

        # 3. Niveau
        if niveau not in NIVEAUX:
            raise DonneeInvalide(
                "Niveau : débutant, intermédiaire ou avancé.")

        # 4. Nombre de places
        if not isinstance(places, int) or isinstance(places, bool):
            raise DonneeInvalide("Places : un nombre entier est attendu.")
        if not PLACES_MIN <= places <= PLACES_MAX:
            raise DonneeInvalide(
                f"Places : entre {PLACES_MIN} et {PLACES_MAX}.")

        # Les affectations n'ont lieu qu'une fois tout validé :
        # l'objet ne peut pas exister dans un état invalide.
        self.__matricule = matricule
        self.__courriel = courriel.lower()
        self.__niveau = niveau
        self.__places = places

    def resume(self):
        return (f"{self.__matricule} — {self.__courriel} — "
                f"{self.__niveau} — {self.__places} place(s)")


if __name__ == "__main__":
    valides = [
        ("2026001", "ana@grasset.qc.ca", "débutant", 1),
        ("2026002", "Luis.Ramirez@Grasset.qc.ca", "avancé", 4),
        ("2026003", "carla_b@grasset.qc.ca", "intermédiaire", 2),
        ("2026004", "d-nguyen@grasset.qc.ca", "débutant", 3),
    ]

    invalides = [
        ("20260", "ana@grasset.qc.ca", "débutant", 1),          # trop court
        ("2026001 ", "ana@grasset.qc.ca", "débutant", 1),       # espace final
        ("2026001", "ana@gmail.com", "débutant", 1),            # mauvais domaine
        ("2026001", "ana@grasset.qc.ca", "expert", 1),          # niveau inconnu
        ("2026001", "ana@grasset.qc.ca", "débutant", 0),        # hors intervalle
        ("2026001", "ana@grasset.qc.ca", "débutant", "deux"),   # mauvais type
    ]

    print("== Saisies valides")
    for essai in valides:
        print("  Acceptée :", Inscription(*essai).resume())

    print("\n== Saisies invalides")
    for essai in invalides:
        try:
            Inscription(*essai)
        except DonneeInvalide as e:
            print(f"  Refusée  : {str(essai):58} -> {e}")
        else:
            print(f"  PROBLÈME : {essai} a été acceptée")

    print("\n== Le piège match / fullmatch")
    print("  re.match('\\\\d{7}', '2026001 ')     ->",
          bool(re.match(r"\d{7}", "2026001 ")), "(laisse passer)")
    print("  re.fullmatch('\\\\d{7}', '2026001 ') ->",
          bool(re.fullmatch(r"\d{7}", "2026001 ")), "(refuse)")
