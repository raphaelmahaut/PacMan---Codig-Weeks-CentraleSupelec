import pygame
import random as rd
from jeu.changement import *
from operator import itemgetter
from jeu.changement_fantome import *
from collections import deque


'''Ce module permet de définir la future action de chaque fantome.
Chaque fantome a un comportement different, donc les fonctions associées le sont également.
La fonction de mouvement permet de vérifier si le mouvement est possible ou non, pour éviter tout bug ou collision incorrecte '''

'''Comportement des fantômes
    - Blinky (fantome rouge): chasse toujours Pacman (chemin le plus direct), en visant la case du joueur
    - Pinky (fantome rose): essaie de coincer pacman en le contournant, en visant 4 cases devant Pacman
    - Inky (fantome bleu): vise selon un vecteur composé des positions de pacman et blinky, pour essayer
 de predire la position de pacman (direction de la fuite logique du joueur)
    - Clyde (fantome orange): chasse pacman comme blinky si ce dernier est loin (8 cases min) et prend une direction aléatoire sinon'''


'''Les fantomes ont plusieurs phases:
    - Chasse : les fantômes suivent leur algorithme de base de chasse de pacman (ci-dessus)
    - Scatter : les fantômes reviennent à leur base dans les coins du jeu, laissant le joueur tranquille
    - Peur : quand pacman a la super gomme, les fantomes le fuient'''

'''mouvement_fantome change les directions que prennent les fantomes en fonction 
de leur environnement (position, possibilité de mouvement, joueur, direction'''


