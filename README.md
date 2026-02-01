# devil-fruit-slicer
# Devil Fruit Slicer - One Piece Edition

Un jeu de type "Fruit Ninja" inspiré du célèbre manga/anime One Piece. Tranchez des Devil Fruits en appuyant sur les bonnes touches du clavier.

## Description

Dans ce jeu, vous devez trancher les Devil Fruits qui apparaissent à l'écran en appuyant rapidement sur les touches correspondantes. Attention aux bombes qui mettent fin au jeu instantanément. Utilisez les glaçons pour ralentir le temps et attrapez le fruit rare doré pour obtenir un bonus de points massif.

## Fonctionnalités

### Devil Fruits Disponibles

4 Devil Fruits canoniques de One Piece avec leurs utilisateurs:
- Gomu Gomu no Mi (Monkey D. Luffy)
- Mera Mera no Mi (Portgas D. Ace)
- Hie Hie no Mi (Kuzan/Aokiji)
- Yami Yami no Mi (Marshall D. Teach)

### Fruit Rare

Ope Ope no Mi (Trafalgar Law) - Vaut 10 points au lieu de 1

### Objets Spéciaux

- Bombes: Termine le jeu immédiatement
- Glaçons: Gèle le temps pendant 4 secondes

### Système de Progression

- Niveaux avec difficulté croissante
- Combos pour récompenser les réflexes rapides
- Système de strikes: 3 fruits manqués = Game Over
- Montée de niveau tous les 10 points

### Interface Graphique

- Thème One Piece avec fond océanique
- Nuages et vagues animés
- Drapeaux pirates
- Palette de couleurs inspirée de l'univers One Piece
- Effets de particules lors du tranchage

### Audio

- Support pour fichiers MP3 One Piece
- Synthèse audio automatique avec numpy si les fichiers sont manquants
- Sons uniques pour chaque Devil Fruit
- Musique de menu en boucle

## Comment Jouer

### Contrôles

| Touche | Action |
|--------|--------|
| G | Trancher Gomu Gomu no Mi (Violet) |
| M | Trancher Mera Mera no Mi (Orange Feu) |
| H | Trancher Hie Hie no Mi (Bleu Glace) |
| Y | Trancher Yami Yami no Mi (Noir) |
| O | Trancher Ope Ope no Mi (Doré - Rare) |
| I | Trancher Glaçon (Ralentit le temps) |
| X | NE PAS trancher (Bombe) |
| SPACE | Démarrer / Rejouer |
| ESC | Quitter |

### Règles du Jeu

1. Tranchez les fruits en appuyant sur la touche correspondante affichée
2. Évitez les bombes (touche X) - elles terminent le jeu immédiatement
3. Attrapez le fruit rare doré (O) pour gagner 10 points d'un coup
4. Utilisez les glaçons (I) stratégiquement pour ralentir le temps
5. Ne manquez pas plus de 3 fruits ou c'est Game Over
6. Montez de niveau tous les 10 points pour augmenter la difficulté

### Système de Score

- Fruit normal: +1 point
- Fruit rare (Ope Ope no Mi): +10 points
- Combo (plusieurs fruits en même temps): Points bonus
- Fruit manqué: +1 strike (3 strikes = Game Over)

## Installation

### Prérequis

- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

1. Cloner ou télécharger le projet

```bash
git clone https://github.com/votre-username/devil-fruit-slicer.git
cd devil-fruit-slicer
```

2. Installer les dépendances

```bash
pip install pygame numpy
```

3. Configuration des assets (optionnel)

Pour une expérience complète, ajoutez vos propres fichiers:

```
assets/
├── sounds/
│   ├── harbour_village.mp3
│   ├── cliffhanger.mp3
│   └── gomu_gomu_no.mp3
├── fruits/
│   ├── orange.png
│   ├── red.png
│   ├── bleu.png
│   └── purple.png
└── items/
    ├── ice.png
    └── bomb.png
```

Note: Le jeu fonctionne sans ces fichiers. Des images et sons de remplacement seront générés automatiquement.

4. Lancer le jeu

```bash
python devil_fruit_slicer_improved__4_.py
```

## Technologies Utilisées

- Pygame: Framework principal pour le jeu et le rendu graphique
- NumPy: Génération de sons synthétiques et calculs mathématiques
- Python Wave: Création de fichiers audio WAV
- Python Math: Calculs trigonométriques pour les animations

