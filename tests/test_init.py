from jeu.init import*


def test_init_grille():
    Grille, position, position_base = init_grille()
    assert type(Grille) == np.ndarray
    assert type(position) == tuple and type(position_base) == tuple
    nb_lignes, nb_colonnes = np.shape(Grille)
    assert 0 <= position[0] < nb_lignes
    assert 0 <= position[1] < nb_colonnes
    assert 2 <= position_base[0] < nb_lignes-2
    assert 2 <= position_base[1] < nb_colonnes-2
