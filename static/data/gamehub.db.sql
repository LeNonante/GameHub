-- Pour creer cette base, supprimer celle qui existe et lancer la commande : sqlite3 /workspaces/GameHub/static/data/gamehub.db < /workspaces/GameHub/static/data/gamehub.db.sql
-- Création de la base de données GameHub

-- Table Jeux

PRAGMA foreign_keys = ON;
-- Table Jeux
CREATE TABLE IF NOT EXISTS Jeux (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    GameType INTEGER,
    GameName TEXT
);

-- Table Parties
CREATE TABLE IF NOT EXISTS Parties (
    GameCode TEXT PRIMARY KEY,
    JeuId INTEGER,
    EtatLancement INTEGER DEFAULT 0,
    sessionHote TEXT,
    Timestamp INTEGER,
    FOREIGN KEY(JeuId) REFERENCES Jeux(Id),
    FOREIGN KEY(sessionHote) REFERENCES Joueurs(session)
);

-- Table PartiesAgentTrouble
CREATE TABLE IF NOT EXISTS PartiesAgentTrouble (
    GameCode TEXT PRIMARY KEY,
    Etat INTEGER DEFAULT 0,
    Plateau TEXT,
    FOREIGN KEY(GameCode) REFERENCES Parties(GameCode)
);

-- Table Joueurs
CREATE TABLE IF NOT EXISTS Joueurs (
    session TEXT PRIMARY KEY,
    Pseudo TEXT,
    GameCode TEXT,
    FOREIGN KEY(GameCode) REFERENCES Parties(GameCode)
);

-- Table JoueursAgentTrouble
CREATE TABLE IF NOT EXISTS JoueursAgentTrouble (
    session TEXT PRIMARY KEY,
    lieu TEXT,
    role TEXT,
    carte TEXT,
    FOREIGN KEY(session) REFERENCES Joueurs(session)
);

-- Insertion des jeux
INSERT INTO Jeux (GameType, GameName) VALUES (1, 'AgentTrouble');
INSERT INTO Jeux (GameType, GameName) VALUES (2, 'Insider');