from PIL import Image
import PIL
from numpy.testing._private.utils import HAS_REFCOUNT
import pygame
import random as rd
import time
import copy
import numpy as np
import pyperclip


def dessin_nb():
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    center_x, center_y = 120, 100

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS,Arial', 24)
    prompt = font.render('Nombre de lignes: ', True, (255, 255, 255))
    prompt_rect = prompt.get_rect(center=(center_x, center_y))

    ligne_input_value = ""
    ligne_input = font.render(ligne_input_value, True, (255, 255, 255))
    ligne_input_rect = ligne_input.get_rect(topleft=prompt_rect.topright)

    continuer = True

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    continuer = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    ligne_input_value = ligne_input_value[:-1]
                else:
                    ligne_input_value += event.unicode
                ligne_input = font.render(
                    ligne_input_value, True, (255, 255, 255))
                ligne_input_rect = ligne_input.get_rect(
                    topleft=prompt_rect.topright)

        screen.fill(0)
        screen.blit(prompt, prompt_rect)
        screen.blit(ligne_input, ligne_input_rect)
        pygame.display.flip()

        clock.tick(30)

    font = pygame.font.SysFont('Comic Sans MS,Arial', 24)
    prompt = font.render('Nombre de colonnes: ', True, (255, 255, 255))
    prompt_rect = prompt.get_rect(center=(center_x, center_y))

    colonne_input_value = ""
    colonne_input = font.render(colonne_input_value, True, (255, 255, 255))
    colonne_input_rect = colonne_input.get_rect(topleft=prompt_rect.topright)

    continuer = True

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    continuer = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    colonne_input_value = colonne_input_value[:-1]
                else:
                    colonne_input_value += event.unicode
                colonne_input = font.render(
                    colonne_input_value, True, (255, 255, 255))
                colonne_input_rect = colonne_input.get_rect(
                    topleft=prompt_rect.topright)
            clock.tick(30)

        screen.fill(0)
        screen.blit(prompt, prompt_rect)
        screen.blit(colonne_input, colonne_input_rect)
        pygame.display.flip()

    ligne = int(ligne_input_value)
    colonne = int(colonne_input_value)

    pygame.quit()

    pygame.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    h = min(40, (width-10)//colonne, (height-100)//ligne)
    print(h)
    screen = pygame.display.set_mode((h*colonne, h*ligne))
    center_x, center_y = 100, 100

    clock = pygame.time.Clock()
    Grille = np.zeros((ligne, colonne), dtype=int)

    continuer = True
    while continuer:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break

        if pygame.mouse.get_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()
            Grille[mouse_position[1]//h, mouse_position[0]//h] = 1
        if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_a]:
            mouse_position = pygame.mouse.get_pos()
            Grille[mouse_position[1]//h, mouse_position[0]//h] = 0

        screen.fill(0)
        for i in range(ligne):
            for j in range(colonne):
                if Grille[i, j]:
                    pygame.draw.rect(screen, (0,  0, 255), pygame.Rect(
                        h*j, h*i, h-2, h-2))
                else:
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(
                        h*j, h*i, h-2, h-2))

        pygame.display.flip()

    Grille = str([list(ligne) for ligne in list(Grille)])
    Grille = Grille.replace("],", "],\n")
    pyperclip.copy(Grille)
    pygame.quit()


def propag(grid, couleur, mouse_position, h, long, larg):
    anc = grid[mouse_position[1]//h, mouse_position[0]//h]
    grid[mouse_position[1]//h, mouse_position[0]//h] = couleur

    done = True
    while done:
        done = False
        for i in range(long):
            for j in range(larg):
                if grid[i, j] == couleur:
                    if grid[i, j-1] == anc:
                        grid[i, j-1] = couleur
                        done = True
                    if grid[i-1, j] == anc:
                        grid[i-1, j] = couleur
                        done = True
                    if grid[i+1, j] == anc:
                        grid[i+1, j] = couleur
                        done = True
                    if grid[i, j+1] == anc:
                        grid[i, j+1] = couleur
                        done = True


def dessin_couleur():
    pygame.init()
    screen = pygame.display.set_mode((300, 200))
    center_x, center_y = 120, 100

    couleur = [0,  0, 214, 255]

    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Comic Sans MS,Arial', 24)
    prompt = font.render('Nombre de lignes: ', True, (255, 255, 255))
    prompt_rect = prompt.get_rect(center=(center_x, center_y))

    ligne_input_value = ""
    ligne_input = font.render(ligne_input_value, True, (255, 255, 255))
    ligne_input_rect = ligne_input.get_rect(topleft=prompt_rect.topright)

    continuer = True

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    continuer = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    ligne_input_value = ligne_input_value[:-1]
                else:
                    ligne_input_value += event.unicode
                ligne_input = font.render(
                    ligne_input_value, True, (255, 255, 255))
                ligne_input_rect = ligne_input.get_rect(
                    topleft=prompt_rect.topright)

        screen.fill(0)
        screen.blit(prompt, prompt_rect)
        screen.blit(ligne_input, ligne_input_rect)
        pygame.display.flip()

        clock.tick(30)

    font = pygame.font.SysFont('Comic Sans MS,Arial', 24)
    prompt = font.render('Nombre de colonnes: ', True, (255, 255, 255))
    prompt_rect = prompt.get_rect(center=(center_x, center_y))

    colonne_input_value = ""
    colonne_input = font.render(colonne_input_value, True, (255, 255, 255))
    colonne_input_rect = colonne_input.get_rect(topleft=prompt_rect.topright)

    continuer = True

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    continuer = False
                    break
                elif event.key == pygame.K_BACKSPACE:
                    colonne_input_value = colonne_input_value[:-1]
                else:
                    colonne_input_value += event.unicode
                colonne_input = font.render(
                    colonne_input_value, True, (255, 255, 255))
                colonne_input_rect = colonne_input.get_rect(
                    topleft=prompt_rect.topright)
            clock.tick(30)

        screen.fill(0)
        screen.blit(prompt, prompt_rect)
        screen.blit(colonne_input, colonne_input_rect)
        pygame.display.flip()

    ligne = int(ligne_input_value)
    colonne = int(colonne_input_value)

    pygame.quit()

    pygame.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    h = min(40, (width-10)//colonne, (height-150)//ligne)
    screen = pygame.display.set_mode((h*colonne, h*ligne + 50))
    center_x, center_y = 100, 100

    clock = pygame.time.Clock()
    im = PIL.Image.open("packages_textures/2000.png")
    Grille = np.array(im)
    """[[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,  0, 1],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  1,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  1,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  1,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  1,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  1,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  1,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  1,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  1,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]"""
    """[[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0, 1],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 0,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
                    [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]"""

    #Grille[:, :,  0] = Grille[:, :,  0].dot(rot)
    #Grille[:, :, 1] = Grille[:, :, 1].dot(rot)
    #Grille[:, :,  2] = Grille[:, :,  2].dot(rot)
    #Grille[:, :,  3] = Grille[:, :,  3].dot(rot)
    #Grille = np.zeros((ligne, colonne, 4), dtype=int)
    #Grille[:, :,  0] = Grille[:, :,  0].transpose()
    #Grille[:, :, 1] = Grille[:, :, 1].transpose()
    #Grille[:, :,  2] = Grille[:, :,  2].transpose()
    #Grille[:, :,  3] = Grille[:, :,  3].transpose()
    print(np.shape(Grille))
    continuer = True
    while continuer:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                break

        if pygame.key.get_pressed()[pygame.K_w]:
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                couleur = Grille[mouse_position[1]//h, mouse_position[0]//h]
                print(couleur)
        elif pygame.key.get_pressed()[pygame.K_x]:
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                propag(Grille, couleur, mouse_position, h, ligne, colonne)
        else:
            if pygame.mouse.get_pressed()[0]:
                mouse_position = pygame.mouse.get_pos()
                Grille[mouse_position[1]//h, mouse_position[0]//h] = couleur
            if pygame.mouse.get_pressed()[0] and pygame.key.get_pressed()[pygame.K_q]:
                mouse_position = pygame.mouse.get_pos()
                Grille[mouse_position[1]//h,
                       mouse_position[0]//h] = [0,  0,  0,  0]

        if pygame.key.get_pressed()[pygame.K_r]:
            couleur[0] = (couleur[0] + 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_e]:
            couleur[0] = (couleur[0] - 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_g]:
            couleur[1] = (couleur[1] + 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_f]:
            couleur[1] = (couleur[1] - 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_b]:
            couleur[2] = (couleur[2] + 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_v]:
            couleur[2] = (couleur[2] - 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_t]:
            couleur[4] = (couleur[4] - 1) % 255
            print(couleur)
        if pygame.key.get_pressed()[pygame.K_p]:
            couleur = [255, 255, 255, 255]
            print(couleur)
        # bleu marine
        if pygame.key.get_pressed()[pygame.K_n]:
            couleur = [0,  0, 90, 255]
            print(couleur)
        # bleu ciel
        if pygame.key.get_pressed()[pygame.K_m]:
            couleur = [221, 191, 171, 255]
            print(couleur)
        # orange
        if pygame.key.get_pressed()[pygame.K_o]:
            couleur = [254, 138,  0, 255]
            print(couleur)
        # rose
        if pygame.key.get_pressed()[pygame.K_l]:
            couleur = [254, 69, 137, 255]
            print(couleur)
        # rouge
        if pygame.key.get_pressed()[pygame.K_k]:
            couleur = [19, 167, 254, 255]
            print(couleur)

        screen.fill((255, 255, 255))
        for i in range(ligne):
            for j in range(colonne):
                pygame.draw.rect(screen, Grille[i, j, :3], pygame.Rect(
                    h*j, h*i, h-2, h-2))
                pygame.draw.rect(screen, Grille[i, j, :3], pygame.Rect(
                    h*j, h*i, h-2, h-2))
                if Grille[i, j,  3] == 0:
                    pygame.draw.rect(screen, "red", pygame.Rect(
                        h*j, h*i, h-5, h-5))

        pygame.draw.rect(screen, couleur, pygame.Rect(
            50, h*(i+1), h-2, h-2))

        pygame.display.flip()

    IM = Grille.astype('uint8')
    im = Image.fromarray(IM, mode='RGBA')
    im.save("packages_textures/5000.png")


def changement(grid, couleur, anc, h, long, larg):

    done = True
    while done:
        done = False
        for i in range(long):
            for j in range(larg):
                if list(grid[i, j]) == couleur:
                    grid[i, j] = anc


def transpose():
    Trad = {"orange": [254, 138, 0, 255],
            "red": [254, 56, 78, 255], "pink": [254, 69, 137, 255]}
    for dir in ["h", "g", "b", "d"]:
        for i in range(1, 4):
            for cou in ["orange", "pink", "red"]:
                im = PIL.Image.open(
                    "packages_textures/fantome{}{}{}.png".format(str(cou), str(dir), str(i)))
                Grille = np.array(im)

                changement(Grille, [0, 160, 253, 255], Trad[cou], 2, 26, 26)

                IM = Grille.astype('uint8')
                im = Image.fromarray(IM, mode='RGBA')
                im.save(
                    "packages_textures/fantome{}{}{}.png".format(str(cou), str(dir), str(i)))


dessin_couleur()
