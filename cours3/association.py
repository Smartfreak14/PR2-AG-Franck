class Cours :
    def __init__(self, code):
        self.code = code
        self.titulaire = None

class Professeur :
    def __init__(self, nom):
        self.nom = nom

    def enseigner(self, cours):
        cours.titulaire = self
        return f"{self.nom} enseigne le cours {cours.code}"

professeur1 = Professeur("Dr. Dupont")
cours1 = Cours("Math101")
resultat = professeur1.enseigner(cours1)
print(resultat)  # Affiche : Dr. Dupont enseigne le cours Math101
del professeur1
print(cours1.code) 