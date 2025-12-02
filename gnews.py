import requests
from datetime import datetime
from config import GNEWS_API_KEY

def get_news(keywords_dict, max_articles=20):
    #Interroge l'API GNews en utilisant une recherche "AND" sur les mots-clés principaux.
    if not keywords_dict or not keywords_dict.get("principal"):
        return []
    
    mots_principaux = keywords_dict["principal"]
    query = " AND ".join(f'"{word}"' for word in mots_principaux)
    
    try:
        url = "https://gnews.io/api/v4/search"
        params = {"q": query, "lang": "fr", "max": max_articles, "apikey": GNEWS_API_KEY}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        formatted_articles = []
        for art in articles:
            date_obj = datetime.strptime(art["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            formatted_articles.append({
                "titre": art["title"],
                "description": art["description"] or "Pas de description disponible.",
                "date": date_obj.strftime("%Y-%m-%d %H:%M"),
                "theme": ", ".join(mots_principaux),
                "url": art["url"],
                "contenu_complet": None,
                "image": art.get("image", None)
            })
        return formatted_articles
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API GNews : {e}")
        return []