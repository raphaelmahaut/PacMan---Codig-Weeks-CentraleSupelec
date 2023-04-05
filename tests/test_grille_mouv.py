import numpy as np
from jeu.grille_mouv import*


grille_test = np.array([[1, 1, 1, 0, 1, 1, 1],
                        [1, 0, 0, 0, 0, 0, 1],
                        [1, 0, 1, 0, 1, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 1, 1, 1]])

grille_mouv_test = np.array([[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                             [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 1, 1], [
                                 0, 0, 1, 1], [0, 1, 1, 0], [0, 0, 0, 0]],
                             [[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [
                                 0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
                             [[0, 0, 1, 1], [1, 0, 1, 1], [0, 0, 1, 1], [1, 1, 1, 1], [
                                 0, 0, 1, 1], [1, 0, 1, 1], [0, 0, 1, 1]],
                             [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]])


def test_init_grille_mouv():
    grille_fonc = init_grille_mouv(grille_test)
    a, b = np.shape(grille_test)
    for i in range(a):
        for j in range(b):
            for k in range(4):
                assert(grille_fonc[i][j][k] == grille_mouv_test[i][j][k])
