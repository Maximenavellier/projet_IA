import streamlit as st
import re
import time
from datetime import datetime

# --- CONFIGURATION (Doit être la 1ère commande) ---
st.set_page_config( 
    page_title="Culturia",
    page_icon="📰",
    layout="wide"
)

# --- IMPORTS / MOCKS ---
try:
    from persistence import load_ratings, save_ratings
    from utils import get_search_query, scrape_articles_parallel
    from gnews import get_news
except ImportError:
    def load_ratings(): return {}
    def save_ratings(r): pass
    def get_search_query(q): return {"principal": q.split(), "secondaire": []}
    def scrape_articles_parallel(arts):
        # Simulation d'un contenu VRAIMENT plus long
        for a in arts: 
            # On ajoute du faux texte pour simuler un article complet
            a['contenu_complet'] = a['description'] + " " + " ".join(["Ceci est un paragraphe de remplissage pour simuler le contenu complet de l'article." for _ in range(10)])
        return arts
    def get_news(k, max_articles=5):
        return [{"titre": f"Résultat {i+1} : L'impact de {k['principal']}", "url": "#", "date": "2023-12-01", "description": "Ceci est une brève description de l'article visible au premier coup d'œil...", "image": f"https://picsum.photos/{800+i}/{600+i}", "theme": "Test"} for i in range(max_articles)]

# --- CORRECTION ORTHOGRAPHE ---
def suggerer_correction(query):
    corrections = {
        "orelsn": "Orelsan", "footbal": "Football", "parie": "Paris",
        "musiqe": "Musique", "cinma": "Cinéma", "zelda": "The Legend of Zelda"
    }
    query_lower = query.lower()
    for faute, correct in corrections.items():
        if faute in query_lower:
            return query_lower.replace(faute, correct)
    return None

def local_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Erreur : Fichier {file_name} introuvable.")

# Chargement du style
local_css("style.css")

# --- SESSION STATE ---
if 'article_ratings' not in st.session_state: st.session_state.article_ratings = load_ratings()
if 'page' not in st.session_state: st.session_state.page = "Recherche" 
if 'num_articles' not in st.session_state: st.session_state.num_articles = 5
if 'history' not in st.session_state: st.session_state.history = []

def add_to_history(article):
    if not st.session_state.history or st.session_state.history[0]['titre'] != article['titre']:
        st.session_state.history.insert(0, article)
        if len(st.session_state.history) > 10:
            st.session_state.history = st.session_state.history[:10]

# --- FONCTIONS D'AIDE ---
def generate_word_list_html(article, query_words):
    """Génère la liste HTML des mots avec leur compteur (x3)."""
    # On cherche dans tout le texte (titre + contenu)
    full_text = (article['titre'] + " " + article.get('contenu_complet', article['description'])).lower()
    
    html_items = ""
    for mot in query_words:
        mot_lower = mot.lower()
        # Comptage simple
        count = full_text.count(mot_lower)
        if count > 0:
            html_items += f"<li>{mot} (x{count})</li>"
            
    if not html_items:
        html_items = "<li>Aucun mot clé trouvé dans le texte</li>"
    return html_items

# --- FONCTIONS D'AFFICHAGE ---

def afficher_resultats_recherche(articles, keywords_dict, num_to_show):
    
    results_container = st.empty()
    if not articles:
        st.warning("🤔 Aucun article trouvé.")
        return

    with results_container.container():
        # Scraping pour avoir le contenu complet (simulé)
        articles_with_content = scrape_articles_parallel(articles)
        scored_articles = [{"article": art, "score": 100} for art in articles_with_content] 
        query_words = keywords_dict["principal"]
        
        # --- 1. HERO CARD ---
        meilleur_article = scored_articles[0]['article']
        add_to_history(meilleur_article)
        
        # Génération liste mots
        mots_li = generate_word_list_html(meilleur_article, query_words)

        # HTML DE LA HERO CARD (SANS INDENTATION !!!)
        html_hero = f"""
<div class="article-card-hero">
<a href="{meilleur_article["url"]}" target="_blank" style="text-decoration:none;">
<h2 class="card-title">{meilleur_article["titre"]}</h2>
</a>
<div class="card-image-container">
<img src="{meilleur_article["image"]}" alt="Image Article">
</div>

<div class="card-text">
{meilleur_article['description']}
</div>

<details class="read-more-details">
<summary>Lire l'article complet</summary>
<div class="full-content-text">
{meilleur_article.get('contenu_complet', 'Contenu non disponible.')}
</div>
</details>

<details>
<summary>Mots en commun</summary>
<ul>{mots_li}</ul>
</details>

<div class="card-meta">
Source • {meilleur_article["date"]}
</div>
</div>
"""
        st.markdown(html_hero, unsafe_allow_html=True)

        # --- 2. CARTES SECONDAIRES ---
        if len(scored_articles) > 1:
            st.markdown("---")
            st.markdown("### Autres résultats")
            
            secondary_list = scored_articles[1:num_to_show+1]
            
            for i in range(0, len(secondary_list), 2):
                col1, col2 = st.columns(2)
                
                def get_mini_card_html(item_obj):
                    art = item_obj['article']
                    # Mots en commun pour cet article spécifique
                    mini_mots_li = generate_word_list_html(art, query_words)
                    
                    return f"""
<div class="article-card-secondary">
<a href="{art["url"]}" target="_blank" style="text-decoration:none;">
<div class="secondary-title">{art["titre"]}</div>
</a>
<div class="card-image-container">
<img src="{art["image"]}" alt="Image">
</div>

<div class="card-text" style="font-size: 0.9rem;">
{art["description"][:120]}...
</div>

<details class="read-more-details">
<summary>Lire la suite</summary>
<div class="full-content-text">
{art.get('contenu_complet', art['description'])}
</div>
</details>

<details>
<summary>Mots en commun</summary>
<ul>{mini_mots_li}</ul>
</details>

<div class="card-meta">
{art["date"]}
</div>
</div>
"""
                with col1:
                    st.markdown(get_mini_card_html(secondary_list[i]), unsafe_allow_html=True)
                
                if i + 1 < len(secondary_list):
                    with col2:
                        st.markdown(get_mini_card_html(secondary_list[i+1]), unsafe_allow_html=True)
                
                st.write("") 

