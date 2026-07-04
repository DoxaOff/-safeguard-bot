# Où mettre ces fichiers

```
C:\Users\Donip\Documents\GuardBot\
├── bot.py
├── .env
├── config.json          ← généré automatiquement au premier lancement
├── cogs\
│   ├── __init__.py
│   ├── Guardadmin.py     (inchangé, toujours vide)
│   ├── Guardbasic.py     ← REMPLACE ton fichier vide
│   ├── Guardconfig.py    ← REMPLACE ton fichier vide
│   └── Guardtest.py      (inchangé)
└── utils\                ← NOUVEAU dossier
    ├── __init__.py
    ├── data.py
    └── triggers.py
```

## À installer

```
py -3.12 -m pip install nextcord
```
(tu l'as sûrement déjà si `/ping` fonctionne)

## Rôles utilisés

- **Modérateur/trice** : gère les mots, catégories, salons exclus, salons de
  confession, de suggestion et à fil automatique.
- **Fondateur** : seul rôle autorisé à utiliser `/définirlogs`.

Si ces noms de rôle ne sont pas exacts sur ton serveur, corrige les
constantes `ROLE_MODERATION` et `ROLE_LOGS` en haut de `cogs/Guardconfig.py`.

## Commandes disponibles

| Commande | Rôle requis | Effet |
|---|---|---|
| `/ajoutercategories` | Modérateur/trice | Surveille une catégorie entière |
| `/retirercategorie` | Modérateur/trice | Arrête de surveiller une catégorie |
| `/retirerunsalon` | Modérateur/trice | Exclut un salon précis (ex: triggerWarning) |
| `/ajouterunsalon` | Modérateur/trice | Réintègre un salon précédemment exclu |
| `/ajoutermot` | Modérateur/trice | Ajoute un mot sensible |
| `/retirermot` | Modérateur/trice | Retire un mot sensible |
| `/liste` | tout le monde | Affiche la liste des mots sensibles |
| `/définirlogs` | Fondateur | Définit le salon de logs |
| `/ajoutersalonconfession` | Modérateur/trice | Surveille un salon de confession (Anonymous RP) |
| `/retirersalonconfession` | Modérateur/trice | Arrête de surveiller un salon de confession |
| `/ajoutersalonsuggestion` | Modérateur/trice | Active réactions ✅❌ + fil auto sur un salon |
| `/retirersalonsuggestion` | Modérateur/trice | Désactive ce comportement |
| `/ajoutersalonfil` | Modérateur/trice | Crée un fil automatiquement à chaque message |
| `/retirersalonfil` | Modérateur/trice | Désactive la création automatique de fil |

## Points à vérifier / adapter toi-même

1. **`NOMS_SALONS_DEFOULOIR`** dans `Guardbasic.py` : j'ai mis `["défouloir"]`
   à titre d'exemple — remplace par le(s) vrai(s) nom(s) de salon(s) chez toi
   (ex : `["défouloir", "défouloir-nsfw"]`).
2. **Salon exclu "triggerWarning"** : une fois les cogs en place, utilise
   `/retirerunsalon` dessus pour qu'il soit ignoré par la détection.
3. **Synchronisation des commandes** : selon comment `bot.py` appelle
   `bot.sync_application_commands()`, les nouvelles commandes peuvent mettre
   jusqu'à 1h à apparaître globalement — pense à synchroniser sur ton serveur
   de test (`guild_ids`) si tu veux les voir tout de suite.
4. J'ai ajouté quelques commandes "miroir" qui n'étaient pas explicitement
   demandées (`/retirercategorie`, `/ajouterunsalon`,
   `/retirersalonconfession`, `/ajoutersalonsuggestion`,
   `/retirersalonsuggestion`, `/ajoutersalonfil`, `/retirersalonfil`) pour que
   toute la config soit pilotable sans toucher au fichier JSON à la main.
   Dis-moi si tu préfères que je les retire.

## Ce que j'ai gardé de ton ancien code

- La logique exacte de détection (`find_trigger_word`, `contains_spoiler`) —
  maintenant dans `utils/triggers.py` pour être partagée entre les deux cogs.
- Le comportement des confessions Anonymous RP, du Défouloir, des salons de
  suggestion et à fil automatique — repris tel quel dans `Guardbasic.py`.
- Le format exact du DM de notification et de l'embed de logs.

Tout est stocké dans `config.json` (créé automatiquement au premier lancement
si absent), donc plus besoin de toucher au code pour changer la config.
