-- Pour creer cette base, supprimer celle qui existe et lancer la commande : 
--     sqlite3 static/data/gamehub.db < static/data/gamehub.db.sql : Windows dans invite de commande (pas powershell)
--     sqlite3 /workspaces/GameHub/static/data/gamehub.db < /workspaces/GameHub/static/data/gamehub.db.sql : Linux dans terminal

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
    session TEXT,
    Pseudo TEXT,
    GameCode TEXT,
    PRIMARY KEY(session, GameCode),
    FOREIGN KEY(GameCode) REFERENCES Parties(GameCode)
);

-- Table JoueursAgentTrouble
CREATE TABLE IF NOT EXISTS JoueursAgentTrouble (
    session TEXT,
    lieu TEXT,
    role TEXT,
    carte TEXT,
    GameCode TEXT,
    PRIMARY KEY(session, GameCode)
);

-- Insertion des jeux
INSERT INTO Jeux (GameType, GameName) VALUES (1, 'AgentTrouble');
INSERT INTO Jeux (GameType, GameName) VALUES (2, 'Insider');