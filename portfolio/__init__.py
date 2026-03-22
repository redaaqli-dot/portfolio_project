import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Application Factory : crée et configure l'instance Flask."""
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-cyber-portfolio-super-secure')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 # Limite à 5 MB pour la sécurité

    db.init_app(app)

    # --- ENREGISTREMENT DES ROUTES (Blueprints) ---
    with app.app_context():
        # Importation des modèles pour la création des tables
        from . import models 
        
        # Création automatique du fichier portfolio.db dans le dossier instance/
        db.create_all()

        # CES DEUX LIGNES SONT MAINTENANT ACTIVÉES :
        from . import routes
        app.register_blueprint(routes.bp)

    return app