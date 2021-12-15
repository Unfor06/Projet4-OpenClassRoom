from models import db_save


class Formulaire:
    @staticmethod
    def gerer_formulaire(fields: list):
        reponses = {}
        for field in fields:
            reponses[field.name] = field.poser_question()
        db_save()
        return reponses