# --- CONTENU DES PAGES ---

def page_recherche(num_articles_to_show):
    question = st.text_input("Recherche", placeholder="sur quel sujet souhaitez vous vous renseigner aujourd'hui ?", label_visibility="collapsed")
    
    correction = None
    if question:
        correction = suggerer_correction(question)
    
    if correction:
        st.markdown(f"""
        <div style="background-color: rgba(255, 193, 7, 0.1); border: 1px solid #ffc107; color: var(--text-color); padding: 10px; border-radius: 10px; margin-bottom: 20px; font-family: var(--font-body); text-align:center;">
            💡 Vouliez-vous dire <strong><em>"{correction}"</em></strong> ? 
        </div>
        """, unsafe_allow_html=True)

    if question:
        keywords_dict = get_search_query(question)
        with st.spinner(f"🔍 Recherche en cours..."):
            try:
                articles = get_news(keywords_dict, max_articles=20)
                if articles: 
                    afficher_resultats_recherche(articles, keywords_dict, num_articles_to_show)
            except Exception as e:
                st.error(f"Erreur lors de la recherche : {e}")

def page_generale(num_articles_to_show):
    st.header("📰 Parcourir les articles")

    theme_filter = st.radio("Thème", ["Sport", "Musique", "Jeux Vidéo", "Technologie", "Actualité"], horizontal=True, label_visibility="collapsed")
    query = theme_filter if theme_filter != "Actualité" else "actualité générale"
    
    with st.spinner(f"Chargement..."):
        try:
            arts = get_news({"principal": [query], "secondaire": []}, max_articles=num_articles_to_show * 2)
            # On ajoute aussi du faux contenu pour la page parcourir
            arts = scrape_articles_parallel(arts)
        except: arts = []

    if not arts:
        st.warning("Aucun article disponible.")
    else:
        for i in range(0, len(arts[:num_articles_to_show]), 2):
            col1, col2 = st.columns(2)
            
            def get_browse_card(art):
                img_div = f'<div class="card-image-container"><img src="{art["image"]}" alt="Image"></div>' if art['image'] else ""
                # Même logique "Lire la suite" pour le mode parcourir
                return f"""
<div class="article-card-secondary" style="height: 100%;">
<a href="{art["url"]}" target="_blank" style="text-decoration:none;">
<div class="secondary-title">{art["titre"]}</div>
</a>
{img_div}
<div class="card-text">{art["description"][:130]}...</div>

<details class="read-more-details">
<summary>Lire la suite</summary>
<div class="full-content-text">
{art.get('contenu_complet', art['description'])}
</div>
</details>

<div class="card-meta">{art["date"]}</div>
</div>
"""
            with col1: st.markdown(get_browse_card(arts[i]), unsafe_allow_html=True)
            if i + 1 < len(arts):
                with col2: st.markdown(get_browse_card(arts[i+1]), unsafe_allow_html=True)
            st.write("")

# --- LAYOUT PRINCIPAL ---
with st.container():
    st.markdown('<div class="nav-container-custom">', unsafe_allow_html=True)
    
    nav_cols = st.columns([1.2, 1.2, 1.2, 0.8])
    
    with nav_cols[0]:
        if st.button("Rechercher par mots-clés", use_container_width=True):
            st.session_state.page = "Recherche"
            st.rerun()

    with nav_cols[1]:
        if st.button("Parcourir les articles", use_container_width=True):
            st.session_state.page = "Parcourir"
            st.rerun()

    with nav_cols[2]:
        with st.expander("Historique 🕒"):
            if not st.session_state.history:
                st.write("Aucun historique.")
            else:
                for item in st.session_state.history:
                    st.markdown(f'<div class="history-item"><a href="{item["url"]}" target="_blank">📄 {item["titre"][:30]}...</a></div>', unsafe_allow_html=True)

    with nav_cols[3]:
        sub_cols = st.columns([1, 1.5, 1])
        if sub_cols[0].button("−", key="minus", use_container_width=True):
            st.session_state.num_articles = max(1, st.session_state.num_articles - 1)
            st.rerun()
            
        sub_cols[1].markdown(
            f"""
            <div style="text-align: center; font-family: Merriweather; font-size: 0.65rem; margin-bottom: 0px; white-space: nowrap;">articles affichés</div>
            <div style="text-align: center; border: 2px solid var(--border-color); border-radius: 6px; font-weight: bold; background: var(--card-bg); color: var(--text-color); font-size: 0.9rem;">{st.session_state.num_articles}</div>
            """, 
            unsafe_allow_html=True
        )
        if sub_cols[2].button("+", key="plus", use_container_width=True):
            st.session_state.num_articles = min(20, st.session_state.num_articles + 1)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="branding-container"><h1 class="brand-title">Culturia</h1><div class="tagline">Arrêtez de scroller, commencez à vous cultiver.</div></div>', unsafe_allow_html=True)

if st.session_state.page == "Recherche":
    page_recherche(st.session_state.num_articles)
elif st.session_state.page == "Parcourir":
    page_generale(st.session_state.num_articles)