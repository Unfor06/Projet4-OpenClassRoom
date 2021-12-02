from models import db_save


def gerer_formulaire(fields: list):
    reponses = {}
    for field in fields:
        reponses[field.name] = field.poser_question()
    db_save()
    return reponses
