from config import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

# ========== GESTION DES UTILISATEURS ==========

def creer_utilisateur(nom_utilisateur, email, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        mot_de_passe_hash = generate_password_hash(mot_de_passe)
        cursor.execute(
            "INSERT INTO Utilisateurs (nom_utilisateur, email, mot_de_passe) VALUES (?, ?, ?)",
            (nom_utilisateur, email, mot_de_passe_hash)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la création de l'utilisateur: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def verifier_utilisateur(email, mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Utilisateurs WHERE email = ?", (email,))
        utilisateur = cursor.fetchone()
        if utilisateur and check_password_hash(utilisateur[3], mot_de_passe):
            return {
                'id': utilisateur[0],
                'nom_utilisateur': utilisateur[1],
                'email': utilisateur[2]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def get_utilisateur_by_id(id_utilisateur):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Utilisateurs WHERE id_utilisateur = ?", (id_utilisateur,))
        utilisateur = cursor.fetchone()
        if utilisateur:
            return {
                'id': utilisateur[0],
                'nom_utilisateur': utilisateur[1],
                'email': utilisateur[2],
                'date_creation': utilisateur[4] if len(utilisateur) > 4 else None
            }
        return None
    finally:
        cursor.close()
        conn.close()

# ========== GESTION DES ASSOCIATIONS (CRUD) ==========

def creer_association(NomA, CompteBANK, tel, ville, pays):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO Association (NomA, CompteBANK, tel, ville, pays)
               VALUES (?, ?, ?, ?, ?)""",
            (NomA, CompteBANK, tel, ville, pays)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la création de l'association: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_toutes_associations():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Association ORDER BY NomA")
        associations = cursor.fetchall()
        return [{
            'IdA': a[0],
            'NomA': a[1],
            'CompteBANK': a[2],
            'tel': a[3],
            'ville': a[4],
            'pays': a[5]
        } for a in associations]
    finally:
        cursor.close()
        conn.close()

def get_association_by_id(IdA):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Association WHERE IdA = ?", (IdA,))
        a = cursor.fetchone()
        if a:
            return {
                'IdA': a[0],
                'NomA': a[1],
                'CompteBANK': a[2],
                'tel': a[3],
                'ville': a[4],
                'pays': a[5]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def modifier_association(IdA, NomA, CompteBANK, tel, ville, pays):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Association
               SET NomA=?, CompteBANK=?, tel=?, ville=?, pays=?
               WHERE IdA=?""",
            (NomA, CompteBANK, tel, ville, pays, IdA)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la modification de l'association: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def supprimer_association(IdA):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Association WHERE IdA = ?", (IdA,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de l'association: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# ========== GESTION DES DONATEURS (CRUD) ==========

def creer_donateur(nom, tel, mail, BP, ville):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO Donateur (nom, tel, mail, BP, ville)
               VALUES (?, ?, ?, ?, ?)""",
            (nom, tel, mail, BP, ville)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la création du donateur: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_tous_donateurs():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Donateur ORDER BY nom")
        donateurs = cursor.fetchall()
        return [{
            'id': d[0],
            'nom': d[1],
            'tel': d[2],
            'mail': d[3],
            'BP': d[4],
            'ville': d[5]
        } for d in donateurs]
    finally:
        cursor.close()
        conn.close()

def get_donateur_by_id(id_donateur):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Donateur WHERE id = ?", (id_donateur,))
        d = cursor.fetchone()
        if d:
            return {
                'id': d[0],
                'nom': d[1],
                'tel': d[2],
                'mail': d[3],
                'BP': d[4],
                'ville': d[5]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def modifier_donateur(id_donateur, nom, tel, mail, BP, ville):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Donateur
               SET nom=?, tel=?, mail=?, BP=?, ville=?
               WHERE id=?""",
            (nom, tel, mail, BP, ville, id_donateur)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la modification du donateur: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def supprimer_donateur(id_donateur):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Donateur WHERE id = ?", (id_donateur,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du donateur: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# ========== GESTION DES DONS (CRUD) ==========

def creer_don(libelle, description, IdA, id_donateur):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO Don (libelle, description, IdA, id)
               VALUES (?, ?, ?, ?)""",
            (libelle, description, IdA, id_donateur)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la création du don: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_tous_dons():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT d.IdD, d.libelle, d.description, d.date_don,
                      a.NomA, a.IdA,
                      don.nom, don.id
               FROM Don d
               INNER JOIN Association a ON d.IdA = a.IdA
               INNER JOIN Donateur don ON d.id = don.id
               ORDER BY d.date_don DESC"""
        )
        dons = cursor.fetchall()
        return [{
            'IdD': don[0],
            'libelle': don[1],
            'description': don[2],
            'date_don': don[3],
            'association_nom': don[4],
            'IdA': don[5],
            'donateur_nom': don[6],
            'id_donateur': don[7]
        } for don in dons]
    finally:
        cursor.close()
        conn.close()

def get_don_by_id(IdD):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT d.IdD, d.libelle, d.description, d.date_don,
                      a.NomA, d.IdA,
                      don.nom, d.id
               FROM Don d
               INNER JOIN Association a ON d.IdA = a.IdA
               INNER JOIN Donateur don ON d.id = don.id
               WHERE d.IdD = ?""",
            (IdD,)
        )
        don = cursor.fetchone()
        if don:
            return {
                'IdD': don[0],
                'libelle': don[1],
                'description': don[2],
                'date_don': don[3],
                'association_nom': don[4],
                'IdA': don[5],
                'donateur_nom': don[6],
                'id_donateur': don[7]
            }
        return None
    finally:
        cursor.close()
        conn.close()

def modifier_don(IdD, libelle, description, IdA, id_donateur):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Don
               SET libelle=?, description=?, IdA=?, id=?
               WHERE IdD=?""",
            (libelle, description, IdA, id_donateur, IdD)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la modification du don: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def supprimer_don(IdD):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Don WHERE IdD = ?", (IdD,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du don: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_dons_par_donateur(id_donateur):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT IdD, libelle, description, date_don
               FROM Don
               WHERE id = ?
               ORDER BY date_don DESC""",
            (id_donateur,)
        )
        dons = cursor.fetchall()
        return [{
            'IdD': don[0],
            'libelle': don[1],
            'description': don[2],
            'date_don': don[3]
        } for don in dons]
    finally:
        cursor.close()
        conn.close()

# ========== FONCTIONS POUR PROFIL & HISTORIQUE ==========

def modifier_utilisateur(id_utilisateur, nom_utilisateur, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE Utilisateurs
               SET nom_utilisateur=?, email=?
               WHERE id_utilisateur=?""",
            (nom_utilisateur, email, id_utilisateur)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la modification de l'utilisateur: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def changer_mot_de_passe(id_utilisateur, nouveau_mot_de_passe):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        mot_de_passe_hash = generate_password_hash(nouveau_mot_de_passe)
        cursor.execute(
            """UPDATE Utilisateurs
               SET mot_de_passe=?
               WHERE id_utilisateur=?""",
            (mot_de_passe_hash, id_utilisateur)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors du changement de mot de passe: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_dons_filtres(periode=None, association_id=None, donateur_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """SELECT d.IdD, d.libelle, d.description, d.date_don,
                          a.NomA, a.IdA,
                          don.nom, don.id
                   FROM Don d
                   INNER JOIN Association a ON d.IdA = a.IdA
                   INNER JOIN Donateur don ON d.id = don.id
                   WHERE 1=1"""
        params = []

        # Filtrage par période
        if periode == 'aujourdhui':
            query += " AND CAST(d.date_don AS DATE) = CAST(GETDATE() AS DATE)"
        elif periode == 'semaine':
            query += " AND d.date_don >= DATEADD(day, -7, GETDATE())"
        elif periode == 'mois':
            query += " AND d.date_don >= DATEADD(month, -1, GETDATE())"
        elif periode == 'annee':
            query += " AND d.date_don >= DATEADD(year, -1, GETDATE())"

        # Filtrage par association
        if association_id:
            query += " AND d.IdA = ?"
            params.append(association_id)

        # Filtrage par donateur
        if donateur_id:
            query += " AND d.id = ?"
            params.append(donateur_id)

        query += " ORDER BY d.date_don DESC"

        cursor.execute(query, params)
        dons = cursor.fetchall()
        return [{
            'IdD': don[0],
            'libelle': don[1],
            'description': don[2],
            'date_don': don[3],
            'association_nom': don[4],
            'IdA': don[5],
            'donateur_nom': don[6],
            'id_donateur': don[7]
        } for don in dons]
    finally:
        cursor.close()
        conn.close()

def compter_dons_par_periode(periode):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if periode == 'aujourdhui':
            query = "SELECT COUNT(*) FROM Don WHERE CAST(date_don AS DATE) = CAST(GETDATE() AS DATE)"
        elif periode == 'semaine':
            query = "SELECT COUNT(*) FROM Don WHERE date_don >= DATEADD(day, -7, GETDATE())"
        elif periode == 'mois':
            query = "SELECT COUNT(*) FROM Don WHERE date_don >= DATEADD(month, -1, GETDATE())"
        else:
            query = "SELECT COUNT(*) FROM Don"

        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0
    finally:
        cursor.close()
        conn.close()

# ========== FONCTIONS POUR STATISTIQUES GRAPHIQUES ==========

def get_dons_par_mois():
    """Obtenir le nombre de dons par mois pour les 12 derniers mois"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT
                FORMAT(date_don, 'yyyy-MM') as mois,
                COUNT(*) as nombre_dons
            FROM Don
            WHERE date_don >= DATEADD(month, -12, GETDATE())
            GROUP BY FORMAT(date_don, 'yyyy-MM')
            ORDER BY FORMAT(date_don, 'yyyy-MM')
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return [{'mois': r[0], 'nombre': r[1]} for r in results]
    finally:
        cursor.close()
        conn.close()

def get_dons_par_association():
    """Obtenir le nombre de dons par association"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT
                a.NomA,
                COUNT(d.IdD) as nombre_dons
            FROM Association a
            LEFT JOIN Don d ON a.IdA = d.IdA
            GROUP BY a.NomA, a.IdA
            ORDER BY nombre_dons DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return [{'nom': r[0], 'nombre': r[1]} for r in results]
    finally:
        cursor.close()
        conn.close()

def get_top_donateurs(limit=10):
    """Obtenir les top donateurs"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT TOP (?)
                don.nom,
                COUNT(d.IdD) as nombre_dons
            FROM Donateur don
            LEFT JOIN Don d ON don.id = d.id
            GROUP BY don.nom, don.id
            ORDER BY nombre_dons DESC
        """
        cursor.execute(query, (limit,))
        results = cursor.fetchall()
        return [{'nom': r[0], 'nombre': r[1]} for r in results]
    finally:
        cursor.close()
        conn.close()

def get_evolution_dons_semaine():
    """Obtenir l'évolution des dons pour les 7 derniers jours"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT
                CAST(date_don AS DATE) as jour,
                COUNT(*) as nombre_dons
            FROM Don
            WHERE date_don >= DATEADD(day, -7, GETDATE())
            GROUP BY CAST(date_don AS DATE)
            ORDER BY CAST(date_don AS DATE)
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return [{'jour': r[0].strftime('%Y-%m-%d') if r[0] else '', 'nombre': r[1]} for r in results]
    finally:
        cursor.close()
        conn.close()
