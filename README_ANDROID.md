# 📱 Watchlist — Version Android (APK)

Version mobile simplifiée de la Watchlist, construite avec [Kivy](https://kivy.org/) et compilée automatiquement en APK grâce à GitHub Actions.

## Pourquoi une version séparée ?

Streamlit (utilisé pour la version bureau/web) ne permet pas de générer une application Android installable. Cette version utilise donc un framework différent, pensé pour le mobile : Kivy, toujours en Python.

C'est une **version simplifiée** par rapport à l'app Streamlit complète : pour l'instant, elle permet seulement d'ajouter une œuvre (titre + type), de la voir dans une liste, de la marquer comme terminée, ou de la supprimer. Les fonctionnalités plus avancées (XP, rangs, filtres, notation) pourront être ajoutées dans une prochaine version une fois cette base validée.

## Comment récupérer l'APK

L'APK est compilé automatiquement par GitHub à chaque mise à jour du code (via GitHub Actions). Pour le récupérer :

1. Va dans l'onglet **Actions** de ce dépôt GitHub
2. Clique sur le dernier workflow **"Build APK Android"** marqué d'une coche verte ✅
3. Tout en bas de la page, dans la section **Artifacts**, télécharge **watchlist-apk** (un fichier `.zip` contenant l'APK)
4. Décompresse-le pour récupérer le fichier `.apk`

## Installer l'APK sur un téléphone Android

1. Transfère le fichier `.apk` sur ton téléphone (par mail, Google Drive, câble USB, etc.)
2. Ouvre le fichier depuis ton téléphone
3. Android va probablement bloquer l'installation par défaut ("Sources inconnues bloquées") — accepte d'autoriser l'installation pour cette source dans les paramètres proposés
4. L'application s'installe et une icône "Watchlist" apparaît sur l'écran d'accueil

**Note de sécurité** : ce blocage par défaut est une protection normale d'Android contre les applications qui ne viennent pas du Play Store. Comme ce code est open-source et visible sur ce dépôt, n'importe qui peut en vérifier le contenu avant de l'installer.

## Compiler soi-même (optionnel, avancé)

La compilation se fait via [Buildozer](https://buildozer.readthedocs.io/), qui ne fonctionne que sous Linux. Si tu veux compiler en local plutôt que via GitHub Actions, il te faut une machine Linux (ou une machine virtuelle Linux) avec Buildozer installé :

```bash
pip install buildozer cython
cd android
buildozer android debug
```

L'APK généré se trouve ensuite dans `android/bin/`.

## Structure du projet

```
android/
├── main.py            # Code de l'application Kivy
├── buildozer.spec      # Configuration de compilation Android
```

## Stack technique

- Python
- [Kivy](https://kivy.org/) — framework d'interface graphique multiplateforme
- [Buildozer](https://buildozer.readthedocs.io/) — outil de compilation Python → APK Android
- GitHub Actions — compilation automatique dans le cloud

## Limites de cette version

- Pas de système XP/rangs (présent dans la version Streamlit)
- Pas de filtres ni de tri
- Pas de notation par étoiles
- Interface volontairement minimale, à enrichir progressivement
