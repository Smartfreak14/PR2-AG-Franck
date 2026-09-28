from abc import ABC, abstractmethod


class Observateur(ABC):
    """Interface des objets qui souhaitent recevoir une notification."""

    @abstractmethod
    def actualiser(self, temperature):
        pass


class Affichage(Observateur):
    def actualiser(self, temperature):
        print(f"Affichage : temperature actuelle = {temperature} C")


class Alerte(Observateur):
    def actualiser(self, temperature):
        if temperature >= 30:
            print(f"Alerte : temperature elevee ({temperature} C)")


class StationMeteo:
    """Sujet : conserve les observateurs et les avertit d'un changement."""

    def __init__(self):
        self._observateurs = []
        self._temperature = None

    def ajouter_observateur(self, observateur):
        self._observateurs.append(observateur)

    def retirer_observateur(self, observateur):
        self._observateurs.remove(observateur)

    def definir_temperature(self, temperature):
        self._temperature = temperature
        self._notifier()

    def _notifier(self):
        for observateur in self._observateurs:
            observateur.actualiser(self._temperature)


def demo():
    print("=== Observer : notifications de la station meteo ===")
    station = StationMeteo()
    affichage = Affichage()
    alerte = Alerte()
    station.ajouter_observateur(affichage)
    station.ajouter_observateur(alerte)

    station.definir_temperature(24)
    station.definir_temperature(32)

    print("""
L'Observer cree une relation un-a-plusieurs : une StationMeteo (le sujet)
possede plusieurs observateurs. Quand sa temperature change, elle appelle
actualiser sur chacun d'eux, sans connaitre leurs details.

Apport : les composants sont faiblement couples. On peut ajouter un nouvel
observateur, par exemple un enregistreur ou une application mobile, sans
modifier StationMeteo. On peut aussi retirer un observateur a tout moment.
""")


if __name__ == "__main__":
    demo()