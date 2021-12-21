from controllers.controller import generic_report
from controllers.fields import ChoiceField, Field, EmptyField, MultipleChoiceField
from controllers.form import Formulaire
from models import db_save, tournois, joueurs, Tournoi, Blitz, Bullet, CoupRapide
from exceptions import ValidationError
from view import TournoisView
from controllers.menu import Menu

FORM_START_TOURNAMENT = [ChoiceField("tournoi", "Choisir le tournoi", tournois)]

FORM_TOURNOI = [
    Field("nom", "Quel est le nom du tournoi ?"),
    Field("lieu", "Quel est le lieu du tournoi ?"),
    Field("date", "Quel est la date du tournoi ?"),
    Field("nb_de_tours", "Combien ya t'il de nombre de tours ?", convertisseur=int),
    EmptyField("tournees", tuple()),
    MultipleChoiceField(
        "joueurs",
        "Joueurs dans le tournoi:",
        joueurs,
        Field(
            "",
            "Combien de joueurs ?",
            validateur=lambda s: s.strip().isnumeric(),
            convertisseur=int,
        ),
    ),
    ChoiceField(
        "controle_du_temps",
        "Méthode de contrôle du temps",
        [Blitz(), Bullet(), CoupRapide()],
    ),
    Field("description", "Description du tournoi:"),
]


def go_to_next_turn(tournoi):
    try:
        tournoi.passer_au_tour_suivant()
    except ValidationError as e:
        TournoisView.print_next_turn(e)


def choisir_match(tournoi):
    if not tournoi.tour_en_cours:
        TournoisView.print_choisir_match
        return
    match = Formulaire.gerer_formulaire(
        [ChoiceField("match", "Quel match ?", tuple(tournoi.tour_en_cours.matchs))]
    )["match"]
    return match


def choisir_gagnant(match):
    gagnant = Formulaire.gerer_formulaire(
        [
            ChoiceField(
                "gagnant",
                "Qui est le gagnant ?",
                [match.joueur_noir, match.joueur_blanc],
            )
        ]
    )["gagnant"]
    return gagnant


def cloturer_match(tournoi):
    match = choisir_match(tournoi)
    gagnant = choisir_gagnant(match)
    try:
        match.cloturer(gagnant)
    except ValidationError as e:
        print(str(e))
    db_save()


MENU_GESTION_TOURNOI = [
    ("Passer au prochain tour", go_to_next_turn),
    ("Saisir les resultats d'un match", cloturer_match),
    ("Afficher classement", TournoisView.classement),
    ("Afficher état tour actuel", generic_report),
]


def start_tournament():
    tournoi = Formulaire.gerer_formulaire(FORM_START_TOURNAMENT)["tournoi"]
    tournoi.lancer()
    gerer_tournoi(tournoi)
    db_save()


def menu_tournoi():
    controller_tournoi = ControllerTournoi()
    print("1) Créer tournoi")
    print("2) Modifier tournoi")
    print("3) Gérer tournoi")
    choix = input("Votre choix: ")
    if choix == "1":
        controller_tournoi.lancer_tournoi()
    elif choix == "2":
        t = controller_tournoi.choisir_tournoi()
        if t:
            controller_tournoi.editer_tournoi(t)
    elif choix == "3":
        t = controller_tournoi.choisir_tournoi()
        if t:
            gerer_tournoi(t)


def gerer_tournoi(tournoi):
    Menu.gerer_menu(MENU_GESTION_TOURNOI, context=[tournoi])


class ControllerTournoi:
    @staticmethod
    def lancer_tournoi():
        while True:
            if joueurs:
                reponses = Formulaire.gerer_formulaire(FORM_TOURNOI)
            else:
                print("Il n'y a pas assez de joueurs dans la base pour créer un tournoi")
                break
            try:
                tournoi = Tournoi(**reponses)
                db_save()
                return tournoi
            except ValidationError as e:
                TournoisView.print_lancer_tournoi(e)
    
    @staticmethod
    def editer_tournoi(tournoi: Tournoi):
        if tournoi.has_started or tournoi.is_finished:
            TournoisView.print_editer_tournoi
            return None     
        TournoisView.print_editer_tournoi_2()
        Formulaire.gerer_formulaire(FORM_TOURNOI)
        db_save()

    @staticmethod
    def choisir_tournoi():
        controller = ControllerTournoi()
        options_tournoi = [(t.nom, lambda t=t: controller.editer_tournoi(t)) for t in tournois]
        Menu.gerer_menu(options_tournoi, nb_fois=1)
