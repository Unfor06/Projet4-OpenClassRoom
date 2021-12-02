from controllers.menu import gerer_menu
from controllers.tournoi import menu_tournoi, start_tournament
from controllers.joueurs import menu_joueurs


def menu_principal():
    gerer_menu(
        [
            ("Gérer tournoi", menu_tournoi),
            ("Gérer joueurs", menu_joueurs),
            ("Lancer un tournoi", start_tournament),
        ]
    )
