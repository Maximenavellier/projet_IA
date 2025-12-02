import re
from newspaper import Article
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import STOP_WORDS

def scrape_article_content(url):
    #Utilise newspaper3k pour extraire le contenu complet d'un article.
    try:
        article = Article(url, language='fr')
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Erreur lors du scraping de {url}: {e}")
        return None

def scrape_articles_parallel(articles, max_workers=5):
    """Scrape le contenu complet de plusieurs articles en parallèle."""
    def scrape_single(article):
        content = scrape_article_content(article['url'])
        article['contenu_complet'] = content if content else article['description']
        return article
    
    scraped_articles = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scrape_single, art): art for art in articles}
        for future in as_completed(futures):
            try:
                scraped_articles.append(future.result())
            except Exception as e:
                print(f"Erreur lors du scraping: {e}")
                scraped_articles.append(futures[future])
    return scraped_articles

def get_search_query(question):
    #Nettoie la question de l'utilisateur pour ne garder que les mots-clés pertinents.
    question_lower = question.lower().strip()
    words = re.split(r'\W+', question_lower)
    meaningful_words = [word for word in words if word and word not in STOP_WORDS]
    
    if not meaningful_words:
        return {"principal": [question], "secondaire": []}
    
    mots_secondaires = {"vues", "nombre", "combien", "dernier", "dernière", "nouveau", "nouvelle", "récent", "récente", "sorti", "sortie", "annonce", "annoncé", "fait"}
    mots_principaux = [word for word in meaningful_words if word not in mots_secondaires]
    mots_contexte = [word for word in meaningful_words if word in mots_secondaires]
    
    if not mots_principaux:
        mots_principaux = mots_contexte
        mots_contexte = []
        
    return {"principal": mots_principaux, "secondaire": mots_contexte}