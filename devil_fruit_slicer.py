"""
Un jeu de type "Fruit Ninja" avec le thème One Piece.
Le joueur doit trancher les Devil Fruits qui apparaissent à l'écran
en appuyant sur les touches correspondantes.

Auteur: Étudiant Première Année Informatique
Thème: One Piece (Manga/Anime)
"""

import pygame      # Bibliothèque pour créer des jeux
import random      # Pour générer des nombres aléatoires
import math        # Pour les calculs mathématiques (sin, cos, etc.)
import sys         # Pour quitter le programme proprement
import os          # Pour vérifier l'existence des fichiers
import numpy as np # Pour la synthèse audio
import wave        # Pour créer des fichiers WAV
import io          # Pour gérer les flux de données

# INITIALISATION DE PYGAME

pygame.init()  # Démarre tous les modules Pygame

# CONSTANTES DU JEU

# Dimensions de la fenêtre du jeu
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
FPS           = 60        # Images par seconde (fluidité)
SAMPLE_RATE   = 44100     # Taux d'échantillonnage pour l'audio

# Palette de couleurs One Piece
SKY_BLUE = (135, 206, 250)              # Bleu ciel pour le fond
OCEAN_BLUE = (41, 128, 185)             # Bleu océan pour les vagues
WHITE    = (255, 255, 255)              # Blanc
BLACK    = (0, 0, 0)                    # Noir
RED      = (231, 76, 60)                # Rouge pour les bombes
ORANGE   = (243, 156, 18)               # Orange pour le titre
GOLD     = (255, 215, 0)                # Or pour le fruit rare
YELLOW   = (241, 196, 15)               # Jaune
GREEN    = (46, 204, 113)               # Vert pour le niveau
DARK_PURPLE = (76, 40, 130)             # Violet foncé
FIRE_ORANGE = (230, 126, 34)            # Orange feu (Mera Mera)
ICE_BLUE    = (52, 152, 219)            # Bleu glace (Hie Hie)
DARK_BLACK  = (44, 34, 54)              # Noir foncé (Yami Yami)
STRAW_HAT_YELLOW = (255, 223, 0)        # Jaune chapeau de paille
PIRATE_FLAG_BLACK = (20, 20, 20)        # Noir du drapeau pirate


# FICHIERS AUDIO ONE PIECE

# Chemins vers les fichiers MP3 One Piece pour les effets sonores
SOUND_FILES = {
    'victory':   r'C:\Users\labed\Desktop\assets\sounds\harbour_village.mp3',  # Son de victoire (combo/rare)
    'bomb':      r'C:\Users\labed\Desktop\assets\sounds\harbour_village.mp3',  # Son d'explosion (bombe)
    'gameover':  r'C:\Users\labed\Desktop\assets\sounds\harbour_village.mp3',  # Son de game over
    'slice':     r'C:\Users\labed\Desktop\assets\sounds\cliffhanger.mp3',      # Son de tranchage (pas utilisé)
    'levelup':   r'C:\Users\labed\Desktop\assets\sounds\gomu_gomu_no.mp3',     # Son de montée de niveau
}


# IMAGES DES PERSONNAGES ONE PIECE (décoration du menu)

ONE_PIECE_IMAGES = [
    r'C:\Users\labed\Downloads\caa5abf2a4d5718806c925fd7fc730fe.png',
    r'C:\Users\labed\Downloads\71e2b1cef174820602aa8026118d7702.png',
    r'C:\Users\labed\Downloads\10d317c4d928ef3b5243686c5b466b00.png',
    r'C:\Users\labed\Downloads\7e4e136037f8cd63909a685d814e3049.png',
    r'C:\Users\labed\Downloads\0a0fa232685e7271b48e9658e3b812f8 (1).png',
]

# ─────────────────────────────────────────────
# DÉFINITIONS DES DEVIL FRUITS (canoniques de One Piece)
# ─────────────────────────────────────────────
# Chaque fruit a:
# - name: Nom du fruit en japonais
# - image: Chemin vers l'image du fruit
# - key: Touche du clavier pour le trancher
# - letter: Lettre affichée sur le fruit
# - color: Couleur du fruit
# - sound: Nom du son à jouer
# - user: Utilisateur du fruit dans One Piece
# - type_name: Type de Devil Fruit (Paramecia, Logia, Zoan)
FRUITS = [
    {
        'name':      'Gomu Gomu no Mi',      # Fruit du Caoutchouc
        'image':     r'C:\Users\labed\Desktop\assets\fruits\orange.png',
        'key':       pygame.K_g,              # Touche G
        'letter':    'G',
        'color':     (155, 89, 182),          # Violet
        'sound':     'gomu',
        'user':      'Monkey D. Luffy',       # Luffy
        'type_name': 'Paramecia',
    },
    {
        'name':      'Mera Mera no Mi',      # Fruit du Feu
        'image':     r'C:\Users\labed\Desktop\assets\fruits\red.png',
        'key':       pygame.K_m,              # Touche M
        'letter':    'M',
        'color':     FIRE_ORANGE,             # Orange feu
        'sound':     'mera',
        'user':      'Portgas D. Ace',        # Ace
        'type_name': 'Logia',
    },
    {
        'name':      'Hie Hie no Mi',        # Fruit de la Glace
        'image':     r'C:\Users\labed\Desktop\assets\fruits\bleu.png',
        'key':       pygame.K_h,              # Touche H
        'letter':    'H',
        'color':     ICE_BLUE,                # Bleu glace
        'sound':     'hie',
        'user':      'Kuzan (Aokiji)',        # Aokiji
        'type_name': 'Logia',
    },
    {
        'name':      'Yami Yami no Mi',      # Fruit de l'Obscurité
        'image':     r'C:\Users\labed\Desktop\assets\fruits\purple.png',
        'key':       pygame.K_y,              # Touche Y
        'letter':    'Y',
        'color':     DARK_BLACK,              # Noir foncé
        'sound':     'yami',
        'user':      'Marshall D. Teach',     # Barbe Noire
        'type_name': 'Logia',
    },
]

