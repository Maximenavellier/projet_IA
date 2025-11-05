import streamlit as st
import requests

st.set_page_config(page_title="Mon IA", page_icon="🤖")
st.title("🤖 MON ASSISTANT IA")
st.write("**Spécialiste : Sport 🏆 • Musique 🎵 • Jeux Vidéo 🎮 • Actualité 🌍**")

# --- CONFIGURATION GNEWS ---
GNEWS_API_KEY = "7d4dac92369bac5d8cd91e547bef9f54"

class GnewsClient:
    def __init__(self):
        self.api_key = GNEWS_API_KEY

    def search_news(self, query, max_results=3):
        """Recherche des actualités avec Gnews"""
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": query,
                "lang": "fr",
                "max": max_results,
                "apikey": self.api_key
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                return articles
            return []
        except Exception as e:
            st.error(f"Erreur GNews: {e}")
            return []
        
# Initialiser le client GNews
gnews = GnewsClient()


# BASES DE CONNAISSANCES
SPORT = {
    "ballon dor 2023": "Lionel Messi a remporté le Ballon d'Or 2023",
    "jo 2024": "Les Jeux Olympiques 2024 à Paris : 26 juillet - 11 août 2024",
    "coupe du monde 2022": "Argentine championne contre la France"
}

MUSIQUE = {
    "zola": "Zola a gagné le prix de l'Album Révélation aux Victoires 2024",
    "victoires 2024": "Cérémonie des Victoires de la Musique 2024 en février"
}

JEUX = {
    "goty 2023": "Baldur's Gate 3 a été élu Jeu de l'Année 2023",
    "gta 6": "GTA VI est annoncé pour 2025"
}

# FONCTION DE RECHERCHE
def trouver_reponse(question):
    question_lower = question.lower()
    
    # TES RÈGLES EXISTANTES (Sport, Musique, Jeux)
    if "ballon" in question_lower: return f"🏆 {SPORT['ballon dor 2023']}"
    if "jo" in question_lower: return f"🎯 {SPORT['jo 2024']}"
    if "goty" in question_lower: return f"🎮 {JEUX['goty 2023']}"
    # ... [tes autres règles]
    
    # NOUVEAU : RECHERCHE D'ACTUALITÉS
    if any(mot in question_lower for mot in ["actualité", "news", "actu", "nouvelle", "information"]):
        mots_cles = question_lower
        articles = gnews.search_news(mots_cles)
        
        if articles:
            reponse = "📰 **Actualités récentes :**\n\n"
            for i, article in enumerate(articles[:2]):  # 2 premiers articles
                reponse += f"**{i+1}. {article['title']}**\n"
                reponse += f"{article['description']}\n"
                reponse += f"[Lire la suite]({article['url']})\n\n"
            return reponse
        else:
            return "📰 Aucune actualité trouvée pour le moment."
    
    return "🤔 Je n'ai pas encore la réponse à cette question."

# INTERFACE
question = st.text_input("🎯 **Pose ta question :**")

if question:
    with st.spinner("🔍 Je recherche la réponse..."):
        reponse = trouver_reponse(question)
    
    st.success("✅ **Réponse :**")
    st.info(reponse)

# EXEMPLES DE QUESTIONS
st.divider()
st.write("💡 **Exemples à tester :**")
st.code("- ballon d'or 2023\n- JO 2024\n- GOTY 2023\n- Zola victoires\n- GTA 6")