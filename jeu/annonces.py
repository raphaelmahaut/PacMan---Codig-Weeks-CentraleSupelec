import pygame


# affiche "pause" en jaune dans la grille de jeu
def annonce_pause(fenetre, position_annonce):
    font = pygame.font.Font(None, 24)
    text = font.render("Pause", 1, "yellow")
    rect_text = text.get_rect()
    rect_text.centerx = fenetre.get_rect().centerx
    rect_text.centery = position_annonce
    fenetre.blit(text, rect_text)


# affiche "Prêt !" en jaune dans la grille de jeu
def annonce_pret(fenetre, position_annonce):
    font = pygame.font.Font(None, 24)
    text = font.render("Prêt !", 1, "yellow")
    rect_text = text.get_rect()
    rect_text.centerx = fenetre.get_rect().centerx
    rect_text.centery = position_annonce
    fenetre.blit(text, rect_text)


# affiche "Game Over" en jaune dans la grille de jeu
def annonce_game_over(fenetre, position_annonce):
    font = pygame.font.Font(None, 24)
    text = font.render("Game Over", 1, "yellow")
    rect_text = text.get_rect()
    rect_text.centerx = fenetre.get_rect().centerx
    rect_text.centery = position_annonce
    fenetre.blit(text, rect_text)


# affiche "Niveau réussi" en jaune dans la grille de jeu
def annonce_victoire(fenetre, position_annonce):
    font = pygame.font.Font(None, 24)
    text = font.render("Niveau réussi", 1, "yellow")
    rect_text = text.get_rect()
    rect_text.centerx = fenetre.get_rect().centerx
    rect_text.centery = position_annonce
    fenetre.blit(text, rect_text)


# affiche "score" et le score au dessus de la grille de jeu
def annonce_score(fenetre_score, score, Rp, Rg, Id):
    fenetre_score.fill(0)
    font = pygame.font.Font(None, 24)
    text_score1 = font.render("Score", 1, (255, 255, 255))
    text_score2 = font.render(
        "{}".format(str(score)), 1, (255, 255, 255))
    rect_score1 = text_score1.get_rect()

    rect_score1.centerx = fenetre_score.get_rect().centerx
    rect_score1.centery = 25

    rect_score2 = text_score2.get_rect()
    rect_score2.centerx = fenetre_score.get_rect().centerx
    rect_score2.centery = 55

    font = pygame.font.Font(None, 24)
    text_scorep1 = font.render("R. {}".format(Id[:10]), 1, (255, 255, 255))
    text_scorep2 = font.render(
        "{}".format(str(Rp)), 1, (255, 255, 255))
    rect_scorep1 = text_scorep1.get_rect()

    rect_scorep1.centerx = fenetre_score.get_rect().centerx - 130
    rect_scorep1.centery = 25

    rect_scorep2 = text_scorep2.get_rect()
    rect_scorep2.centerx = fenetre_score.get_rect().centerx - 130
    rect_scorep2.centery = 55

    font = pygame.font.Font(None, 24)
    text_scoreg1 = font.render("Record", 1, (255, 255, 255))
    text_scoreg2 = font.render(
        "{}".format(str(Rg)), 1, (255, 255, 255))
    rect_scoreg1 = text_scoreg1.get_rect()

    rect_scoreg1.centerx = fenetre_score.get_rect().centerx + 130
    rect_scoreg1.centery = 25

    rect_scoreg2 = text_scoreg2.get_rect()
    rect_scoreg2.centerx = fenetre_score.get_rect().centerx + 130
    rect_scoreg2.centery = 55

    fenetre_score.blit(text_score1, rect_score1)
    fenetre_score.blit(text_score2, rect_score2)
    fenetre_score.blit(text_scorep1, rect_scorep1)
    fenetre_score.blit(text_scorep2, rect_scorep2)
    fenetre_score.blit(text_scoreg1, rect_scoreg1)
    fenetre_score.blit(text_scoreg2, rect_scoreg2)


# affiche le nombre de vies restantes en dessous de la grille de jeu avec des pacman
def annonce_vies(fenetre_vies, vies, niveau):
    fenetre_vies.fill(0)
    for i in range(vies):
        fenetre_vies.blit(pygame.image.load(
            "packages_textures/Pacg3.png").convert_alpha(), (10 + 30*i, 23))
    font = pygame.font.Font(None, 24)
    text = font.render("Niveau {}".format(str(niveau)), 1, "yellow")
    rect_text = text.get_rect()
    rect_text.centerx = fenetre_vies.get_rect().centerx * 1.6
    rect_text.centery = 35
    fenetre_vies.blit(text, rect_text)
