# Notre Assistant IA

Assistant Intelligent

Projet de fin d’année : IA sous forme de site web intelligent proposant des articles personnalisés sur le sport, la musique, les jeux vidéos et l'actualité générale.

## 🚀 Fonctionnalités

- **Interface Multi-Pages :** Navigation claire entre un mode "Recherche" et un mode "Parcourir les articles".
- **Recherche par Pertinence :** Un algorithme de recherche qui analyse les mots-clés dans les titres et descriptions pour classer les résultats par pertinence.
- **Options de Tri Avancées :**
  - Triez les résultats de recherche par pertinence, date de publication (récente ou ancienne).
  - Triez les articles en mode "Parcourir" par date ou par note.
- **Système de Notation Persistant :**
  - Notez les articles de 1 à 5 étoiles.
  - Vos notes sont sauvegardées localement dans un fichier `ratings.json` et sont conservées entre les sessions.
- **Affichage Dynamique et Intuitif :**
  - Les résultats de recherche similaires sont présentés dans des sections dépliables (`expanders`) pour une meilleure lisibilité.
  - Une animation de fondu a été ajoutée pour une expérience utilisateur plus fluide lors de l'affichage des résultats.
- **Contrôle de l'Affichage :** Choisissez le nombre d'articles à afficher via un sélecteur dans la barre latérale.
- **Base de Données Enrichie :** Contient une large sélection d'articles sur 4 thèmes : Sport, Musique, Jeux Vidéo, et Actualité.

## 👥 Équipe

- Noam Boutounas
- Maxime Navellier

## 📦 Installation

1.  Assurez-vous d'avoir Python installé sur votre machine.
2.  Clonez ou téléchargez ce projet.
3.  Ouvrez un terminal dans le dossier du projet et installez les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

4.  Lancez l'application Streamlit :

    ```bash
    streamlit run app.py
    ```

