from jeu.end import *
import pygame


def test_Game_Over():
    assert not Game_Over(3)
    assert not Game_Over(1)
    assert Game_Over(0)


def test_Victoire():
    groupe_test = pygame.sprite.Group()
    assert Victoire(groupe_test, groupe_test)
