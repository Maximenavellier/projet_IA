import streamlit as st
import re
import time
from datetime import datetime
import json
import os
import requests
from fuzzywuzzy import process

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Mon IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MON ASSISTANT IA")
st.write("**Spécialiste : Sport 🏆 • Musique 🎵 • Jeux Vidéo 🎮 • Actualité 🌍**")

# --- CLÉ API ET CONSTANTES ---
GNEWS_API_KEY = "7d4dac92369bac5d8cd91e547bef9f54"  # Remplacez par votre clé API GNews
RATINGS_FILE = "ratings.json"

# Mots à ignorer pour ne pas polluer la recherche
STOP_WORDS = set(["le", "la", "les", "un", "une", "des", "de", "du", "au", "aux", "et", "ou", "est", "sont", "a", "ont", "qui", "que", "quoi", "dont", "où", "je", "tu", "il", "elle", "nous", "vous", "ils", "elles", "quel", "quelle", "quelles", "quels", "mon", "ton", "son", "notre", "votre", "leur", "dans", "sur", "avec", "pour", "par", "sans", "comment", "pourquoi", "quand"])


# --- GESTION DES NOTES (PERSISTANCE) ---
def load_ratings():
    if os.path.exists(RATINGS_FILE):
        try:
            with open(RATINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_ratings(ratings):
    with open(RATINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(ratings, f, indent=4)

if 'article_ratings' not in st.session_state:
    st.session_state.article_ratings = load_ratings()


# --- FONCTIONS PRINCIPALES ---

def get_search_query(question):
    """
    Nettoie la question de l'utilisateur pour ne garder que les mots-clés pertinents.
    Retourne une liste de mots-clés.
    """
    question_lower = question.lower().strip()
    words = re.split(r'\W+', question_lower)
    meaningful_words = [word for word in words if word and word not in STOP_WORDS]
    
    if not meaningful_words:
        return [question] # Si tout est filtré, on garde la question originale
        
    print(f"Mots-clés extraits de la requête : {meaningful_words}")
    return meaningful_words


def get_news(keywords, max_articles=20):
    """
    Interroge l'API GNews en utilisant une recherche "OU" sur les mots-clés.
    """
    if not keywords:
        return []
    
    # Construit une requête de type "mot1 OR mot2 OR mot3"
    # Cela permet de trouver des articles contenant au moins un des mots-clés.
    query = " OR ".join(f'"{word}"' for word in keywords)
    
    try:
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": query,
            "lang": "fr",
            "max": max_articles,
            "apikey": GNEWS_API_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        formatted_articles = []
        for art in articles:
            formatted_articles.append({
                "titre": art["title"],
                "description": art["description"] or "Pas de description disponible.",
                "date": datetime.strptime(art["publishedAt"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d"),
                "theme": ", ".join(keywords),
                "url": art["url"]
            })
        return formatted_articles
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion à l'API GNews : {e}")
        return []
    except Exception as e:
        st.error(f"Une erreur est survenue : {e}")
        return []

def afficher_resultats_recherche(articles, query_words, num_to_show):
    """Affiche les résultats de la recherche avec effet de fondu et expanders."""
    fade_in_css = """
    <style>
    @keyframes fadeIn {
      0% { opacity: 0; transform: translateY(15px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
      animation: fadeIn 0.5s ease-out;
    }
    </style>
    """
    st.markdown(fade_in_css, unsafe_allow_html=True)
    
    results_container = st.empty()
    if not articles:
        st.warning("🤔 Aucun article trouvé pour cette recherche.")
        return

    time.sleep(0.01)

    with results_container.container():
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        # Calcul du score de pertinence basé sur les mots de la requête originale
        scored_articles = []
        for article in articles:
            contenu = (article["titre"] + " " + article["description"]).lower()
            mots_contenu = re.split(r'\W+', contenu)
            score = sum(mots_contenu.count(mot) for mot in query_words)
            
            # Bonus si plusieurs mots-clés sont présents
            mots_trouves = sum(1 for mot in query_words if mot in mots_contenu)
            if mots_trouves > 1:
                score += mots_trouves * 5 # Ajoute un bonus pour chaque mot-clé supplémentaire trouvé
            
            if score > 0:
                scored_articles.append({"article": article, "score": score})
        
        # Trier par score
        scored_articles.sort(key=lambda x: x["score"], reverse=True)

        if not scored_articles:
            st.warning("🤔 Aucun article pertinent trouvé après filtrage.")
            return

        # Afficher le meilleur résultat
        meilleur_article = scored_articles[0]
        score_text = f"(Mots en commun : {meilleur_article['score']})"
        st.success(f"✅ **Meilleur résultat** {score_text}")
        with st.container(border=True):
            st.subheader(f"[{meilleur_article['article']['titre']}]({meilleur_article['article']['url']})")
            st.caption(f"Date : {meilleur_article['article']['date']}")
            st.write(meilleur_article['article']['description'])

        # Afficher les 5 autres résultats pertinents sous forme d'expanders
        if len(scored_articles) > 1:
            st.write("---")
            st.info("🔎 **Autres résultats similaires :**")
            for res in scored_articles[1:num_to_show + 1]: # Affiche les 5 suivants
                score_text = f"| Mots en commun : {res['score']}"
                expander_label = f"**{res['article']['titre']}** (Date : {res['article']['date']}) {score_text}"
                with st.expander(expander_label):
                    st.write(res['article']['description'])
                    st.markdown(f"[Lire l'article complet]({res['article']['url']})")
        
        st.markdown('</div>', unsafe_allow_html=True)

def page_recherche(num_articles_to_show):
    """Contenu de la page de recherche par mots-clés."""
    st.header("🔍 Recherche par mots-clés")
    question = st.text_input("Posez votre question ou entrez des mots-clés ici :", key="search_query")

    if question:
        query_words = get_search_query(question)
        st.write(f"Recherche d'articles pour : **'{' '.join(query_words)}'**")
        
        with st.spinner(f"🔍 Recherche des actualités..."):
            articles = get_news(query_words, max_articles=20) # On récupère plus d'articles pour avoir un meilleur tri
        
        if articles:
            afficher_resultats_recherche(articles, query_words, num_articles_to_show)

def page_generale(num_articles_to_show):
    """Contenu de la page générale pour parcourir les articles."""
    st.header("📰 Parcourir les articles")

    st.sidebar.subheader("Options d'affichage")
    theme_filter = st.sidebar.radio("Filtrer par thème", ["Sport", "Musique", "Jeux Vidéo", "Technologie", "Actualité"])
    sort_by = st.sidebar.radio("Trier par", ["Date (plus récent)", "Meilleures notes"])

    query = theme_filter if theme_filter != "Actualité" else "actualité générale"
    
    with st.spinner(f"Chargement des articles sur le thème '{query}'..."):
        articles_a_afficher = get_news(query.split(), max_articles=num_articles_to_show * 2)

    if sort_by == "Date (plus récent)":
        articles_a_afficher.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    elif sort_by == "Meilleures notes":
        articles_a_afficher.sort(key=lambda x: st.session_state.article_ratings.get(x['titre'], 0), reverse=True)

    if not articles_a_afficher:
        st.warning("Aucun article à afficher pour cette catégorie.")
    else:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        for i, article in enumerate(articles_a_afficher[:num_articles_to_show]):
            with st.container(border=True):
                st.subheader(f"[{article['titre']}]({article['url']})")
                st.caption(f"Thème : {article['theme']} | Date : {article['date']}")
                st.write(article['description'])
                
                note_actuelle = st.session_state.article_ratings.get(article['titre'], 0)
                note = st.radio(
                    "Votre note :", 
                    options=[1, 2, 3, 4, 5], 
                    index=note_actuelle - 1 if note_actuelle > 0 else 2,
                    key=f"note_{article['titre']}_{i}", 
                    horizontal=True
                )
                
                if note_actuelle != note:
                    st.session_state.article_ratings[article['titre']] = note
                    save_ratings(st.session_state.article_ratings)
                    st.rerun()
                
                note_display = st.session_state.article_ratings.get(article['titre'], 0)
                if note_display > 0:
                    st.markdown(f"**Votre note : {'⭐' * note_display}**")
                else:
                    st.markdown("_Pas encore noté_")
            st.write("")
        st.markdown('</div>', unsafe_allow_html=True)

# --- Logique principale de l'application ---

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une page", ["Recherche par mots-clés", "Parcourir les articles"])
st.sidebar.divider()

st.sidebar.subheader("Paramètres d'affichage")
num_articles = st.sidebar.number_input("Nombre d'articles à afficher", min_value=1, max_value=20, value=5, step=1)
st.sidebar.divider()

if page == "Recherche par mots-clés":
    page_recherche(num_articles)
elif page == "Parcourir les articles":
    page_generale(num_articles)
