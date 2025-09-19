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
│   │   ├── database.db                 # 🗄️ Base de données SQLite
│   │   └── database.db.sql            # 📋 Schéma de la base
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

## 🚀 Installation et lancement

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

3. **Initialisez la base de données** (si nécessaire) :
   ```bash
   sqlite3 database.db < database.db.sql
   ```

4. **Lancez l'application** :
   ```bash
   python app.py
   ```

5. **Accédez à l'interface** : [http://localhost:5000](http://localhost:5000)

## 🎯 Utilisation

1. **Accueil** : Sélectionnez un jeu dans la liste
2. **Création de partie** : Entrez votre pseudo et créez une nouvelle partie
3. **Rejoindre une partie** : Utilisez le code de partie fourni par l'hôte
4. **Lobby** : Attendez les autres joueurs et lancez la partie
5. **Jeu** : Profitez de l'expérience de jeu interactive !

## 🔧 Ajouter un nouveau jeu

### 1. Configuration
Ajoutez les informations dans `static/data/games_infos.json` :
```json
{
  "id": 3,
  "title": "Nouveau Jeu",
  "description": "Description du jeu...",
  "min_players": 3,
  "max_players": 8,
  "duration": "30-45 min",
  "image": "static/ressourcesJeux/NouveauJeu/NouveauJeu.png",
  "rules": "static/ressourcesJeux/NouveauJeu/rules.md"
}
```

### 2. Ressources
Créez le dossier `static/ressourcesJeux/NouveauJeu/` avec :
- `NouveauJeu.png` : Image de couverture
- `rules.md` : Règles en Markdown
- `assets/` : Images du plateau et cartes
- `NouveauJeuFunctions.py` : Logique du jeu

### 3. Templates
Créez le template de jeu dans `templates/nouveau_jeu_game.html`

### 4. Routes
Ajoutez les routes nécessaires dans `app.py`

## 🛠️ Technologies utilisées

- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.12**
- ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) **Flask 3.x**
- ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white) **SQLite 3**
- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) **HTML5**
- ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white) **CSS3**
- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) **JavaScript**

## 📋 À faire

- [ ] Finaliser les règles Insider
- [ ] Ajouter segment paramètres jeux sur lobby
- [ ] Tester création partie Agent Trouble multi-joueurs
- [ ] Modifier état partie dans BDD
- [ ] Optimiser le template Agent Trouble
- [ ] Créer images cartes personnages restantes
- [ ] Implémenter système de logs de partie

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment procéder :

1. **Fork** le projet
2. **Créez** une branche pour votre fonctionnalité (`git checkout -b feature/NouvelleFonctionnalite`)
3. **Committez** vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/NouvelleFonctionnalite`)
5. **Ouvrez** une Pull Request

### Types de contributions recherchées
- 🎮 Nouveaux jeux
- 🐛 Corrections de bugs
- ✨ Améliorations UX/UI
- 📖 Documentation
- 🧪 Tests unitaires

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier `LICENSE` pour plus de détails.

## 👤 Auteur

**LeNonante** - [GitHub](https://github.com/LeNonante)

---

*Développé avec ❤️ pour les passionnés de jeux de société*

