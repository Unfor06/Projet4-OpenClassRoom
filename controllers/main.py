from controllers.tournoi import menu_tournoi, start_tournament
from controllers.joueurs import menu_joueurs
from controllers.menu import Menu


def menu_principal():
    Menu.gerer_menu(
        [
            ("Gérer tournoi", menu_tournoi),
            ("Gérer joueurs", menu_joueurs),
            ("Lancer un tournoi", start_tournament),
        ]
    )
    