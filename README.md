# Plant-Man (Pac-man, projet semaine 2)


## L'équipe

Aymeric Bénéat--Byron  
Loris Chaine  
Basilisse Legrain 
Raphaël Mahaut  
Thomas Norodom  
Candice Roze (Forum)  


## Documentation

[Tutoriel pygame assez intéressant](https://zestedesavoir.com/tutoriels/pdf/846/pygame-pour-les-zesteurs.pdf)  
[Tutoriel forme en pygame](https://www.pygame.org/docs/ref/rect.html)  
[Détails techniques Pac-Man](https://www.grospixels.com/site/pacman1.php)  
[Autres détails techniques Pac-Man](https://strategywiki.org/wiki/Pac-Man/Gameplay)



### Comment lancer le jeu ?


Cloner le gitlab
Importer les modules suivant avec la commande "pip install <module>" :
    - pygame
    - numpy
    - random
    - copy
    - operator
Vérifier que le shell est bien dans le répertoire 'Plant-Man', puis lancer l'exécution de main.py


    Attention : certaine cartes son ne prennet pas en compte pygame.mixer:
        si vous avez cette erreur : MUSIQUE = pygame.mixer.music.load("musique.mp3")
        pygame.error: Failed loading libmpg123-0.dll: Le module spécifié est introuvable.
    Dans main.py : supprimez les lignes 255 à 257 incluses (pygame.mixer.init(),MUSIQUE = pygame.mixer.music.load("musique.mp3"), pygame.mixer.music.play(10, 0.0))


## Comment jouer ?

Le jeu commence 3 secondes après le lancement du programme. Pac-man est contrôlé avec les flèches du clavier.
Pour réussir un niveau, collecter toutes les gommes présentes dans la grille. Mais attention, se faire capturer par les fantômes qui rodent dans la cage coûte une vie !

But du jeu : passer le plus de niveau possible et faire le plus haut score avec une limite de trois vies.

Possibilité de faire pause dans le jeu en appuyant sur la barre espace.

Objets spéciaux :
    - les super-gommes : elles sont plus grosses que les gommes classiques. Lorsque Pac-man en attrape une, les fantômes deviennent bleus et ont temporairement peur de lui. 
    - les fruits : ils ajoutent des points au score quand ils sont attrapés. Il en apparaît un différent à chaque nouveau niveau.


## Objectifs

* 1er MVP :
Fonctionnalité 1 : Créer la grille de jeu  
Fonctionnalité 2 : Contrôler Pac-Man
    - Étape 1 : Afficher Pac-Man  
    - Étape 2 : Faire bouger Pac-Man  
Fonctionnalité 3 : Gérer les gommes
    - Étape 1 : Afficher les gommes  
    - Étape 2 : Gérer les collision entre Pac-Man et les gommes  
    - Étape 3 : Fin du jeu (toutes les gommes collectées)  

--> Pac-man peut se déplacer dans une grille et attraper les gommes. Le jeu se termine lorsque toutes les gommes sont collectées. Mettons à présent en scène les fantômes.

* 2e MVP :
Fonctionnalité 4 : Afficher l'interface  
Fonctionnalité 5 : Ajouter les fantômes
    - Étape 1 : Afficher les fantômes  
    - Étape 2 : Faire bouger les fantômes (de manière aléatoire dans un premier temps)
    - Étape 3 : Gérer la collision Pac-Man / fantôme

--> Les fantômes se déplacent en choisissant aléatoirement une direction à chaque intersection. Jeu terminé lorsque toutes les gommes sont récupérées OU quand un fantôme touche Pac-man

* 3e MVP :
Fonctionnalité 6 : Prise en compte de boules spéciales et changement de l’interaction entre Pac-Man et les fantômes lorsque cette boule est attrapée
Fonctionnalité 7 : Ajout de paramètres de jeu
    - Étape 1 : Affichage du score 
    - Étape 2 : Affichage des vies
    - Étape 3 : Affichage des fruits  
Fonctionnalité 8 : Paramétrer le mouvement des fantômes, avoir des fantômes intelligents
    - Étape 1 : Chaque fantôme a une manière singulière de se déplacer, ils peuvent ainsi se coordonner pour capturer Pac-Man : 
        - Blinky, le fantôme rouge, vise la case de Pac-Man (il le poursuit directement)
        - Pinky, le fantôme rose, vise 4 cases devant Pac-Man (cela le fait contourner Pac-Man (il essaie donc de le prendre en tenaille avec Blinky ))
        - Clyde, le fantôme orange, chasse Pac-Man comme Blinky si ce dernier est loin (plus de 8 cases), sinon il prend une direction aléatoire
        - Inky, le fantôme bleu, vise la case définie par la case de Blinky et le double du vecteur entre Pac-Man et Blinky (il essaie donc d'aller là où Pac-Man fuit logiquement Blinky)
    - Étape 2 : le fantôme rouge se met en colère lorsque un certain nombre de gommes est attrapé, il s'accélère
    - Étape 3 : Cycles de 30s. Pendant 24-27 secondes, les fantômes chassent Pac-Man. Pendant le temps restant, chaque fantôme part dans un coin de la grille
Fonctionnalité 9 : Gérer les différents niveaux
    - Étape 1 : Créer les différents niveaux
    - Étape 2 : Gérer l'apparition des fruits
    - Étape 3 : Modifier la vitesse des fantômes selon le niveau

--> Chacun des 4 fantômes a une manière personnelle de bouger. Les super-gommes changent temporairement le cours du jeu lorsqu'elles sont attrapées : les fantômes ont peur de Pac-man, et lorsqu'il les touchent, ils sont téléportés et repartent depuis leur base. Prise en compte de vies : Pac-man peut être touché 3 fois avant que la partie soit perdue. On compte également un score. À chaque niveau, un fruit peut apparaître. Lorsqu'il est capturé, il rapporte beaucoup de points au joueur. Lorsqu'un niveau est réussi, un nouveau niveau commence et la vitesse des fantômes est augmentée.


## Organisation
* presentation.pdf contient les slides de la soutance
* analyse.txt contient la réflexion initiale autour du jeu (sprints, objetcifs, fonctionnalités)
* Dossier tests: contient les fichiers des tests des fonctions du jeu
* Dosser test_coverage : contient la marche ) suivre pour faire un test coverage dans command.text et contient le dernier rapport html en date.
* main.py: Fichier à éxécuter pour lancer le jeu
* annonces.py: Affichage des différents textes en fonction de la situation
* changement.py: Permettre au joueur de changer de direction lorsque c'est possible
* changement_fantome.py: Idem que changement.py mais pour les fantômes (Sans la possibilité de faire demi-tour)
* collision.py: Gérer les collisions entre le joueur et les murs ou le joueur et les fantômes (en ramenant le joueur à sa place initiale dans le deuxième cas)
* db.py: dictionnaire des paramètres de chaque niveaux (vitesses, fruits...)
* end.py: Issue du jeu (Game over si plus de vies ou Victoire si plus de gommes)
* entité.py: définir Pac-Man et les fantômes 
* fruit_tunnel: apparition des fruits et gestion de la vitesse dans le fruit_tunnel
* grille_init_gum.py: Gestion des gommes (placement, manger, bonus...)
* grille_mouv.py: mouvements possibles à chaque intersection
* init.py: création de la grille
* menu.py: menu principal du jeu
* mouvement_fantome.py: comportement de chaque fantome
* mouvement_joueur.py: prise en compte des commandes du joueur
* textures.py: ouvrir les textures pour les murs
* Dossier packages_textures: design de Pac-Man, des murs, des fruits et des fantomes
* test.py: appelle toutes les fonctions tests


### Comment tester le jeu ?
Installer pytest
La commande à appliquer se trouve dans test_coverage/command.text.
Cela crée un rapport html des tests des fonctions testables (n'utilisant que peu pygame)
Le dernier rapport fait par l'équipe est test_coverage/test_coverage.html

### Amélioration possibles

* Ajouter un base de donnée liée au login permettant de sauvegarder le niveau atteint lors de la dernière partie et le score (actuellement peut importe ce qui est rentré le bouton se change en charger et celui-ci lance le jeu)
* Permettre aux utilisateurs de choisir d'autres maps (ce qui nécéssite la création d'une grille avec la place des murs et leur design, et la place de gommes)
