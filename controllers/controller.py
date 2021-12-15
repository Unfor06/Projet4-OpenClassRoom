from view import JoueursView
from view import TournoisView


def report_joueurs(tournoi):
    choix = input(
        "Comment voulez vous trier les joueurs ? (C)lassement ou (A)lphabétique"
    )
    if choix.lower() == "c":
        JoueursView.afficher_liste_joueurs(tournoi, "c")
    elif choix.lower() == "a":
        JoueursView.afficher_liste_joueurs(tournoi, "a")


def report_tours(tournoi):
    TournoisView.afficher_liste_tour(tournoi.tours)


def report_matchs(tournoi):
    TournoisView.afficher_liste_match(tournoi.match)


def generic_report(tournoi):
    print("1) Liste des joueurs dans le tournoi")
    print("2) Liste des tours dans le tournoi")
    print("3) Liste des matchs dans le tournoi")
    choix = input("Votre choix:")
    if choix == "1":
        report_joueurs(tournoi)
    elif choix == "2":
        report_tours(tournoi)
    elif choix == "3":
        report_matchs(tournoi)
