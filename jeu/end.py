import numpy as np
import pygame


# renvoie True si le joueur n'a plus de vies
def Game_Over(Vies):
    return Vies == 0


# renvoie True si toutes les gommes ont été mangées
def Victoire(Gomme, Super_Gomme):
    return len(pygame.sprite.Group.sprites(Gomme)) + len(pygame.sprite.Group.sprites(Super_Gomme)) == 0