def mouvement_fantome(Blinky, Pinky, Inky, Clyde, grille_mouv, size, joueur, vitesses, phase):
    Trad_mouv = {"aucune": (0, 0), "haut": (0, -1),
                 "bas": (0, 1), "gauche": (-1, 0), "droite": (1, 0)}

    # renvoie la position du joueur sur la grille
    case_joueur = case_actuelle(joueur)
    if phase[0] >= phase[1]:  # verifie le mode de jeu, si on est en mode 'scatter'
        # renvoient les cases visées par les fantômes (coins)
        case_visée_Blinky = (1, 26)
        case_visée_Pinky = (1, 1)
        case_visée_Inky = (29, 26)
        case_visée_Clyde = (29, 1)
    else:  # si on est en mode chasse
        # renvoient les cases visée par chaque fantome selon leur algorithme
        case_visée_Blinky = case_joueur
        case_visée_Pinky = case_visee_Pinky(case_joueur, joueur.direction)
        case_visée_Inky = case_visee_Inky(case_joueur, Blinky)
        case_visée_Clyde = None

    Blinky.frame += 1
    # le mouvement ne s'effectue pas si la frame n'est pas apparue (mouvement frame par frame)
    if Blinky.frame >= vitesses.Blinky[Blinky.vitesse.index(1)][0]:
        vitesses.Blinky[Blinky.vitesse.index(1)].rotate(-1)
        if not Blinky.depart:  # la sequence de départ est différente du comportement des fantômes
            if not Blinky.nouvelle_direction:  # on cherche une nouvelle direction si le fantome n'en a pas
                # comportement normal si le fantômes n'est pas appeuré (super gomme)
                if not Blinky.peur:
                    Blinky.nouvelle_direction = choix_dir(
                        Blinky, case_visée_Blinky, grille_mouv)  # cette fonction renvoie la direction à prendre en fonction de la position du fantome et du joueur(plus court chemin)
                else:
                    Blinky.nouvelle_direction = choix_dir_peur(
                        Blinky, case_joueur, grille_mouv)  # renvoie la direction à prendre pour s'éloigner de pacman

            Blinky.direction, Blinky.nouvelle_direction, Blinky.ancienne_direction = changement_fantome(
                Blinky, grille_mouv)  # changement de direction dans les données de fantome
        else:
            Blinky.direction = Blinky.depart.pop()
            if Blinky.direction == "changement":
                Blinky.vitesse[0] = 0
                Blinky.retour = 0
                Blinky.valeur.image = pygame.image.load(
                    "packages_textures/tunnel.png")  # montre le nombre de point lorque le fantôme est mangé
                Blinky.direction = Blinky.depart.pop()
                Blinky.peur = 0

        Blinky.frame = 0  # changement de frame du fantome, permettant le déplacement
        Blinky.vx, Blinky.vy = Trad_mouv[Blinky.direction]
        Blinky.rect.x = (Blinky.rect.x + Blinky.vx) % size[0]
        Blinky.rect.y = (Blinky.rect.y + Blinky.vy) % size[1]

    Pinky.frame += 1
    # le mouvement ne s'effectue pas si la frame n'est pas apparue (mouvement frame par frame)
    if Pinky.frame >= vitesses.Pinky[Pinky.vitesse.index(1)][0]:
        vitesses.Pinky[Pinky.vitesse.index(1)].rotate(-1)
        if not Pinky.depart:  # la sequence de départ est différente du comportement des fantômes
            if not Pinky.nouvelle_direction:  # on cherche une nouvelle direction si le fantome n'en a pas
                # comportement normal si le fantômes n'est pas appeuré (super gomme)
                if not Pinky.peur:
                    Pinky.nouvelle_direction = choix_dir(
                        Pinky, case_visée_Pinky, grille_mouv)  # cette fonction renvoie la direction à prendre en fonction de la position du fantome et du joueur(manoeuvre de contournement)
                else:
                    Pinky.nouvelle_direction = choix_dir_peur(
                        Pinky, case_joueur, grille_mouv)  # renvoie la direction à prendre pour s'éloigner de pacman

            Pinky.direction, Pinky.nouvelle_direction, Pinky.ancienne_direction = changement_fantome(
                Pinky, grille_mouv)
        else:
            Pinky.direction = Pinky.depart.pop()
            if Pinky.direction == "changement":
                Pinky.vitesse[0] = 0
                Pinky.retour = 0
                Pinky.valeur.image = pygame.image.load(
                    "packages_textures/tunnel.png")  # affiche les points lorsque mangé
                Pinky.direction = Pinky.depart.pop()
                Pinky.peur = 0

        Pinky.frame = 0  # changement de frame, permettant le mouvement
        Pinky.vx, Pinky.vy = Trad_mouv[Pinky.direction]
        Pinky.rect.x = (Pinky.rect.x + Pinky.vx) % size[0]
        Pinky.rect.y = (Pinky.rect.y + Pinky.vy) % size[1]

    # le mouvement ne s'effectue pas si la frame n'est pas apparue (mouvement frame par frame)
    Inky.frame += 1
    if Inky.frame >= vitesses.Inky[Inky.vitesse.index(1)][0]:
        vitesses.Inky[Inky.vitesse.index(1)].rotate(-1)
        if not Inky.depart:  # la sequence de départ est différente du comportement des fantômes
            if not Inky.nouvelle_direction:  # on cherche une nouvelle direction si le fantome n'en a pas
                # comportement normal si le fantômes n'est pas appeuré (super gomme)
                if not Inky.peur:
                    Inky.nouvelle_direction = choix_dir(
                        Inky, case_visée_Inky, grille_mouv)  # renvoie la direction ) prendre pour rejoindre un vecteur désigné par pacman et blinky
                else:
                    Inky.nouvelle_direction = choix_dir_peur(
                        Inky, case_joueur, grille_mouv)

            Inky.direction, Inky.nouvelle_direction, Inky.ancienne_direction = changement_fantome(
                Inky, grille_mouv)  # renvoie la direction à prendre pour s'éloigner de pacman
        else:
            Inky.direction = Inky.depart.pop()
            if Inky.direction == "changement":
                Inky.vitesse[0] = 0
                Inky.retour = 0
                Inky.valeur.image = pygame.image.load(
                    "packages_textures/tunnel.png")  # affiche les points lorsque mangé
                Inky.direction = Inky.depart.pop()
                Inky.peur = 0

        Inky.frame = 0  # changement de frame du fantome, permettant le déplacement
        Inky.vx, Inky.vy = Trad_mouv[Inky.direction]
        Inky.rect.x = (Inky.rect.x + Inky.vx) % size[0]
        Inky.rect.y = (Inky.rect.y + Inky.vy) % size[1]

    # le mouvement ne s'effectue pas si la frame n'est pas apparue (mouvement frame par frame)
    Clyde.frame += 1
    if Clyde.frame >= vitesses.Clyde[Clyde.vitesse.index(1)][0]:
        vitesses.Clyde[Clyde.vitesse.index(1)].rotate(-1)
        if not Clyde.depart:  # la sequence de départ est différente du comportement des fantômes
            if not Clyde.nouvelle_direction:  # on cherche une nouvelle direction si le fantome n'en a pas
                # comportement normal si le fantômes n'est pas appeuré (super gomme)
                if not Clyde.peur:
                    if case_visée_Clyde:  # verification du mode (scatter)
                        Clyde.nouvelle_direction = choix_dir(
                            Clyde, case_visée_Clyde, grille_mouv)  # retour à la base
                    else:
                        # vérification de la position (si trop proche, choix random, sinon chase)
                        ci, cj = case_actuelle(Clyde)
                        ji, jj = case_joueur
                        if ((ci - ji) < 8) and (cj - jj):
                            Clyde.nouvelle_direction = "aucune"
                            while Clyde.nouvelle_direction == "aucune" or Clyde.nouvelle_direction == Clyde.direction:
                                Clyde.nouvelle_direction = rd.choice(
                                    ["haut", "bas", "gauche", "droite"])  # choix aléatoire, boucle pour éviter que le fantôme ne s'arrête si il renvoie unee direction impossible
                        else:
                            Clyde.nouvelle_direction = choix_dir(
                                Clyde, case_joueur, grille_mouv)  # chase

                else:
                    Clyde.nouvelle_direction = choix_dir_peur(
                        Clyde, case_joueur, grille_mouv)  # direction à prendre pour s'éloigner de pacman

            Clyde.direction, Clyde.nouvelle_direction, Clyde.ancienne_direction = changement_fantome(
                Clyde, grille_mouv)  # changement direction

        else:
            Clyde.direction = Clyde.depart.pop()
            if Clyde.direction == "changement":
                Clyde.vitesse[0] = 0
                Clyde.retour = 0
                Clyde.valeur.image = pygame.image.load(
                    "packages_textures/tunnel.png")  # affichage points
                Clyde.direction = Clyde.depart.pop()
                Clyde.peur = 0

        Clyde.frame = 0  # changement de frame => mouvement
        Clyde.vx, Clyde.vy = Trad_mouv[Clyde.direction]
        Clyde.rect.x = (Clyde.rect.x + Clyde.vx) % size[0]
        Clyde.rect.y = (Clyde.rect.y + Clyde.vy) % size[1]


