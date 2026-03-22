import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from portfolio import db
from portfolio.models import SiteConfig, Project, Experience, Education, Certification

def seed_database():
    with app.app_context():
        # Nettoyage et recréation de la structure
        db.drop_all()
        db.create_all()
        print("Base de données réinitialisée avec les nouvelles tables.")

        # 1. Configuration et Listes simples
        config = SiteConfig(
            full_name="REDA AQLI",
            role="Étudiant Ingénieur en Cybersécurité",
            hero_intro="Sécuriser l'avenir numérique.",
            hero_secondary="Passionné par la protection des systèmes d'information, les réseaux et le développement.",
            location="Casablanca, Maroc",
            track="Cybersécurité",
            focus="Réseaux & Programmation",
            about_main="Étudiant ingénieur en cybersécurité à l'ENSA Oujda, disposant de bases solides en réseaux, programmation et sécurité des systèmes d'information.",
            about_secondary="Curieux, rigoureux et motivé, je développe mes compétences à travers des projets académiques, des certifications reconnues et des expériences terrain. Mon objectif est de renforcer mon expertise technique et de contribuer à des projets concrets.",
            email="redaaqli18@gmail.com",
            linkedin="https://www.linkedin.com/in/redaaqli/",
            # Nouvelles listes
            programming_languages="Java, Python, C, Bash, SQL",
            languages="Arabe (Maternelle), Français (Courant), Anglais (Opérationnel)",
            strengths="Curieux, Rigoureux, Motivé, Créatif, Esprit d'analyse",
            extracurricular="Business E-commerce (lmaroqi.parfums), Veille technologique Cybersécurité, Recherche sur l'innovation et la créativité intuitive"
        )
        db.session.add(config)

        # 2. Expériences Professionnelles
        exp1 = Experience(
            title="Stagiaire E-commerce & Web",
            company="Boutique e-commerce",
            period="Août 2025 - Sept 2025",
            description="Soutien aux opérations quotidiennes. Participation à la digitalisation des processus administratifs et web. Gestion du contenu et suivi technique du site (front & back office)."
        )
        exp2 = Experience(
            title="Développement Java & IA",
            company="Kleos Solutions",
            period="Juillet 2025 - Août 2025",
            description="Participation à l'implémentation d'un chatbot IA intégré à une solution applicative. Programmation Java de niveau débutant, renforcement en algorithmique et structuration du code."
        )
        exp3 = Experience(
            title="Communication Digitale & Analyse de Données",
            company="Twistana",
            period="Juillet 2024 - Août 2024",
            description="Mobilisation de compétences créatives et IT pour soutenir la stratégie de contenu Instagram. Analyse basique des performances et de l'engagement."
        )
        exp4 = Experience(
            title="Développement logiciel",
            company="Capital Soft Sarl",
            period="Juin 2024 - Juillet 2024",
            description="Projet de plateforme pour un club sportif (cahier des charges, UI/UX). Structuration des fonctionnalités et des parcours utilisateurs."
        )
        db.session.add_all([exp1, exp2, exp3, exp4])

        # 3. Parcours Académique
        edu1 = Education(
            degree="Diplôme d'Ingénieur d'État - Cybersécurité",
            institution="ENSA Oujda",
            period="2023 - 2028",
            description="Cycle préparatoire + cycle ingénieur. Spécialisation en Sécurité des Systèmes d'Information."
        )
        edu2 = Education(
            degree="Baccalauréat Sciences Physique",
            institution="Lycée Chawki, Casablanca",
            period="2023",
            description="Mention : Très Bien."
        )
        db.session.add_all([edu1, edu2])

        # 4. Certifications
        cert1 = Certification(name="CCNA - Cisco Certified Network Associate", issuer="Cisco", date_obtained="En cours")
        cert2 = Certification(name="CS50's Introduction to Cybersecurity", issuer="Harvard University", date_obtained="Décembre 2025")
        cert3 = Certification(name="NASA Space Apps Challenge", issuer="NASA", date_obtained="Octobre 2024")
        cert4 = Certification(name="Hack to the Future 4", issuer="Hackathon", date_obtained="Janvier 2022")
        cert5 = Certification(name="GREEN-TC 2021", issuer="Compétition", date_obtained="Première place")
        db.session.add_all([cert1, cert2, cert3, cert4, cert5])

        # 5. Projets
        projet1 = Project(title="Implémentation d'algorithmes cryptographiques", slug="implementation-crypto-java", category="Cybersécurité", short_description="Développement d'algorithmes de cryptographie en Java.", stack="Java, Cryptographie", featured=True)
        projet2 = Project(title="Seismo Safe", slug="seismo-safe", category="Application Mobile", short_description="Application mobile d'alerte sismique.", stack="NASA Space Apps", featured=True)
        projet3 = Project(title="S.O.S Asylum", slug="sos-asylum", category="Plateforme Web", short_description="Plateforme d'assistance internationale.", stack="Hack to the Future", featured=True)
        db.session.add_all([projet1, projet2, projet3])
        
        db.session.commit()
        print("Les données complètes de Reda ont été injectées avec succès !")

if __name__ == '__main__':
    seed_database()