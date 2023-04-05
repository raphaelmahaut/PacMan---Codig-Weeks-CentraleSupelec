import numpy as np
import pygame
import random as rd
from jeu.entité import *


'''Les fonctions suivantes créent les classes des gommes et murs, puis affichent les sprites en fonction de leur position dans la grille'''


class Gum(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "packages_textures/Gomme.png").convert_alpha()  # chargement texture
        self.rect = self.image.get_rect()
        self.rect.center = ((pos[1] + 0.5) * 14,
                            (pos[0] + 0.5) * 14)  # position en fonction de la position grille et de la taille en pixel


class Super_gum(pygame.sprite.Sprite):  # comme fonction précédente
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image = pygame.image.load(
            "packages_textures/SuperGomme.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((pos[1] + 0.5) * 14,
                            (pos[0] + 0.5) * 14)


class Tunnel(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "packages_textures/tunnel.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((pos[1] + 0.5) * 14,
                            (pos[0] + 0.5) * 14)


class Fin_tunnel(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "packages_textures/tunnel.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = ((pos[1] + 0.5) * 14,
                            (pos[0] + 0.5) * 14)


# crée la grille de placement des gommes, puis les affiche
def grille_placement_gum(grid, pos):
    groupe_gum = pygame.sprite.Group()

    long, larg = np.shape(grid)
    x, y = pos
    x = int(x)
    y = int(y)

    grid[x, y] = -1  # code de la gomme simple dans la grille
    done = True
    while done:
        done = False
        for i in range(long):  # toutes les gommes de la grille
            for j in range(larg):
                if grid[i, j] == -1:  # vérifie la position (pas un mur)
                    if (0 <= i < long) & (0 <= j-1 < larg):
                        if grid[i, j-1] == 0:
                            grid[i, j-1] = -1
                            groupe_gum.add(Gum((i, j-1)))
                            done = True
                    if (0 <= i-1 < long) & (0 <= j < larg):
                        if grid[i-1, j] == 0:
                            grid[i-1, j] = -1
                            groupe_gum.add(Gum((i-1, j)))
                            done = True
                    if (0 <= i+1 < long) & (0 <= j < larg):
                        if grid[i+1, j] == 0:
                            grid[i+1, j] = -1
                            groupe_gum.add(Gum((i+1, j)))
                            done = True
                    if (0 <= i < long) & (0 <= j+1 < larg):
                        if grid[i, j+1] == 0:
                            grid[i, j+1] = -1
                            groupe_gum.add(Gum((i, j+1)))
                            done = True

    # prend une gomme au hasard et la remplace par une super pac gomme
    groupe_super_gum = pygame.sprite.Group()
    for i in range(4):
        gum = rd.choice(pygame.sprite.Group.sprites(groupe_gum))
        groupe_super_gum.add(Super_gum(gum.rect.center))

        gum.kill()  # enlève la gomme remplacée

    # renvoie le groupe, ce qui a pour effet de faire apparaître les gommes grâce à la fonction main
    return groupe_gum, groupe_super_gum


# ajoute les gums, tunnels à leur groupes respectifs, pour les collisions
def placement_gum(Grille):
    nb_lignes, nb_colonnes = np.shape(Grille)

    groupe_gum = pygame.sprite.Group()
    groupe_super_gum = pygame.sprite.Group()
    groupe_tunnel = pygame.sprite.Group()
    groupe_fin_tunnel = pygame.sprite.Group()

    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            if Grille[i, j] == -1:  # code gomme
                groupe_gum.add(Gum((i, j)))
            elif Grille[i, j] == -2:  # code super gomme
                groupe_super_gum.add(Super_gum((i, j)))
            elif Grille[i, j] == -3:  # code tunnel
                groupe_tunnel.add(Tunnel((i, j)))
            elif Grille[i, j] == -3:  # code fin de tunnel
                groupe_fin_tunnel.add(Fin_tunnel((i, j)))

    return groupe_gum, groupe_super_gum, groupe_tunnel, groupe_fin_tunnel


'''Cette fonction permet de gérer la collision entre Pac-Man et les gommes, et ajoute le score associé'''


def manger(joueur, groupe_gum, groupe_super_gum, groupe_fantome, groupe_fruit, fps, bonus, Val_bon, score, apparition, temps_peur):
    Trad_inv = {'haut': 'bas', 'bas': 'haut',
                'gauche': 'droite', 'droite': 'gauche', 'aucune': 'aucune'}
    # gère la collison de sprite entre deux groupes
    if pygame.sprite.spritecollide(joueur, groupe_gum, True):
        score += 10
    for fruit in pygame.sprite.spritecollide(joueur, groupe_fruit, True):
        score += fruit.point
        Val_bon.temps = 3*fps
        Val_bon.image = pygame.image.load(
            "packages_textures/{}.png".format(str(fruit.point)))
    if Val_bon.temps:
        Val_bon.temps -= 1
        if not Val_bon.temps:
            Val_bon.image = pygame.image.load(
                "packages_textures/tunnel.png")
    if pygame.sprite.spritecollide(joueur, groupe_super_gum, True):
        score += 50
        bonus = 200
        joueur.pouvoir = temps_peur*fps  # donne la fonction  du pouvoir au joueur
        for fantome in pygame.sprite.Group.sprites(groupe_fantome):
            # donne le sprite peur aux fantomes
            fantome.texture_act_peur = [0, 1]
            fantome.peur = 1  # donne le comportement peur aux fantomes
            fantome.vitesse[2] = 1  # diminue leur vitesse
            # inverse leur direction (début de fuite)
            fantome.direction = Trad_inv[fantome.direction]
    return score, bonus, apparition
