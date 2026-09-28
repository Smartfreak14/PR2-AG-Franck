"""
420-PR2-AG — Séance 6 — Atelier : le code à corriger

Ce module simule le portail de notes d'un petit collège. Il contient deux
défauts du même type que ceux décrits dans les CVE de la liste fournie :
  - un défaut de la famille A03 (injection) ;
  - un défaut de la famille A01 (contrôle d'accès).

Votre travail :
  1. identifiez la ligne exacte qui porte chaque défaut ;
  2. expliquez en une phrase pourquoi elle est dangereuse ;
  3. corrigez-la, puis exécutez test_cve_equivalent.py — les deux tests
     d'attaque doivent échouer et les trois tests d'usage normal doivent
     continuer à passer ;
  4. ajoutez une seconde couche de défense (validation en liste blanche)
     et expliquez ce qu'elle apporte en plus.

Ne modifiez PAS le fichier de tests.

Exécution :  python3 cve_equivalent.py
"""

import sqlite3


class AccesRefuse(Exception):
    """L'utilisateur n'a pas le droit d'effectuer cette opération."""


COLONNES_AFFICHABLES = ("cours", "note", "session")


class PortailNotes:
    def __init__(self):
        self.con = sqlite3.connect(":memory:")
        self.con.execute(
            "CREATE TABLE releve ("
            "  id INTEGER, etudiant TEXT, cours TEXT, note INTEGER, session TEXT)")
        self.con.executemany(
            "INSERT INTO releve VALUES (?, ?, ?, ?, ?)",
            [(1, "ana", "420-PR2", 88, "A2026"),
             (2, "ana", "420-BD1", 74, "A2026"),
             (3, "luis", "420-PR2", 91, "A2026"),
             (4, "carla", "420-RE1", 65, "A2026")])
        self.con.commit()

    # ------------------------------------------------------------------
    # DÉFAUT 1 — famille OWASP : ..........
    # Ligne fautive : ..........
    # Pourquoi : ..........
    # ------------------------------------------------------------------
    def chercher_par_cours(self, etudiant, cours):
        requete = (f"SELECT cours, note, session FROM releve "
                   f"WHERE etudiant = '{etudiant}' AND cours = '{cours}'")
        return self.con.execute(requete).fetchall()

    # ------------------------------------------------------------------
    # DÉFAUT 2 — famille OWASP : ..........
    # Ligne fautive : ..........
    # Pourquoi : ..........
    # ------------------------------------------------------------------
    def afficher_releve(self, id_releve, utilisateur_connecte):
        ligne = self.con.execute(
            "SELECT etudiant, cours, note FROM releve WHERE id = ?",
            (id_releve,)).fetchone()
        if ligne is None:
            raise AccesRefuse("Relevé introuvable.")
        return {"etudiant": ligne[0], "cours": ligne[1], "note": ligne[2]}

    # ------------------------------------------------------------------
    # Fourni à titre de comparaison : ce tri est déjà correct.
    # Un nom de colonne ne peut pas être un paramètre SQL ; il est donc
    # comparé à une liste blanche écrite dans le module.
    # ------------------------------------------------------------------
    def trier(self, etudiant, colonne):
        if colonne not in COLONNES_AFFICHABLES:
            raise ValueError(f"Colonne non autorisée : {colonne}")
        return self.con.execute(
            f"SELECT cours, note, session FROM releve "
            f"WHERE etudiant = ? ORDER BY {colonne}", (etudiant,)).fetchall()


if __name__ == "__main__":
    portail = PortailNotes()

    print("== Usage normal")
    print("  Ana, 420-PR2 :", portail.chercher_par_cours("ana", "420-PR2"))
    print("  Tri par note :", portail.trier("ana", "note"))

    print("\n== Ce qui ne devrait pas fonctionner")
    print("  Saisie forgée :",
          portail.chercher_par_cours("ana", "x' OR '1'='1"))
    print("  Relevé d'un autre étudiant :",
          portail.afficher_releve(3, "ana"))
