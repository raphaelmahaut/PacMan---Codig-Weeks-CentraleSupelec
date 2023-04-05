import pygame
from main import mainloop
from jeu.db import*


# Affiche la fenêtre de menu
def menu(fenetre_globale, Id="Anonyme", Mdp="", Rp=0, Nm=1, Ns=1, Vs=3, Scs=0, NJ=0, quit=False):

    _, _, Rp, Nm, _, _, _, NJ = verif(
        Id, Mdp)

    fenetre_globale.fill(0)
    hauteur = fenetre_globale.get_size()[1]//4
    if Ns != 1:
        hauteur = fenetre_globale.get_size()[1]//5

        bt_charger = pygame.Surface((200, 50))
        bt_charger.fill((195, 195, 195))
        rect_charger = bt_charger.get_rect()
        rect_charger.centerx = fenetre_globale.get_rect().centerx
        rect_charger.centery = 4*hauteur
        fenetre_globale.blit(bt_charger, rect_charger)

        bt_charger2 = pygame.Surface((194, 44))
        bt_charger2.fill(0)
        rect_charger2 = bt_charger2.get_rect()
        rect_charger2.centerx = fenetre_globale.get_rect().centerx
        rect_charger2.centery = 4*hauteur
        fenetre_globale.blit(bt_charger2, rect_charger2)

        font = pygame.font.Font(None, 24)
        text = font.render("Reprendre", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_charger.centerx
        rect_text.centery = rect_charger.centery
        fenetre_globale.blit(text, rect_text)

    bt_login = pygame.Surface((200, 50))
    bt_login.fill((195, 195, 195))
    rect_login = bt_login.get_rect()
    rect_login.centerx = fenetre_globale.get_rect().centerx
    rect_login.centery = hauteur
    fenetre_globale.blit(bt_login, rect_login)

    bt_login2 = pygame.Surface((194, 44))
    bt_login2.fill(0)
    rect_login2 = bt_login2.get_rect()
    rect_login2.centerx = fenetre_globale.get_rect().centerx
    rect_login2.centery = hauteur
    fenetre_globale.blit(bt_login2, rect_login2)

    # Bouton "Login" pour s'identifier
    font = pygame.font.Font(None, 24)
    text = font.render("Identification", 1, (195, 195, 195))
    rect_text = text.get_rect()
    rect_text.centerx = rect_login.centerx
    rect_text.centery = rect_login.centery
    fenetre_globale.blit(text, rect_text)

    bt_original = pygame.Surface((40, 45))
    bt_original.fill((195, 195, 195))
    rect_original = bt_original.get_rect()
    rect_original.centerx = 30
    rect_original.centery = 30
    fenetre_globale.blit(bt_original, rect_original)

    bt_original2 = pygame.Surface((34, 39))
    bt_original2.fill(0)
    rect_original2 = bt_original2.get_rect()
    rect_original2.centerx = 30
    rect_original2.centery = 30
    fenetre_globale.blit(bt_original2, rect_original2)

    bt_original = pygame.Surface((24, 4))
    bt_original.fill((195, 195, 195))
    rect_original = bt_original.get_rect()
    rect_original.centerx = 30
    rect_original.centery = 20
    fenetre_globale.blit(bt_original, rect_original)

    bt_original = pygame.Surface((24, 4))
    bt_original.fill((195, 195, 195))
    rect_original = bt_original.get_rect()
    rect_original.centerx = 30
    rect_original.centery = 30
    fenetre_globale.blit(bt_original, rect_original)

    bt_original = pygame.Surface((24, 4))
    bt_original.fill((195, 195, 195))
    rect_original = bt_original.get_rect()
    rect_original.centerx = 30
    rect_original.centery = 40
    fenetre_globale.blit(bt_original, rect_original)

    bt_original = pygame.Surface((200, 50))
    bt_original.fill((195, 195, 195))
    rect_original = bt_original.get_rect()
    rect_original.centerx = fenetre_globale.get_rect().centerx
    rect_original.centery = 2*hauteur
    fenetre_globale.blit(bt_original, rect_original)

    bt_original2 = pygame.Surface((194, 44))
    bt_original2.fill(0)
    rect_original2 = bt_original2.get_rect()
    rect_original2.centerx = fenetre_globale.get_rect().centerx
    rect_original2.centery = 2*hauteur
    fenetre_globale.blit(bt_original2, rect_original2)

    bt_score = pygame.Surface((200, 50))
    bt_score.fill((195, 195, 195))
    rect_score = bt_score.get_rect()
    rect_score.centerx = fenetre_globale.get_rect().centerx
    rect_score.centery = 3*hauteur
    fenetre_globale.blit(bt_score, rect_score)

    bt_score2 = pygame.Surface((194, 44))
    bt_score2.fill(0)
    rect_score2 = bt_score2.get_rect()
    rect_score2.centerx = fenetre_globale.get_rect().centerx
    rect_score2.centery = 3*hauteur
    fenetre_globale.blit(bt_score2, rect_score2)

    # Bouton "Pac-Man" pour lancer le jeu
    font = pygame.font.Font(None, 24)
    text = font.render("Pac-Man", 1, (195, 195, 195))
    rect_text = text.get_rect()
    rect_text.centerx = rect_original.centerx
    rect_text.centery = rect_original.centery
    fenetre_globale.blit(text, rect_text)

    # Bouton "Aide" pour afficher les règles du jeu
    font = pygame.font.Font(None, 24)
    text = font.render("Aide", 1, (195, 195, 195))
    rect_text = text.get_rect()
    rect_text.centerx = rect_score.centerx
    rect_text.centery = rect_score.centery
    fenetre_globale.blit(text, rect_text)

    while True:
        if quit:
            return Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        if (pos[1] - 25)//hauteur == 1 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                            return Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, 1

                        if 10 < pos[1] < 55 and 10 < pos[0] < 50:
                            return statistiques(fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)

                        if (pos[1] - 25)//hauteur == 2 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                            aide(fenetre_globale, Id, Mdp,
                                 Rp, Nm, Ns, Vs, Scs, NJ)

                        if Ns != 1:
                            if (pos[1] - 25)//hauteur == 3 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                                return Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, Ns

                        if (pos[1] - 25)//hauteur == 0 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                            return login(fenetre_globale)

        pygame.display.flip()


