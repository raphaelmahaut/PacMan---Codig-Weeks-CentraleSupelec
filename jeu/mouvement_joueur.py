import pygame
from jeu.changement import *
from collections import deque


def mouvement_joueur(Joueur, Grille_mouv, size):
    Trad_mouv = {"aucune": (0, 0), "haut": (0, -1),
                 "bas": (0, 1), "gauche": (-1, 0), "droite": (1, 0)}

    Joueur.frame += 1  # changement de frame
    Joueur.direction, Joueur.nouvelle_direction = changement(
        Joueur, Grille_mouv)  # changement de direction (qui check si la direction est possible), voir fonction associée
    # changement de la direction à prendre
    Joueur.vx, Joueur.vy = Trad_mouv[Joueur.direction]
    if Joueur.frame == Joueur.vitesse:
        Joueur.frame = 0
        # changement de la position
        Joueur.rect.x = (Joueur.rect.x + Joueur.vx) % size[0]
        Joueur.rect.y = (Joueur.rect.y + Joueur.vy) % size[1]
