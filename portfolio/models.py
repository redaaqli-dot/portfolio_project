from datetime import datetime
from . import db

class SiteConfig(db.Model):
    """Table unique pour la configuration générale du portfolio."""
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    hero_intro = db.Column(db.Text, nullable=True)
    hero_secondary = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    track = db.Column(db.String(100), nullable=True)
    focus = db.Column(db.String(100), nullable=True)
    about_main = db.Column(db.Text, nullable=True)
    about_secondary = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    github = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    resume_filename = db.Column(db.String(255), nullable=True)
    profile_image_filename = db.Column(db.String(255), nullable=True)
    
    # Nouveaux champs pour les listes simples (stockés sous forme de texte séparé par des virgules)
    programming_languages = db.Column(db.Text, nullable=True)
    languages = db.Column(db.Text, nullable=True)
    strengths = db.Column(db.Text, nullable=True)
    extracurricular = db.Column(db.Text, nullable=True)

class Experience(db.Model):
    """Table pour le parcours professionnel."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    period = db.Column(db.String(100), nullable=False) # ex: "Juillet 2025 - Août 2025"
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Education(db.Model):
    """Table pour le parcours académique."""
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(150), nullable=False)
    institution = db.Column(db.String(150), nullable=False)
    period = db.Column(db.String(100), nullable=False) # ex: "2023 - 2028"
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Certification(db.Model):
    """Table pour les certificats."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    issuer = db.Column(db.String(100), nullable=True) # ex: "Harvard University"
    date_obtained = db.Column(db.String(100), nullable=True)
    
    # Nouveaux champs pour les fichiers
    logo_filename = db.Column(db.String(255), nullable=True) # Logo de l'entreprise
    file_filename = db.Column(db.String(255), nullable=True) # Le certificat (PDF ou Image)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    """Table pour stocker tes projets."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    short_description = db.Column(db.String(255), nullable=False)
    full_description = db.Column(db.Text, nullable=True)
    stack = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    demo_url = db.Column(db.String(255), nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    """Table pour les messages du formulaire de contact."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)