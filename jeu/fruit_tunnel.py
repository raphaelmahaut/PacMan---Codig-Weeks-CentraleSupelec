import pygame
'''ces fonctions définissent les fruits, ce qu'il se passe quand on les mange et ce qu'il se passe quand on entre dans un tunnel'''


class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos, fruit_niveau):  # initialisation de la position
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "packages_textures/{}.png".format(fruit_niveau[0])).convert_alpha()  # chargement texture
        self.rect = self.image.get_rect()
        self.rect.center = ((pos[1] + 0.5) * 14,
                            (pos[0] + 0.5) * 14)
        self.point = fruit_niveau[1]


def ralentissement_tunnel(groupe_fantome, groupe_tunnel, groupe_fin_tunnel):
    for fantome in pygame.sprite.Group.sprites(groupe_fantome):
        # vérification de la position
        if pygame.sprite.spritecollide(fantome, groupe_tunnel, False):
            fantome.vitesse[1] = 1  # changement de la valeur de vitesse
        elif pygame.sprite.spritecollide(fantome, groupe_fin_tunnel, False):
            fantome.vitesse[1] = 0