# ─────────────────────────────────────────────
# FRUIT RARE SPÉCIAL - Apparaît une fois par niveau
# ─────────────────────────────────────────────
# L'Ope Ope no Mi vaut 10 points au lieu de 1!
RARE_FRUIT = {
    'name':      'Ope Ope no Mi',            # Fruit de l'Opération (Trafalgar Law)
    'image':     r'C:\Users\labed\Desktop\assets\fruits\orange.png',
    'key':       pygame.K_o,                  # Touche O
    'letter':    'O',
    'color':     GOLD,                        # Couleur dorée
    'sound':     'rare',
    'user':      'Trafalgar Law',
    'type_name': 'Paramecia',
    'points':    10,                          # Donne 10 points!
}

# ─────────────────────────────────────────────
# OBJETS SPÉCIAUX (bombes et glace)
# ─────────────────────────────────────────────
SPECIAL_ITEMS = [
    {
        'name':   'Hie Hie Glacon',          # Glaçon qui gèle le temps
        'image':  r'C:\Users\labed\Desktop\assets\items\ice.png',
        'key':    pygame.K_i,                 # Touche I
        'letter': 'I',
        'type':   'ice',                      # Type spécial: glace
        'color':  (173, 216, 230),            # Bleu clair
        'sound':  'ice',
    },
    {
        'name':   'Bomu Bomu Bomb',          # Bombe qui termine le jeu
        'image':  r'C:\Users\labed\Desktop\assets\items\bomb.png',
        'key':    pygame.K_x,                 # Touche X
        'letter': 'X',
        'type':   'bomb',                     # Type spécial: bombe
        'color':  RED,                        # Rouge
        'sound':  'bomb',
    },
]

# ─────────────────────────────────────────────
# SYSTÈME DE NIVEAUX
# ─────────────────────────────────────────────
POINTS_PER_LEVEL = 10  # Il faut 10 points pour passer au niveau suivant

def get_level_params(level):
    """
    Calcule les paramètres du jeu selon le niveau actuel.
    Plus le niveau est élevé, plus le jeu est difficile.
    
    Args:
        level (int): Niveau actuel du joueur
        
    Returns:
        dict: Dictionnaire avec les paramètres de difficulté
    """
    lvl = min(level, 8)  # Niveau maximum 8 (après, la difficulté ne change plus)
    return {
        'spawn_interval':  max(400,  1200 - (lvl - 1) * 100),  # Temps entre apparitions (ms)
        'max_on_screen':   min(6,    2 + (lvl - 1)),            # Nombre max de fruits à l'écran
        'special_chance':  min(0.40, 0.20 + (lvl - 1) * 0.03), # Chance d'apparition d'objets spéciaux
        'vy_min':         -12 - (lvl - 1) * 0.5,                # Vitesse verticale minimum
        'vy_max':         -18 - (lvl - 1) * 0.8,                # Vitesse verticale maximum
        'gravity':         0.3 + (lvl - 1) * 0.02,              # Force de gravité
    }

# ─────────────────────────────────────────────
# SYNTHÈSE AUDIO
# ─────────────────────────────────────────────
# Ces fonctions créent des sons de remplacement si les fichiers MP3 n'existent pas.
# Elles utilisent numpy pour générer des ondes sonores mathématiques.
# NOTE: Les vrais sons One Piece sont chargés depuis les fichiers MP3 quand disponibles.
# ─────────────────────────────────────────────
SR = SAMPLE_RATE  # Taux d'échantillonnage (44100 Hz)

def _mono_to_stereo_wav(mono_int16):
    """
    Convertit un signal audio mono en stéréo au format WAV.
    
    Args:
        mono_int16 (numpy.array): Signal audio mono en entiers 16 bits
        
    Returns:
        bytes: Données audio au format WAV
    """
    # Duplique le canal mono pour créer la stéréo (gauche et droite identiques)
    stereo = np.column_stack((mono_int16, mono_int16)).flatten()
    
    # Crée un fichier WAV en mémoire
    buf = io.BytesIO()
    w = wave.open(buf, 'wb')
    w.setnchannels(2)      # 2 canaux (stéréo)
    w.setsampwidth(2)      # 2 octets par échantillon (16 bits)
    w.setframerate(SR)     # Taux d'échantillonnage
    w.writeframes(stereo.astype(np.int16).tobytes())
    w.close()
    return buf.getvalue()

def _to_sound(mono_int16):
    """
    Convertit un signal audio mono en objet Sound de Pygame.
    
    Args:
        mono_int16 (numpy.array): Signal audio mono
        
    Returns:
        pygame.mixer.Sound: Objet son prêt à être joué
    """
    wav_bytes = _mono_to_stereo_wav(mono_int16)
    buf = io.BytesIO(wav_bytes)
    return pygame.mixer.Sound(buf)

def _synth_slice():
    """Son de tranchage - Swoosh rapide descendant"""
    dur = 0.15  # Durée en secondes
    t   = np.linspace(0, dur, int(SR * dur), endpoint=False)  # Axe du temps
    freq = 2000 - 1200 * (t / dur)  # Fréquence qui descend de 2000Hz à 800Hz
    env  = np.exp(-t * 40)          # Enveloppe exponentielle (décroissance rapide)
    sig  = np.sin(2 * np.pi * freq * t) * env  # Signal sinusoïdal modulé
    sig += np.random.randn(len(t)) * 0.15 * np.exp(-t * 30)  # Bruit blanc ajouté
    return (sig * 0.7 * 32767).astype(np.int16)

def _synth_fruit_slice(base_freq, harmonics):
    """
    Son de tranchage de Devil Fruit - Tonalité personnalisée.
    
    Args:
        base_freq (float): Fréquence de base
        harmonics (list): Liste de tuples (harmonique, amplitude)
    """
    dur = 0.22
    t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.exp(-t * 22)  # Enveloppe
    sig = np.zeros_like(t)
    # Ajoute chaque harmonique
    for h, amp in harmonics:
        sig += np.sin(2 * np.pi * base_freq * h * t) * amp
    sig *= env
    sig += np.random.randn(len(t)) * 0.08 * np.exp(-t * 28)  # Texture
    return (sig * 0.65 * 32767).astype(np.int16)

def _synth_rare():
    """Son spécial pour le fruit rare - Comme 'ROOM!' de Law"""
    dur = 0.5
    t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.exp(-t * 8)
    # Plusieurs fréquences superposées pour un son riche
    sig = (np.sin(2 * np.pi * 800 * t) * 0.3
         + np.sin(2 * np.pi * 1200 * t) * 0.2
         + np.sin(2 * np.pi * 1600 * t) * 0.15) * env
    return (sig * 32767).astype(np.int16)

