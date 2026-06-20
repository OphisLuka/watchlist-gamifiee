# 🎬 Watchlist gamifiée — Films, Séries, Mangas, Animés

Application web (Streamlit) pour organiser tout ce qu'on veut regarder — films, séries, mangas, animés — avec un système de progression inspiré des jeux vidéo : gagne de l'XP en terminant des œuvres et fais monter ton rang de cinéphile.

## Pourquoi ce projet ?

Entre les recommandations d'amis, les bandes-annonces vues en passant et les scrolls infinis sur les plateformes de streaming, la liste de "choses à regarder un jour" devient vite ingérable. Ce projet structure cette liste en un vrai petit workflow, et ajoute une couche de gamification pour transformer le visionnage en progression plutôt qu'en simple consommation passive.

## Fonctionnalités

- **Workflow en 4 statuts** :
  - 🔎 **À vérifier** — une idée notée, pas encore confirmée
  - 📺 **À regarder** — confirmée intéressante, en attente
  - 🏁 **Terminé** — regardée en entier, notée, peut devenir favorite
  - 🗑️ **Écarté** — vérifiée puis jugée pas intéressante
- **Système XP et rangs** : chaque œuvre terminée rapporte de l'XP selon son type (Film, Série, Manga, Anime), avec 7 paliers de rang à débloquer, du *Spectateur occasionnel* à la *Légende du visionnage*
- **Notation par étoiles** des œuvres terminées
- **Favoris** pour mettre en avant ses œuvres préférées
- **Filtres et tri** : par type, genre, favoris, date d'ajout, note
- **Statistiques visuelles** : répartition de ce qui a été terminé par type et par genre
- Toutes les données restent **locales** (fichier CSV sur ta machine)

## Aperçu

*(à ajouter : captures d'écran de l'application)*

## Installation

```bash
git clone https://github.com/OphisLuka/watchlist-gamifiee.git
cd watchlist-gamifiee
pip install -r requirements.txt
```

## Utilisation

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement dans le navigateur à l'adresse `http://localhost:8501`.

Cette application étant une app web, elle est aussi accessible depuis le navigateur d'un smartphone sur le même réseau (voir l'adresse "Network URL" affichée au lancement), sans rien installer de plus.

## Système XP

| Type d'œuvre | XP gagné |
|---|---|
| Film | 10 |
| Manga | 20 |
| Anime | 25 |
| Série | 30 |

| XP requis | Rang |
|---|---|
| 0 | 🍿 Spectateur occasionnel |
| 50 | 🎬 Curieux culturel |
| 150 | 🎞️ Cinéphile en herbe |
| 300 | 🏆 Cinéphile confirmé |
| 600 | 🌟 Critique averti |
| 1000 | 👑 Encyclopédie vivante |
| 1800 | 💎 Légende du visionnage |

## Stack technique

- Python
- [Streamlit](https://streamlit.io/) — interface web interactive
- [pandas](https://pandas.pydata.org/) — manipulation des données

## Limites et pistes d'amélioration

- Pas de récupération automatique d'infos (affiche, synopsis) depuis une API externe type TMDB — tout est saisi manuellement pour l'instant
- Pas de système multi-utilisateurs : une seule watchlist locale par installation
- Pistes futures : intégration d'une API de films/séries pour auto-compléter les fiches, export PDF/partage de classement, déploiement en ligne (Streamlit Community Cloud) pour un accès multi-appareils sans dépendre du même réseau local

## Auteur

[OphisLuka](https://github.com/OphisLuka) — en alternance Ingénieur IA (OpenClassrooms).