# Fonction lancée lorsqu'on clique sur "Login" : permet de rentrer son pseudo et son mot de passe
def login(fenetre_globale):

    clock = pygame.time.Clock()
    hauteur = fenetre_globale.get_size()[1]//7
    largeur = fenetre_globale.get_size()[0]//2
    choix = 1
    font = pygame.font.Font(None, 24)
    prompt1 = font.render('Mot de passe: ', True, (195, 195, 195))
    message_mdp = prompt1.get_rect(center=(largeur - 85, 2*hauteur))

    mdp_input_value = ""
    mdp_input = font.render(mdp_input_value, True, (195, 195, 195))
    mdp_input_rect = mdp_input.get_rect(topleft=message_mdp.topright)

    font = pygame.font.Font(None, 24)
    prompt2 = font.render('Pseudo:  ', True, (195, 195, 195))
    message_pseudo = prompt2.get_rect(center=(largeur-60, hauteur))

    pseudo_input_value = "▮"
    pseudo_input = font.render(pseudo_input_value, True, (195, 195, 195))
    pseudo_input_rect = pseudo_input.get_rect(
        topleft=(mdp_input_rect.topleft[0], mdp_input_rect.topleft[1] - hauteur))

    font = pygame.font.Font(None, 24)

    erreur = font.render(
        "", 1, (195, 195, 195))
    rect_erreur = erreur.get_rect()
    rect_erreur.centerx = fenetre_globale.get_rect().centerx
    rect_erreur.centery = 6*hauteur

    while True:
        clock.tick(30)
        fenetre_globale.fill(0)

        bt_original = pygame.Surface((200, 50))
        bt_original.fill((195, 195, 195))
        rect_original = bt_original.get_rect()
        rect_original.centerx = fenetre_globale.get_rect().centerx
        rect_original.centery = 3*hauteur
        fenetre_globale.blit(bt_original, rect_original)

        bt_original2 = pygame.Surface((194, 44))
        bt_original2.fill(0)
        rect_original2 = bt_original2.get_rect()
        rect_original2.centerx = fenetre_globale.get_rect().centerx
        rect_original2.centery = 3*hauteur
        fenetre_globale.blit(bt_original2, rect_original2)

        font = pygame.font.Font(None, 24)
        text = font.render("Valider", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = rect_original.centery
        fenetre_globale.blit(text, rect_text)

        rect_original.centery = 4*hauteur
        fenetre_globale.blit(bt_original, rect_original)

        rect_original2.centery = 4*hauteur
        fenetre_globale.blit(bt_original2, rect_original2)

        font = pygame.font.Font(None, 24)
        text = font.render("Créer", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = rect_original.centery
        fenetre_globale.blit(text, rect_text)

        rect_original.centery = 5*hauteur
        fenetre_globale.blit(bt_original, rect_original)

        rect_original2.centery = 5*hauteur
        fenetre_globale.blit(bt_original2, rect_original2)

        font = pygame.font.Font(None, 24)
        text = font.render("Retour", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = rect_original.centery
        fenetre_globale.blit(text, rect_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return menu(fenetre_globale, quit=1)

            elif event.type == pygame.KEYDOWN:
                if choix:
                    pseudo_input_value = pseudo_input_value[:-1]
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        choix = 0
                        mdp_input_value += "▮"
                        mdp_input = font.render(
                            mdp_input_value, True, (195, 195, 195))
                        mdp_input_rect = mdp_input.get_rect(
                            topleft=message_mdp.topright)
                    elif event.key == pygame.K_BACKSPACE:
                        pseudo_input_value = pseudo_input_value[:-1]
                        pseudo_input_value += "▮"
                    else:
                        pseudo_input_value += event.unicode
                        pseudo_input_value += "▮"

                    pseudo_input = font.render(
                        pseudo_input_value, True, (195, 195, 195))
                    pseudo_input_rect = pseudo_input.get_rect(
                        topleft=message_pseudo.topright)

                else:
                    mdp_input_value = mdp_input_value[:-1]
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        choix = 1
                        pseudo_input_value += "▮"
                        pseudo_input = font.render(
                            pseudo_input_value, True, (195, 195, 195))
                        pseudo_input_rect = pseudo_input.get_rect(
                            topleft=message_pseudo.topright)
                    elif event.key == pygame.K_BACKSPACE:
                        mdp_input_value = mdp_input_value[:-1]
                        mdp_input_value += "▮"
                    else:
                        mdp_input_value += event.unicode
                        mdp_input_value += "▮"
                    mdp_input = font.render(
                        mdp_input_value, True, (195, 195, 195))
                    mdp_input_rect = mdp_input.get_rect(
                        topleft=message_mdp.topright)

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[1] - 25)//hauteur == 2 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):

                if pseudo_input_value[-1] == "▮":
                    pseudo_input_value = pseudo_input_value[:-1]
                elif mdp_input_value[-1] == "▮":
                    mdp_input_value = mdp_input_value[:-1]

                Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ = verif(
                    pseudo_input_value, mdp_input_value)

                if choix:
                    pseudo_input_value += "▮"
                else:
                    mdp_input_value += "▮"

                if NJ:
                    return menu(fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)
                else:
                    font = pygame.font.Font(None, 24)
                    if NJ == 0:
                        erreur = font.render(
                            "Mauvais mot de passe", 1, (195, 195, 195))
                    else:
                        erreur = font.render(
                            "Ce joueur n'existe pas", 1, (195, 195, 195))
                    rect_erreur = erreur.get_rect()
                    rect_erreur.centerx = fenetre_globale.get_rect().centerx
                    rect_erreur.centery = 6*hauteur

            if (pos[1] - 25)//hauteur == 3 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                if pseudo_input_value[-1] == "▮":
                    pseudo_input_value = pseudo_input_value[:-1]
                elif mdp_input_value[-1] == "▮":
                    mdp_input_value = mdp_input_value[:-1]
                n = attribution(pseudo_input_value)
                if n:
                    création(Id=pseudo_input_value, Mdp=mdp_input_value,
                             Rp=0, Nm=1, Ns=1, Vs=3, Scs=0, NJ=n)
                    return menu(fenetre_globale, Id=pseudo_input_value, Mdp=mdp_input_value, Rp=0, Nm=1, Ns=1, Vs=3, Scs=0, NJ=n)
                else:
                    erreur = font.render(
                        "Le pseudo est déjà pris", 1, (195, 195, 195))
                    rect_erreur = erreur.get_rect()
                    rect_erreur.centerx = fenetre_globale.get_rect().centerx
                    rect_erreur.centery = 6*hauteur

            if (pos[1] - 25)//hauteur == 4 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                return menu(fenetre_globale)

        fenetre_globale.blit(prompt2, message_pseudo)
        fenetre_globale.blit(pseudo_input, pseudo_input_rect)
        fenetre_globale.blit(prompt1, message_mdp)
        fenetre_globale.blit(mdp_input, mdp_input_rect)
        fenetre_globale.blit(erreur, rect_erreur)
        pygame.display.flip()


# Fonction lancée lorqu'on clique sur "Aide" : affiche les règles du jeu
def aide(fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ):

    clock = pygame.time.Clock()
    hauteur = fenetre_globale.get_size()[1]//8

    while True:
        clock.tick(30)
        fenetre_globale.fill(0)

        bt_original = pygame.Surface((200, 50))
        bt_original.fill((195, 195, 195))
        rect_original = bt_original.get_rect()
        rect_original.centerx = fenetre_globale.get_rect().centerx
        rect_original.centery = 7*hauteur
        fenetre_globale.blit(bt_original, rect_original)

        bt_original2 = pygame.Surface((194, 44))
        bt_original2.fill(0)
        rect_original2 = bt_original2.get_rect()
        rect_original2.centerx = fenetre_globale.get_rect().centerx
        rect_original2.centery = 7*hauteur
        fenetre_globale.blit(bt_original2, rect_original2)

        font = pygame.font.Font(None, 24)
        text = font.render("Retour", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = rect_original.centery
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Appuyez sur les touches de direction du", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 40
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "clavier pour déplacer le Pac-Man.", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 70
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Appuyez sur espace pour mettre en pause.", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 120
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Les fruits apparaissent une fois par niveau", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 170
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "et rapportent des points.", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 200
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Mangez-les si vous êtes gourmand !", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 230
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Quand vous mangez les super-gommes, ", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 280
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "les fantômes ont temporairement peur de vous", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 310
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "et vous pouvez alors les manger.", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 340
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Mangez toutes les gommes", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 390
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "pour réussir un niveau !", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 420
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render(
            "Epanouissez-vous !", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = 480
        fenetre_globale.blit(text, rect_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return menu(fenetre_globale, quit=1)

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[1] - 25)//hauteur == 6 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                return menu(fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)

        pygame.display.flip()


def statistiques(fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ):
    clock = pygame.time.Clock()
    hauteur = fenetre_globale.get_size()[1]//8

    ID, RP, NM = création(Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, True)
    _, _, _, _, _, _, _, NJ = verif(Id, Mdp)
    nmax = len(ID)

    n = 12

    while True:
        clock.tick(30)
        fenetre_globale.fill(0)

        bt_original = pygame.Surface((200, 50))
        bt_original.fill((195, 195, 195))
        rect_original = bt_original.get_rect()
        rect_original.centerx = fenetre_globale.get_rect().centerx
        rect_original.centery = 7*hauteur
        fenetre_globale.blit(bt_original, rect_original)

        bt_original2 = pygame.Surface((194, 44))
        bt_original2.fill(0)
        rect_original2 = bt_original2.get_rect()
        rect_original2.centerx = fenetre_globale.get_rect().centerx
        rect_original2.centery = 7*hauteur
        fenetre_globale.blit(bt_original2, rect_original2)

        font = pygame.font.Font(None, 24)
        text = font.render("Retour", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = rect_original.centerx
        rect_text.centery = rect_original.centery
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render("Rang", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = 40
        rect_text.centery = 30
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render("Pseudo", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = 125
        rect_text.centery = 30
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render("Rec. perso.", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = 230
        rect_text.centery = 30
        fenetre_globale.blit(text, rect_text)

        font = pygame.font.Font(None, 24)
        text = font.render("Niv. max", 1, (195, 195, 195))
        rect_text = text.get_rect()
        rect_text.centerx = 340
        rect_text.centery = 30
        fenetre_globale.blit(text, rect_text)

        for i in range(n-11, n+1):
            couleur = (195, 195, 195)
            if i >= nmax:
                break
            if i == NJ and Id != "Anonyme":
                couleur = (195, 20, 20)

            font = pygame.font.Font(None, 24)
            text = font.render("{}".format(i), 1, couleur)
            rect_text = text.get_rect()
            rect_text.centerx = 40
            rect_text.centery = (i+13-n)*30
            fenetre_globale.blit(text, rect_text)

            font = pygame.font.Font(None, 24)
            text = font.render("{}".format(ID[i]), 1, couleur)
            rect_text = text.get_rect()
            rect_text.centerx = 125
            rect_text.centery = (i+13-n)*30
            fenetre_globale.blit(text, rect_text)

            font = pygame.font.Font(None, 24)
            text = font.render("{}".format(RP[i]), 1, couleur)
            rect_text = text.get_rect()
            rect_text.centerx = 230
            rect_text.centery = (i+13-n)*30
            fenetre_globale.blit(text, rect_text)

            font = pygame.font.Font(None, 24)
            text = font.render("{}".format(NM[i]), 1, couleur)
            rect_text = text.get_rect()
            rect_text.centerx = 340
            rect_text.centery = (i+13-n)*30
            fenetre_globale.blit(text, rect_text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return menu(fenetre_globale, quit=1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 5 and n < nmax-1:
                    n += 1
                if event.button == 4 and n > 12:
                    n -= 1

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if (pos[1] - 25)//hauteur == 6 and ((pos[1] - 25) % hauteur > hauteur - 50) and ((fenetre_globale.get_rect().centerx - 100) < pos[0] < (fenetre_globale.get_rect().centerx + 100)):
                return menu(fenetre_globale, Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ)

        pygame.display.flip()
