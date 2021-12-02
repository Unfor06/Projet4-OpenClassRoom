import view


def gerer_menu(options, context=[]):
    while True:
        choix = view.afficher_menu(options)
        if choix.lower() == "q":
            break
        try:
            choix = int(choix) - 1
        except ValueError:
            print("Veuillez choisir une valeur valide")
            continue
        option_choisie, callback_choisi = options[choix]
        callback_choisi(*context)
