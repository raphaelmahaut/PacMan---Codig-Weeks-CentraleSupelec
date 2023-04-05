import csv
from collections import deque
import numpy as np
import copy
from more_itertools import sort_together


# Dictionnaire des niveaux
# Pour chaque niveau :
# fruit correspondant avec le nombre de points du fruit
# liste des vitesses des fantômes: mort, tunnel, peur, colère, normale
# temps bonus lorsqu'on mange une super-gomme
# nombre de gommes retantes à partir duquel le fantôme rouge se met en colère
"""Niveaux = {1: [['cerise', 100], [2, 9, 8, 5, 1], 6, 20],
           2: [['fraise', 300], [2, 8, 7, 4, 6], 5, 20],
           3: [['abricot', 500], [2, 7, 7, 4, 5], 4, 30],
           4: [['abricot', 500], [2, 7, 7, 3, 5], 3, 30],
           5: [['pomme', 700], [2, 7, 6, 3, 4], 2, 50],
           6: [['pomme', 700], [2, 7, 6, 3, 4], 5, 50],
           7: [['ananas', 1000], [2, 7, 5, 3, 4], 2, 70],
           8: [['ananas', 1000], [2, 7, 5, 2, 4], 2, 80],
           9: [['galaxian', 2000], [2, 7, 5, 2, 4], 1, 100],
           10: [['galaxian', 2000], [2, 7, 4, 2, 3], 5, 100],
           11: [['cloche', 3000], [2, 7, 4, 2, 3], 2, 130],
           12: [['cloche', 3000], [2, 7, 4, 2, 3], 1, 150],
           13: [['cle', 5000], [2, 7, 4, 2, 3], 1, 150],
           14: [['cle', 5000], [2, 6, 3, 2, 2], 3, 170],
           15: [['cle', 5000], [2, 6, 3, 2, 2], 1, 180],
           16: [['cle', 5000], [2, 6, 3, 1, 2], 1, 190],
           17: [['cle', 5000], [2, 6, 3, 1, 2], 0, 200],
           18: [['cle', 5000], [2, 5, 3, 1, 2], 1, 220],
           19: [['cle', 5000], [2, 5, 2, 1, 1], 0, 240]}
"""
Niveaux = {1: [['cerise', 100], [2, 9, 7, 5.4, 6.5], 6, 20],
           2: [['fraise', 300], [2, 8, 7, 5.2, 6], 5, 20],
           3: [['abricot', 500], [2, 7, 6.5, 5, 5.5], 4, 30],
           4: [['abricot', 500], [2, 7, 6.2, 4.8, 5.3], 3, 30],
           5: [['pomme', 700], [2, 7, 5.7, 4.6, 5], 2, 50],
           6: [['pomme', 700], [2, 7, 5.4, 4.4, 5], 5, 50],
           7: [['ananas', 1000], [2, 7, 5, 4.2, 4.7], 2, 70],
           8: [['ananas', 1000], [2, 7, 5, 4, 4.7], 2, 80],
           9: [['galaxian', 2000], [2, 7, 5, 4, 4.5], 1, 100],
           10: [['galaxian', 2000], [2, 7, 5, 4, 4.3], 5, 100],
           11: [['cloche', 3000], [2, 7, 4.7, 3.8, 4.3], 2, 130],
           12: [['cloche', 3000], [2, 7, 4.5, 3.5, 4], 1, 150],
           13: [['cle', 5000], [2, 7, 4.5, 3.2, 3.8], 1, 150],
           14: [['cle', 5000], [2, 6, 4.5, 3, 3.6], 3, 170],
           15: [['cle', 5000], [2, 6, 4.2, 3, 3.5], 1, 180],
           16: [['cle', 5000], [2, 6, 4, 3, 3.5], 1, 190],
           17: [['cle', 5000], [2, 6, 4, 2.8, 3.5], 0, 200],
           18: [['cle', 5000], [2, 5, 4, 2.5, 3.5], 1, 220],
           19: [['cle', 5000], [2, 5, 3.7, 2, 3.5], 0, 240]}


