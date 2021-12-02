from exceptions import ValidationError
import random
import pickle

joueurs = []
tournois = []


def db_save():
    with open("joueurs.db", "wb") as f:
        pickle.dump(joueurs, f)
    with open("tournois.db", "wb") as f:
        pickle.dump(tournois, f)


def db_load():
    global joueurs
    global tournois
    with open("joueurs.db", "rb") as f:
        joueurs = pickle.load(f)
    with open("tournois.db", "rb") as f:
        tournois = pickle.load(f)


class Tournoi:
    def __init__(
        self,
        nom,
        lieu,
        date,
        tournees,
        joueurs,
        controle_du_temps,
        description,
        nb_de_tours=4,
    ) -> None:
        self.nom = nom
        self.lieu = lieu
        self.date = date
        assert isinstance(nb_de_tours, int), "nb_tours doit être un int"
        self.nb_de_tours = nb_de_tours
        self.tournees = list(tournees)
        assert all(
            isinstance(t, Ronde) for t in tournees
        ), "tournees doit être une liste de Rondes"
        self.joueurs = list(joueurs)
        assert all(
            isinstance(j, Joueur) for j in joueurs
        ), f"joueurs doit être une liste de Joueurs, reçu: {joueurs}"
        if len(joueurs) % 2 != 0:
            raise ValidationError("Le nombre de joueurs doit être pair.")
        self.controle_du_temps = controle_du_temps
        if not isinstance(controle_du_temps, (Blitz, Bullet, CoupRapide)):
            raise NotImplementedError("On ne supporte que Blitz, Bullet, Coup rapide.")
        self.description = description
        self.tours_passes = []
        self.tour_en_cours = None
        tournois.append(self)

    def __str__(self):
        return f"{self.nom}"

    def donner_joueurs(self, ordre_de_tri):
        if ordre_de_tri == "C":
            return sorted(self.joueurs, key=lambda j:j.classement, reverse=True)
        elif ordre_de_tri == "A":
            return sorted(self.joueurs)
        
    @property
    def score(self):
        score = {}
        for match in self.tours_passes:
            for j, s in match.score.items():
                if j in score:
                    score[j] += s

                else:
                    score[j] = s
        return score

    @property
    def nb_joueurs(self):
        return len(self.joueurs)

    @property
    def is_finished(self):
        return len(self.tours_passes) == self.nb_de_tours

    @property
    def has_started(self):
        return bool(self.tours_passes or self.tour_en_cours)

    def lancer(self):
        if self.has_started:
            raise ValidationError("Le tournoi a déjà été lancé")
        self.passer_au_tour_suivant()

    def passer_au_tour_suivant(self):
        if self.tours_passes and not self.tours_passes[-1].est_termine:
            raise AssertionError("Le dernier tour n'est pas encore fini")
        if self.is_finished:
            raise ValidationError(
                "Nombre de tour maximal atteint. Le tournoi est déjà terminé"
            )

        if self.tour_en_cours:
            if not self.tour_en_cours.est_termine:
                raise ValidationError("Le tour en cours n'est pas terminé")
            self.tours_passes.append(self.tour_en_cours)

        self.tour_en_cours = Tour(self.generer_matchs())

        assert len(self.tours_passes) <= self.nb_de_tours

    def generer_matchs(self) -> list:
        if not self.tours_passes:
            coupure = len(self.joueurs) // 2
            joueurs = sorted(self.joueurs, key=lambda j: j.classement, reverse=True)

            matchs = []
            for j_superieur, j_inferieur in zip(joueurs[:coupure], joueurs[coupure:]):
                joueur_blanc, joueur_noir = random.sample([j_superieur, j_inferieur], 2)
                match = Match(joueur_blanc, joueur_noir)
                matchs.append(match)

            return matchs
        else:
            joueurs = sorted(self.joueurs, key=lambda j: self.score[j], reverse=True)
            matchs = []
            while joueurs:
                j1 = joueurs.pop(0)
                j2 = sorted(
                    joueurs, key=lambda j: (self.nb_match_contre(j1, j), -self.score[j])
                )[0]
                joueurs.remove(j2)
                matchs.append(Match(j1, j2))
            
            return matchs
    
    def nb_match_contre(self, j1, j2) -> int:
        return sum(
            1 for t in self.tours_passes for m in t.matchs if j1 in m and j2 in m
        )


class Temps:
    def __str__(self):
        return self.__class__.__name__


class Blitz(Temps):
    pass


class Bullet(Temps):
    pass


class CoupRapide(Temps):
    pass


class Joueur:
    def __init__(self, nom, prenom, date_de_naissance, sexe, classement) -> None:
        self.nom = nom
        self.prenom = prenom
        self.date_de_naissance = date_de_naissance
        self.sexe = sexe
        self.classement = classement
        if classement < 0:
            raise ValueError("Le classement doit être positif.")
        joueurs.append(self)

    def __str__(self):
        return self.nom + " " + self.prenom


class Match:
    def __init__(self, joueur_blanc, joueur_noir) -> None:
        assert joueur_blanc is not joueur_noir

        self.joueur_blanc, self.joueur_noir = joueur_blanc, joueur_noir
        self.score = {
            joueur_blanc: 0,
            joueur_noir: 0,
        }
        self.has_ended = False

    def __str__(self):
        return f"{self.joueur_blanc} vs {self.joueur_noir}"

    def cloturer(self, gagnant: Joueur):
        if self.has_ended:
            raise ValidationError("Le match a déjà été cloturé.")
        if gagnant:
            self.score[gagnant] += 1
        else:
            self.score[self.joueur_blanc] += 0.5
            self.score[self.joueur_noir] += 0.5
        self.has_ended = True

    def __contains__(self, joueurs):
        return joueurs in (self.joueur_noir, self.joueur_blanc)


class Tour:
    def __init__(self, matchs):
        self.matchs = matchs

    @property
    def score(self):
        score = {}
        for match in self.matchs:
            score.update(match.score)
        return score

    @property
    def est_termine(self):
        return all(m.has_ended for m in self.matchs)


class Ronde:
    pass

try:
    db_load()
except FileNotFoundError:
    db_save()