## Structure du Code

```
devil_fruit_slicer_improved__4_.py
├── Configuration (lignes 1-172)
│   ├── Imports et initialisation
│   ├── Constantes du jeu
│   ├── Définitions des Devil Fruits
│   └── Système de niveaux
│
├── Backend - Logique (lignes 173-700)
│   ├── Synthèse audio
│   ├── Gestion des fruits (spawn, update, collision)
│   ├── Système de particules
│   └── Mécaniques de jeu
│
└── Frontend - Interface (lignes 701-1206)
    ├── Chargement des images
    ├── Fonctions de dessin (nuages, vagues, texte)
    ├── Écrans (menu, jeu, game over)
    └── Boucle principale
```

## Système de Niveaux

La difficulté augmente progressivement avec votre score :

| Niveau | Points Requis | Effets |
|--------|---------------|---------|
| 1 | 0-9 | Vitesse normale, 2 fruits max |
| 2 | 10-19 | +10% vitesse, 3 fruits max |
| 3 | 20-29 | +20% vitesse, 4 fruits max |
| 4 | 30-39 | +30% vitesse, 5 fruits max |
| 5+ | 40+ | Vitesse maximale, 6 fruits max |

### Paramètres Ajustés par Niveau

- spawn_interval: Temps entre apparitions (diminue)
- max_on_screen: Nombre maximum de fruits à l'écran (augmente)
- special_chance: Probabilité d'objets spéciaux (augmente)
- velocity: Vitesse de lancement des fruits (augmente)
- gravity: Force de gravité appliquée (augmente légèrement)

## Palette de Couleurs One Piece

Le jeu utilise une palette de couleurs inspirée de One Piece:

- SKY_BLUE: Fond ciel (135, 206, 250)
- OCEAN_BLUE: Vagues océaniques (41, 128, 185)
- FIRE_ORANGE: Mera Mera no Mi (230, 126, 34)
- ICE_BLUE: Hie Hie no Mi (52, 152, 219)
- GOLD: Fruit rare (255, 215, 0)
- STRAW_HAT_YELLOW: Chapeau de paille (255, 223, 0)

## Dépannage

### Le jeu ne démarre pas
- Vérifiez que Python 3.7+ est installé : `python --version`
- Vérifiez que pygame est installé : `pip show pygame`
- Réinstallez les dépendances : `pip install --upgrade pygame numpy`

### Pas de son
- Les fichiers MP3 sont optionnels - des sons synthétiques seront générés
- Vérifiez que pygame.mixer est initialisé correctement
- Vérifiez le volume de votre système

### Images manquantes
- Le jeu génère automatiquement des images de remplacement colorées
- Les chemins d'images peuvent être personnalisés dans le code (lignes 54-72)

### Performance lente
- Réduisez FPS dans le code (ligne 30): FPS = 30
- Fermez les autres applications
- Vérifiez que votre système répond aux exigences minimales

## Contribution

Les contributions sont les bienvenues. Pour contribuer:

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (git checkout -b feature/AmazingFeature)
3. Commit vos changements (git commit -m 'Add some AmazingFeature')
4. Push vers la branche (git push origin feature/AmazingFeature)
5. Ouvrir une Pull Request

## Idées d'Amélioration

- Ajouter plus de Devil Fruits (Logia, Zoan)
- Système de high scores persistant
- Power-ups additionnels
- Mode multijoueur
- Animations de particules plus élaborées
- Menu de paramètres
- Support manette de jeu
- Thèmes alternatifs

## Licence

Ce projet est un projet éducatif créé par un étudiant en première année d'informatique.

Disclaimer: One Piece est la propriété d'Eiichiro Oda et Shueisha. Ce projet est un fan-game non commercial créé à des fins éducatives.

## Auteur

Étudiant Première Année Informatique

Projet créé dans le cadre de l'apprentissage de Python et Pygame.

## Remerciements

- Eiichiro Oda pour l'univers incroyable de One Piece
- Pygame Community pour l'excellent framework
- Fruit Ninja pour l'inspiration du gameplay
- Tous les fans de One Piece

---

"I'm gonna be King of the Pirates!" - Monkey D. Luffy

Bon jeu et que le Grand Line soit avec vous.