'''choix_dir_peur renvoie la direction (possible) à prendre pour pour s'éloigner de pacman. 
Pour cela, elle classe les distances à pacman des chemins par rapport aux cases où le fantome peut aller possiblement,
 et renvoie la direction possible dont la distance est la plus élevée '''


def choix_dir_peur(fantome, case_joueur, grille_mouv):
    Deplacement_inv = {'haut': 1, 'bas': 0, 'gauche': 3, 'droite': 2}

    (ji, jj) = case_joueur  # renvoie case du joueur
    (fi, fj) = case_actuelle(fantome)  # case du fantome
    act = fantome.direction
    anc = fantome.ancienne_direction
    if act == 'haut':  # permet d'éviter les calculs de directions qui ne nous intéressent pas, ici bas car le fantome a un mouvemnt vers le haut
        long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]],
                [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]], [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]
# distance 2 de la possible duture case à pacman, direction associée, et possibilité du mouvement
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

    # évite de prioriser une direction par rapport à une autre
    rd.shuffle(long)
    # trie la liste par distance la plus grande
    dist = sorted(long, key=itemgetter(0), reverse=True)
    # verifie que la direction peut être emprunter, sinon essaie la seconde meilleure
    for k in range(len(dist)):
        if dist[k][2] == True:
            dir = dist[k][1]
            break
    return dir


