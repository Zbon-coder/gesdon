# GesDon - Gestion de Dons

Une application web moderne et élégante pour la gestion des dons destinés aux associations caritatives.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2019+-red.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0-38bdf8.svg)

## Table des matières

- [À propos](#à-propos)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Base de données](#base-de-données)
- [Captures d'écran](#captures-décran)
- [Contribuer](#contribuer)
- [Licence](#licence)

## À propos

**GesDon** est une application web complète de gestion de dons développée avec Flask et SQL Server. Elle permet aux organisations de suivre efficacement les dons reçus, de gérer les donateurs, les associations bénéficiaires et de générer des statistiques détaillées.

Le projet a été conçu avec une interface utilisateur moderne utilisant Tailwind CSS, offrant une expérience utilisateur fluide et responsive.

## Fonctionnalités

### Gestion des utilisateurs

- Authentification sécurisée (inscription/connexion)
- Hachage des mots de passe avec Werkzeug
- Gestion de profil utilisateur
- Système de sessions Flask

### Gestion des donateurs

- Ajouter, modifier et supprimer des donateurs
- Informations complètes (nom, téléphone, email, BP, ville)
- Liste avec recherche et filtrage
- Interface moderne avec avatars et badges

### Gestion des dons

- Enregistrement détaillé des dons
- Liaison avec les donateurs et associations
- Description et libellé personnalisables
- Horodatage automatique
- Visualisation en tableau responsive

### Gestion des associations

- Gestion des organisations bénéficiaires
- Informations complètes (nom, sigle, adresse, contact)
- Liaison avec les dons reçus

### Tableau de bord

- Vue d'ensemble des statistiques
- Graphiques interactifs (Chart.js)
- Statistiques sur 7 jours
- Cartes récapitulatives des dons récents

### Historique et statistiques

- Timeline des dons avec filtrage
- Statistiques mensuelles
- Analyse par association
- Top donateurs
- Graphiques d'évolution

## Technologies utilisées

### Backend

- **Flask 3.1.2** - Framework web Python
- **Python 3.8+** - Langage de programmation
- **SQL Server** - Base de données relationnelle
- **pyodbc 5.3.0** - Connecteur Python pour SQL Server
- **Werkzeug 3.1.4** - Utilitaires WSGI (hachage de mots de passe)
- **Flask-Login 0.6.3** - Gestion des sessions utilisateur

### Frontend

- **Tailwind CSS 3.0** - Framework CSS utility-first
- **Bootstrap Icons** - Bibliothèque d'icônes
- **Chart.js 4.4.0** - Graphiques interactifs
- **Jinja2 3.1.6** - Moteur de templates

### Outils de développement

- **Flask-WTF 1.2.2** - Intégration WTForms
- **WTForms 3.2.1** - Validation de formulaires

## Prérequis

Avant de commencer, assurez-vous d'avoir installé:

- Python 3.8 ou supérieur
- SQL Server 2019 ou supérieur
- ODBC Driver 17 for SQL Server
- pip (gestionnaire de paquets Python)
- Git (optionnel)

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/gesdon.git
cd gesdon
```

### 2. Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données

#### Créer la base de données

Exécutez les scripts SQL suivants dans SQL Server Management Studio (SSMS):

```sql
CREATE DATABASE Gestion_Don;
GO

USE Gestion_Don;
GO

-- Table Utilisateurs
CREATE TABLE Utilisateur (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom_utilisateur NVARCHAR(100) NOT NULL,
    email NVARCHAR(150) UNIQUE NOT NULL,
    mot_de_passe NVARCHAR(255) NOT NULL,
    date_creation DATETIME DEFAULT GETDATE()
);

-- Table Donateurs
CREATE TABLE Donateur (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom NVARCHAR(150) NOT NULL,
    tel NVARCHAR(20),
    mail NVARCHAR(150),
    BP NVARCHAR(50),
    ville NVARCHAR(100)
);

-- Table Associations
CREATE TABLE Association (
    IdA INT PRIMARY KEY IDENTITY(1,1),
    NomA NVARCHAR(200) NOT NULL,
    sigle NVARCHAR(50),
    ville NVARCHAR(100),
    BP NVARCHAR(50),
    tel NVARCHAR(20),
    email NVARCHAR(150)
);

-- Table Dons
CREATE TABLE Don (
    IdD INT PRIMARY KEY IDENTITY(1,1),
    libelle NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    IdA INT NOT NULL,
    id INT NOT NULL,
    date_don DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (IdA) REFERENCES Association(IdA),
    FOREIGN KEY (id) REFERENCES Donateur(id)
);
```

## Configuration

### 1. Configuration de la base de données

Modifiez le fichier [config.py](config.py) selon votre configuration SQL Server:

```python
import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"  # Modifiez si nécessaire
        "DATABASE=Gestion_Don;"
        "Trusted_Connection=yes;"  # Ou utilisez UID et PWD
    )
    return conn
```

### 2. Clé secrète Flask

Dans [app.py](app.py), modifiez la clé secrète pour la production:

```python
app.secret_key = 'votre_cle_secrete_tres_securisee_ici_2024'
```

## Utilisation

### Démarrer l'application

```bash
python app.py
```

L'application sera accessible à l'adresse: `http://127.0.0.1:5000`

### Premier démarrage

1. Accédez à `/register` pour créer un compte
2. Connectez-vous avec vos identifiants
3. Commencez par ajouter des associations
4. Ajoutez des donateurs
5. Enregistrez vos premiers dons

### Navigation

- **Accueil** (`/dashboard`) - Tableau de bord avec statistiques
- **Associations** (`/associations`) - Gestion des organisations
- **Donateurs** (`/donateurs`) - Gestion des donateurs
- **Dons** (`/dons`) - Gestion des dons
- **Historique** (`/historique`) - Timeline des dons
- **Statistiques** (`/statistiques`) - Analyses et graphiques
- **Profil** (`/profil`) - Gestion du compte utilisateur

## Structure du projet

```text
gesdon/
│
├── app.py                  # Application Flask principale
├── config.py               # Configuration de la base de données
├── models.py               # Modèles et fonctions de base de données
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
│
├── static/                # Fichiers statiques
│   └── style.css          # Styles CSS personnalisés
│
└── templates/             # Templates Jinja2
    ├── base.html          # Template de base
    ├── login.html         # Page de connexion
    ├── register.html      # Page d'inscription
    ├── dashboard.html     # Tableau de bord
    ├── profil.html        # Profil utilisateur
    │
    ├── associations.html           # Liste des associations
    ├── form_association.html       # Formulaire association
    │
    ├── donateurs.html              # Liste des donateurs
    ├── form_donateur.html          # Formulaire donateur
    │
    ├── dons.html                   # Liste des dons
    ├── form_don.html               # Formulaire don
    │
    ├── historique.html             # Timeline des dons
    └── statistiques.html           # Statistiques et graphiques
```

## Base de données

### Schéma relationnel

```text
┌─────────────────┐
│   Utilisateur   │
├─────────────────┤
│ id (PK)         │
│ nom_utilisateur │
│ email           │
│ mot_de_passe    │
│ date_creation   │
└─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    Donateur     │       │       Don       │       │   Association   │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────│ IdD (PK)        │──────►│ IdA (PK)        │
│ nom             │       │ libelle         │       │ NomA            │
│ tel             │       │ description     │       │ sigle           │
│ mail            │       │ IdA (FK)        │       │ ville           │
│ BP              │       │ id (FK)         │       │ BP              │
│ ville           │       │ date_don        │       │ tel             │
└─────────────────┘       └─────────────────┘       │ email           │
                                                     └─────────────────┘
```

### Relations entre les tables

- Un **Don** est lié à un **Donateur** (relation N:1)
- Un **Don** est lié à une **Association** (relation N:1)
- Un **Donateur** peut faire plusieurs dons (relation 1:N)
- Une **Association** peut recevoir plusieurs dons (relation 1:N)

## Captures d'écran

### Vue du tableau de bord

Interface moderne avec statistiques en temps réel et graphiques interactifs.

### Vue de la liste des donateurs

Tableau responsive avec avatars, badges et actions rapides (modifier/supprimer).

### Vue du formulaire de don

Interface intuitive avec sélection d'association et donateur, validation en temps réel.

### Vue des statistiques

Graphiques détaillés par mois, par association, et évolution hebdomadaire.

## Fonctionnalités de sécurité

- Hachage des mots de passe avec Werkzeug
- Protection CSRF avec Flask-WTF
- Sessions sécurisées
- Décorateur `@login_required` pour les routes protégées
- Validation des données côté serveur
- Échappement automatique des données avec Jinja2

## Design et UX

### Palette de couleurs

- **Violet** (`#667eea` → `#764ba2`) - Identité principale
- **Vert** (`#50c878`) - Actions positives (dons)
- **Rouge** (`#e74c3c`) - Actions de suppression
- **Ambre** (`#f59e0b`) - Modifications

### Animations

- Transitions fluides (0.2-0.3s)
- Effets hover avec scale et shadow
- États focus avec rings colorés
- Glassmorphism sur la navigation

### Responsive Design

- Mobile-first approach
- Breakpoints Tailwind (sm, md, lg, xl)
- Tables scrollables sur mobile
- Navigation adaptative

## Contribuer

Les contributions sont les bienvenues! Pour contribuer:

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Auteurs

- **Votre Nom** - Développement initial

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## Support

Pour toute question ou problème:

- Ouvrez une issue sur GitHub
- Contactez-nous à: [bonz@gmail.com](mailto:support@gesdon.com)

---

© 2026 GesDon - Gestion de Dons | Tous droits réservés
