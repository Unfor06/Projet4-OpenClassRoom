from controllers.fields import ChoiceField, Field
from controllers.form import Formulaire
from models import db_save
from models import joueurs, Joueur
from view import JoueursView
from controllers.menu import Menu

FORM_JOUEUR = [
    Field("nom", "Quel est votre nom ?"),
    Field("prenom", "Quel est votre prénom ?"),
    Field("date_de_naissance", "Quelle est votre date de naissance ?"),
    ChoiceField("sexe", "Votre genre ?", ["H", "F"]),
    Field(
        "classement", "Votre classement elo ?", lambda s: s.strip("-").isdigit(), int
    ),
]


def menu_joueurs():
    controller_joueurs = ControllerJoueurs()
    Menu.gerer_menu(
        [
            ("Créer nouveau joueur", controller_joueurs.creer_joueur),
            ("Modifier joueur", controller_joueurs.choisir_joueur),
            ("Lister joueurs", JoueursView.lister_joueurs),
        ]
    )


class ControllerJoueurs:
    @staticmethod
    def creer_joueur():
        while True:
            reponses = Formulaire.gerer_formulaire(FORM_JOUEUR)
            try:
                joueur = Joueur(**reponses)
                db_save()
                return joueur
            except Exception as e:
                JoueursView.print_cree_joueur(e)
    
    @staticmethod
    def editer_joueur(joueur):
        print(f"Joueur choisi: {joueur.nom}, {joueur.prenom}")
        reponses = Formulaire.gerer_formulaire(FORM_JOUEUR)
        joueur.nom = reponses["nom"]
        joueur.prenom = reponses["prenom"]
        joueur.date_de_naissance = reponses["date_de_naissance"]
        joueur.sexe = reponses["sexe"]
        joueur.classement = reponses["classement"]
        db_save()
    
    @staticmethod
    def choisir_joueur():
        controller = ControllerJoueurs()
        options_joueurs = [(j.nom, lambda j=j: controller.editer_joueur(j)) for j in joueurs]
        Menu.gerer_menu(options_joueurs, nb_fois=1)


