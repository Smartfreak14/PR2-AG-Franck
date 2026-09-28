# Séance 6 — OWASP Top 10 et validation des entrées

| Fichier | Rôle | Pour qui |
|---|---|---|
| `01_demo_injection.py` | Injection SQL : version vulnérable, version paramétrée, cas du nom de colonne | Démonstration en classe |
| `02_demo_valider_echapper.py` | Valider / assainir / échapper, liste noire contre liste blanche, hachage | Démonstration en classe |
| `vulnerable.py` | Micro-exercice 1 : trois extraits à corriger (A03, A01, A02) | Fourni aux étudiants |
| `vulnerable_corrige.py` | Corrigé du micro-exercice 1, avec les justifications | Enseignant |
| `inscription_depart.py` | Micro-exercice 2 : squelette du validateur en liste blanche | Fourni aux étudiants |
| `inscription_corrige.py` | Corrigé du micro-exercice 2, y compris le piège `match` / `fullmatch` | Enseignant |
| `cve_equivalent.py` | Atelier : code affecté de deux défauts (injection + contrôle d'accès) | Fourni aux étudiants |
| `test_cve_equivalent.py` | Atelier : 3 tests d'usage, 2 tests d'attaque. À ne pas modifier | Fourni aux étudiants |
| `cve_equivalent_corrige.py` | Corrigé de l'atelier, avec CWE et défense en profondeur | Enseignant |

## À déposer sur Léa avant la séance
`vulnerable.py`, `inscription_depart.py`, `cve_equivalent.py`,
`test_cve_equivalent.py`, plus votre liste de CVE à étudier.

## Déroulement de l'atelier
```
python3 test_cve_equivalent.py   # avant correction : 3 / 5
# ... les étudiants corrigent cve_equivalent.py ...
python3 test_cve_equivalent.py   # après correction : 5 / 5
```

## Note
Tout s'exécute en local, sur une base SQLite en mémoire. Aucun réseau, aucun
fichier écrit sur le disque, aucun système tiers n'est sollicité.
