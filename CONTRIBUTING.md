# Contribuer

Merci de votre intérêt ! Quelques règles simples.

## Attribution (important)

Toute contribution, réutilisation ou version modifiée doit conserver la mention
de l'auteur original, **Vincent Borreux**, dans les crédits ou la documentation
(voir [NOTICE](NOTICE) et [LICENSE](LICENSE)).

## Mise en place

```bash
git clone <URL_DU_DEPOT> word-clock
cd word-clock
./run.sh test        # crée le venv, installe PyQt6 et lance les tests
./run.sh             # lance le widget
```

## Avant de proposer une modification

- Lancez la suite de tests : `./run.sh test` (aucun test ne doit échouer).
- Respectez le style existant (Python 3.10+, `from __future__ import annotations`,
  pas de dépendance supplémentaire sans justification).
- Pour une nouvelle langue : ajoutez `locales/xx.py`, enregistrez-la dans
  `locales/__init__.py`, complétez `i18n.py` et `flags.py`, puis vérifiez que le
  test d'ordre de lecture passe.
- Décrivez clairement le changement dans la pull request.

## Signaler un problème

Indiquez la distribution, la session (Wayland/X11), la version de Python et la
sortie de `./run.sh test` si possible.
