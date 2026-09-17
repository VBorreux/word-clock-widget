# Word Clock — horloge textuelle façon Qlocktwo

Widget de bureau Linux qui affiche l'heure en toutes lettres, dans une grille de
caractères : les mots de l'heure courante s'illuminent, les autres restent
éteints. Inspiré de l'horloge **Qlocktwo** de Biegert & Funk (projet non
affilié, voir la section *Marque*).

**Langues :** français, anglais, allemand, espagnol, italien, néerlandais,
portugais, russe, chinois, arabe (optionnel).

> **English:** a Linux desktop word-clock widget (Qlocktwo-style) written in
> Python + PyQt6, with 10 languages, a settings dialog, system-tray support and
> packaging. See the [English summary](#english-summary).

---

## Aperçu

Exemple à 10 h 15 en français :

```
I L E S T Q U A T R E
D O U Z E T R O I S A
O N Z E C I N Q B C D
S E P T H U I T E F G
N E U F D E U X U N E
S I X D I X H I J K L
H E U R E S H E U R E
M O I N S E T L E M N
Q U A R T D E M I E O
V I N G T C I N Q P Q
D I X R S T U V W X Y
```

Les lettres `IL EST DIX HEURES ET QUART` sont éclairées ; elles se lisent dans
l'ordre, de haut en bas. Quatre points dans les coins indiquent les minutes
exactes (1 à 4 au-delà du multiple de 5).

## Fonctionnalités

- Fenêtre sans bordure, translucide, aux coins arrondis, déplaçable à la souris.
- Illumination avec effet de lueur (glow) réglable.
- 10 langues, grilles disposées pour que chaque phrase se lise naturellement.
- Interface et menus traduits dans la langue de l'application.
- Sélecteur de langue avec drapeaux (dessinés, sans images externes).
- Menu clic droit : réglages, langue, opacité, taille, couleurs, toujours
  au-dessus, quitter.
- Fenêtre de réglages complète : couleurs, fond, opacité, taille, police,
  intensité du glow, arrondi des coins, vitesse de rafraîchissement, heure
  numérique (12/24 h) et date, points des minutes.
- Aperçu en direct et thèmes prédéfinis (Sombre, Clair, Néon, Ambre, Minimal).
- Icône de zone de notification (menu et afficher/masquer).
- Configuration par machine dans `~/.config/qlocktwo/`.
- Service `systemd --user` et entrée d'autostart XDG.
- Empaquetage : bundle PyInstaller, `.deb`, AppImage.
- Aucune dépendance en dehors de PyQt6, entièrement installée dans un `venv`.

## Prérequis

- Linux avec un serveur graphique (Wayland ou X11).
- Python 3.10+ avec le support `venv` (`python3-venv`).
- PyQt6 (installé automatiquement dans `.venv`).

## Démarrage rapide

```bash
git clone https://github.com/VBorreux/word-clock-widget.git word-clock
cd word-clock
./run.sh
```

`run.sh` détecte un interpréteur Python capable de créer un environnement
virtuel, crée `.venv` si besoin, installe les dépendances puis lance le widget.
Rien n'est installé sur le système hôte.

Variantes :

```bash
./run.sh --settings   # ouvre directement la fenêtre de réglages
./run.sh test         # lance la suite de tests dans le venv
./run.sh --no-install # lance sans réinstaller les dépendances
```

Pour choisir l'interpréteur : `PYTHON=/usr/bin/python3.12 ./run.sh`.

## Utilisation

- **Déplacer** : clic gauche maintenu (drag).
- **Menu** : clic droit → Réglages, Langue, Opacité, Taille, Couleurs,
  Toujours au-dessus, Quitter.
- **Raccourcis** : `Ctrl+,` (réglages), `Ctrl+Q` / `Échap` (quitter).
- La position, la langue et tous les réglages sont sauvegardés dans
  `~/.config/qlocktwo/config.json` (surcharge possible via `QLOCKTWO_CONFIG`).

## Configuration

| Clé | Défaut | Description |
| --- | --- | --- |
| `language` | `en` | Code de langue (`fr`, `en`, `de`, `es`, `it`, `nl`, `pt`, `ru`, `zh`, `ar`) |
| `active_color` / `inactive_color` | `#FFFFFF` / `#222222` | Couleur des lettres |
| `background_color` | `#101014` | Couleur de fond |
| `opacity` | `0.85` | Opacité du fond (0.05–1.0) |
| `scale` | `1.0` | Taille de la grille |
| `glow` / `glow_strength` | `true` / `1.0` | Effet de lueur et intensité |
| `font_family` / `font_scale` | `""` / `1.0` | Police (`""` = auto) et taille du texte |
| `corner_radius` | `20` | Arrondi des coins |
| `show_dots` | `true` | Points des minutes |
| `show_digital` / `clock_24h` / `show_date` | `false` / `true` / `false` | Heure numérique et date |
| `refresh_ms` | `1000` | Intervalle de rafraîchissement |
| `always_on_top` | `false` | Toujours au-dessus |
| `enable_optional_locales` | `false` | Afficher l'arabe |
| `show_tray` | `true` | Icône de zone de notification |

## Langues

Les grilles sont définies dans `locales/`. Chaque module expose une grille, un
mapping mot → segments et une fonction `build(heure, minute)`. Un test garantit
que les mots s'illuminent toujours dans l'ordre de lecture.

Pour ajouter une langue : créez `locales/xx.py` sur le modèle d'une langue
existante, puis enregistrez-la dans `locales/__init__.py`. Ajoutez la traduction
de l'interface dans `i18n.py` et un drapeau dans `flags.py`.

## Service systemd et autostart

```bash
./service.sh install     # service systemd --user (démarrage à la session)
./service.sh uninstall
./service.sh start|stop|restart|status
./service.sh autostart   # alternative : entrée XDG autostart
./service.sh no-autostart
```

Contrôle du service : `systemctl --user status qlocktwo`.

## Empaquetage

```bash
./packaging/build.sh pyinstaller   # bundle autonome (build/dist/qlocktwo)
./packaging/build.sh deb           # paquet .deb
./packaging/build.sh appimage      # AppImage
./packaging/build.sh all
./packaging/build.sh clean
```

Les artefacts sont générés dans `build/` (ignoré par git).

## Structure du projet

```
locales/          grilles et logique horaire (10 langues)
flags.py          drapeaux dessinés avec Qt
i18n.py           traductions de l'interface
presets.py        thèmes de couleurs
settings.py       configuration (XDG) + valeurs par défaut
settings_dialog.py fenêtre de réglages
widget.py         fenêtre et rendu de la grille
tray.py           icône de zone de notification
main.py           point d'entrée
run.sh            environnement virtuel + lancement
service.sh        service systemd --user / autostart
packaging/        PyInstaller, .deb, AppImage
tests/            tests unitaires (unittest)
```

## Tests

```bash
./run.sh test
# ou, dans un venv avec PyQt6 :
python -m unittest discover -s tests -v
```

Les tests couvrent les grilles et l'ordre de lecture, la configuration,
l'i18n, les drapeaux et le rendu hors écran du widget.

## Crédits et licence

- **Auteur : Vincent Borreux** — © 2026.
- Distribué sous licence **MIT** (voir [LICENSE](LICENSE)).
- Toute utilisation, copie, modification ou redistribution, totale ou partielle,
  doit **conserver la mention de l'auteur original** et créditer
  **Vincent Borreux** dans les crédits ou la documentation du projet.
  Les versions modifiées doivent aussi indiquer qu'elles sont basées sur ce
  travail original (voir [NOTICE](NOTICE)).

Merci de mentionner « Word Clock de Vincent Borreux » lorsque vous réutilisez ou
modifiez ce code.

## Marque

« Qlocktwo » / « QlockTwo » est une marque de son propriétaire (Biegert & Funk).
Ce projet est un hommage indépendant, **non affilié** et non approuvé par le
propriétaire de la marque. Il n'utilise aucune ressource de l'horloge originale.

---

## English summary

A frameless Linux desktop word-clock widget (Qlocktwo-style) built with Python
and PyQt6. It lights up the words of the current time in a letter grid, supports
10 languages, a full settings dialog (colours, background, opacity, size, font,
glow, corner radius, refresh rate, digital time/date), live preview, colour
presets, a system-tray icon, per-machine configuration, a `systemd --user`
service and packaging (PyInstaller, `.deb`, AppImage).

```bash
git clone https://github.com/VBorreux/word-clock-widget.git word-clock && cd word-clock
./run.sh          # creates .venv, installs deps, launches the widget
./run.sh test     # runs the test suite
```

**Author: Vincent Borreux** — MIT licensed. Any use, copy, modification or
redistribution must keep the original author's credit (see [NOTICE](NOTICE)).
"Qlocktwo" is a trademark of its respective owner; this project is an
independent, non-affiliated tribute.
