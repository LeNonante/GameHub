# GameHub 🎲

GameHub est une plateforme web collaborative permettant de jouer à des jeux de société modernes en ligne. Développée en Python avec Flask, elle offre une expérience de jeu fluide et moderne pour des jeux comme Agent Trouble, Insider, et bien d'autres à venir.

## 🎮 Jeux disponibles

- **Agent Trouble** : Jeu de rôle et de déduction où les joueurs incarnent différents personnages dans une intrigue captivante
- **Insider** : Jeu de communication et de bluff (en développement)
- D'autres jeux à venir...

## ✨ Fonctionnalités principales

- 🎯 **Création et gestion de parties multijoueurs** : Créez ou rejoignez des parties avec un code unique
- 🏠 **Système de lobby interactif** : Interface conviviale pour gérer les joueurs et lancer les parties
- 🃏 **Attribution automatique des rôles** : Chaque joueur reçoit ses cartes et son rôle de manière sécurisée
- 🖼️ **Affichage dynamique** : Plateau et cartes affichés en temps réel avec images haute qualité
- 📱 **Interface responsive** : Compatible desktop, tablette et mobile
- 🔧 **Architecture modulaire** : Ajout facile de nouveaux jeux

## 🏗️ Architecture technique

### Stack technologique
- **Backend** : Python 3.12 + Flask
- **Base de données** : SQLite avec schéma relationnel
- **Frontend** : HTML5 + CSS3 + JavaScript vanilla
- **Templating** : Jinja2
- **Images** : Stockage base64 pour les plateaux et stockage "brut" pour les cartes

### Structure du projet
```
GameHub/
├── app.py                      # 🚀 Application Flask principale
├── requirements.txt            # 📦 Dépendances Python
│
├── static/                     # 📁 Ressources statiques
│   ├── css/
│   │   ├── style.css          # 🎨 Styles généraux
│   │   ├── game_detail.css    # 🎨 Styles pages jeux
│   │   └── agent_trouble_game.css # 🎨 Styles Agent Trouble
│   ├── data/
│   │   ├── games_infos.json   # 🎮 Configuration des jeux
│   │   ├── schemas.drawio     # 📊 Schéma base de données
│   │   ├── database.db        # 🗄️ Base de données SQLite
│   │   └── database.db.sql    # 📋 Schéma de la base
│   │
│   ├── gestionDB.py           # 🗄️ Fonctions base de données
│   └── ressourcesJeux/        # 🖼️ Assets des jeux
│       ├── AgentTrouble/
│       │   ├── assets/        # Images plateau et cartes
│       │   ├── rules.md       # 📖 Règles du jeu
│       │   └── AgentTroubleFunctions.py # 🔧 Logique métier
│       └── Insider/
│
├── templates/                  # 🖥️ Templates HTML
│   ├── index.html             # 🏠 Page d'accueil
│   ├── game_detail.html       # 📖 Détails et règles des jeux
│   ├── game_lobby.html        # 🏠 Lobby des parties
│   └── agent_trouble_game.html # 🎮 Interface de jeu Agent Trouble
│
└── assets/                     # 📁 Ressources développement
    └── gestionSession.py       # 🔐 Gestion sessions utilisateurs
```

## 🗄️ Base de données

Le projet utilise un schéma SQLite relationnel avec les tables principales :

- **Jeux** : Configuration des jeux disponibles
- **Parties** : Sessions de jeu actives
- **PartiesAgentTrouble** : Données spécifiques Agent Trouble
- **Joueurs** : Informations des participants
- **JoueursAgentTrouble** : Rôles et cartes spécifiques

## 🌐 Jouer en ligne

**🎮 [Accéder à GameHub](LIEN)**

La plateforme est accessible directement depuis votre navigateur, aucune installation requise !

## 🚀 Installation et lancement en local

### Prérequis
- Python 3.8+
- Git

### Installation
1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/LeNonante/GameHub.git
   cd GameHub
   ```

2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancez l'application** :
   ```bash
   python app.py
   ```

5. **Accédez à l'interface** : [http://localhost:5000](http://localhost:5000)

## 🛠️ Technologies utilisées

- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.12**
- ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) **Flask 3.x**
- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite 3**
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) **HTML5**
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) **CSS3**
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript**

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**LeNonante** - [GitHub](https://github.com/LeNonante)


