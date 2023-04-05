import pygame
import numpy as np
import random as rd
import copy
from operator import itemgetter


# permet d'afficher le bonus lorsque l'on mange un fantome et les fruits
class Valeur(pygame.sprite.Sprite):
    def __init__(self, centre, valeur):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "packages_textures/{}.png".format(str(valeur))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = centre
        self.temps = 0


class Plant_man(pygame.sprite.Sprite):  # classe associée à Pac-Man
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        # import des textures
        self.textures = [[pygame.image.load("packages_textures/Pac{}{}.png".format(j, str(i))).convert_alpha()
                         for i in [1, 2, 3, 2]] for j in ["h", "b", "g", "d"]]
        self.image = self.textures[2][0]
        self.texture_act = [0, 4, 2]

        # positionnement de Pac-Man
        self.rect = self.image.get_rect()
        self.rect.centerx = ((pos[1] + 0.5)*14)
        self.rect.centery = ((pos[0] + 0.5)*14)

        # initialisation des directions et d'autres paramètres
        self.direction = "gauche"
        self.nouvelle_direction = None
        self.initx = self.rect.x
        self.inity = self.rect.y
        self.vitesse = 5
        self.frame = 0
        self.pouvoir = 0

    def reinitialisation(self):  # replace Pac-Man lorsqu'il perd une vie
        self.direction = "gauche"
        self.rect.x = self.initx
        self.rect.y = self.inity
        self.texture_act = [0, 4, 2]
        self.image = self.textures[2][self.texture_act[0]]

    def anim(self):  # anime le mouvement de la bouche de Pac-Man
        Indice = {"haut": 0, "bas": 1, "gauche": 2, "droite": 3}
        if self.direction != "aucune":
            self.texture_act[2] = Indice[self.direction]
            self.texture_act[0] = (
                1 + self.texture_act[0]) % self.texture_act[1]
            self.image = self.textures[self.texture_act[2]
                                       ][self.texture_act[0]]


