from models import tournois, Joueur, joueurs
from colorama import init, Fore, Style

init()


def liste_tournoi():
    for i, tournoi in enumerate(tournois, start=1):
        print(f"{i}) {tournoi.nom}, du: {tournoi.date}. Lieu: {tournoi.lieu}")


def afficher_menu(options, start=1):
    for i, (option, callback) in enumerate(options, start=start):
        print(f"{i}) {option}")
    print("q) Quitter")
    return input("Votre choix ?")


def erreur_formulaire(raison_erreur):
    print(Fore.RED + "Formulaire invalide pour la raison suivante :" + Style.RESET_ALL)
    print(raison_erreur)
    choix = input("Que voulez-vous faire ? (c)ontinuer ou (a)rrêter (choix par défaut)")
    if choix in ["c", "a"]:
        return choix
    else:
        return "a"


def afficher_liste_joueurs(tournoi, ordre_de_tri):
    joueurs_tries = tournoi.donner_joueurs(ordre_de_tri.strip().upper())
    joueur: Joueur = None
    if ordre_de_tri == "C":
        for i, joueur in enumerate(joueurs_tries, start=1):
            if i == 1:
                print(
                    Fore.GREEN
                    + f"{i}/ {joueur.classement} {joueur.nom} {joueur.prenom}"
                    + Style.RESET_ALL
                )
            else:
                print(f"{i}/ {joueur.classement} {joueur.nom} {joueur.prenom}")
    else:
        for i, joueur in enumerate(joueurs_tries, start=1):
            print(f"{i}/ {joueur.nom} {joueur.prenom} {joueur.classement}")


def classement(tournoi):
    for j, score in tournoi.score.items():
        print (j, score)


def print_question(liste_des_choix, nb_choix):
    print(f"Choix n°{len(liste_des_choix) + 1}/{nb_choix}")  


def print_cree_joueur(e):
    print(f"Le formulaire est invalide car : {e}")


def lister_joueurs(joueurs=joueurs):
    for i, joueur in enumerate(joueurs, start=1):
        print(f"{i}) {joueur.nom}, {joueur.prenom}. Classement: {joueur.classement}")


def print_next_turn(e):
    print(str(e))


def print_choisir_match(tournoi):
    print("Le tournoi n'a aucun tour en cours")


def print_lancer_tournoi(e):
    print(f"Le formulaire est invalide car : {e}")


def print_editer_tournoi(tournoi):
    print(
            f"Impossible de modifier le tournoi {tournoi.nom} car il est déjà démarré ou arrêté."
        )


def print_editer_tournoi_2(tournoi):
    print(f"Tournoi choisi: {tournoi.nom}")    
