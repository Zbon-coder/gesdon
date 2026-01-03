-- Script de création de la base de données pour l'application de gestion de dons
-- Basé sur le schéma fourni : Association, Donateur, Don

USE Gestion_Don;
GO

-- Suppression des tables dans l'ordre inverse des dépendances
IF OBJECT_ID('Don', 'U') IS NOT NULL
    DROP TABLE Don;
GO

IF OBJECT_ID('Donateur', 'U') IS NOT NULL
    DROP TABLE Donateur;
GO

IF OBJECT_ID('Association', 'U') IS NOT NULL
    DROP TABLE Association;
GO

IF OBJECT_ID('Utilisateurs', 'U') IS NOT NULL
    DROP TABLE Utilisateurs;
GO

-- Table des utilisateurs (pour la connexion)
CREATE TABLE Utilisateurs (
    id_utilisateur INT IDENTITY(1,1) PRIMARY KEY,
    nom_utilisateur NVARCHAR(100) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe NVARCHAR(255) NOT NULL,
    date_creation DATETIME DEFAULT GETDATE()
);
GO

-- Table Association
CREATE TABLE Association (
    IdA INT IDENTITY(1,1) PRIMARY KEY,
    NomA NVARCHAR(100) NOT NULL,
    CompteBANK NVARCHAR(50),
    tel NVARCHAR(20),
    ville NVARCHAR(100),
    pays NVARCHAR(100)
);
GO

-- Table Donateur
CREATE TABLE Donateur (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nom NVARCHAR(100) NOT NULL,
    tel NVARCHAR(20),
    mail NVARCHAR(100),
    BP NVARCHAR(50),
    ville NVARCHAR(100)
);
GO

-- Table Don
CREATE TABLE Don (
    IdD INT IDENTITY(1,1) PRIMARY KEY,
    libelle NVARCHAR(100) NOT NULL,
    description NVARCHAR(500),
    IdA INT NOT NULL,
    id INT NOT NULL,
    date_don DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdA) REFERENCES Association(IdA) ON DELETE CASCADE,
    FOREIGN KEY (id) REFERENCES Donateur(id) ON DELETE CASCADE
);
GO

-- Index pour améliorer les performances
CREATE INDEX idx_donateur_nom ON Donateur(nom);
CREATE INDEX idx_don_association ON Don(IdA);
CREATE INDEX idx_don_donateur ON Don(id);
CREATE INDEX idx_don_date ON Don(date_don);
GO

-- Insertion de données de test
INSERT INTO Utilisateurs (nom_utilisateur, email, mot_de_passe)
VALUES ('admin', 'admin@gesdon.com', 'pbkdf2:sha256:600000$test$hash'); -- Mot de passe: admin123

INSERT INTO Association (NomA, CompteBANK, tel, ville, pays)
VALUES
    ('Association Caritative Benin', 'BJ12345678901234567890', '+229 12 34 56 78', 'Cotonou', 'Benin'),
    ('Aide Humanitaire Plus', 'BJ98765432109876543210', '+229 98 76 54 32', 'Porto-Novo', 'Benin');
GO

INSERT INTO Donateur (nom, tel, mail, BP, ville)
VALUES
    ('Dupont Jean', '+229 61 23 45 67', 'jean.dupont@email.com', 'BP 123', 'Cotonou'),
    ('Martin Marie', '+229 69 87 65 43', 'marie.martin@email.com', 'BP 456', 'Abomey-Calavi'),
    ('Kouassi Pierre', '+229 67 11 22 33', 'pierre.kouassi@email.com', 'BP 789', 'Parakou');
GO

INSERT INTO Don (libelle, description, IdA, id)
VALUES
    ('Don mensuel', 'Don régulier pour soutenir les activités', 1, 1),
    ('Don ponctuel', 'Contribution pour projet éducatif', 1, 2),
    ('Don matériel', 'Fournitures scolaires et vêtements', 2, 1),
    ('Don alimentaire', 'Denrées alimentaires pour les nécessiteux', 2, 3);
GO
