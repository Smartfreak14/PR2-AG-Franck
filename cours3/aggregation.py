class Equipe:
    def __init__(self,nom):
        self.nom = nom
        self.membres = []

    def ajouter_membre(self, membre):
        self.membres.append(membre)
        return f"{membre.nom} a été ajouté à l'équipe {self.nom}"
class Employe:
    def __init__(self, nom):
        self.nom = nom

ana = Employe("Ana")
equipe1 = Equipe("Développement")
resultat = equipe1.ajouter_membre(ana)
print(resultat) 

del equipe1
print(ana.nom)  # Affiche : Ana