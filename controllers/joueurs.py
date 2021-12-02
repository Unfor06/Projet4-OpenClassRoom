from controllers.fields import ChoiceField, Field
from controllers.form import gerer_formulaire
from controllers.menu import gerer_menu
from models import db_save
from models import joueurs, Joueur
from view import print_cree_joueur , lister_joueurs

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
    gerer_menu(
        [
            ("Créer nouveau joueur", creer_joueur),
            ("Modifier joueur", choisir_joueur),
            ("Lister joueurs", lister_joueurs),
        ]
    )


def creer_joueur():
    while True:
        reponses = gerer_formulaire(FORM_JOUEUR)
        try:
            joueur = Joueur(**reponses)
            db_save()
            return joueur
        except Exception as e:
            print_cree_joueur(e)


def editer_joueur(joueur):
    print(f"Joueur choisi: {joueur.nom}, {joueur.prenom}")
    reponses = gerer_formulaire(FORM_JOUEUR)
    joueur.nom = reponses["nom"]
    joueur.prenom = reponses["prenom"]
    joueur.date_de_naissance = reponses["date_de_naissance"]
    joueur.sexe = reponses["sexe"]
    joueur.classement = reponses["classement"]
    db_save()


def choisir_joueur():
    options_joueurs = [(j.nom, lambda: editer_joueur(j)) for j in joueurs]
    gerer_menu(options_joueurs)
