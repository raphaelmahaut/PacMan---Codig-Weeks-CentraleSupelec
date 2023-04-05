import numpy as np

'''cette fonction change la direction et la nouvelle direction du fantome en 
fonction de la possibilité du changement de direction (repertoriée dans grille-mouv)'''


def changement_fantome(joueur, grille_mouv):
    Déplacement = {'haut': 0, 'bas': 1, 'gauche': 2, 'droite': 3}
    nb_lignes, nb_colonnes = np.shape(grille_mouv)[:2]
    (j, i, vert, hor) = (((joueur.rect.centerx - 7) // 14) % nb_colonnes, ((joueur.rect.centery - 7) // 14) % nb_lignes,
                         joueur.rect.centerx % 14 == 7, joueur.rect.centery % 14 == 7)

    if joueur.direction == 'haut':
        joueur.ancienne_direction = 'haut'
    if joueur.direction == 'bas':
        joueur.ancienne_direction = 'bas'
    if joueur.direction == 'gauche':
        joueur.ancienne_direction = 'gauche'
    if joueur.direction == 'droite':
        joueur.ancienne_direction = 'droite'

    if joueur.nouvelle_direction:
        # verifie la possibilité du mouvement
        if grille_mouv[i, j, Déplacement[joueur.nouvelle_direction]] == True:
            # verifie le type de couloir vert = vertical, hor = horizontal
            if joueur.nouvelle_direction == 'haut' and vert:
                return ("haut", None, joueur.ancienne_direction)
            if joueur.nouvelle_direction == 'bas' and vert:
                return ("bas", None, joueur.ancienne_direction)
            if joueur.nouvelle_direction == 'gauche' and hor:
                return ("gauche", None, joueur.ancienne_direction)
            if joueur.nouvelle_direction == 'droite' and hor:
                return ("droite", None, joueur.ancienne_direction)
    if vert and hor:  # gestion des coins, le fantome ne doit pas s'y arrêter, mais peut faire demi-tour
        if joueur.direction != "aucune":
            if grille_mouv[i, j, Déplacement[joueur.direction]] == False:
                return ("aucune", None, joueur.ancienne_direction)
        if joueur.direction == "aucune":
            return ("aucune", None, joueur.ancienne_direction)
    return (joueur.direction, joueur.nouvelle_direction, joueur.ancienne_direction)
