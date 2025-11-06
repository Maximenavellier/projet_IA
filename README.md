# Notre Assistant IA

Assistant Intelligent développé avec **Streamlit**

Projet de fin d’année : IA sous forme de site web intelligent proposant des articles personnalisés sur le sport, la musique, les jeux vidéos et l'actualité générale.

## Fonctionnalités

- **Interface Multi-Pages :** Navigation claire entre un mode "Recherche" et un mode "Parcourir les articles".
- **Recherche Intelligente et Pertinente :**
  - **Analyse sémantique :** L'IA distingue les mots-clés principaux des mots de contexte pour affiner la recherche.
  - **Extraction de contenu (avec `Newspaper3k`) :** L'assistant ne se contente pas des titres ou descriptions. Il scrape le contenu complet des articles pour une analyse en profondeur.
  - **Algorithme de score avancé :** La pertinence est calculée en fonction de la présence obligatoire des mots-clés principaux, de leur fréquence, et d'un bonus s'ils apparaissent dans le titre.
- **Options de Tri Avancées :**
  - Triez les résultats de recherche par pertinence ou par date de publication.
  - Triez les articles en mode "Parcourir" par date ou par note.
- **Système de Notation Persistant :**
  - Notez les articles de 1 à 5 étoiles.
  - Vos notes sont sauvegardées localement dans un fichier `ratings.json` et sont conservées entre les sessions.
- **Affichage Dynamique et Intuitif :**
  - **Présentation claire :** Le meilleur résultat est mis en avant, tandis que les autres articles similaires sont groupés dans des sections dépliables.
  - **Contenu intégré :** Lisez un résumé ou l'intégralité du contenu de l'article directement dans l'application, avec un lien vers la source originale.
  - **Visuels attractifs :** Les images des articles sont directement affichées pour une meilleure expérience visuelle.
- **Contrôle de l'Affichage :** Choisissez le nombre d'articles à afficher via un sélecteur dans la barre latérale.
- **Contenu en Temps Réel (avec `GNews API`) :** Les articles sont récupérés en direct pour garantir des informations toujours à jour.
- **Performances Optimisées :** Le scraping du contenu de plusieurs articles est effectué en parallèle pour réduire le temps de chargement.

## Équipe

- Noam Boutounas
- Maxime Navellier

## Installation

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
