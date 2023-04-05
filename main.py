# Coucou les plantes !
from re import I
import pygame
import numpy as np
from jeu.init import*
from jeu.entité import *
from jeu.end import *
from jeu.changement import *
from jeu.grille_init_gum import *
from jeu.grille_mouv import*
from jeu.annonces import*
from jeu.mouvement_fantome import *
from jeu.mouvement_joueur import *
from jeu.textures import *
from jeu.menu import *
from jeu.fruit_tunnel import *
from jeu.db import *
from jeu.collision import *
import csv


def mainloop(continuer=True):  # boucle principale du jeu
    global vies, niveau, score, groupe_gum, groupe_super_gum, groupe_tunnel, groupe_fin_tunnel, fenetre, fenetre_globale, fenetre_score, fenetre_vies, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, RG

    # affiche les vies et le niveau au début du jeu
    annonce_vies(fenetre_vies, vies, niveau)
    fenetre_globale.blit(fenetre_vies, (0, size[1] + 100))

    # recherche les parmètres utilisés dans le niveau
    fruit_niveau, previtesses, temps_peur, colere = selection_paramètres(
        niveau)
    vitesses = Vitesse(previtesses)
    # initialise les variables locales à la loop
    mode = 0
    frame = 0
    bonus = 200
    phase = [30*fps, 25*fps]
    delai = 3*fps
    apparition = rd.randint(150, 180)

    while continuer:
        # demande à la boucle de travailler avec le nombre de fps voulu
        clock.tick(fps)

        # regarde si l'on ferme le jeu ou si une pause est demandée
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and mode == 0:
                fenetre.blit(image_grille, (0, 0))
                annonce_pause(fenetre, position_annonce)
                mode = 2

        # récupere les evenements
        key = pygame.key.get_pressed()

        if mode == 0:  # mode jeu
            fenetre.blit(image_grille, (0, 0))
            groupe_fruit.draw(fenetre)
            groupe_valeur.draw(fenetre)

            # regarde si on a gagner on si on est game-over
            if Game_Over(vies):
                mode = 1
                annonce_game_over(fenetre, position_annonce)
                continue

            elif Victoire(groupe_gum, groupe_super_gum):
                mode = 4
                annonce_victoire(fenetre, position_annonce)
                delai = -1

            # vérifie l'appuie des fléhes
            if key[pygame.K_UP]:
                Joueur.nouvelle_direction = "haut"

            elif key[pygame.K_DOWN]:
                Joueur.nouvelle_direction = "bas"

            elif key[pygame.K_LEFT]:
                Joueur.nouvelle_direction = "gauche"

            elif key[pygame.K_RIGHT]:
                Joueur.nouvelle_direction = "droite"

            if not delai:  # permet d'attendre lorsque la partie se lance ou que l'on perd une vie

                frame += 1
                if frame == 15:  # aniation des sprites toutes les 15 secondes
                    frame = 0
                    Joueur.anim()
                    for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                        if not fantome.retour:
                            fantome.anim()

                if phase[0]:  # coordonne le mouvement des fantomes en phases ou ils cherchent Pac-Man et ou ils vont dans les coins
                    phase[0] -= 1
                else:
                    phase[0] = 30*fps
                    phase[1] = rd.randint(24*fps, 27*fps)

                # ralenti les fantomes dans le tunnel
                ralentissement_tunnel(
                    groupe_fantome, groupe_tunnel, groupe_fin_tunnel)

                # fait apparaitre les fruits et met Blinky en colere
                n = len(pygame.sprite.Group.sprites(groupe_gum))
                if n == apparition:
                    if not pygame.sprite.Group.sprites(groupe_fruit):
                        groupe_fruit.add(
                            Fruit((position_base[0] + 3, position_base[1]), fruit_niveau))
                        apparition += 1
                if n <= colere:
                    Blinky.vitesse[3] = 1

                # fait bouger les entités

                mouvement_fantome(Blinky, Pinky, Inky, Clyde, Grille_mouv,
                                  size, Joueur, vitesses, phase)

                mouvement_joueur(Joueur, Grille_mouv, size)

                # mange les gommes
                score, bonus, apparition = manger(Joueur, groupe_gum,
                                                  groupe_super_gum, groupe_fantome, groupe_fruit, fps, bonus, Val_bon, score, apparition, temps_peur)

                # gére les collisions et le bonus
                if Joueur.pouvoir:
                    Joueur.pouvoir -= 1
                    if Joueur.pouvoir == fps:
                        for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                            fantome.texture_act_peur = [0, 4]
                    if not Joueur.pouvoir:
                        for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                            fantome.peur = 0
                            fantome.vitesse[2] = 0
                            if not fantome.retour:
                                fantome.anim()

                    for fantome in collision_fantome(Joueur, groupe_fantome):
                        if fantome.peur:
                            if fantome.peur == 1:
                                fantome.peur = 2
                                score += bonus
                                fantome.vitesse[2] = 0
                                fantome.mort(Grille_mouv, bonus)
                                bonus *= 2
                        else:  # réinitialise les entités
                            vies -= 1
                            delai = 3*fps
                            reinitialisation(Joueur, groupe_fantome)
                            annonce_vies(fenetre_vies, vies, niveau)
                            fenetre_globale.blit(
                                fenetre_vies, (0, size[1] + 100))
                            for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                                fantome.peur = 0
                                fantome.retour = 0
                                fantome.valeur.image = pygame.image.load(
                                    "packages_textures/tunnel.png")
                                fantome.vitesse[2] = 0
                            Joueur.pouvoir = 0

                elif collision_fantome(Joueur, groupe_fantome):
                    vies -= 1
                    delai = 3*fps
                    reinitialisation(Joueur, groupe_fantome)
                    annonce_vies(fenetre_vies, vies, niveau)
                    fenetre_globale.blit(fenetre_vies, (0, size[1] + 100))
                    for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                        fantome.peur = 0
                        fantome.retour = 0
                        fantome.valeur.image = pygame.image.load(
                            "packages_textures/tunnel.png")
                        fantome.vitesse[2] = 0

            elif delai > 0:  # au début d'une partie ou lorsquel'on perd une vie
                delai -= 1
                annonce_pret(fenetre, position_annonce)

        elif mode == 1:  # lorsque l'on est game-over

            if score > Rp:
                Rp = score
            if niveau > Nm:
                Nm = niveau
            if Rp > int(RG[1]):
                RG[1] = Rp
                RG[2] = Id
                RG = RG[:3]
            elif Id not in RG and Rp == int(RG[1]):
                RG.append(Id)

            création(Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)
            _, _, _, _, _, _, _, NJ = verif(Id, Mdp)

            if key[pygame.K_SPACE]:

                # réinitialise le jeu en envoyant sur le menu
                Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, niveau = menu(
                    fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)
                if niveau > 1:
                    score = Scs
                    vies = Vs
                else:
                    score = 0
                    vies = 3
                if niveau:
                    annonce_vies(fenetre_vies, vies, niveau)
                    fenetre_globale.blit(fenetre_vies, (0, size[1] + 100))

                    groupe_tunnel.empty()
                    groupe_fruit.empty()
                    reinitialisation(Joueur, groupe_fantome)

                    groupe_gum, groupe_super_gum, groupe_tunnel, groupe_fin_tunnel = placement_gum(
                        Grille)
                    fruit_niveau, previtesses, temps_peur, colere = selection_paramètres(
                        niveau)
                    vitesses = Vitesse(previtesses)
                    for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                        fantome.peur = 0
                        fantome.retour = 0
                        fantome.valeur.image = pygame.image.load(
                            "packages_textures/tunnel.png")
                        fantome.vitesse[2] = 0
                    Joueur.pouvoir = 0

                    mode = 0
                    delai = 3*fps

                else:
                    continuer = False

        elif mode in {2, 3}:  # lorsque le jeu est en pause
            if not key[pygame.K_SPACE]:  # attend que espace soit laché
                mode = 3
            if key[pygame.K_SPACE] and mode == 3:
                mode = 0
        else:
            if score > Rp:
                Rp = score
            if niveau > Nm:
                Nm = niveau
            if Rp > int(RG[1]):
                RG[1] = Rp
                RG[2] = Id
                RG = RG[:3]
            elif Id not in RG and Rp == int(RG[1]):
                RG.append(Id)

            création(Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)
            _, _, _, _, _, _, _, NJ = verif(Id, Mdp)

            if pygame.key.get_pressed()[pygame.K_s]:
                Ns, Vs, Scs = niveau+1, vies, score

            if key[pygame.K_SPACE]:  # réinitialise le niveu après une victoire

                niveau += 1
                annonce_vies(fenetre_vies, vies, niveau)
                fenetre_globale.blit(fenetre_vies, (0, size[1] + 100))

                groupe_tunnel.empty()
                groupe_fruit.empty()
                reinitialisation(Joueur, groupe_fantome)

                groupe_gum, groupe_super_gum, groupe_tunnel, groupe_fin_tunnel = placement_gum(
                    Grille)
                fruit_niveau, previtesses, temps_peur, colere = selection_paramètres(
                    niveau)
                vitesses = Vitesse(previtesses)
                for fantome in pygame.sprite.Group.sprites(groupe_fantome):
                    fantome.peur = 0
                    fantome.retour = 0
                    fantome.valeur.image = pygame.image.load(
                        "packages_textures/tunnel.png")
                    fantome.vitesse = [0, 0, 0, 0, 1]
                Joueur.pouvoir = 0

                mode = 0
                delai = 3*fps
            continue

        # affiche les éléments du jeu

        annonce_score(fenetre_score, score, Rp, RG[1], Id)
        groupe_super_gum.draw(fenetre)
        groupe_gum.draw(fenetre)
        groupe_bonus.draw(fenetre)
        groupe_joueur.draw(fenetre)
        groupe_fantome.draw(fenetre)
        fenetre_globale.blit(fenetre_score, (0, 0))
        fenetre_globale.blit(fenetre, (0, 100))
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()  # initialistion pygame
    clock = pygame.time.Clock()  # horloge du jeu
    fps = 280   # fps du jeu

    # mise en place de la musique

    pygame.mixer.init()
    MUSIQUE = pygame.mixer.music.load("musique.mp3")
    pygame.mixer.music.play(10, 0.0)

    # initialisation des variables globales

    vies = 3
    score = 0
    niveau = 1
    NJ = 0  # numéro du joueur (0 s'il n'est pas identifié)

    with open('DB.csv', 'r+') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.reader(f)
        for i in obj:
            pass
        RG = i

    # initialisation des grilles et des variable liées

    Grille, position, position_base = init_grille()
    Grille_mouv = init_grille_mouv(Grille)
    position_annonce = (position_base[0] + 3.5)*14
    nb_lignes, nb_colonnes = np.shape(Grille)
    size = [14*nb_colonnes, 14*nb_lignes]

    # initialisation de la fenetre d'affichage

    fenetre_globale = pygame.display.set_mode((size[0], size[1] + 170))
    pygame.display.set_caption("Plant-man")

    fenetre_globale.fill((0, 0, 0))

    fenetre = pygame.Surface(size)
    fenetre_score = pygame.Surface((size[0], 100))
    fenetre_vies = pygame.Surface((size[0], 70))

    # importtion des textures des murs

    textures = ouvertures()

    # déclaration des fantomes et de Pac-Man

    Joueur = Plant_man(position)

    Blinky = Fantome(
        (position_base[0] - 3, position_base[1]), "red")
    Pinky = Fantome(
        (position_base[0], position_base[1]), "pink")
    Inky = Fantome(
        (position_base[0], position_base[1] - 2), "blue")
    Clyde = Fantome(
        (position_base[0], position_base[1] + 2), "orange")

    # déclaration des groupes d'objets à faie apparaitre au cour du jeu

    groupe_joueur = pygame.sprite.Group()
    groupe_joueur.add(Joueur)

    groupe_fantome = pygame.sprite.Group()
    groupe_fantome.add(Blinky)
    groupe_fantome.add(Pinky)
    groupe_fantome.add(Inky)
    groupe_fantome.add(Clyde)

    groupe_gum, groupe_super_gum, groupe_tunnel, groupe_fin_tunnel = placement_gum(
        Grille)

    groupe_fruit = pygame.sprite.Group()
    groupe_valeur = pygame.sprite.Group()
    groupe_valeur.add(Blinky.valeur)
    groupe_valeur.add(Pinky.valeur)
    groupe_valeur.add(Inky.valeur)
    groupe_valeur.add(Clyde.valeur)

    groupe_bonus = pygame.sprite.Group()
    Val_bon = Valeur((fenetre.get_rect().centerx, position_annonce), "tunnel")
    groupe_bonus.add(Val_bon)

    # conversion d'une grille numérique en image de fond, export et réimport pour la fluidité du jeu

    dessin_grille(Grille, fenetre, nb_lignes,
                  nb_colonnes, textures)

    pygame.image.save(fenetre, "packages_textures/fond_grille.png")
    image_grille = pygame.image.load(
        "packages_textures/fond_grille.png").convert_alpha()

    # envoie sur le menu puis lance la boucle principale
    Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, niveau = menu(fenetre_globale)
    if niveau > 1:
        score = Scs
        vies = Vs
    else:
        score = 0
    if niveau:
        mainloop()

    création(Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)

    pygame.quit()
