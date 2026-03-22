import os
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from .models import SiteConfig, Project, ContactMessage, Experience, Education, Certification
from . import db

bp = Blueprint('main', __name__)

# --- CONFIGURATION SÉCURITÉ ---
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")

# Extensions autorisées pour éviter l'exécution de code malveillant
ALLOWED_CV_EXTENSIONS = {'pdf'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename, allowed_set):
    """Vérifie si l'extension du fichier fait partie de la liste blanche."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

# ==========================================
# ROUTES PUBLIQUES
# ==========================================

@bp.route('/')
def index():
    config = SiteConfig.query.first()
    
    # On récupère les projets en les triant du plus récent au plus ancien
    projects = Project.query.order_by(Project.created_at.desc()).all()
    
    # On récupère les nouvelles données (triées par ID décroissant pour avoir les plus récentes en haut)
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    educations = Education.query.order_by(Education.id.desc()).all()
    certifications = Certification.query.order_by(Certification.id.desc()).all()
    
    return render_template('index.html', 
                           config=config, 
                           projects=projects,
                           experiences=experiences,
                           educations=educations,
                           certifications=certifications)
@bp.route('/project/<slug>')
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    config = SiteConfig.query.first()
    return render_template('project_detail.html', project=project, config=config)

# ==========================================
# ROUTES POUR SERVIR LES FICHIERS UPLOADÉS
# ==========================================

@bp.route('/uploads/cv/<filename>')
def uploaded_cv(filename):
    """Permet au navigateur de télécharger ou lire le CV."""
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], 'cv'), filename)

@bp.route('/uploads/profile/<filename>')
def uploaded_profile(filename):
    """Permet d'afficher la photo de profil sur le site."""
    return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile'), filename)

# ==========================================
# ROUTES ADMINISTRATION
# ==========================================

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if 'is_admin' in session:
        return redirect(url_for('main.admin_dashboard'))

    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['is_admin'] = True
            flash("Accès autorisé. Bienvenue.", "success")
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash("Accès refusé. Mot de passe incorrect.", "error")

    return render_template('admin/login.html')

@bp.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('main.index'))

@bp.route('/admin/dashboard')
def admin_dashboard():
    if 'is_admin' not in session:
        flash("Accès restreint. Veuillez vous identifier.", "error")
        return redirect(url_for('main.admin_login'))
    return render_template('admin/dashboard.html')

@bp.route('/admin/config', methods=['GET', 'POST'])
def edit_config():
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))

    config = SiteConfig.query.first()
    if not config:
        config = SiteConfig()
        db.session.add(config)

    if request.method == 'POST':
        config.full_name = request.form.get('full_name')
        config.role = request.form.get('role')
        config.hero_intro = request.form.get('hero_intro')
        config.hero_secondary = request.form.get('hero_secondary')
        config.about_main = request.form.get('about_main')
        config.about_secondary = request.form.get('about_secondary')
        config.github = request.form.get('github')
        config.linkedin = request.form.get('linkedin')
        config.programming_languages = request.form.get('programming_languages')
        config.languages = request.form.get('languages')
        config.strengths = request.form.get('strengths')
        config.extracurricular = request.form.get('extracurricular')
        db.session.commit()
        flash("Configuration système mise à jour.", "success")
        return redirect(url_for('main.admin_dashboard'))

    return render_template('admin/edit_config.html', config=config)

@bp.route('/admin/uploads', methods=['GET', 'POST'])
def admin_uploads():
    """Route pour gérer l'upload du CV et de la photo de profil."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))

    config = SiteConfig.query.first()

    if request.method == 'POST':
        # 1. Gestion de la photo de profil
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '' and allowed_file(file.filename, ALLOWED_IMG_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile', filename))
                config.profile_image_filename = filename
                flash("Photo de profil uploadée avec succès.", "success")

        # 2. Gestion du CV
        if 'cv_file' in request.files:
            file = request.files['cv_file']
            if file and file.filename != '' and allowed_file(file.filename, ALLOWED_CV_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'cv', filename))
                config.resume_filename = filename
                flash("CV (PDF) uploadé avec succès.", "success")

        db.session.commit()
        return redirect(url_for('main.admin_uploads'))

    return render_template('admin/uploads.html', config=config)
# ==========================================
# CRUD PROJETS (Create, Read, Update, Delete)
# ==========================================

@bp.route('/admin/projects')
def manage_projects():
    """Affiche la liste de tous les projets."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    # On récupère tous les projets, du plus récent au plus ancien
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/manage_projects.html', projects=projects)

