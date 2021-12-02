from view import print_question


class Field:
    def __init__(
        self, name, question, validateur=lambda s: True, convertisseur=lambda s: s
    ):
        self.name = name
        self.question = question
        self.validateur = validateur
        self.convertisseur = convertisseur

    def initialize_field(self):
        pass

    def poser_question(self):
        while True:
            reponse = input(self.question)
            if self.validateur(reponse):
                try:
                    return self.convertisseur(reponse)
                except Exception as e:
                    print(
                        f"'{reponse}' est une valeur invalide pour la raison suivante (vérifié par le modèle) : {e}"
                    )
            else:
                print("Invalide car on ne passe même pas le validateur")


class EmptyField(Field):
    def __init__(self, name, valeur):
        self.name = name
        self.valeur = valeur

    def poser_question(self):
        return self.valeur


class ChoiceField(Field):
    def __init__(self, name, question, liste_choix, convertisseur=lambda s: s):
        self.liste_choix = liste_choix
        self.question = question
        self.name = name
        self.convertisseur = convertisseur

    def poser_question(self):
        if len(self.liste_choix) == 0:
            raise IndexError("Il n'y a pas assez de choix possibles")
        while True:
            print(self.question)
            for i, element in enumerate(self.liste_choix, start=1):
                print(f"{i}) {element} ?")

            reponse: str = input("Quel est votre choix ?")
            try:
                reponse: int = int(reponse) - 1
                if reponse < 0:
                    raise ValueError
            except ValueError:
                print("Veuillez taper un nombre compris entre 1 et ...")
                continue
            try:
                return self.convertisseur(self.liste_choix[reponse])
            except IndexError:
                print("Veuillez taper un nombre compris entre 1 et ...")
                continue


class MultipleChoiceField(ChoiceField):
    def __init__(self, name, question, liste_choix, nb_choix):
        self.nb_choix = nb_choix
        super().__init__(name, question, liste_choix)

    def poser_question(self):
        liste_des_choix = []
        if isinstance(self.nb_choix, Field):
            nb_choix = self.nb_choix.poser_question()
        if nb_choix > len(self.liste_choix):
            raise IndexError("Il n'y a pas assez de choix possibles")
        while len(liste_des_choix) < nb_choix:
            print_question(liste_des_choix, nb_choix)
            liste_des_choix.append(super().poser_question())
        return liste_des_choix