def _synth_combo():
    """Son de combo - Arpège ascendant"""
    parts = []
    for i, f in enumerate([440, 554, 659]):  # Notes: La, Do#, Mi
        dur = 0.18
        t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
        env = np.exp(-t * 12)
        parts.append(np.sin(2 * np.pi * f * t) * env * 0.5)
        if i < 2:
            parts.append(np.zeros(int(SR * 0.06)))  # Silence entre notes
    return (np.concatenate(parts) * 32767).astype(np.int16)

def _synth_miss():
    """Son de fruit manqué - Ton bas et triste"""
    dur = 0.30
    t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.exp(-t * 15)
    sig = np.sin(2 * np.pi * 80 * t) * env * 0.6  # 80 Hz = note très basse
    sig += np.random.randn(len(t)) * np.exp(-t * 20) * 0.2  # Bruit
    return (sig * 32767).astype(np.int16)

def _synth_bomb():
    """Son d'explosion - Grondement grave avec crépitements"""
    dur = 0.70
    t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.exp(-t * 8)
    # Grondement bas (40Hz et 60Hz)
    rumble = np.sin(2 * np.pi * 40 * t) * env * 0.45
    rumble += np.sin(2 * np.pi * 60 * t) * env * 0.25
    # Crépitement (bruit blanc)
    crack  = np.random.randn(len(t)) * np.exp(-t * 22) * 0.45
    return ((rumble + crack) * 32767).astype(np.int16)

def _synth_ice():
    """Son de glace - Tons cristallins aigus"""
    dur = 0.55
    t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
    env = np.exp(-t * 10)
    # Superposition de fréquences aiguës (1200, 2400, 3600 Hz)
    sig = (np.sin(2 * np.pi * 1200 * t) * 0.30
         + np.sin(2 * np.pi * 2400 * t) * 0.20
         + np.sin(2 * np.pi * 3600 * t) * 0.12) * env
    return (sig * 32767).astype(np.int16)

def _synth_levelup():
    """Son de montée de niveau - Arpège triomphant"""
    parts = []
    for f in [523, 784]:  # Notes: Do, Sol (une quinte)
        dur = 0.35
        t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
        env = np.exp(-t * 6)
        # Note fondamentale + harmonique
        parts.append((np.sin(2 * np.pi * f * t) * 0.4
                     + np.sin(2 * np.pi * f * 2 * t) * 0.15) * env)
        parts.append(np.zeros(int(SR * 0.08)))  # Pause
    return (np.concatenate(parts) * 32767).astype(np.int16)

def _synth_gameover():
    """Son de game over - Descente chromatique triste"""
    parts = []
    for f in [392, 330, 262]:  # Notes descendantes: Sol, Mi, Do
        dur = 0.40
        t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
        env = np.exp(-t * 5)
        parts.append((np.sin(2 * np.pi * f * t) * 0.35
                     + np.sin(2 * np.pi * f * 1.5 * t) * 0.10) * env)
        parts.append(np.zeros(int(SR * 0.12)))  # Pause
    return (np.concatenate(parts) * 32767).astype(np.int16)

def _synth_menu_theme():
    """Thème du menu - Mélodie simple et entraînante"""
    notes = [(330, 0.30), (392, 0.20), (440, 0.30),
             (523, 0.40), (440, 0.20), (392, 0.30), (330, 0.50)]
    parts = []
    for f, dur in notes:
        t   = np.linspace(0, dur, int(SR * dur), endpoint=False)
        env = np.minimum(1.0, t * 20) * np.exp(-t * 3)  # Attaque + décroissance
        parts.append((np.sin(2 * np.pi * f * t) * 0.24
                     + np.sin(2 * np.pi * f * 2 * t) * 0.08) * env)
    return (np.concatenate(parts) * 32767).astype(np.int16)

def synthesize_all_sounds():
    """
    Charge les effets sonores One Piece depuis les fichiers MP3.
    Génère des sons de remplacement si les fichiers sont manquants.
    
    Returns:
        dict: Dictionnaire contenant tous les sons du jeu
    """
    sounds = {}
    
    print("  Loading One Piece sound effects:\n")
    
    # Tente de charger les vrais sons One Piece depuis les MP3
    real_sounds_loaded = {}
    for sound_name, sound_path in SOUND_FILES.items():
        try:
            sounds[sound_name] = pygame.mixer.Sound(sound_path)
            real_sounds_loaded[sound_name] = True
            print(f"    ✓ Loaded {sound_name}: {os.path.basename(sound_path)}")
        except Exception as e:
            print(f"    ✗ Failed to load {sound_name}: {e}")
            real_sounds_loaded[sound_name] = False
    
    # Génère des sons de synthèse pour ceux qui manquent
    print("\n  Generating fallback sounds for missing files:")
    
    if not real_sounds_loaded.get('slice'):
        sounds['slice'] = _to_sound(_synth_slice())
        print(f"    ✓ Synthesized: slice")
    
    if not real_sounds_loaded.get('bomb'):
        sounds['bomb'] = _to_sound(_synth_bomb())
        print(f"    ✓ Synthesized: bomb")
    
    if not real_sounds_loaded.get('gameover'):
        sounds['gameover'] = _to_sound(_synth_gameover())
        print(f"    ✓ Synthesized: gameover")
    
    if not real_sounds_loaded.get('levelup'):
        sounds['levelup'] = _to_sound(_synth_levelup())
        print(f"    ✓ Synthesized: levelup")
    
    # Génère toujours ces sons additionnels (pas de MP3 pour eux)
    sounds['combo'] = _to_sound(_synth_combo())      # Son de combo
    sounds['miss'] = _to_sound(_synth_miss())        # Son de fruit manqué
    sounds['ice'] = _to_sound(_synth_ice())          # Son de glace
    sounds['menu'] = _to_sound(_synth_menu_theme())  # Musique du menu
    
    # Sons spécifiques pour chaque Devil Fruit
    sounds['gomu'] = _to_sound(_synth_fruit_slice(800,  [(1, 0.40), (2, 0.25), (3, 0.10)]))  # Luffy
    sounds['mera'] = _to_sound(_synth_fruit_slice(1400, [(1, 0.35), (1.5, 0.22), (2, 0.14)]))  # Ace
    sounds['hie'] = _to_sound(_synth_fruit_slice(2200, [(1, 0.30), (2, 0.20), (3, 0.14)]))  # Aokiji
    sounds['yami'] = _to_sound(_synth_fruit_slice(200,  [(1, 0.40), (2, 0.16), (4, 0.08)]))  # Barbe Noire
    sounds['rare'] = _to_sound(_synth_rare())        # Fruit rare (Law)
    
    print(f"\n  Total sounds ready: {len(sounds)}")
    return sounds