def convertion(niv):
    Dic = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           2: [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
           3: [1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
           4: [1, 0, 1, 0, 0, 1, 0, 1, 0, 0],
           5: [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
           6: [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
           7: [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
           8: [1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
           9: [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]}

    Nivc = {}

    for i in range(len(niv)):
        Vt = []
        for j in niv[(i+1)][1]:
            A = Dic[int(10*j - int(j)*10)]
            B = [int(j) for b in range(10)]
            V = deque([A[v]+B[v] for v in range(10)])
            Vt.append(V)
        Nivc[i+1] = (niv[i+1][0], Vt, niv[i+1][2], niv[i+1][3])

    return Nivc


Niveaux = convertion(Niveaux)


# Renvoie les paramètres du niveau en cours


def selection_paramètres(niveau):
    # on ne peut pas dépasser le niveau 19
    if niveau > 19:
        indice = 19
    else:
        indice = niveau
    return Niveaux[indice]


def verif(pseudo, mdp):
    with open('DB.csv', 'r') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.reader(f)
        ID, MDP, RP, NM, NS, VS, SCS, RG = (i for i in obj)

        if pseudo in ID:
            NJ = ID.index(pseudo)
            if pseudo == "Anonyme":
                return "Anonyme", "", int(RP[NJ]), int(NM[NJ]), 1, 3, 0, NJ
            if MDP[NJ] == mdp:
                Id, Mdp, Rp, Nm, Ns, Vs, Scs = ID[NJ], MDP[NJ], int(
                    RP[NJ]), int(NM[NJ]), int(NS[NJ]), int(VS[NJ]), int(SCS[NJ])
                return Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ
            else:

                return "Anonyme", "", 0, 1, 1, 3, 0, 0
        else:
            return "Anonyme", "", 0, 1, 1, 3, 0, None


def attribution(pseudo):
    with open('DB.csv', 'r') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.reader(f)
        ID, MDP, RP, NM, NS, VS, SCS, RG = (i for i in obj)
        if not pseudo in ID:
            n = len(ID)
            return n
        return None


def création(Id, Mdp, Rp, Nm, Ns, Vs, Scs, NJ, envoie=False):
    with open('DB.csv', 'r+') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.reader(f)
        ID, MDP, RP, NM, NS, VS, SCS, RG = (i for i in obj)
        if 0 < NJ < len(ID):
            ID[NJ], MDP[NJ], RP[NJ], NM[NJ], NS[NJ], VS[NJ], SCS[NJ] = Id, Mdp, Rp, Nm, Ns, Vs, Scs
        elif NJ == 0:
            if Rp > int(RG[1]):
                RG[1] = Rp
                RG[2] = Id
                RG = RG[:3]
        else:
            ID.append(Id)
            MDP.append(Mdp)
            RP.append(Rp)
            NM.append(Nm)
            NS.append(Ns)
            VS.append(Vs)
            SCS.append(Scs)
        if Rp > int(RG[1]):
            RG[1] = Rp
            RG[2] = Id
            RG = RG[:3]
        elif Id not in RG and Rp == int(RG[1]):
            RG.append(Id)
        RP[1:] = list(map(int, RP[1:]))
        RP[1:], ID[1:], MDP[1:], NM[1:], NS[1:], VS[1:], SCS[1:] = sort_together(
            [RP[1:], ID[1:], MDP[1:], NM[1:], NS[1:], VS[1:], SCS[1:]], reverse=True)

    data = [ID, MDP, RP, NM, NS, VS, SCS, RG]
    fichier = open('DB.csv', 'w+', newline='')
    obj = csv.writer(fichier)
    for element in data:
        obj.writerow(element)
    fichier.close()

    if envoie:
        return ID, RP, NM


class Vitesse():
    def __init__(self, previtesse):
        self.Blinky = copy.deepcopy(previtesse)
        self.Pinky = copy.deepcopy(previtesse)
        self.Inky = copy.deepcopy(previtesse)
        self.Clyde = copy.deepcopy(previtesse)
