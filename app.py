import streamlit as st
import requests
from fuzzywuzzy import fuzz, process

# ================= CONFIG =================
GNEWS_API_KEY = "7d4dac92369bac5d8cd91e547bef9f54"

# ================= GNEWS =================
class GNewsClient:
    def __init__(self):
        self.api_key = GNEWS_API_KEY
    
    def search_news(self, query):
        try:
            url = "https://gnews.io/api/v4/search"
            params = {
                "q": query,
                "lang": "fr", 
                "max": 3,
                "apikey": self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("articles", [])
            return []
        except Exception as e:
            return []

gnews = GNewsClient()

# ================= DÉTECTION INTELLIGENTE AVEC FUZZY MATCHING =================
def detecter_sujet_actualites(question):
    question = question.lower().strip()
    
    # DICTIONNAIRE ÉNORME AVEC FAUTES COURANTES
    mots_cles = {
        "football": [
            # Variations football
            "foot", "football", "foutball", "fout", "fouballe", "fouteballe", "fouteball",
            "soccer", "ballon", "match", "but", "goal", "stade", "terrain",
            # Clubs français
            "psg", "paris saint germain", "paris sg", "psj", "p s g",
            "om", "olympique marseille", "marseille", "l'om",
            "ol", "olympique lyonnais", "lyon", "l'ol",
            "as monaco", "monaco", "as m", 
            "lille", "losc", "nice", "rennes", "saint etienne", "asse",
            # Clubs européens
            "real madrid", "real", "barcelone", "barça", "barca", "fc barcelone",
            "manchester united", "man u", "manchester utd", "man united",
            "chelsea", "liverpool", "liverpool fc", "arsenal", "manchester city", "man city",
            "juventus", "juve", "bayern", "bayern munich", "inter", "ac milan", "milan",
            # Compétitions
            "ligue 1", "ligue un", "ligue1", "ligue une", "ligue1", "l1",
            "champions league", "ligue des champions", "ldc", "ucl",
            "europa league", "ligue europa", "conference league",
            "coupe de france", "cdf", "coupe du monde", "mondial", "world cup",
            "euro", "euro 2024", "qualif", "qualification",
            # Joueurs
            "mbappé", "mbappe", "kylian", "kylian mbappé",
            "dembélé", "dembele", "ousmane", "ousmane dembélé",
            "mess", "messi", "lionel", "lionel messi",
            "ronaldo", "cristiano", "cristiano ronaldo", "cr7",
            "benzema", "karim", "karim benzema",
            "neymar", "neymar jr",
            "haaland", "erling", "erling haaland",
            "griezmann", "antoine", "antoine griezmann",
            "pogba", "paul pogba", "kanté", "kante", "ngolo kanté",
            "giroud", "olivier giroud", "thuram", "marcus thuram"
        ],
        "musique": [
            # Variations musique
            "musique", "muzik", "musik", "muzique", "musiq", "music", 
            "chanson", "chansons", "son", "sons", "titre", "titres", "morceau", "morceaux",
            "album", "albums", "ep", "mixtape", "playlist",
            "artiste", "artistes", "chanteur", "chanteurs", "chanteuse", "chanteuses",
            "rappeur", "rappeurs", "rappeuse", "rappeuses", "slammeur", "slammeuse",
            "concert", "concerts", "show", "shows", "performance", "live",
            "festival", "festivals", "coachella", "woodsht", "hellfest", "solidays",
            # Genres musicaux
            "rap", "hip hop", "hiphop", "rnb", "r&b", "r and b",
            "variété", "variete", "variété française", "vf",
            "pop", "rock", "electro", "électro", "house", "techno", "jazz", "classique",
            "reggae", "metal", "punk", "blues", "soul", "funk", "disco",
            # Artistes
            "zola", "zola musique", " Jul ", "juL", "nia", "ninho", "ninHo", 
            "pnl", "p n l", "damso", "orelsan", "lomepal", "nekfeu",
            "angele", "stromae", "indila", "christine and the queens",
            "david guetta", "guetta", "dj snake", "martin solveig",
            # Plateformes
            "streaming", "spotify", "deezer", "apple music", "youtube music", "yt music",
            "soundcloud", "napster", "tidal", "amazon music"
        ],
        "jeux_video": [
            # Variations jeux vidéo
            "jeu", "jeux", "video", "vidéo", "gaming", "game", "gamer", "jouer",
            "jeux vidéos", "jeux videos", "jeu video", "jeu vidéo", "jv",
            "playstation", "ps", "ps4", "ps5", "play station", "sony",
            "xbox", "x box", "xbox series x", "xbox series s", "microsoft",
            "nintendo", "switch", "nintendo switch", "wii", "gameboy", "ds",
            "pc gaming", "pc gamer", "ordinateur", "steam", "epic games", "ubisoft",
            "esport", "e-sport", "esports", "competitive gaming",
            "streamer", "stream", "twitch", "youtube gaming", "youtubeur gaming",
            # Jeux populaires
            "fortnite", "minecraft", "gta", "grand theft auto", "gtav", "gta v",
            "call of duty", "cod", "warzone", "modern warfare",
            "fifa", "ea sports fc", "fc 26", "pro evolution soccer", "pes",
            "assassin's creed", "assassin creed", "ac valhalla",
            "zelda", "legend of zelda", "tears of the kingdom", "breath of the wild",
            "mario", "super mario", "mario kart", "pokemon", "pokémon",
            "league of legends", "lol", "dota", "dota 2",
            "counter strike", "cs", "csgo", "cs:go", "valorant",
            "world of warcraft", "wow", "final fantasy", "ffxiv"
        ],
        "technologie": [
            "tech", "technologie", "technologies", "high tech", "high-tech",
            "ia", "intelligence artificielle", "ai", "artificial intelligence",
            "chatgpt", "gpt", "openai", "midjourney", "dalle",
            "apple", "iphone", "ipad", "mac", "macbook", "ios", "macos",
            "google", "android", "pixel", "chrome", "youtube",
            "meta", "facebook", "instagram", "whatsapp", "threads",
            "microsoft", "windows", "surface", "xbox", "linkedin",
            "amazon", "alexa", "prime", "aws",
            "tesla", "elon musk", "spacex", "neuralink",
            "samsung", "galaxy", "smartphone", "telephone", "mobile",
            "ordinateur", "pc", "laptop", "tablette", "tablet",
            "internet", "web", "reseau", "réseau", "wifi", "5g", "fibre"
        ]
    }
    
    # 1. RECHERCHE EXACTE RAPIDE
    for sujet, mots in mots_cles.items():
        for mot in mots:
            if mot in question:
                return sujet, mot
    
    # 2. FUZZY MATCHING POUR LES FAUTES
    tous_mots_cles = []
    for sujet, mots in mots_cles.items():
        for mot in mots:
            tous_mots_cles.append((mot, sujet))
    
    meilleur_match, score = process.extractOne(question, [mot for mot, sujet in tous_mots_cles])
    
    # Seuil ajustable : 65% pour être très tolérant
    if score > 65:
        for mot, sujet in tous_mots_cles:
            if mot == meilleur_match:
                return sujet, meilleur_match
    
    return "general", question

# ================= BASES DE CONNAISSANCES =================
SPORT = {
    "ballon dor 2023": "Lionel Messi a remporté le Ballon d'Or 2023",
    "jo 2024": "Les Jeux Olympiques 2024 à Paris : 26 juillet - 11 août 2024",
    "coupe du monde 2022": "Argentine championne contre la France (3-3, 4-2 t.a.b)"
}

MUSIQUE = {
    "zola": "Zola a gagné le prix de l'Album Révélation aux Victoires 2024",
    "victoires 2024": "Cérémonie des Victoires de la Musique 2024 en février"
}

JEUX = {
    "goty 2023": "Baldur's Gate 3 a été élu Jeu de l'Année 2023 aux Game Awards",
    "gta 6": "GTA VI est annoncé pour 2025 par Rockstar Games"
}

# ================= IA INTELLIGENTE =================
def trouver_reponse(question):
    question_lower = question.lower()
    
    # 1. RÈGLES FIXES EXISTANTES
    if "ballon" in question_lower: return f"🏆 {SPORT['ballon dor 2023']}"
    if "jo" in question_lower: return f"🎯 {SPORT['jo 2024']}"
    if "zola" in question_lower: return f"🎵 {MUSIQUE['zola']}"
    if "goty" in question_lower: return f"🎮 {JEUX['goty 2023']}"
    if "gta" in question_lower: return f"🚗 {JEUX['gta 6']}"
    
    # 2. DÉTECTION INTELLIGENTE POUR ACTUALITÉS
    sujet, mot_cle = detecter_sujet_actualites(question)
    
    if sujet != "general" or any(mot in question_lower for mot in ["actualité", "news", "actu", "nouvelle"]):
        recherche = mot_cle if sujet != "general" else question
        articles = gnews.search_news(recherche)
        
        if articles:
            reponse = f"📰 **Actualités {sujet.replace('_', ' ')} :**\n\n"
            for i, article in enumerate(articles):
                reponse += f"**{i+1}. {article['title']}**\n"
                if article['description']:
                    reponse += f"{article['description'][:150]}...\n"
                reponse += f"[📖 Lire la suite]({article['url']})\n\n"
            return reponse
        return f"📰 Aucune actualité trouvée sur '{recherche}'"
    
    return "🤔 Je n'ai pas encore la réponse. Essayez 'actualité [sujet]' !"

# ================= INTERFACE =================
st.set_page_config(page_title="Mon IA", page_icon="🤖", layout="wide")
st.title("🤖 MON ASSISTANT IA INTELLIGENT")
st.write("**Sport 🏆 • Musique 🎵 • Jeux Vidéo 🎮 • Technologie 💻 • Actualité 🌍**")

# Zone de chat
question = st.text_input("🎯 **Pose ta question :**", placeholder="Ex: football, musique, om, ligue 1, jeux vidéos...")

if question:
    with st.spinner("🔍 Je recherche la réponse..."):
        reponse = trouver_reponse(question)
    
    st.success("✅ **Réponse :**")
    st.info(reponse)

# Section démo
st.divider()
st.write("💡 **Exemples à tester (avec fautes) :**")
col1, col2, col3 = st.columns(3)

with col1:
    st.code("""
foutball
ligue un  
psj
messi
    """)

with col2:
    st.code("""
muzik
rap
zola
concert
    """)

with col3:
    st.code("""
jeu video
gta 6
playstation
fortnite
    """)