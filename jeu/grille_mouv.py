import numpy as np
#from carbonai import PowerMeter

# 4 direction [haut, bas, gauche, droite], [True, False, False, True]
# rien :
# mur : [False, False, False, False]
# couloir horizontal : [False, False, True, True]
# couloir vertical : [True, True, False, False]
# carrefour : [True, True, True, True]
# T sans le gauche : [True, True, False, True]
# T sans le droit : [True, True, True, False]
# T sans le bas : [True, False, True, True]
# T sans le haut : [False, True, True, True]


#power_meter = PowerMeter(project_name="plant-man", is_online=False, location="FR")

'''Cette fonction renvoie automatiquement la grille qui gère les direction possible à chaque case.
Cela se présente comme un array de listes qui contiennent des listes de 4 booléens, correspondant 
à la possibilité d'aller en haut, bas, gauche, droite '''


def init_grille_mouv(grille):
    (a, b) = np.shape(grille)
    list1 = []
    for i in range(b):
        list1.append([False, False, False, False])  # init list
    grillelist = []
    for j in range(a):
        grillelist.append(list1)  # init grille

    grille_mouv = np.array(grillelist)
    for j in range(b):
        for i in range(a):  # grille est une matrice qui contient 0 si la case est un mur

            # on gère d'abord les bords du jeu, pour éviter erreur indice et vérifier la possibilité du tunnel
            if i == 0 or i == (a-1):
                if j == 0 or j == (b-1):
                    grille_mouv[i][j] = [False, False, False, False]
                else:
                    if grille[i][j] <= 0:
                        grille_mouv[i][j] = [True, True, False, False]

            if j == 0 or j == (b-1):
                if i == 0 or i == (a-1):
                    grille_mouv[i][j] = [False, False, False, False]
                else:
                    if grille[i][j] <= 0:
                        grille_mouv[i][j] = [False, False, True, True]

            # selon les cases adjacentes, on déduit alors les possibilités de déplacement
            if i != 0 and i != (a-1) and j != 0 and j != (b-1):
                pos = [False, False, False, False]
                if grille[i][j + 1] <= 0:
                    pos[3] = True
                if grille[i][j - 1] <= 0:
                    pos[2] = True
                if grille[i - 1][j] <= 0:
                    pos[0] = True
                if grille[i + 1][j] <= 0:
                    pos[1] = True

                grille_mouv[i][j] = pos

            if grille[i][j] >= 1:  # on revérifie que la case n'est pas un mur
                # si oui, elle a peut être été modifié à cause des cases adjacentes, donc on referme les mouvements
                grille_mouv[i][j] = [False, False, False, False]

    return grille_mouv
