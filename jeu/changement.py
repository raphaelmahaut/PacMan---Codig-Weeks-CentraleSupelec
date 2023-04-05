import numpy as np

'''cette fonction change la direction et la nouvelle direction du joueur en 
fonction de la possibilité du changement de direction (repertoriée dans grille-mouv)'''


def changement(joueur, grille_mouv):
    Déplacement = {'haut': 0, 'bas': 1, 'gauche': 2, 'droite': 3}
    nb_lignes, nb_colonnes = np.shape(grille_mouv)[:2]
    (j, i, vert, hor) = (((joueur.rect.centerx - 7) // 14) % nb_colonnes, ((joueur.rect.centery - 7) // 14) % nb_lignes,
                         joueur.rect.centerx % 14 == 7, joueur.rect.centery % 14 == 7)
    if joueur.nouvelle_direction:
        # vérifie la possibilité du mouvement
        if grille_mouv[i, j, Déplacement[joueur.nouvelle_direction]] == True:
            # selon la direction du couloir, on peut alors changer du joueur
            if joueur.nouvelle_direction == 'haut' and vert:
                return ("haut", None)
            if joueur.nouvelle_direction == 'bas' and vert:
                return ("bas", None)
            if joueur.nouvelle_direction == 'gauche' and hor:
                return ("gauche", None)
            if joueur.nouvelle_direction == 'droite' and hor:
                return ("droite", None)
    if vert and hor:  # verifie le type de couloir vert = vertical, hor = horizontal
        if joueur.direction != "aucune":
            if grille_mouv[i, j, Déplacement[joueur.direction]] == False:
                return ("aucune", None)
        if joueur.direction == "aucune":
            return ("aucune", None)
    return (joueur.direction, joueur.nouvelle_direction)
