from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import models

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_tres_securisee_ici_2024'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== ROUTES D'AUTHENTIFICATION ==========

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')

        utilisateur = models.verifier_utilisateur(email, mot_de_passe)
        if utilisateur:
            session['user_id'] = utilisateur['id']
            session['user_nom'] = utilisateur['nom_utilisateur']
            session['user_email'] = utilisateur['email']
            flash(f'Bienvenue {utilisateur["nom_utilisateur"]} !', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom_utilisateur = request.form.get('nom_utilisateur')
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        confirmer_mot_de_passe = request.form.get('confirmer_mot_de_passe')

        if mot_de_passe != confirmer_mot_de_passe:
            flash('Les mots de passe ne correspondent pas.', 'danger')
            return render_template('register.html')

        if models.creer_utilisateur(nom_utilisateur, email, mot_de_passe):
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Erreur lors de l\'inscription. L\'email ou le nom d\'utilisateur existe peut-être déjà.', 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous êtes déconnecté.', 'info')
    return redirect(url_for('login'))

# ========== TABLEAU DE BORD ==========

@app.route('/dashboard')
@login_required
def dashboard():
    donateurs = models.get_tous_donateurs()
    dons = models.get_tous_dons()
    associations = models.get_toutes_associations()

    stats = {
        'total_donateurs': len(donateurs),
        'total_dons': len(dons),
        'total_associations': len(associations)
    }

    derniers_dons = dons[:5]

    return render_template('dashboard.html', stats=stats, derniers_dons=derniers_dons)

# ========== ROUTES CRUD ASSOCIATIONS ==========

@app.route('/associations')
@login_required
def liste_associations():
    associations = models.get_toutes_associations()
    return render_template('associations.html', associations=associations)

@app.route('/associations/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_association():
    if request.method == 'POST':
        NomA = request.form.get('NomA')
        CompteBANK = request.form.get('CompteBANK')
        tel = request.form.get('tel')
        ville = request.form.get('ville')
        pays = request.form.get('pays')

        if models.creer_association(NomA, CompteBANK, tel, ville, pays):
            flash('Association ajoutée avec succès !', 'success')
            return redirect(url_for('liste_associations'))
        else:
            flash('Erreur lors de l\'ajout de l\'association.', 'danger')

    return render_template('form_association.html', association=None)

@app.route('/associations/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_association(id):
    association = models.get_association_by_id(id)

    if not association:
        flash('Association non trouvée.', 'danger')
        return redirect(url_for('liste_associations'))

    if request.method == 'POST':
        NomA = request.form.get('NomA')
        CompteBANK = request.form.get('CompteBANK')
        tel = request.form.get('tel')
        ville = request.form.get('ville')
        pays = request.form.get('pays')

        if models.modifier_association(id, NomA, CompteBANK, tel, ville, pays):
            flash('Association modifiée avec succès !', 'success')
            return redirect(url_for('liste_associations'))
        else:
            flash('Erreur lors de la modification de l\'association.', 'danger')

    return render_template('form_association.html', association=association)

@app.route('/associations/supprimer/<int:id>')
@login_required
def supprimer_association(id):
    if models.supprimer_association(id):
        flash('Association supprimée avec succès !', 'success')
    else:
        flash('Erreur lors de la suppression de l\'association.', 'danger')

    return redirect(url_for('liste_associations'))

# ========== ROUTES CRUD DONATEURS ==========

@app.route('/donateurs')
@login_required
def liste_donateurs():
    donateurs = models.get_tous_donateurs()
    return render_template('donateurs.html', donateurs=donateurs)

@app.route('/donateurs/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_donateur():
    if request.method == 'POST':
        nom = request.form.get('nom')
        tel = request.form.get('tel')
        mail = request.form.get('mail')
        BP = request.form.get('BP')
        ville = request.form.get('ville')

        if models.creer_donateur(nom, tel, mail, BP, ville):
            flash('Donateur ajouté avec succès !', 'success')
            return redirect(url_for('liste_donateurs'))
        else:
            flash('Erreur lors de l\'ajout du donateur.', 'danger')

    return render_template('form_donateur.html', donateur=None)

@app.route('/donateurs/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_donateur(id):
    donateur = models.get_donateur_by_id(id)

    if not donateur:
        flash('Donateur non trouvé.', 'danger')
        return redirect(url_for('liste_donateurs'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        tel = request.form.get('tel')
        mail = request.form.get('mail')
        BP = request.form.get('BP')
        ville = request.form.get('ville')

        if models.modifier_donateur(id, nom, tel, mail, BP, ville):
            flash('Donateur modifié avec succès !', 'success')
            return redirect(url_for('liste_donateurs'))
        else:
            flash('Erreur lors de la modification du donateur.', 'danger')

    return render_template('form_donateur.html', donateur=donateur)

@app.route('/donateurs/supprimer/<int:id>')
@login_required
def supprimer_donateur(id):
    if models.supprimer_donateur(id):
        flash('Donateur supprimé avec succès !', 'success')
    else:
        flash('Erreur lors de la suppression du donateur.', 'danger')

    return redirect(url_for('liste_donateurs'))

# ========== ROUTES CRUD DONS ==========

@app.route('/dons')
@login_required
def liste_dons():
    dons = models.get_tous_dons()
    return render_template('dons.html', dons=dons)

@app.route('/dons/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_don():
    donateurs = models.get_tous_donateurs()
    associations = models.get_toutes_associations()

    if request.method == 'POST':
        libelle = request.form.get('libelle')
        description = request.form.get('description')
        IdA = request.form.get('IdA')
        id_donateur = request.form.get('id_donateur')

        if models.creer_don(libelle, description, IdA, id_donateur):
            flash('Don enregistré avec succès !', 'success')
            return redirect(url_for('liste_dons'))
        else:
            flash('Erreur lors de l\'enregistrement du don.', 'danger')

    return render_template('form_don.html', don=None, donateurs=donateurs, associations=associations)

@app.route('/dons/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_don(id):
    don = models.get_don_by_id(id)
    donateurs = models.get_tous_donateurs()
    associations = models.get_toutes_associations()

    if not don:
        flash('Don non trouvé.', 'danger')
        return redirect(url_for('liste_dons'))

    if request.method == 'POST':
        libelle = request.form.get('libelle')
        description = request.form.get('description')
        IdA = request.form.get('IdA')
        id_donateur = request.form.get('id_donateur')

        if models.modifier_don(id, libelle, description, IdA, id_donateur):
            flash('Don modifié avec succès !', 'success')
            return redirect(url_for('liste_dons'))
        else:
            flash('Erreur lors de la modification du don.', 'danger')

    return render_template('form_don.html', don=don, donateurs=donateurs, associations=associations)

@app.route('/dons/supprimer/<int:id>')
@login_required
def supprimer_don(id):
    if models.supprimer_don(id):
        flash('Don supprimé avec succès !', 'success')
    else:
        flash('Erreur lors de la suppression du don.', 'danger')

    return redirect(url_for('liste_dons'))

# ========== PAGE HISTORIQUE ==========

@app.route('/historique')
@login_required
def historique():
    periode = request.args.get('periode', 'tout')
    association_filter = request.args.get('association', '')
    donateur_filter = request.args.get('donateur', '')

    # Obtenir les dons filtrés
    dons = models.get_dons_filtres(
        periode=periode if periode != 'tout' else None,
        association_id=int(association_filter) if association_filter else None,
        donateur_id=int(donateur_filter) if donateur_filter else None
    )

    # Statistiques
    total_dons = models.compter_dons_par_periode('tout')
    dons_mois = models.compter_dons_par_periode('mois')
    dons_semaine = models.compter_dons_par_periode('semaine')
    dons_aujourdhui = models.compter_dons_par_periode('aujourdhui')

    # Pour les filtres
    associations = models.get_toutes_associations()
    donateurs = models.get_tous_donateurs()

    return render_template('historique.html',
                         dons=dons,
                         total_dons=total_dons,
                         dons_mois=dons_mois,
                         dons_semaine=dons_semaine,
                         dons_aujourdhui=dons_aujourdhui,
                         associations=associations,
                         donateurs=donateurs,
                         periode=periode,
                         association_filter=association_filter,
                         donateur_filter=donateur_filter)

# ========== PAGE PROFIL ==========

@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            nom_utilisateur = request.form.get('nom_utilisateur')
            email = request.form.get('email')

            if models.modifier_utilisateur(session['user_id'], nom_utilisateur, email):
                session['user_nom'] = nom_utilisateur
                session['user_email'] = email
                flash('Profil mis à jour avec succès !', 'success')
            else:
                flash('Erreur lors de la mise à jour du profil.', 'danger')

        elif action == 'change_password':
            ancien_mot_de_passe = request.form.get('ancien_mot_de_passe')
            nouveau_mot_de_passe = request.form.get('nouveau_mot_de_passe')
            confirmer_mot_de_passe = request.form.get('confirmer_mot_de_passe')

            # Vérifier l'ancien mot de passe
            utilisateur = models.verifier_utilisateur(session['user_email'], ancien_mot_de_passe)
            if not utilisateur:
                flash('Ancien mot de passe incorrect.', 'danger')
            elif nouveau_mot_de_passe != confirmer_mot_de_passe:
                flash('Les nouveaux mots de passe ne correspondent pas.', 'danger')
            elif models.changer_mot_de_passe(session['user_id'], nouveau_mot_de_passe):
                flash('Mot de passe changé avec succès !', 'success')
            else:
                flash('Erreur lors du changement de mot de passe.', 'danger')

        return redirect(url_for('profil'))

    # GET request
    utilisateur = models.get_utilisateur_by_id(session['user_id'])
    dons = models.get_tous_dons()
    donateurs = models.get_tous_donateurs()
    associations = models.get_toutes_associations()

    stats = {
        'total_dons': len(dons),
        'total_donateurs': len(donateurs),
        'total_associations': len(associations)
    }

    derniers_dons = dons[:5]

    # Calculer les jours d'activité (depuis la création du compte)
    from datetime import datetime
    if utilisateur.get('date_creation'):
        jours_activite = (datetime.now() - utilisateur['date_creation']).days
    else:
        jours_activite = 0

    return render_template('profil.html',
                         utilisateur=utilisateur,
                         stats=stats,
                         derniers_dons=derniers_dons,
                         jours_activite=jours_activite)

if __name__ == "__main__":
    app.run(debug=True)
