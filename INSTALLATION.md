# Application de Gestion de Dons

Application Flask complète pour gérer les dons, les donateurs et les associations avec SQL Server.

## Structure de la Base de Données

L'application utilise 4 tables principales :

1. **Utilisateurs** : Gestion des comptes (connexion/inscription)
2. **Association** : Organisations bénéficiaires des dons
3. **Donateur** : Personnes effectuant les dons
4. **Don** : Enregistrement des dons avec référence à l'association et au donateur

## Fonctionnalités

- Authentification (Connexion/Inscription)
- Tableau de bord avec statistiques
- CRUD complet pour les associations
- CRUD complet pour les donateurs
- CRUD complet pour les dons
- Interface moderne avec Bootstrap 5

## Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Créer la base de données

```sql
CREATE DATABASE Gestion_Don;
```

### 3. Exécuter le script SQL

```bash
sqlcmd -S localhost -d Gestion_Don -i database.sql
```

### 4. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur `http://127.0.0.1:5000`

## Connexion par défaut

- Email : `admin@gesdon.com`
- Mot de passe : `admin123`

## Structure

- **Association** : IdA, NomA, CompteBANK, tel, ville, pays
- **Donateur** : id, nom, tel, mail, BP, ville
- **Don** : IdD, libelle, description, IdA, id, date_don