def case_actuelle(joueur):  # renvoie la case actuelle (grille i,j)
    centerx = joueur.rect.centerx
    centery = joueur.rect.centery
    # case de 14 pixels, %28 permet de ramener la dernière case vers la première case, permettant de comprendre la téléportation
    return ((centery//14) % 31, (centerx//14) % 28)


def case_visee_Pinky(case_joueur, direction):  # renvoie la case 4 case devant pacman
    (ji, jj) = case_joueur
    Trad = {'haut': [-1, 0], 'bas': [1, 0],
            'gauche': [0, -1], 'droite': [0, 1], 'aucune': [0, 0]}
    add = Trad[direction]
    ji, jj = ji + 4*add[0], jj + 4*add[1]
    if ji == 14:  # téléportation, la case à gauche est équivalente à  celle de droite
        jj = jj % 28
    else:  # vérifie que la case est dans la grille, prend la case la plus prpche sinon
        if jj > 26:
            jj = 26
        if jj < 1:
            jj = 1
        if ji > 29:
            ji = 29
        if ji < 1:
            ji = 1
    return (ji, jj)


# renvoie la case définie par la case de blinky et le vecteur défini par le double de position entre pacman et blinky
def case_visee_Inky(case_joueur, Blinky):
    (ji, jj) = case_joueur
    (bi, bj) = case_actuelle(Blinky)
    ci = (ji - bi)*2
    cj = (jj - bj)*2
    if cj > 26:
        cj = 26
    if cj < 1:
        cj = 1
    if ci > 29:
        ci = 29
    if ci < 1:
        ci = 1
    return (ci, cj)


'''choix_dir_peur renvoie la direction (possible) à prendre pour pour s'approcher de la case visée. 
Pour cela, elle classe les distances à la case des chemins par rapport aux cases où le fantome peut aller possiblement,
 et renvoie la direction possible dont la distance est la plus courte '''


def choix_dir(fantome, case_visée, grille_mouv):

    Deplacement_inv = {'haut': 1, 'bas': 0, 'gauche': 3, 'droite': 2}

    (ji, jj) = case_visée
    (fi, fj) = case_actuelle(fantome)
    act = fantome.direction
    anc = fantome.ancienne_direction
    if act == 'haut':  # permet d'éviter les calculs de directions qui ne nous intéressent pas, ici bas car le fantome a un mouvemnt vers le haut
        long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]],
                [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]], [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]
# distance 2 de la possible duture case à pacman, direction associée, et possibilité du mouvement
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

    rd.shuffle(long)  # evite de prioriser une direction
    dist = sorted(long, key=itemgetter(0))
    for k in range(len(dist)):  # vérifie que la direction est bien possible, puis la renvoie
        if dist[k][2] == True:
            dir = dist[k][1]
            break
    return dir


def choix_dir_test(case_fantome, case_visée, grille_mouv):  # créée pour le test

    Deplacement_inv = {'haut': 1, 'bas': 0, 'gauche': 3, 'droite': 2}

    (ji, jj) = case_visée
    (fi, fj) = case_fantome

    long = [[(fi-1-ji)**2 + (fj - jj)**2, 'haut', grille_mouv[fi][fj][0]], [((fi + 1 - ji)**2 + (fj - jj)**2), 'bas', grille_mouv[fi][fj][1]],
            [((fi - ji)**2 + (fj - 1 - jj)**2), 'gauche', grille_mouv[fi][fj][2]], [(fi - ji)**2 + (fj + 1 - jj)**2, 'droite', grille_mouv[fi][fj][3]]]

    rd.shuffle(long)  # evite de prioriser une direction
    dist = sorted(long, key=itemgetter(0))
    for k in range(len(dist)):  # vérifie que la direction est bien possible, puis la renvoie
        if dist[k][2] == True:
            dir = dist[k][1]
            break
    return dir