# ─────────────────────────────────────────────
# VARIABLES GLOBALES DU JEU
# ─────────────────────────────────────────────
# Ces variables stockent l'état du jeu et sont modifiées pendant l'exécution
screen       = None  # Fenêtre du jeu
clock        = None  # Horloge pour contrôler les FPS
title_font   = None  # Police pour le titre (grande)
large_font   = None  # Police large
medium_font  = None  # Police moyenne
small_font   = None  # Police petite
letter_font  = None  # Police pour les lettres sur les fruits
image_cache  = {}    # Cache des images chargées
onepiece_chars = []  # Images des personnages One Piece
sounds       = {}    # Dictionnaire des sons

# État du jeu
state              = 'menu'  # État actuel: 'menu', 'playing', ou 'gameover'
score              = 0       # Score du joueur
strikes            = 0       # Nombre de fruits manqués (max 3)
combo              = 0       # Taille du combo actuel
combo_display_time = 0       # Moment d'affichage du combo (millisecondes)
frozen_time        = 0       # Jusqu'à quand le temps est gelé (millisecondes)
level              = 1       # Niveau actuel
spawn_timer        = 0       # Chronomètre pour l'apparition des fruits
level_flash_time   = 0       # Moment de l'affichage du nouveau niveau
rare_fruit_spawned = False   # Le fruit rare est-il apparu ce niveau?

# Listes des objets du jeu
fruits     = []  # Liste des fruits à l'écran
particles  = []  # Liste des particules d'effets visuels

# Effets visuels
strike_shake = [0, 0, 0]     # Tremblement des X de strikes
menu_music_channel = None    # Canal audio pour la musique du menu

# ─────────────────────────────────────────────
# FONCTIONS UTILITAIRES POUR LE SON
# ─────────────────────────────────────────────

def play_sound(name, loops=0):
    """
    Joue un effet sonore.
    
    Args:
        name (str): Nom du son à jouer
        loops (int): Nombre de répétitions (-1 = infini)
    """
    if name in sounds:
        sounds[name].play(loops)

def stop_menu_music():
    """Arrête la musique du menu si elle joue."""
    global menu_music_channel
    if menu_music_channel and menu_music_channel.get_busy():
        menu_music_channel.stop()
    menu_music_channel = None

def start_menu_music():
    """Démarre la musique du menu en boucle."""
    global menu_music_channel
    stop_menu_music()
    if 'menu' in sounds:
        menu_music_channel = sounds['menu'].play(loops=-1)  # Joue en boucle infinie

# ─────────────────────────────────────────────
# CHARGEMENT DES IMAGES
# ─────────────────────────────────────────────

def load_images():
    """
    Charge toutes les images du jeu:
    - Images des Devil Fruits
    - Images des objets spéciaux (bombe, glace)
    - Images des personnages One Piece pour la décoration
    
    Si une image n'existe pas, crée une image de remplacement.
    """
    global image_cache, onepiece_chars
    image_cache = {}
    onepiece_chars = []
    
    print("  Loading images:\n")
    
    # Charge toutes les images de fruits et d'objets
    all_items = FRUITS + SPECIAL_ITEMS + [RARE_FRUIT]
    for item in all_items:
        path = item['image']
        print(f"  Trying: {item['name']}")
        try:
            # Charge et redimensionne l'image
            original = pygame.image.load(path)
            image_cache[item['name']] = pygame.transform.smoothscale(original, (130, 130))
            print(f"    ✓ Loaded")
        except Exception as e:
            # Si l'image n'existe pas, crée une image de remplacement
            print(f"    ✗ Using fallback")
            surf = pygame.Surface((130, 130), pygame.SRCALPHA)
            
            # Style spécial pour le fruit rare (doré avec étoiles)
            if item.get('points') == 10:
                pygame.draw.circle(surf, GOLD, (65, 65), 58)
                pygame.draw.circle(surf, YELLOW, (48, 48), 30)
                # Dessine des étoiles
                for i in range(5):
                    angle = (i * 144) * math.pi / 180
                    x = 65 + int(40 * math.cos(angle))
                    y = 65 + int(40 * math.sin(angle))
                    pygame.draw.circle(surf, WHITE, (x, y), 5)
            else:
                # Style normal pour les autres fruits
                pygame.draw.circle(surf, item['color'], (65, 65), 58)
                pygame.draw.circle(surf, (min(255, item['color'][0]+60),
                                          min(255, item['color'][1]+60),
                                          min(255, item['color'][2]+60)), (48, 48), 30)
                pygame.draw.arc(surf, WHITE, (30, 30, 70, 70), 0.5, 2.5, 4)
                pygame.draw.arc(surf, WHITE, (42, 42, 46, 46), 3.5, 5.5, 3)
            image_cache[item['name']] = surf
    
    # Charge les images des personnages One Piece
    print("\n  Loading One Piece character images:")
    for path in ONE_PIECE_IMAGES:
        try:
            img = pygame.image.load(path)
            # Redimensionne à une taille raisonnable pour le menu
            onepiece_chars.append(pygame.transform.smoothscale(img, (120, 120)))
            print(f"    ✓ Loaded character image")
        except Exception as e:
            print(f"    ✗ Failed to load: {path}")

# ─────────────────────────────────────────────
# FRUIT FUNCTIONS
# ─────────────────────────────────────────────
def make_fruit(fruit_data, x, y, params, is_rare=False):
    vy = random.uniform(params['vy_max'], params['vy_min'])
    return {
        'data':           fruit_data,
        'x':              x,
        'y':              y,
        'velocity_x':     random.uniform(-4, 4),
        'velocity_y':     vy,
        'gravity':        params['gravity'],
        'rotation':       random.uniform(0, 360),
        'rotation_speed': random.uniform(-8, 8),
        'size':           130,
        'sliced':         False,
        'slice_time':     0,
        'is_rare':        is_rare,
    }