class Fantome(pygame.sprite.Sprite):  # classe associée aux différents fantomes
    def __init__(self, pos, couleur):
        # mouvements de depart pé déterminé
        Seq_dep = {"red":  ["gauche"]*14 + ["bas"]*(3*14) + ["gauche"]*(4*14 + 7),
                   "pink": ["gauche"]*(4*14 + 7) + ["haut"]*(3*14),
                   "blue": ["gauche"]*(4*14 + 7) + ["haut"]*(3*14) + ["droite"]*(2*14)
                   + (["haut"]*7 + ["bas"] *
                      14 + ["haut"]*7)*2,
                   "orange": ["droite"]*(4*14 + 7) + ["haut"]*(3*14) + ["gauche"]*(2*14)
                   + (["haut"]*7 + ["bas"]*14 + ["haut"]*7)*4}

        pygame.sprite.Sprite.__init__(self)
        # importation des textures
        self.textures = [[pygame.image.load("packages_textures/fantome{}{}{}.png".format(couleur, j, str(i))).convert_alpha()
                         for i in [2, 2, 3, 3]] for j in ["h", "b", "g", "d"]] + [[pygame.image.load("packages_textures/fantome{}{}.png".format(couleur, Seq_dep[couleur][-1][0])).convert_alpha()]]
        self.textures_peur = [pygame.image.load("packages_textures/peurbleu.png").convert_alpha(), pygame.image.load("packages_textures/peurbleu.png").convert_alpha(),
                              pygame.image.load("packages_textures/peurblanc.png").convert_alpha(), pygame.image.load("packages_textures/peurblanc.png").convert_alpha()]
        self.image = self.textures[4][0]
        self.texture_act = [0, 4, 0]
        self.couleur = couleur

        # positionnement du fantome
        self.rect = self.image.get_rect()
        self.rect.centerx = ((pos[1] + 0.5)*14)
        self.rect.centery = ((pos[0] + 0.5)*14)

        # initialisation des directions et d'autres paramètres
        self.direction = Seq_dep[couleur][-1]
        self.nouvelle_direction = None
        self.ancienne_direction = None
        self.initx = self.rect.x
        self.inity = self.rect.y
        self.peur = 0
        self.retour = 0
        self.texture_act_peur = [0, 1]
        self.depart = Seq_dep[couleur]
        self.vitesse = [0, 0, 0, 0, 1]
        self.frame = 0
        self.valeur = Valeur(self.rect.center, "tunnel")

    # replace les fantomes si on est touché et reset les premiers mouvements
    def reinitialisation(self):
        Seq_dep = {"red":  ["bas"]*(3*14) + ["gauche"]*(4*14 + 7),
                   "pink": ["gauche"]*(4*14 + 7) + ["haut"]*(3*14),
                   "blue": ["gauche"]*(4*14 + 7) + ["haut"]*(3*14) + ["droite"]*(2*14)
                   + (["haut"]*7 + ["bas"] *
                      14 + ["haut"]*7)*2,
                   "orange": ["droite"]*(4*14 + 7) + ["haut"]*(3*14) + ["gauche"]*(2*14)
                   + (["haut"]*7 + ["bas"]*14 + ["haut"]*7)*4}
        self.rect.x = self.initx
        self.rect.y = self.inity
        self.depart = Seq_dep[self.couleur]
        self.vitesse = [0, 0, 0, 0, 1]
        self.image = self.textures[4][0]

    def mort(self, grille_mouv, bonus):  # lorsque Pac-Man mage un fantome
        Trad = {"aucune": (0, 0), "haut": (-1, 0),
                "bas": (1, 0), "gauche": (0, -1), "droite": (0, 1)}
        Deplacement_inv = {'haut': "bas", 'bas': "haut",
                           'gauche': "droite", 'droite': "gauche"}

        # calcule des mouvements du fantome pour retourner à la base
        Seq_dep = {"red":  (["droite"]*7 + ["haut"]*(3*14) + ["changement"] + ["bas"]*(3*14) + ["gauche"]*7,
                            ["gauche"]*7 + ["haut"]*(3*14) + ["changement"] + ["bas"]*(3*14) + ["droite"]*7),
                   "pink": (["droite"]*7 + ["haut"]*(3*14) + ["changement"] + ["bas"]*(3*14) + ["gauche"]*7,
                            ["gauche"]*7 + ["haut"]*(3*14) + ["changement"] + ["bas"]*(3*14) + ["droite"]*7),
                   "blue": (["droite"]*7 + ["haut"]*(3*14) + ["droite"]*(2*14) + ["changement"] + ["gauche"]*(2*14) + ["bas"]*(3*14) + ["gauche"]*7,
                            ["gauche"]*7 + ["haut"]*(3*14) + ["droite"]*(2*14) + ["changement"] + ["gauche"]*(2*14) + ["bas"]*(3*14) + ["droite"]*7),
                   "orange": (["droite"]*7 + ["haut"]*(3*14) + ["gauche"]*(2*14) + ["changement"] + ["droite"]*(2*14) + ["bas"]*(3*14) + ["gauche"]*7,
                              ["gauche"]*7 + ["haut"]*(3*14) + ["gauche"]*(2*14) + ["changement"] + ["droite"]*(2*14) + ["bas"]*(3*14) + ["droite"]*7)}

        cible = ((self.rect.centery//14) % 31, (self.rect.centerx//14) % 28)

        chemin_D, chemin_G = Seq_dep[self.couleur]
        position = (11, 14)
        while position != cible:
            direction = choix_dir(
                position, cible, grille_mouv, Deplacement_inv[chemin_D[-1]], Deplacement_inv[chemin_D[-1]])
            chemin_D.extend([Deplacement_inv[direction]]*14)
            position = (position[0] + Trad[direction][0],
                        position[1] + Trad[direction][1])
        position = (11, 13)
        while position != cible:
            direction = choix_dir(
                position, cible, grille_mouv, Deplacement_inv[chemin_G[-1]], Deplacement_inv[chemin_G[-1]])
            chemin_G.extend([Deplacement_inv[direction]]*14)
            position = (position[0] + Trad[direction][0],
                        position[1] + Trad[direction][1])

        if len(chemin_G) < len(chemin_D):
            self.depart = copy.deepcopy(chemin_G)
        else:
            self.depart = copy.deepcopy(chemin_D)

        decy, decx = ((self.rect.centery % 14), (self.rect.centerx % 14))
        if decx < 7:
            self.depart.extend(["droite"]*(7 - decx))
        elif decx > 7:
            self.depart.extend(["gauche"]*(decx - 7))
        if decy < 7:
            self.depart.extend(["bas"]*(7 - decy))
        elif decy > 7:
            self.depart.extend(["haut"]*(decy - 7))

        # affiche le bonus à la place du fantome et change la texture du faantome
        self.retour = 1
        self.image = pygame.image.load(
            "packages_textures/fantome_mort.png").convert_alpha()
        self.valeur.image = pygame.image.load(
            "packages_textures/{}.png".format(str(bonus))).convert_alpha()
        self.valeur.rect.center = self.rect.center
        self.vitesse[0] = 1

    def anim(self):  # choisi la texture du fantome selon la direction et peut les animer si on ajoute quelques textures
        Indice = {"haut": 0, "bas": 1, "gauche": 2, "droite": 3}
        if self.peur:
            self.texture_act_peur[0] = (
                1 + self.texture_act_peur[0]) % self.texture_act_peur[1]
            self.image = self.textures_peur[self.texture_act_peur[0]]
        elif self.direction != "aucune":
            self.texture_act[2] = Indice[self.direction]
            self.texture_act[0] = (
                1 + self.texture_act[0]) % self.texture_act[1]
            self.image = self.textures[self.texture_act[2]
                                       ][self.texture_act[0]]


# calcule le meilleur mouvement à faire  pour rejoindre une destination basé sur le mouvement des fantomes
def choix_dir(case_depart, case_visée, grille_mouv, direction, ancienne_direction):

    Deplacement_inv = {'haut': 1, 'bas': 0, 'gauche': 3, 'droite': 2}

    (ji, jj) = case_visée
    (fi, fj) = case_depart
    act = direction
    anc = ancienne_direction
    if act == 'haut':
        long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]],
                [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]], [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]

    if act == 'bas':
        long = [[((fi + 1 - ji)**2 + (fj - jj)**2), 'bas', grille_mouv[fi][fj][1]],
                [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]], [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]

    if act == 'gauche':
        long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]], [((fi + 1 - ji)**2 + (fj - jj)**2), 'bas', grille_mouv[fi][fj][1]],
                [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]]]

    if act == 'droite':
        long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]], [((fi + 1 - ji)**2 + (fj - jj)**2), 'bas', grille_mouv[fi][fj][1]],
                [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]

    if act == 'aucune':
        long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]], [((fi + 1 - ji)**2 + (fj - jj)**2), 'bas', grille_mouv[fi][fj][1]],
                [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]], [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]
        long[Deplacement_inv[anc]][2] = False

    rd.shuffle(long)
    dist = sorted(long, key=itemgetter(0))
    for k in range(len(dist)):
        if dist[k][2] == True:
            dir = dist[k][1]
            break
    return dir
