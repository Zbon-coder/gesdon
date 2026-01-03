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

    stats = {
        'total_donateurs': len(donateurs),
        'total_dons': len(dons),
        'montant_total': sum(don['montant'] for don in dons)
    }

    derniers_dons = dons[:5]

    return render_template('dashboard.html', stats=stats, derniers_dons=derniers_dons)

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
        prenom = request.form.get('prenom')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        ville = request.form.get('ville')
        code_postal = request.form.get('code_postal')

        if models.creer_donateur(nom, prenom, telephone, email, adresse, ville, code_postal):
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
        prenom = request.form.get('prenom')
        telephone = request.form.get('telephone')
        email = request.form.get('email')
        adresse = request.form.get('adresse')
        ville = request.form.get('ville')
        code_postal = request.form.get('code_postal')

        if models.modifier_donateur(id, nom, prenom, telephone, email, adresse, ville, code_postal):
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

    if request.method == 'POST':
        id_donateur = request.form.get('id_donateur')
        montant = request.form.get('montant')
        type_don = request.form.get('type_don')
        description = request.form.get('description')

        if models.creer_don(id_donateur, montant, type_don, description):
            flash('Don enregistré avec succès !', 'success')
            return redirect(url_for('liste_dons'))
        else:
            flash('Erreur lors de l\'enregistrement du don.', 'danger')

    return render_template('form_don.html', don=None, donateurs=donateurs)

@app.route('/dons/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
def modifier_don(id):
    don = models.get_don_by_id(id)
    donateurs = models.get_tous_donateurs()

    if not don:
        flash('Don non trouvé.', 'danger')
        return redirect(url_for('liste_dons'))

    if request.method == 'POST':
        id_donateur = request.form.get('id_donateur')
        montant = request.form.get('montant')
        type_don = request.form.get('type_don')
        description = request.form.get('description')

        if models.modifier_don(id, id_donateur, montant, type_don, description):
            flash('Don modifié avec succès !', 'success')
            return redirect(url_for('liste_dons'))
        else:
            flash('Erreur lors de la modification du don.', 'danger')

    return render_template('form_don.html', don=don, donateurs=donateurs)

@app.route('/dons/supprimer/<int:id>')
@login_required
def supprimer_don(id):
    if models.supprimer_don(id):
        flash('Don supprimé avec succès !', 'success')
    else:
        flash('Erreur lors de la suppression du don.', 'danger')

    return redirect(url_for('liste_dons'))

if __name__ == "__main__":
    app.run(debug=True)