@bp.route('/admin/projects/add', methods=['GET', 'POST'])
def add_project():
    """Ajoute un nouveau projet."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))

    if request.method == 'POST':
        title = request.form.get('title')
        # Création automatique d'un slug propre (ex: "Mon Projet 1!" -> "mon-projet-1")
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        
        # Pour éviter les doublons de slugs, on ajoute un nombre aléatoire si besoin en production, 
        # mais ici on va garder ça simple.
        
        new_project = Project(
            title=title,
            slug=slug,
            category=request.form.get('category'),
            short_description=request.form.get('short_description'),
            full_description=request.form.get('full_description'),
            stack=request.form.get('stack'),
            github_url=request.form.get('github_url'),
            demo_url=request.form.get('demo_url'),
            featured=True if request.form.get('featured') else False
        )
        db.session.add(new_project)
        db.session.commit()
        flash("Nouveau projet ajouté à l'arsenal.", "success")
        return redirect(url_for('main.manage_projects'))

    return render_template('admin/project_form.html', project=None)

@bp.route('/admin/projects/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    """Modifie un projet existant."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.title = request.form.get('title')
        project.category = request.form.get('category')
        project.short_description = request.form.get('short_description')
        project.full_description = request.form.get('full_description')
        project.stack = request.form.get('stack')
        project.github_url = request.form.get('github_url')
        project.demo_url = request.form.get('demo_url')
        project.featured = True if request.form.get('featured') else False

        db.session.commit()
        flash("Projet mis à jour avec succès.", "success")
        return redirect(url_for('main.manage_projects'))

    return render_template('admin/project_form.html', project=project)

@bp.route('/admin/projects/delete/<int:id>', methods=['POST'])
def delete_project(id):
    """Supprime un projet."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash("Projet effacé de la base de données.", "success")
    return redirect(url_for('main.manage_projects'))
# ==========================================
# GESTION DES MESSAGES DE CONTACT
# ==========================================

@bp.route('/contact', methods=['POST'])
def submit_contact():
    """Traite le formulaire de contact de la page d'accueil publique."""
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Sécurité basique : on vérifie que les champs requis ne sont pas vides
    if not name or not email or not message:
        flash("Veuillez remplir tous les champs obligatoires.", "error")
        return redirect(url_for('main.index') + '#contact')

    new_message = ContactMessage(
        name=name,
        email=email,
        subject=subject,
        message=message
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    flash("Connexion établie. Votre message a été transmis avec succès.", "success")
    return redirect(url_for('main.index') + '#contact')

@bp.route('/admin/messages')
def view_messages():
    """Affiche la boîte de réception dans l'admin."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    # On récupère les messages du plus récent au plus ancien
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@bp.route('/admin/messages/delete/<int:id>', methods=['POST'])
def delete_message(id):
    """Supprime un message de la base de données."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    msg = ContactMessage.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message purgé du système.", "success")
    return redirect(url_for('main.view_messages'))
# ==========================================
# CRUD EXPÉRIENCES PROFESSIONNELLES
# ==========================================

@bp.route('/admin/experiences')
def manage_experiences():
    """Affiche la liste des expériences."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return render_template('admin/manage_experiences.html', experiences=experiences)

@bp.route('/admin/experiences/add', methods=['GET', 'POST'])
def add_experience():
    """Ajoute une nouvelle expérience."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))

    if request.method == 'POST':
        new_exp = Experience(
            title=request.form.get('title'),
            company=request.form.get('company'),
            period=request.form.get('period'),
            description=request.form.get('description')
        )
        db.session.add(new_exp)
        db.session.commit()
        flash("Nouvelle expérience ajoutée au parcours.", "success")
        return redirect(url_for('main.manage_experiences'))

    return render_template('admin/experience_form.html', exp=None)

@bp.route('/admin/experiences/edit/<int:id>', methods=['GET', 'POST'])
def edit_experience(id):
    """Modifie une expérience existante."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    exp = Experience.query.get_or_404(id)

    if request.method == 'POST':
        exp.title = request.form.get('title')
        exp.company = request.form.get('company')
        exp.period = request.form.get('period')
        exp.description = request.form.get('description')
        db.session.commit()
        flash("Expérience mise à jour.", "success")
        return redirect(url_for('main.manage_experiences'))

    return render_template('admin/experience_form.html', exp=exp)

@bp.route('/admin/experiences/delete/<int:id>', methods=['POST'])
def delete_experience(id):
    """Supprime une expérience."""
    if 'is_admin' not in session:
        return redirect(url_for('main.admin_login'))
    
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash("Expérience purgée de la base de données.", "success")
    return redirect(url_for('main.manage_experiences'))