def update_fruit(fruit, frozen):
    if frozen or fruit['sliced']:
        return
    fruit['velocity_y'] += fruit['gravity']
    fruit['y']          += fruit['velocity_y']
    fruit['x']          += fruit['velocity_x']
    fruit['rotation']   += fruit['rotation_speed']

def fruit_is_missed(fruit):
    return fruit['y'] > SCREEN_HEIGHT + fruit['size'] and not fruit['sliced']

def draw_fruit(surf, fruit, font):
    data     = fruit['data']
    base_img = image_cache.get(data['name'])
    x, y     = int(fruit['x']), int(fruit['y'])
    rot      = fruit['rotation']
    size     = fruit['size']
    color    = data['color']

    if fruit['sliced']:
        elapsed  = pygame.time.get_ticks() - fruit['slice_time']
        duration = 700
        alpha    = max(0, 255 - (elapsed * 255 // duration))

        if alpha > 0 and base_img:
            gravity = 0.4
            for half in (fruit['left_half'], fruit['right_half']):
                half['x']  += half['vx']
                half['y']  += half['vy']
                half['vy'] += gravity
                half['rot'] += half['rot_speed']

            half_w = size // 2
            left_crop  = pygame.Surface((half_w, size), pygame.SRCALPHA)
            left_crop.blit(base_img, (0, 0))
            right_crop = pygame.Surface((half_w, size), pygame.SRCALPHA)
            right_crop.blit(base_img, (-half_w, 0))

            for half, crop in ((fruit['left_half'], left_crop),
                               (fruit['right_half'], right_crop)):
                rotated = pygame.transform.rotate(crop, half['rot'])
                rotated.set_alpha(alpha)
                rect = rotated.get_rect(center=(int(half['x']), int(half['y'])))
                surf.blit(rotated, rect)

            # Sparkle effect for rare fruit
            if fruit.get('is_rare'):
                for half in (fruit['left_half'], fruit['right_half']):
                    gs = 50
                    gs_surf = pygame.Surface((gs, gs), pygame.SRCALPHA)
                    pygame.draw.circle(gs_surf, (*GOLD, alpha // 2), (gs // 2, gs // 2), gs // 2)
                    surf.blit(gs_surf, (int(half['x']) - gs // 2, int(half['y']) - gs // 2))

        return elapsed < duration

    # Un-sliced drawing - NO GLOW CIRCLE
    if base_img:
        # Special effects for rare fruit (golden sparkle)
        if fruit.get('is_rare'):
            sparkle_size = int(10 + 5 * math.sin(pygame.time.get_ticks() / 100))
            for angle in [0, 90, 180, 270]:
                rad = math.radians(angle + pygame.time.get_ticks() / 10)
                sx = x + int(70 * math.cos(rad))
                sy = y + int(70 * math.sin(rad))
                pygame.draw.circle(surf, GOLD, (sx, sy), sparkle_size)
        
        # Draw fruit image
        rotated = pygame.transform.rotate(base_img, rot)
        rect    = rotated.get_rect(center=(x, y))
        surf.blit(rotated, rect)

        # Letter label with improved styling
        letter_surf = font.render(data['letter'], True, WHITE)
        letter_rect = letter_surf.get_rect(center=(x, y + 72))

        bg_size = 38
        bg_rect = pygame.Rect(0, 0, bg_size, bg_size)
        bg_rect.center = letter_rect.center

        # Different styling based on type
        if data.get('type') == 'bomb':
            pygame.draw.rect(surf, RED, bg_rect, border_radius=10)
            pygame.draw.rect(surf, (150, 0, 0), bg_rect, 3, border_radius=10)
        elif data.get('type') == 'ice':
            pygame.draw.rect(surf, (173, 216, 230), bg_rect, border_radius=10)
            pygame.draw.rect(surf, WHITE, bg_rect, 3, border_radius=10)
        elif fruit.get('is_rare'):
            # Golden border for rare fruit
            pygame.draw.rect(surf, GOLD, bg_rect, border_radius=10)
            pygame.draw.rect(surf, YELLOW, bg_rect, 4, border_radius=10)
        else:
            pygame.draw.rect(surf, PIRATE_FLAG_BLACK, bg_rect, border_radius=10)
            pygame.draw.rect(surf, color, bg_rect, 3, border_radius=10)

        surf.blit(letter_surf, letter_rect)

    return True

# ─────────────────────────────────────────────
# PARTICLE FUNCTIONS
# ─────────────────────────────────────────────
def make_particle_effect(x, y, color, is_rare=False):
    burst = []
    count = 30 if is_rare else 20
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 12 if is_rare else 10)
        burst.append({
            'x': x, 'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'life': 255,
            'color': color,
            'size': random.randint(4, 9 if is_rare else 7),
        })
    return burst

def update_particles(particle_list):
    for p in particle_list:
        p['x']  += p['vx']
        p['y']  += p['vy']
        p['vy'] += 0.3
        p['life'] -= 5
    particle_list[:] = [p for p in particle_list if p['life'] > 0]

def draw_particles(surf, particle_list):
    for p in particle_list:
        a = max(0, p['life'])
        s = p['size']
        ps = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.circle(ps, (*p['color'], a), (s, s), s)
        surf.blit(ps, (int(p['x']), int(p['y'])))

# ─────────────────────────────────────────────
# SPAWN / SLICE
# ─────────────────────────────────────────────
def spawn_fruit():
    global rare_fruit_spawned
    params = get_level_params(level)
    
    # Check if we should spawn rare fruit (once per level)
    if not rare_fruit_spawned and random.random() < 0.15:  # 15% chance to spawn rare
        fruit_data = RARE_FRUIT
        rare_fruit_spawned = True
        is_rare = True
    elif random.random() < params['special_chance']:
        fruit_data = random.choice(SPECIAL_ITEMS)
        is_rare = False
    else:
        fruit_data = random.choice(FRUITS)
        is_rare = False
    
    x = random.randint(100, SCREEN_WIDTH - 100)
    y = SCREEN_HEIGHT + 80
    fruits.append(make_fruit(fruit_data, x, y, params, is_rare))

def slice_fruits(key):
    global score, combo, combo_display_time, frozen_time, state

    sliced_this_frame = []
    for f in fruits:
        if f['data']['key'] == key and not f['sliced']:
            f['sliced']     = True
            f['slice_time'] = pygame.time.get_ticks()
            f['left_half']  = {
                'x': f['x'], 'y': f['y'],
                'vx': random.uniform(-6, -3),
                'vy': random.uniform(-4, -1),
                'rot': f['rotation'],
                'rot_speed': random.uniform(-12, -6),
            }
            f['right_half'] = {
                'x': f['x'], 'y': f['y'],
                'vx': random.uniform(3, 6),
                'vy': random.uniform(-4, -1),
                'rot': f['rotation'],
                'rot_speed': random.uniform(6, 12),
            }
            sliced_this_frame.append(f)
            particles.extend(make_particle_effect(f['x'], f['y'], f['data']['color'], f.get('is_rare', False)))

    if not sliced_this_frame:
        return

    play_sound(sliced_this_frame[0]['data'].get('sound', 'slice'))
    # Removed the extra slice sound to avoid sound spam

    # Check for bombs
    bombs = [f for f in sliced_this_frame if f['data'].get('type') == 'bomb']
    if bombs:
        play_sound('bomb')
        state = 'gameover'
        for b in bombs:
            for _ in range(3):
                particles.extend(make_particle_effect(b['x'], b['y'], RED))
        return

    # Check for ice
    ice = [f for f in sliced_this_frame if f['data'].get('type') == 'ice']
    if ice:
        play_sound('ice')
        frozen_time = pygame.time.get_ticks() + 4000

    # Check for rare fruit
    rare = [f for f in sliced_this_frame if f.get('is_rare')]
    if rare:
        score += RARE_FRUIT['points']
        combo = RARE_FRUIT['points']
        combo_display_time = pygame.time.get_ticks()
        play_sound('rare')
        play_sound('victory')  # Victory sound for rare fruit!

    # Regular fruits
    regular = [f for f in sliced_this_frame if 'type' not in f['data'] and not f.get('is_rare')]
    if regular:
        count = len(regular)
        score += count
        if count > 1:
            combo = count
            combo_display_time = pygame.time.get_ticks()
            play_sound('combo')
            if count >= 3:  # Big combo gets victory sound!
                play_sound('victory')

# ─────────────────────────────────────────────
# DRAWING HELPERS
# ─────────────────────────────────────────────
def draw_cloud(surf, x, y, width, height):
    """Draw fluffy clouds"""
    pygame.draw.ellipse(surf, WHITE, (x, y + height // 3, width // 3, height // 2))
    pygame.draw.ellipse(surf, WHITE, (x + width // 3, y, width // 2, height))
    pygame.draw.ellipse(surf, WHITE, (x + width // 2, y + height // 3, width // 2, height // 2))

def draw_clouds(surf):
    """Animated clouds in background"""
    for i in range(5):
        cx = (i * 250 + (pygame.time.get_ticks() // 50) % 250) % SCREEN_WIDTH
        draw_cloud(surf, cx, 50 + i * 80, 120, 60)

def draw_waves(surf):
    """Draw ocean waves at bottom"""
    wave_height = 40
    for i in range(20):
        x_offset = (pygame.time.get_ticks() // 30 + i * 50) % SCREEN_WIDTH
        points = [
            (x_offset - 25, SCREEN_HEIGHT - wave_height),
            (x_offset, SCREEN_HEIGHT - wave_height - 15),
            (x_offset + 25, SCREEN_HEIGHT - wave_height),
            (x_offset + 50, SCREEN_HEIGHT),
            (x_offset - 50, SCREEN_HEIGHT)
        ]
        pygame.draw.polygon(surf, OCEAN_BLUE, points)

def draw_outlined_text(surf, font, text, color, outline_color, cx, cy, thickness=3):
    """Draw text with outline for better visibility"""
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx == 0 and dy == 0:
                continue
            o = font.render(text, True, outline_color)
            surf.blit(o, o.get_rect(center=(cx + dx, cy + dy)))
    main = font.render(text, True, color)
    surf.blit(main, main.get_rect(center=(cx, cy)))

def draw_pirate_flag_icon(surf, x, y, size):
    """Draw a small pirate flag (Straw Hat Pirates style)"""
    # Flag background
    pygame.draw.circle(surf, WHITE, (x, y), size)
    pygame.draw.circle(surf, BLACK, (x, y), size - 3)
    # Skull
    pygame.draw.circle(surf, WHITE, (x, y - 3), size // 3)
    # Straw hat
    pygame.draw.ellipse(surf, STRAW_HAT_YELLOW, (x - size//2, y + 2, size, size // 3))
    # Crossbones
    pygame.draw.line(surf, WHITE, (x - size//2 + 5, y + size//2), (x + size//2 - 5, y + size//2), 3)

# ─────────────────────────────────────────────
# SCREEN DRAWERS
# ─────────────────────────────────────────────
def draw_menu():
    """Clean and simple One Piece themed menu with character images on sides"""
    screen.fill(SKY_BLUE)
    draw_clouds(screen)
    draw_waves(screen)
    
    # Display One Piece character images on the LEFT side
    left_x = 30
    left_start_y = 150
    for i in range(min(3, len(onepiece_chars))):
        screen.blit(onepiece_chars[i], (left_x, left_start_y + i * 140))
    
    # Display One Piece character images on the RIGHT side
    right_x = SCREEN_WIDTH - 150
    right_start_y = 150
    for i in range(3, min(5, len(onepiece_chars))):
        screen.blit(onepiece_chars[i], (right_x, right_start_y + (i - 3) * 140))
    
    # Main title - big and bold in CENTER
    draw_outlined_text(screen, title_font, "DEVIL FRUIT", ORANGE, (211, 84, 0), SCREEN_WIDTH // 2, 100, 5)
    draw_outlined_text(screen, title_font, "SLICER", ORANGE, (211, 84, 0), SCREEN_WIDTH // 2, 170, 5)
    
    # Simple subtitle
    subtitle = medium_font.render("One Piece", True, PIRATE_FLAG_BLACK)
    screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 225)))
    
    # Show Devil Fruits with keys - centered
    showcase_y = 280
    spacing = 100
    start_x = SCREEN_WIDTH // 2 - (len(FRUITS) * spacing // 2) + 50
    
    for i, item in enumerate(FRUITS):
        x_pos = start_x + i * spacing
        
        # Fruit image
        img = image_cache.get(item['name'])
        if img:
            small_img = pygame.transform.smoothscale(img, (60, 60))
            screen.blit(small_img, (x_pos - 30, showcase_y))
        
        # Key letter
        key_surf = medium_font.render(item['letter'], True, WHITE)
        key_bg = pygame.Rect(x_pos - 18, showcase_y + 70, 36, 36)
        pygame.draw.rect(screen, item['color'], key_bg, border_radius=8)
        pygame.draw.rect(screen, WHITE, key_bg, 3, border_radius=8)
        screen.blit(key_surf, key_surf.get_rect(center=key_bg.center))
    
    # Instructions box - centered and clean
    y_start = 400
    instructions = [
        "Press letter keys to slice fruits",
        "Rare fruit O = +10 points",
        "Avoid bombs X | Ice I freezes time",
        "3 missed fruits = Game Over",
    ]
    
    for i, line in enumerate(instructions):
        text = small_font.render(line, True, PIRATE_FLAG_BLACK)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, y_start + i * 30)))
    
    # Start prompt - pulsing at bottom
    pulse = abs(math.sin(pygame.time.get_ticks() / 300))
    start_bg = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 70, 400, 50)
    pygame.draw.rect(screen, (255, int(pulse * 200), 0, 180), start_bg, border_radius=15)
    pygame.draw.rect(screen, ORANGE, start_bg, 4, border_radius=15)
    
    start = large_font.render("PRESS SPACE", True, WHITE)
    screen.blit(start, start.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45)))

def draw_playing():
    """Enhanced One Piece themed gameplay UI"""
    screen.fill(SKY_BLUE)
    draw_clouds(screen)
    draw_waves(screen)
    
    # Score panel with pirate theme
    score_bg = pygame.Rect(20, 20, 220, 110)
    pygame.draw.rect(screen, ORANGE, score_bg, border_radius=15)
    pygame.draw.rect(screen, (211, 84, 0), score_bg, 5, border_radius=15)
    
    # Pirate flag icon
    draw_pirate_flag_icon(screen, 45, 45, 18)
    
    sl = small_font.render("SCORE", True, WHITE)
    sv = large_font.render(f"{score:04d}", True, WHITE)
    screen.blit(sl, (score_bg.centerx - sl.get_width() // 2, score_bg.y + 15))
    screen.blit(sv, (score_bg.centerx - sv.get_width() // 2, score_bg.y + 50))
    
    # Level panel
    level_bg = pygame.Rect(260, 20, 150, 110)
    pygame.draw.rect(screen, GREEN, level_bg, border_radius=15)
    pygame.draw.rect(screen, (39, 174, 96), level_bg, 5, border_radius=15)
    
    ll = small_font.render("LEVEL", True, WHITE)
    lv = large_font.render(f"{level}", True, WHITE)
    screen.blit(ll, (level_bg.centerx - ll.get_width() // 2, level_bg.y + 15))
    screen.blit(lv, (level_bg.centerx - lv.get_width() // 2, level_bg.y + 50))
    
    # Progress bar for next level
    points_in_level = score % POINTS_PER_LEVEL
    bar_bg = pygame.Rect(level_bg.x + 10, level_bg.bottom - 20, 130, 12)
    bar_fill_w = int(130 * points_in_level / POINTS_PER_LEVEL)
    pygame.draw.rect(screen, (39, 174, 96), bar_bg, border_radius=5)
    if bar_fill_w > 0:
        pygame.draw.rect(screen, GOLD, pygame.Rect(bar_bg.x, bar_bg.y, bar_fill_w, bar_bg.height), border_radius=5)
    
    # Strike counter (X marks)
    strike_x = SCREEN_WIDTH - 240
    for i in range(3):
        sx = strike_x + i * 70 + strike_shake[i]
        sr = pygame.Rect(sx, 25, 55, 55)
        if i < strikes:
            pygame.draw.rect(screen, RED, sr, border_radius=12)
            pygame.draw.line(screen, WHITE, (sr.left + 12, sr.top + 12), (sr.right - 12, sr.bottom - 12), 6)
            pygame.draw.line(screen, WHITE, (sr.right - 12, sr.top + 12), (sr.left + 12, sr.bottom - 12), 6)
        else:
            pygame.draw.rect(screen, WHITE, sr, 4, border_radius=12)
    
    # Frozen time indicator
    if frozen_time > pygame.time.get_ticks():
        fb = pygame.Rect(SCREEN_WIDTH // 2 - 140, 20, 280, 70)
        pygame.draw.rect(screen, ICE_BLUE, fb, border_radius=12)
        pygame.draw.rect(screen, WHITE, fb, 4, border_radius=12)
        ft = medium_font.render("TIME FROZEN", True, WHITE)
        screen.blit(ft, (fb.centerx - ft.get_width() // 2, fb.y + 20))
    
    # Level up flash
    if level_flash_time > 0:
        elapsed = pygame.time.get_ticks() - level_flash_time
        if elapsed < 1500:
            alpha = max(0, 220 - int(220 * elapsed / 1500))
            flash_surf = pygame.Surface((SCREEN_WIDTH, 100), pygame.SRCALPHA)
            flash_surf.fill((255, 215, 0, alpha))
            screen.blit(flash_surf, (0, SCREEN_HEIGHT // 2 - 50))
            luf = title_font.render(f"LEVEL {level}!", True, WHITE)
            draw_outlined_text(screen, title_font, f"LEVEL {level}!", GOLD, ORANGE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 5)
    
    # Combo display
    if combo > 1 and pygame.time.get_ticks() - combo_display_time < 1800:
        elapsed = pygame.time.get_ticks() - combo_display_time
        cs = 1 + 0.4 * math.sin(elapsed / 80)
        
        if combo >= 10:  # Rare fruit bonus
            combo_text = f"+{combo} POINTS!"
            combo_color = GOLD
        else:
            combo_text = f"COMBO x{combo}!"
            combo_color = YELLOW
        
        ct = large_font.render(combo_text, True, combo_color)
        new_size = (int(ct.get_width() * cs), int(ct.get_height() * cs))
        scaled_ct = pygame.transform.scale(ct, new_size)
        draw_outlined_text(screen, large_font, combo_text, combo_color, RED, SCREEN_WIDTH // 2, 160, 4)
    
    # Draw fruits and particles
    fruits[:] = [f for f in fruits if draw_fruit(screen, f, letter_font)]
    draw_particles(screen, particles)

def draw_gameover():
    """Clean One Piece themed game over screen with character images on sides"""
    screen.fill(SKY_BLUE)
    draw_clouds(screen)
    draw_waves(screen)
    
    # Display One Piece characters on LEFT side
    if len(onepiece_chars) >= 2:
        screen.blit(onepiece_chars[0], (30, 150))
        if len(onepiece_chars) >= 3:
            screen.blit(onepiece_chars[2], (30, 350))
    
    # Display One Piece characters on RIGHT side
    if len(onepiece_chars) >= 2:
        screen.blit(onepiece_chars[1], (SCREEN_WIDTH - 150, 150))
        if len(onepiece_chars) >= 4:
            screen.blit(onepiece_chars[3], (SCREEN_WIDTH - 150, 350))
    
    # Large pirate flag at top center
    draw_pirate_flag_icon(screen, SCREEN_WIDTH // 2, 100, 50)
    
    # Game Over title
    draw_outlined_text(screen, title_font, "GAME OVER", RED, (150, 0, 0), SCREEN_WIDTH // 2, 200, 5)
    
    # Stats box - centered
    stats_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, 270, 500, 140)
    pygame.draw.rect(screen, (255, 255, 255, 220), stats_box, border_radius=20)
    pygame.draw.rect(screen, ORANGE, stats_box, 5, border_radius=20)
    
    st = large_font.render(f"Final Score: {score}", True, PIRATE_FLAG_BLACK)
    screen.blit(st, st.get_rect(center=(SCREEN_WIDTH // 2, 310)))
    
    lt = medium_font.render(f"Level Reached: {level}", True, PIRATE_FLAG_BLACK)
    screen.blit(lt, lt.get_rect(center=(SCREEN_WIDTH // 2, 360)))
    
    # Pirate-themed message
    flavours = [
        "The Grand Line awaits!",
        "Keep sailing, pirate!",
        "Your adventure continues!",
        "Set sail again!",
        "The One Piece is waiting!",
        "Never give up!",
    ]
    chosen = flavours[score % len(flavours)]
    ft = medium_font.render(chosen, True, ORANGE)
    screen.blit(ft, ft.get_rect(center=(SCREEN_WIDTH // 2, 440)))
    
    # Restart prompt - centered at bottom
    pulse = abs(math.sin(pygame.time.get_ticks() / 250))
    restart_bg = pygame.Rect(SCREEN_WIDTH // 2 - 200, 490, 400, 50)
    pygame.draw.rect(screen, (0, int(pulse * 200), 0, 180), restart_bg, border_radius=15)
    pygame.draw.rect(screen, GREEN, restart_bg, 4, border_radius=15)
    
    rt = large_font.render("PRESS SPACE", True, WHITE)
    screen.blit(rt, rt.get_rect(center=(SCREEN_WIDTH // 2, 515)))
    
    qt = small_font.render("ESC to quit", True, PIRATE_FLAG_BLACK)
    screen.blit(qt, qt.get_rect(center=(SCREEN_WIDTH // 2, 560)))

# ─────────────────────────────────────────────
# GAME LOOP FUNCTIONS
# ─────────────────────────────────────────────
def reset_game():
    global score, strikes, combo, combo_display_time, frozen_time
    global fruits, particles, spawn_timer, level, strike_shake, level_flash_time
    global rare_fruit_spawned
    
    score = 0
    strikes = 0
    combo = 0
    combo_display_time = 0
    frozen_time = 0
    level = 1
    level_flash_time = 0
    rare_fruit_spawned = False
    fruits = []
    particles = []
    strike_shake = [0, 0, 0]
    spawn_timer = pygame.time.get_ticks()

def handle_events():
    global state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if state == 'menu' and event.key == pygame.K_SPACE:
                stop_menu_music()
                state = 'playing'
                reset_game()
            elif state == 'playing':
                slice_fruits(event.key)
            elif state == 'gameover' and event.key == pygame.K_SPACE:
                state = 'menu'
                start_menu_music()
    return True

def update():
    global strikes, state, level, spawn_timer, strike_shake, level_flash_time, rare_fruit_spawned
    if state != 'playing':
        return
    
    current_time = pygame.time.get_ticks()
    params = get_level_params(level)
    frozen = frozen_time > current_time
    active_count = sum(1 for f in fruits if not f['sliced'])
    
    # Spawn fruits
    if (current_time - spawn_timer > params['spawn_interval']
            and not frozen
            and active_count < params['max_on_screen']):
        spawn_fruit()
        spawn_timer = current_time
    
    # Update fruits
    for f in fruits:
        update_fruit(f, frozen)
    
    # Check for missed fruits
    missed = [f for f in fruits if fruit_is_missed(f) and 'type' not in f['data']]
    if missed:
        play_sound('miss')
        for i in range(len(missed)):
            idx = strikes + i
            if idx < 3:
                strike_shake[idx] = 8
        strikes += len(missed)
        if strikes >= 3:
            state = 'gameover'
            play_sound('gameover')
    
    fruits[:] = [f for f in fruits if not fruit_is_missed(f)]
    update_particles(particles)
    
    # Shake animation
    for i in range(3):
        if strike_shake[i] > 0:
            strike_shake[i] = max(0, strike_shake[i] - 1)
    
    # Level progression
    new_level = (score // POINTS_PER_LEVEL) + 1
    if new_level != level:
        level = new_level
        level_flash_time = pygame.time.get_ticks()
        rare_fruit_spawned = False  # Reset rare fruit for new level
        play_sound('levelup')
        print(f"  Level {level} reached!")

def draw():
    if state == 'menu':
        draw_menu()
    elif state == 'playing':
        draw_playing()
    elif state == 'gameover':
        draw_gameover()
    pygame.display.flip()

# ─────────────────────────────────────────────
# INIT & MAIN
# ─────────────────────────────────────────────
def init_game():
    global screen, clock
    global title_font, large_font, medium_font, small_font, letter_font
    global sounds
    
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2, buffer=512)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Devil Fruit Slicer - One Piece Edition")
    clock = pygame.time.Clock()
    
    title_font = pygame.font.Font(None, 90)
    large_font = pygame.font.Font(None, 56)
    medium_font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)
    letter_font = pygame.font.Font(None, 32)
    
    print("🎵 Loading One Piece sound effects...")
    sounds = synthesize_all_sounds()
    print()
    
    print("🎨 Loading Devil Fruit images...")
    load_images()
    print("  ✓ Images ready\n")

def main():
    init_game()
    start_menu_music()
    running = True
    while running:
        running = handle_events()
        update()
        draw()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
