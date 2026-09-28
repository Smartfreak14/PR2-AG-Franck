"""
420-PR2-AG — Séance 6 — Atelier : le fichier de tests

NE MODIFIEZ PAS CE FICHIER.

Avant correction :  les 3 tests d'usage passent, les 2 tests d'attaque ÉCHOUENT
                    (c'est-à-dire : l'attaque réussit — le module est vulnérable).
Après correction  :  les 5 tests passent.

Exécution :  python3 test_cve_equivalent.py
"""

from cve_equivalent import PortailNotes, AccesRefuse

resultats = []


def verifier(nom, condition, detail=""):
    resultats.append((nom, condition, detail))


portail = PortailNotes()

# ----------------------------------------------------------------------
# Usage normal — doit continuer à fonctionner après votre correction
# ----------------------------------------------------------------------
lignes = portail.chercher_par_cours("ana", "420-PR2")
verifier("usage 1 — Ana voit sa note de 420-PR2",
         lignes == [("420-PR2", 88, "A2026")],
         f"obtenu : {lignes}")

lignes = portail.chercher_par_cours("ana", "420-BD1")
verifier("usage 2 — Ana voit sa note de 420-BD1",
         lignes == [("420-BD1", 74, "A2026")],
         f"obtenu : {lignes}")

try:
    releve = portail.afficher_releve(1, "ana")
    ok = releve["etudiant"] == "ana" and releve["note"] == 88
except AccesRefuse as e:
    ok, releve = False, str(e)
verifier("usage 3 — Ana accède à son propre relevé", ok, f"obtenu : {releve}")

# ----------------------------------------------------------------------
# Attaques — doivent échouer après votre correction
# ----------------------------------------------------------------------
lignes = portail.chercher_par_cours("ana", "x' OR '1'='1")
verifier("attaque 1 — la saisie forgée ne retourne aucune ligne",
         lignes == [],
         f"obtenu : {lignes}")

try:
    portail.afficher_releve(3, "ana")          # le relevé 3 appartient à Luis
    ok, detail = False, "le relevé d'un autre étudiant a été retourné"
except AccesRefuse:
    ok, detail = True, ""
verifier("attaque 2 — Ana ne peut pas lire le relevé de Luis", ok, detail)

# ----------------------------------------------------------------------
# Bilan
# ----------------------------------------------------------------------
print()
reussis = 0
for nom, condition, detail in resultats:
    if condition:
        reussis += 1
        print(f"  RÉUSSI  {nom}")
    else:
        print(f"  ÉCHOUÉ  {nom}")
        if detail:
            print(f"          {detail}")

print(f"\n{reussis} / {len(resultats)} tests réussis")
if reussis == len(resultats):
    print("Les deux défauts sont corrigés et l'usage normal fonctionne toujours.")
else:
    print("Continuez : un test échoué signale un défaut encore présent.")
