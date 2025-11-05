import streamlit as st

st.set_page_config(page_title="Mon IA", page_icon="🤖")
st.title("🤖 MON ASSISTANT IA")
st.write("**Spécialiste : Sport 🏆 • Musique 🎵 • Jeux Vidéo 🎮 • Actualité 🌍**")

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
    question = question.lower()
    
    # Sport
    if "ballon" in question: return f"🏆 {SPORT['ballon dor 2023']}"
    if "jo" in question or "olympique" in question: return f"🎯 {SPORT['jo 2024']}"
    if "coupe du monde" in question: return f"⚽ {SPORT['coupe du monde 2022']}"
    
    # Musique
    if "zola" in question: return f"🎵 {MUSIQUE['zola']}"
    if "victoire" in question: return f"🏆 {MUSIQUE['victoires 2024']}"
    
    # Jeux vidéo
    if "goty" in question or "jeu de l'année" in question: return f"🎮 {JEUX['goty 2023']}"
    if "gta" in question: return f"🚗 {JEUX['gta 6']}"
    
    return "🤔 Je n'ai pas encore la réponse à cette question. Je m'améliore chaque jour !"

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