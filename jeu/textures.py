import pygame

'''cette fonction permet d'initialiser les textures pour les afficher'''


def ouvertures():
    textures = [0] + [pygame.image.load("packages_textures/mur{}.png".format(
        str(i))).convert_alpha() for i in range(1, 36)]
    return textures
