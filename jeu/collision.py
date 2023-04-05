import pygame


'''ces fonctions gèrent les collisions avec les fantomes et les murs, 
en changeant l'état des fantomes/joueur si leur sprite passe par dessus celui d'un mur
Ramnère le joueur à sa place s'il est mangé'''


def collision_fantome(joueur, groupe_fantome):
    Col = []
    for fantome in groupe_fantome:
        if pygame.sprite.collide_mask(joueur, fantome):
            Col.append(fantome)
    return Col


def reinitialisation(joueur, groupe_fantome):
    joueur.reinitialisation()
    for fantome in pygame.sprite.Group.sprites(groupe_fantome):
        fantome.reinitialisation()
