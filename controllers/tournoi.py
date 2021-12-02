from controllers.controller import generic_report
from controllers.fields import ChoiceField, Field, EmptyField, MultipleChoiceField
from controllers.form import gerer_formulaire
from controllers.menu import gerer_menu
from models import db_save, tournois, joueurs, Tournoi, Blitz, Bullet, CoupRapide
from exceptions import ValidationError
from view import classement, print_choisir_match, print_editer_tournoi, print_editer_tournoi_2, print_lancer_tournoi, print_next_turn

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
        print_next_turn(e)


def choisir_match(tournoi):
    if not tournoi.tour_en_cours:
        print_choisir_match
        return
    match = gerer_formulaire(
        [ChoiceField("match", "Quel match ?", tuple(tournoi.tour_en_cours.matchs))]
    )["match"]
    return match


def choisir_gagnant(match):
    gagnant = gerer_formulaire(
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
    ("Afficher classement", classement),
    ("Afficher état tour actuel", generic_report),
]


def start_tournament():
    tournoi = gerer_formulaire(FORM_START_TOURNAMENT)["tournoi"]
    tournoi.lancer()
    gerer_tournoi(tournoi)
    db_save()


def menu_tournoi():
    print("1) Créer tournoi")
    print("2) Modifier tournoi")
    print("3) Gérer tournoi")
    choix = input("Votre choix: ")
    if choix == "1":
        lancer_tournoi()
    elif choix == "2":
        t = choisir_tournoi()
        if t:
            editer_tournoi(t)
    elif choix == "3":
        t = choisir_tournoi()
        if t :
            gerer_tournoi(t)
        

def gerer_tournoi(tournoi):
    gerer_menu(MENU_GESTION_TOURNOI, context=[tournoi])


def lancer_tournoi():
    while True:
        if joueurs:
            reponses = gerer_formulaire(FORM_TOURNOI)
        else:
            print("Il n'y a pas assez de joueurs dans la base pour créer un tournoi")
            break
        try:
            tournoi = Tournoi(**reponses)
            db_save()
            return tournoi
        except ValidationError as e:
            print_lancer_tournoi(e)


def editer_tournoi(tournoi: Tournoi):
    if tournoi.has_started or tournoi.is_finished:
        print_editer_tournoi
        return None
    print_editer_tournoi_2
    reponses = gerer_formulaire(FORM_TOURNOI)
    db_save()


def choisir_tournoi():
    options_tournoi = [(t.nom, lambda t=t: editer_tournoi(t)) for t in tournois]
    gerer_menu(options_tournoi)
