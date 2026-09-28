"""
420-PR2-AG — Séance 6 — Atelier : CORRIGÉ

DÉFAUT 1 — chercher_par_cours(), la construction de la requête
  Famille : A03 — Injection.  CWE-89 (Neutralisation incorrecte d'éléments
  spéciaux dans une commande SQL).
  Pourquoi : etudiant et cours sont collés dans la chaîne de requête. La saisie
  "x' OR '1'='1" ferme la chaîne littérale et ajoute une condition toujours
  vraie : le filtre sur l'étudiant est neutralisé et tous les relevés sortent.
  Correction : requête paramétrée. La requête part au moteur d'abord, les
  valeurs ensuite ; la donnée ne peut plus modifier la structure.

DÉFAUT 2 — afficher_releve(), l'absence de vérification
  Famille : A01 — Contrôle d'accès défaillant.  CWE-639 (Contournement
  d'autorisation par clé contrôlée par l'utilisateur), souvent appelé IDOR.
  Pourquoi : le paramètre utilisateur_connecte est reçu mais jamais utilisé.
  Il suffit de changer l'identifiant dans l'URL pour lire le relevé d'un autre.
  Correction : comparer le propriétaire du relevé à l'utilisateur connecté,
  et refuser sinon — avec le même message que pour un relevé inexistant, afin
  de ne pas révéler quels identifiants existent.

SECONDE COUCHE (défense en profondeur)
  La requête paramétrée rend l'injection impossible ; la validation en liste
  blanche du code de cours la rend en plus absurde. Les deux sont utiles :
  si un jour quelqu'un réécrit la requête par concaténation, la validation
  limite encore les dégâts. Chaque couche suppose que la précédente a échoué.

Exécution :  python3 cve_equivalent_corrige.py
Pour lancer les tests sur ce corrigé :
    cp cve_equivalent_corrige.py cve_equivalent.py && python3 test_cve_equivalent.py
"""

import re
import sqlite3


class AccesRefuse(Exception):
    """L'utilisateur n'a pas le droit d'effectuer cette opération."""


COLONNES_AFFICHABLES = ("cours", "note", "session")
CODE_COURS = re.compile(r"\d{3}-[A-Z]{2}\d")        # seconde couche : 420-PR2


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
    # DÉFAUT 1 corrigé : requête paramétrée (+ validation en seconde couche)
    # ------------------------------------------------------------------
    def chercher_par_cours(self, etudiant, cours):
        # Seconde couche : un code de cours a une forme connue.
        # Une saisie qui n'a pas cette forme ne mérite pas d'aller plus loin.
        if not CODE_COURS.fullmatch(cours):
            return []
        return self.con.execute(
            "SELECT cours, note, session FROM releve "
            "WHERE etudiant = ? AND cours = ?",
            (etudiant, cours)).fetchall()

    # ------------------------------------------------------------------
    # DÉFAUT 2 corrigé : l'appartenance est vérifiée avant de retourner
    # ------------------------------------------------------------------
    def afficher_releve(self, id_releve, utilisateur_connecte):
        ligne = self.con.execute(
            "SELECT etudiant, cours, note FROM releve WHERE id = ?",
            (id_releve,)).fetchone()
        # Le même message dans les deux cas : ne pas révéler si l'identifiant
        # existe, sans quoi on donne une carte du système à l'attaquant.
        if ligne is None or ligne[0] != utilisateur_connecte:
            raise AccesRefuse("Relevé introuvable ou inaccessible.")
        return {"etudiant": ligne[0], "cours": ligne[1], "note": ligne[2]}

    # ------------------------------------------------------------------
    # Inchangé : un nom de colonne exige une liste blanche
    # ------------------------------------------------------------------
    def trier(self, etudiant, colonne):
        if colonne not in COLONNES_AFFICHABLES:
            raise ValueError(f"Colonne non autorisée : {colonne}")
        return self.con.execute(
            f"SELECT cours, note, session FROM releve "
            f"WHERE etudiant = ? ORDER BY {colonne}", (etudiant,)).fetchall()


if __name__ == "__main__":
    portail = PortailNotes()

    print("== Usage normal — inchangé")
    print("  Ana, 420-PR2 :", portail.chercher_par_cours("ana", "420-PR2"))
    print("  Tri par note :", portail.trier("ana", "note"))
    print("  Son relevé   :", portail.afficher_releve(1, "ana"))

    print("\n== Les deux attaques échouent désormais")
    print("  Saisie forgée :", portail.chercher_par_cours("ana", "x' OR '1'='1"))
    try:
        portail.afficher_releve(3, "ana")
    except AccesRefuse as e:
        print("  Relevé d'un autre étudiant :", e)
