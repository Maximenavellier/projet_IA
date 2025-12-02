Culturia - Assistant Culturel Intelligent
Application web développée avec Streamlit dans le cadre d'un projet de fin d'année. Culturia agrège et analyse des articles d'actualité (Sport, Musique, Jeux Vidéo, Actualité) pour proposer une navigation simplifiée et pertinente.

Fonctionnalités Principales
Interface et Navigation
Design Personnalisé : Interface épurée utilisant des polices Serif (Playfair Display & Merriweather) rappelant la presse traditionnelle.

Mise en Page HTML/CSS : Utilisation de composants HTML personnalisés pour dépasser les limitations natives de Streamlit (cartes articles, grilles, conteneurs).

Standardisation Visuelle : Toutes les images sont automatiquement affichées au format 16/9 via CSS.

Barre de Contrôle : Regroupement de la recherche, du mode "Parcourir", de l'historique et du sélecteur de quantité d'articles.

Recherche et Analyse
Moteur de Recherche : Analyse des mots-clés et distinction entre le sujet principal et le contexte.

Correction Orthographique : Module de détection et de suggestion pour les termes mal orthographiés.

Scraping de Contenu : Extraction du texte intégral des articles via Newspaper3k pour une analyse plus profonde que les simples méta-données.

Scoring de Pertinence : Algorithme calculant la pertinence des articles en fonction de la fréquence des mots-clés (affichage détaillé dans la section "Mots en commun").

Expérience de Lecture
Historique : Accès rapide aux 10 derniers articles consultés via un menu déroulant.

Lecture Intégrée : Possibilité de lire le contenu complet de l'article directement dans l'application via un bouton dépliant, sans redirection obligatoire.

Filtrage Thématique : Mode "Parcourir" permettant de trier les articles par catégorie (Sport, Tech, etc.).

Aspects Techniques
API GNews : Récupération des flux d'actualités en temps réel.

Persistance des Données : Sauvegarde locale des notes attribuées aux articles (ratings.json).

Optimisation : Utilisation du multi-threading pour le scraping des articles afin de réduire les temps de chargement.

Équipe développement :

Noam Boutounas
Maxime Navellier

Installation
Assurez-vous d'avoir Python installé sur votre machine.

Clonez ou téléchargez ce projet.

Ouvrez un terminal dans le dossier du projet et installez les dépendances :

pip install -r requirements.txt

Lancez l'application Streamlit :

streamlit run app.py
