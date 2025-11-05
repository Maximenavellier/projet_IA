import streamlit as st
import re
import time
from datetime import datetime
import json
import os

# --- Configuration de la Page ---
st.set_page_config(
    page_title="Mon IA",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 MON ASSISTANT IA")
st.write("**Spécialiste : Sport 🏆 • Musique 🎵 • Jeux Vidéo 🎮 • Actualité 🌍**")

# --- Base de Données ---
# NOTE: Pour une application plus grande, il serait préférable de charger ces données depuis un fichier externe (ex: JSON).
BASE_DE_DONNEES = [
    # Sport
    {"titre": "Lionel Messi remporte le Ballon d'Or 2023", "date": "2023-10-30", "theme": "Sport", "description": "L'Argentin Lionel Messi a été sacré Ballon d'Or pour la huitième fois, un record absolu dans l'histoire du football. Cette récompense vient couronner une carrière exceptionnelle et sa victoire en Coupe du Monde 2022 avec l'Argentine."},
    {"titre": "Messi sacré Ballon d'Or 2023 : une huitième étoile pour la légende", "date": "2023-10-30", "theme": "Sport", "description": "Lionel Messi a remporté son huitième Ballon d'Or, consolidant sa place comme le plus grand joueur de football de tous les temps. Malgré une saison en demi-teinte avec le PSG, sa victoire en Coupe du Monde a pesé lourd dans la balance."},
    {"titre": "Les Jeux Olympiques de Paris 2024", "date": "2024-07-26", "theme": "Sport", "description": "Les JO 2024 se tiendront à Paris du 26 juillet au 11 août. La cérémonie d'ouverture, prévue sur la Seine, s'annonce spectaculaire. De nouvelles épreuves comme le breaking feront leur apparition, tandis que des sites emblématiques de la capitale française accueilleront les compétitions."},
    {"titre": "Paris 2024 : la flamme olympique arrivera à Marseille le 8 mai", "date": "2024-05-08", "theme": "Sport", "description": "Le parcours de la flamme olympique pour les Jeux de Paris 2024 a été dévoilé. Elle arrivera à Marseille le 8 mai, avant de traverser toute la France jusqu'à la cérémonie d'ouverture le 26 juillet."},

    {"titre": "L'Argentine championne du monde de football 2022", "date": "2022-12-18", "theme": "Sport", "description": "Au terme d'une finale légendaire contre la France, l'Argentine de Lionel Messi a remporté la Coupe du Monde 2022 au Qatar. Le match s'est terminé sur un score de 3-3 après prolongations, avec un triplé de Kylian Mbappé, avant que l'Albiceleste ne s'impose aux tirs au but."},
    {"titre": "Coupe du Monde 2022 : le sacre de Messi et de l'Argentine", "date": "2022-12-18", "theme": "Sport", "description": "L'Argentine a remporté la Coupe du Monde 2022 face à la France dans un match épique. Lionel Messi a enfin décroché le titre qui manquait à son palmarès, entrant un peu plus dans la légende du football."},
    {"titre": "Record du monde du 100m par Usain Bolt", "date": "2009-08-16", "theme": "Sport", "description": "Usain Bolt détient toujours le record du monde du 100 mètres en 9,58 secondes, établi lors des championnats du monde d'athlétisme à Berlin. Cette performance reste l'un des exploits les plus marquants de l'histoire du sport."},
    {"titre": "Athlétisme : Usain Bolt, l'homme le plus rapide du monde", "date": "2009-08-16", "theme": "Sport", "description": "Le Jamaïcain Usain Bolt a marqué l'histoire de l'athlétisme en établissant de nouveaux records du monde sur 100m et 200m aux championnats du monde de Berlin. Sa vitesse et son charisme ont fasciné le monde entier."},
    {"titre": "La France championne du monde de handball 2023", "date": "2023-01-29", "theme": "Sport", "description": "L'équipe de France masculine de handball a remporté son septième titre de championne du monde en battant le Danemark en finale. Les Experts, menés par Nikola Karabatic, continuent de marquer l'histoire de leur sport."},
    {"titre": "Handball : les Bleus au sommet du monde pour la septième fois", "date": "2023-01-29", "theme": "Sport", "description": "L'équipe de France de handball a remporté son septième titre de championne du monde en dominant le Danemark en finale. Les Experts ont confirmé leur statut de meilleure équipe de l'histoire du handball."},
    {"titre": "Max Verstappen, triple champion du monde de F1", "date": "2023-10-07", "theme": "Sport", "description": "Le pilote néerlandais Max Verstappen a remporté son troisième titre consécutif de champion du monde de Formule 1 avec l'écurie Red Bull Racing. Sa domination sur la saison 2023 a été quasi totale, avec un nombre record de victoires."},
    {"titre": "F1 : Verstappen écrase la concurrence et remporte un troisième titre", "date": "2023-10-07", "theme": "Sport", "description": "Max Verstappen a dominé la saison de Formule 1 2023, remportant son troisième titre de champion du monde avec une avance considérable sur ses concurrents. Sa maîtrise et la performance de sa Red Bull ont été impressionnantes."},
    {"titre": "Novak Djokovic dépasse le record de titres en Grand Chelem", "date": "2023-06-11", "theme": "Sport", "description": "En remportant Roland-Garros 2023, le serbe Novak Djokovic a remporté son 23ème titre du Grand Chelem, dépassant ainsi Rafael Nadal et établissant un nouveau record chez les hommes dans l'histoire du tennis."},
    {"titre": "Tennis : Djokovic entre dans l'histoire avec un 23ème Grand Chelem", "date": "2023-06-11", "theme": "Sport", "description": "Novak Djokovic a remporté Roland-Garros 2023, son 23ème titre du Grand Chelem, dépassant ainsi le record de Rafael Nadal. Le Serbe continue de repousser les limites de son sport."},
    {"titre": "L'Afrique du Sud gagne la Coupe du Monde de Rugby 2023", "date": "2023-10-28", "theme": "Sport", "description": "Les Springboks d'Afrique du Sud ont remporté la Coupe du Monde de Rugby 2023 en France, en battant la Nouvelle-Zélande en finale. C'est leur quatrième titre mondial, un record."},
    {"titre": "Rugby : l'Afrique du Sud conserve son titre de championne du monde", "date": "2023-10-28", "theme": "Sport", "description": "L'Afrique du Sud a remporté la Coupe du Monde de Rugby 2023 en battant la Nouvelle-Zélande dans une finale serrée. Les Springboks ont confirmé leur statut de nation dominante du rugby mondial."},
    {"titre": "Les Denver Nuggets champions NBA pour la première fois", "date": "2023-06-12", "theme": "Sport", "description": "Portés par un Nikola Jokic exceptionnel, élu MVP des finales, les Denver Nuggets ont remporté le premier titre NBA de leur histoire en battant le Miami Heat."},
    {"titre": "NBA : les Nuggets de Denver enfin champions avec Jokic", "date": "2023-06-12", "theme": "Sport", "description": "Les Denver Nuggets ont remporté leur premier titre NBA en battant le Miami Heat en finale. Nikola Jokic a été élu MVP des finales, couronnant une saison exceptionnelle."},
    {"titre": "Le Tour de France 2023 remporté par Jonas Vingegaard", "date": "2023-07-23", "theme": "Sport", "description": "Le cycliste danois Jonas Vingegaard a remporté son deuxième Tour de France consécutif après un duel intense avec le slovène Tadej Pogacar. Sa performance dans les Alpes a été décisive."},
    {"titre": "Cyclisme : Vingegaard triomphe sur le Tour de France pour la deuxième fois", "date": "2023-07-23", "theme": "Sport", "description": "Jonas Vingegaard a remporté le Tour de France 2023, dominant Tadej Pogacar dans les étapes de montagne. Le Danois a confirmé son statut de meilleur grimpeur du monde."},
    {"titre": "L'Espagne remporte la Coupe du Monde féminine de football 2023", "date": "2023-08-20", "theme": "Sport", "description": "L'équipe nationale espagnole a été sacrée championne du monde pour la première fois de son histoire en battant l'Angleterre 1-0 en finale. Ce tournoi a connu un succès populaire et médiatique sans précédent pour le football féminin."},
    {"titre": "Football féminin : l'Espagne championne du monde pour la première fois", "date": "2023-08-20", "theme": "Sport", "description": "L'Espagne a remporté la Coupe du Monde féminine de football 2023 en battant l'Angleterre en finale. Ce titre marque une étape importante pour le développement du football féminin en Espagne et dans le monde."},
    {"titre": "Teddy Riner, onzième titre de champion du monde de judo", "date": "2023-05-13", "theme": "Sport", "description": "Le judoka français Teddy Riner a conquis son onzième titre de champion du monde dans la catégorie des plus de 100 kg, à Doha. Un exploit qui le place encore un peu plus au panthéon de son sport, à un an des JO de Paris."},
    {"titre": "Judo : Teddy Riner invincible, sacré champion du monde pour la onzième fois", "date": "2023-05-13", "theme": "Sport", "description": "Teddy Riner a remporté son onzième titre de champion du monde de judo, confirmant sa domination inégalée dans sa catégorie. Le Français vise désormais les Jeux Olympiques de Paris 2024."},
    {"titre": "Le phénomène Victor Wembanyama en NBA", "date": "2023-06-22", "theme": "Sport", "description": "Le jeune prodige français Victor Wembanyama a été drafté en première position par les San Antonio Spurs. Son arrivée en NBA est l'une des plus attendues de l'histoire, en raison de sa taille et de ses compétences uniques."},
    {"titre": "NBA : Victor Wembanyama, le basketteur français qui affole l'Amérique", "date": "2023-06-22", "theme": "Sport", "description": "Victor Wembanyama, jeune basketteur français, a été sélectionné en première position de la draft NBA par les San Antonio Spurs. Son talent exceptionnel et sa taille impressionnante suscitent un engouement sans précédent."},
    {"titre": "Manchester City réalise un triplé historique", "date": "2023-06-10", "theme": "Sport", "description": "L'équipe de Manchester City, entraînée par Pep Guardiola, a réalisé un triplé historique en remportant la Premier League, la FA Cup et sa toute première Ligue des Champions lors de la saison 2022-2023."},
    {"titre": "Football : Manchester City entre dans l'histoire avec un triplé", "date": "2023-06-10", "theme": "Sport", "description": "Manchester City a réalisé une saison exceptionnelle en remportant la Premier League, la FA Cup et la Ligue des Champions. L'équipe de Pep Guardiola a marqué l'histoire du football anglais."},
    {"titre": "Kylian Mbappé devient le meilleur buteur de l'histoire du PSG", "date": "2023-03-04", "theme": "Sport", "description": "En marquant son 201ème but, Kylian Mbappé a dépassé Edinson Cavani pour devenir le meilleur buteur de tous les temps du Paris Saint-Germain. Une performance réalisée en seulement six saisons au club."},
    {"titre": "PSG : Mbappé dépasse Cavani et devient le meilleur buteur de l'histoire du club", "date": "2023-03-04", "theme": "Sport", "description": "Kylian Mbappé a dépassé Edinson Cavani pour devenir le meilleur buteur de l'histoire du Paris Saint-Germain. Le jeune attaquant français continue d'impressionner par son talent et son efficacité."},

    # Musique
    {"titre": "Gazo & Tiakola remportent les Victoires de la Musique 2024", "date": "2024-02-09", "theme": "Musique", "description": "Les rappeurs Gazo et Tiakola ont été les grands gagnants des Victoires de la Musique 2024, remportant plusieurs prix dont celui de l'artiste masculin de l'année. Leur succès confirme la place prépondérante du rap dans le paysage musical français."},
    {"titre": "Victoires de la Musique 2024 : triomphe pour Gazo et Tiakola", "date": "2024-02-09", "theme": "Musique", "description": "Gazo et Tiakola ont dominé la cérémonie des Victoires de la Musique 2024, remportant plusieurs récompenses. Leur succès témoigne de l'influence croissante du rap dans la musique française."},
    {"titre": "Sortie de l'album 'Midnights' de Taylor Swift", "date": "2022-10-21", "theme": "Musique", "description": "Taylor Swift a battu des records de streaming avec son dixième album studio, 'Midnights'. L'album, qui explore des thèmes nocturnes et introspectifs, a été acclamé par la critique et a dominé les classements mondiaux pendant des semaines."},
    {"titre": "Taylor Swift bat tous les records avec son nouvel album 'Midnights'", "date": "2022-10-21", "theme": "Musique", "description": "Taylor Swift a sorti son dixième album studio, 'Midnights', qui a battu des records de streaming en quelques jours. L'album explore des thèmes personnels et a été salué par les fans et la critique."},
    {"titre": "Daft Punk annonce sa séparation", "date": "2021-02-22", "theme": "Musique", "description": "Le duo iconique de la musique électronique française, Daft Punk, a annoncé sa séparation après 28 ans de carrière via une vidéo intitulée 'Epilogue'. Cette annonce a provoqué une onde de choc mondiale parmi les fans et l'industrie musicale."},
    {"titre": "Daft Punk : fin d'une légende de la musique électronique", "date": "2021-02-22", "theme": "Musique", "description": "Le groupe Daft Punk a annoncé sa séparation après 28 ans de carrière. Le duo français a marqué l'histoire de la musique électronique avec ses albums emblématiques et ses performances visuelles spectaculaires."},
    {"titre": "Le festival de Coachella 2024", "date": "2024-04-12", "theme": "Musique", "description": "L'édition 2024 du festival de Coachella, en Californie, a vu des performances mémorables de Lana Del Rey, Tyler, the Creator et Doja Cat en têtes d'affiche. Le festival reste un rendez-vous incontournable pour la musique et les tendances."},
    {"titre": "Coachella 2024 : un festival haut en couleurs avec Lana Del Rey, Tyler, the Creator et Doja Cat", "date": "2024-04-12", "theme": "Musique", "description": "Le festival de Coachella 2024 a été marqué par les performances de Lana Del Rey, Tyler, the Creator et Doja Cat. Le festival a attiré des milliers de fans et a été un événement majeur pour la musique et la mode."},
    {"titre": "Rosalía remporte un Grammy pour 'Motomami'", "date": "2023-02-05", "theme": "Musique", "description": "L'artiste espagnole Rosalía a gagné le Grammy du meilleur album de rock ou de musique alternative latine pour son projet innovant 'Motomami'. L'album est salué pour sa fusion audacieuse de flamenco, de reggaeton et de sons expérimentaux."},
    {"titre": "Rosalía récompensée aux Grammy Awards pour son album 'Motomami'", "date": "2023-02-05", "theme": "Musique", "description": "Rosalía a remporté le Grammy Award du meilleur album de rock ou de musique alternative latine pour son album 'Motomami'. L'artiste espagnole a été saluée pour son approche novatrice et sa fusion des genres musicaux."},
    {"titre": "Le succès de la tournée 'The Eras Tour' de Taylor Swift", "date": "2023-03-17", "theme": "Musique", "description": "La tournée mondiale 'The Eras Tour' de Taylor Swift est devenue un phénomène culturel et économique, battant des records de vente de billets. Chaque concert, d'une durée de plus de trois heures, retrace l'ensemble de sa carrière musicale."},
    {"titre": "Taylor Swift : sa tournée 'The Eras Tour' bat tous les records", "date": "2023-03-17", "theme": "Musique", "description": "La tournée 'The Eras Tour' de Taylor Swift est devenue la plus lucrative de l'histoire de la musique. La chanteuse américaine a attiré des millions de fans à travers le monde et a généré des revenus considérables."},
    {"titre": "Beyoncé sort l'album 'Renaissance'", "date": "2022-07-29", "theme": "Musique", "description": "Avec son album 'Renaissance', Beyoncé rend hommage aux pionniers noirs de la house et de la disco. L'album a été universellement salué pour sa production audacieuse et son énergie festive, remportant plusieurs Grammy Awards."},
    {"titre": "Beyoncé : son album 'Renaissance' célèbre la culture house et disco", "date": "2022-07-29", "theme": "Musique", "description": "Beyoncé a sorti son album 'Renaissance', un hommage à la culture house et disco. L'album a été salué pour son énergie positive et ses influences musicales variées."},
    {"titre": "Le retour de PNL avec un nouveau single", "date": "2024-11-20", "theme": "Musique", "description": "Après des années de silence, le duo de rap français PNL (Peace N' Lovés) a fait un retour surprise avec un nouveau single qui a immédiatement dominé les plateformes de streaming. Leur communication mystérieuse continue de fasciner leur large base de fans."},
    {"titre": "PNL : le groupe de rap français fait son grand retour", "date": "2024-11-20", "theme": "Musique", "description": "Le groupe de rap PNL a fait son retour avec un nouveau single après plusieurs années d'absence. Le duo français a immédiatement dominé les classements et a suscité l'enthousiasme de ses fans."},
    {"titre": "Orelsan remplit La Défense Arena pour un concert historique", "date": "2022-12-10", "theme": "Musique", "description": "Le rappeur caennais Orelsan a conclu sa tournée 'Civilisation Tour' par un concert monumental à Paris La Défense Arena devant 40 000 personnes, confirmant son statut d'artiste majeur de la scène française."},
    {"titre": "Orelsan : un concert exceptionnel à La Défense Arena", "date": "2022-12-10", "theme": "Musique", "description": "Orelsan a donné un concert mémorable à La Défense Arena, réunissant 40 000 spectateurs. Le rappeur français a confirmé son statut d'artiste majeur de la scène musicale française."},
    {"titre": "Le phénomène K-Pop Blackpink à Coachella", "date": "2023-04-15", "theme": "Musique", "description": "Le groupe de K-Pop Blackpink est devenu le premier groupe coréen à être tête d'affiche du célèbre festival Coachella. Leur performance a été saluée comme un moment historique pour la représentation de la musique asiatique sur la scène mondiale."},
    {"titre": "Blackpink : le groupe de K-Pop enflamme Coachella", "date": "2023-04-15", "theme": "Musique", "description": "Le groupe de K-Pop Blackpink a été l'une des têtes d'affiche du festival de Coachella. Leur performance a été saluée comme un moment historique pour la musique coréenne."},
    {"titre": "Sortie de l'album 'Utopia' de Travis Scott", "date": "2023-07-28", "theme": "Musique", "description": "Très attendu, l'album 'Utopia' du rappeur américain Travis Scott a connu un succès commercial massif. L'album se distingue par ses productions complexes et ses nombreuses collaborations prestigieuses, notamment avec Beyoncé, Drake et The Weeknd."},
    {"titre": "Travis Scott : son album 'Utopia' est un succès planétaire", "date": "2023-07-28", "theme": "Musique", "description": "Travis Scott a sorti son album 'Utopia', qui a connu un succès commercial important. L'album a été salué pour ses productions innovantes et ses collaborations prestigieuses."},
    {"titre": "Le succès de l'album 'Sincèrement' de Hamza", "date": "2023-02-17", "theme": "Musique", "description": "Le rappeur belge Hamza a connu un grand succès avec son album 'Sincèrement', qui a été certifié double disque de platine. L'album est porté par des mélodies accrocheuses et des collaborations efficaces, notamment avec Damso."},
    {"titre": "Hamza : son album 'Sincèrement' certifié double platine", "date": "2023-02-17", "theme": "Musique", "description": "Hamza a connu un grand succès avec son album 'Sincèrement', qui a été certifié double disque de platine. Le rappeur belge a confirmé son statut d'artiste majeur de la scène rap francophone."},
    {"titre": "Le Hellfest, plus grand festival de metal de France", "date": "2024-06-27", "theme": "Musique", "description": "Le Hellfest, situé à Clisson, continue de s'imposer comme l'un des plus grands festivals de musiques extrêmes au monde. L'édition 2024 a rassemblé des centaines de milliers de fans avec des têtes d'affiche comme Metallica et Foo Fighters."},
    {"titre": "Hellfest 2024 : le festival metal incontournable en France", "date": "2024-06-27", "theme": "Musique", "description": "Le Hellfest a rassemblé des centaines de milliers de fans de metal à Clisson. L'édition 2024 a été marquée par les performances de Metallica et Foo Fighters."},
    {"titre": "L'album posthume de Johnny Hallyday", "date": "2021-10-22", "theme": "Musique", "description": "Un album posthume de Johnny Hallyday, intitulé 'Made in Rock'n'Roll', a été publié, contenant des enregistrements inédits. Les fans ont répondu présents, propulsant l'album en tête des ventes et prouvant que l'idole des jeunes reste inoubliable."},
    {"titre": "Johnny Hallyday : un album posthume pour faire revivre la légende", "date": "2021-10-22", "theme": "Musique", "description": "Un album posthume de Johnny Hallyday est sorti, contenant des chansons inédites. Les fans ont répondu présents et ont propulsé l'album en tête des ventes."},
    {"titre": "Billie Eilish et son engagement pour le climat", "date": "2022-08-01", "theme": "Musique", "description": "La jeune star de la pop Billie Eilish utilise sa notoriété pour promouvoir la cause environnementale. Sa tournée mondiale 'Happier Than Ever' a été conçue pour être la plus écologique possible, en partenariat avec l'organisation Reverb."},
    {"titre": "Billie Eilish : une artiste engagée pour la planète", "date": "2022-08-01", "theme": "Musique", "description": "Billie Eilish utilise sa notoriété pour sensibiliser le public aux problèmes environnementaux. Sa tournée 'Happier Than Ever' a été conçue pour minimiser son impact sur la planète."},

    # Jeux Vidéo
    {"titre": "Baldur's Gate 3 élu Jeu de l'Année (GOTY) 2023", "date": "2023-12-07", "theme": "Jeux Vidéo", "description": "Le RPG Baldur's Gate 3 du studio Larian a triomphé aux Game Awards 2023, remportant le prix suprême de Jeu de l'Année (GOTY). Le jeu est salué pour sa narration profonde, sa liberté d'action et la richesse de son univers inspiré de Donjons & Dragons."},
    {"titre": "Baldur's Gate 3 : le RPG qui a conquis le monde du jeu vidéo", "date": "2023-12-07", "theme": "Jeux Vidéo", "description": "Baldur's Gate 3 a été élu Jeu de l'Année aux Game Awards 2023. Le jeu a été salué pour son histoire complexe, ses personnages attachants et son gameplay immersif."},
    {"titre": "Annonce de la sortie de GTA 6 pour 2025", "date": "2023-12-05", "theme": "Jeux Vidéo", "description": "Rockstar Games a officiellement annoncé que Grand Theft Auto VI (GTA 6) sortira en 2025. La première bande-annonce a battu des records de vues sur YouTube, révélant un retour à Vice City et un duo de protagonistes, dont une femme pour la première fois."},
    {"titre": "GTA 6 : Rockstar Games dévoile la première bande-annonce", "date": "2023-12-05", "theme": "Jeux Vidéo", "description": "Rockstar Games a dévoilé la première bande-annonce de Grand Theft Auto VI (GTA 6). La bande-annonce a confirmé le retour à Vice City et a présenté les deux personnages principaux du jeu."},
    {"titre": "Le succès phénoménal de Palworld", "date": "2024-01-19", "theme": "Jeux Vidéo", "description": "Le jeu de survie avec des créatures, Palworld, a connu un lancement explosif en 2024, se vendant à des millions d'exemplaires en quelques jours. Son mélange de crafting, d'exploration et de capture de 'Pals' a créé un buzz mondial, malgré les controverses sur ses similitudes avec Pokémon."},
    {"titre": "Palworld : le jeu qui mélange Pokémon et survie fait sensation", "date": "2024-01-19", "theme": "Jeux Vidéo", "description": "Palworld a connu un lancement réussi grâce à son mélange de Pokémon et de survie. Le jeu a attiré des millions de joueurs et a suscité des débats sur ses similitudes avec la franchise Pokémon."},
    {"titre": "Nintendo annonce la successeure de la Switch", "date": "2024-05-07", "theme": "Jeux Vidéo", "description": "Le président de Nintendo a confirmé qu'une nouvelle console, successeur de la populaire Switch, sera annoncée officiellement avant la fin de l'année fiscale en mars 2025. Les rumeurs évoquent une puissance accrue tout en conservant un concept hybride salon/portable."},
    {"titre": "Nintendo : une nouvelle console Switch en préparation", "date": "2024-05-07", "theme": "Jeux Vidéo", "description": "Nintendo a annoncé qu'une nouvelle console Switch était en préparation. La console devrait être plus puissante que la Switch actuelle et pourrait conserver le concept hybride salon/portable."},
    {"titre": "Elden Ring, GOTY 2022", "date": "2022-12-08", "theme": "Jeux Vidéo", "description": "Le jeu de FromSoftware, Elden Ring, a été couronné Jeu de l'Année 2022. Créé en collaboration avec l'écrivain George R. R. Martin, son monde ouvert immense, son gameplay exigeant et sa direction artistique ont été largement acclamés par les joueurs et la critique."},
    {"titre": "Elden Ring : le jeu de FromSoftware élu Jeu de l'Année", "date": "2022-12-08", "theme": "Jeux Vidéo", "description": "Elden Ring a été élu Jeu de l'Année 2022. Le jeu a été salué pour son monde ouvert, son gameplay difficile et son ambiance unique."},
    {"titre": "The Legend of Zelda: Tears of the Kingdom, un chef-d'œuvre", "date": "2023-05-12", "theme": "Jeux Vidéo", "description": "Suite directe de Breath of the Wild, The Legend of Zelda: Tears of the Kingdom a repoussé les limites de la créativité. Ses nouveaux pouvoirs, 'Amalgame' et 'Emprise', permettent aux joueurs de construire des véhicules et des armes uniques, offrant une liberté de jeu sans précédent."},
    {"titre": "Zelda : Tears of the Kingdom, un chef-d'œuvre de créativité", "date": "2023-05-12", "theme": "Jeux Vidéo", "description": "The Legend of Zelda: Tears of the Kingdom a été salué pour sa créativité et son gameplay innovant. Le jeu offre une grande liberté aux joueurs et leur permet de construire des objets uniques."},
    {"titre": "Le rachat d'Activision Blizzard par Microsoft", "date": "2023-10-13", "theme": "Jeux Vidéo", "description": "Après un long processus de validation réglementaire, Microsoft a finalisé le rachat historique d'Activision Blizzard King pour près de 69 milliards de dollars. Cette acquisition place des licences majeures comme Call of Duty, World of Warcraft et Candy Crush sous l'égide de Xbox."},
    {"titre": "Microsoft rachète Activision Blizzard pour 69 milliards de dollars", "date": "2023-10-13", "theme": "Jeux Vidéo", "description": "Microsoft a finalisé le rachat d'Activision Blizzard pour 69 milliards de dollars. L'acquisition place des jeux comme Call of Duty et World of Warcraft sous le contrôle de Microsoft."},
    {"titre": "Hades II lancé en accès anticipé", "date": "2024-05-06", "theme": "Jeux Vidéo", "description": "La suite du très acclamé roguelike Hades a été lancée en accès anticipé sur Steam et l'Epic Games Store. Hades II met en scène Melinoë, la sœur de Zagreus, qui doit affronter Chronos, le Titan du Temps. Le jeu a reçu un accueil extrêmement positif."},
    {"titre": "Hades II : la suite du roguelike acclamé est disponible en accès anticipé", "date": "2024-05-06", "theme": "Jeux Vidéo", "description": "Hades II est disponible en accès anticipé sur Steam et Epic Games Store. Le jeu a été salué pour son gameplay et son histoire captivante."},
    {"titre": "Le succès continu de Fortnite avec ses nouveaux modes", "date": "2023-12-02", "theme": "Jeux Vidéo", "description": "Fortnite a prouvé sa capacité à se réinventer avec le lancement de trois nouveaux modes de jeu majeurs : LEGO Fortnite (survie et construction), Rocket Racing (course arcade) et Fortnite Festival (jeu de rythme par les créateurs de Rock Band)."},
    {"titre": "Fortnite : de nouveaux modes de jeu pour relancer l'intérêt", "date": "2023-12-02", "theme": "Jeux Vidéo", "description": "Fortnite a lancé de nouveaux modes de jeu pour attirer de nouveaux joueurs. Les modes LEGO Fortnite, Rocket Racing et Fortnite Festival offrent des expériences de jeu variées."},
    {"titre": "Cyberpunk 2077: La rédemption avec la version 2.0 et Phantom Liberty", "date": "2023-09-26", "theme": "Jeux Vidéo", "description": "Après un lancement désastreux en 2020, le studio CD Projekt Red a réussi à redorer l'image de Cyberpunk 2077 grâce à une mise à jour majeure (2.0) et une extension acclamée, 'Phantom Liberty', avec l'acteur Idris Elba. Le jeu est désormais considéré comme une excellente expérience RPG."},
    {"titre": "Cyberpunk 2077 : le jeu renaît de ses cendres avec la version 2.0 et Phantom Liberty", "date": "2023-09-26", "theme": "Jeux Vidéo", "description": "Cyberpunk 2077 a connu un grand succès après une mise à jour majeure et la sortie de l'extension Phantom Liberty. Le jeu est désormais salué pour son gameplay et son histoire."},
    {"titre": "Helldivers 2, le shooter coopératif surprise de 2024", "date": "2024-02-08", "theme": "Jeux Vidéo", "description": "Helldivers 2 a surpris tout le monde en devenant un immense succès sur PlayStation 5 et PC. Ce jeu de tir coopératif à la troisième personne, avec son ambiance de satire militaire et son gameplay intense, a rassemblé une communauté de millions de joueurs."},
    {"titre": "Le film Super Mario Bros. bat des records au box-office", "date": "2023-04-05", "theme": "Jeux Vidéo", "description": "Le film d'animation 'Super Mario Bros., le film' est devenu l'adaptation de jeu vidéo la plus rentable de l'histoire. Produit par Illumination et Nintendo, le film a séduit les familles et les fans du plombier moustachu grâce à sa fidélité et son humour."},
    {"titre": "Le Steam Deck de Valve popularise le jeu PC portable", "date": "2022-02-25", "theme": "Jeux Vidéo", "description": "Le Steam Deck, un PC de jeu portable conçu par Valve, a connu un grand succès. Il permet aux joueurs d'accéder à leur bibliothèque Steam en déplacement, offrant une alternative puissante à la Nintendo Switch pour ceux qui préfèrent l'écosystème PC."},
    {"titre": "L'e-sport continue sa croissance explosive", "date": "2024-01-01", "theme": "Jeux Vidéo", "description": "L'e-sport (sport électronique) poursuit sa croissance avec des audiences qui rivalisent avec celles des sports traditionnels. Des jeux comme League of Legends, Counter-Strike 2 et Valorant organisent des championnats du monde dotés de millions de dollars de prix."},
    {"titre": "Le phénomène des 'Cozy Games'", "date": "2023-01-01", "theme": "Jeux Vidéo", "description": "Les 'cozy games' (jeux douillets) sont de plus en plus populaires. Des titres comme Animal Crossing, Stardew Valley ou Disney Dreamlight Valley offrent des expériences relaxantes, sans stress, axées sur la créativité, la décoration et les interactions sociales positives."},

    # Actualité
    {"titre": "Progrès de l'IA avec les modèles de langage génératifs", "date": "2023-03-14", "theme": "Actualité", "description": "Les modèles de langage comme GPT-4 d'OpenAI ou Gemini de Google ont démontré des capacités impressionnantes en matière de génération de texte, de traduction et de code. Ces intelligences artificielles (IA) ouvrent de nouvelles perspectives dans de nombreux domaines professionnels et créatifs."},
    {"titre": "La population mondiale dépasse les 8 milliards", "date": "2022-11-15", "theme": "Actualité", "description": "Selon les Nations Unies, la population mondiale a officiellement franchi le cap des 8 milliards d'habitants. Cette croissance démographique pose des défis majeurs en termes de ressources, de climat et de développement durable, particulièrement en Asie et en Afrique."},
    {"titre": "Le télescope James Webb révèle des images inédites de l'univers", "date": "2022-07-12", "theme": "Actualité", "description": "Le télescope spatial James Webb (JWST) a fourni les images infrarouges les plus profondes et les plus nettes de l'univers primitif jamais vues. Ses observations permettent aux scientifiques d'étudier la formation des premières galaxies et étoiles."},
    {"titre": "L'Union Européenne adopte l'AI Act", "date": "2024-03-13", "theme": "Actualité", "description": "Le Parlement européen a approuvé l'AI Act, une législation pionnière visant à réglementer l'utilisation de l'intelligence artificielle. Le texte classe les systèmes d'IA par niveau de risque et interdit certaines applications jugées trop dangereuses pour les droits des citoyens."},
    {"titre": "La voiture électrique poursuit son essor", "date": "2024-01-01", "theme": "Actualité", "description": "Les ventes de voitures électriques continuent d'augmenter dans le monde, poussées par les politiques environnementales, les subventions et les innovations technologiques. Cependant, des défis subsistent concernant le prix, l'autonomie et le déploiement des bornes de recharge."},
    {"titre": "La mission Artemis I de la NASA, un retour vers la Lune", "date": "2022-11-16", "theme": "Actualité", "description": "La NASA a lancé avec succès la mission Artemis I, un vol d'essai sans équipage de sa nouvelle fusée géante SLS et de la capsule Orion autour de la Lune. Cette mission marque la première étape du programme visant à ramener des astronautes sur la surface lunaire."},
    {"titre": "L'année 2023, la plus chaude jamais enregistrée", "date": "2024-01-09", "theme": "Actualité", "description": "Le service européen Copernicus a confirmé que l'année 2023 a été l'année la plus chaude jamais enregistrée au niveau mondial. Ce record est attribué au changement climatique d'origine humaine, amplifié par le phénomène El Niño."},
    {"titre": "L'essor des IA génératrices d'images comme Midjourney et DALL-E", "date": "2022-07-20", "theme": "Actualité", "description": "Des intelligences artificielles comme Midjourney, DALL-E 2 et Stable Diffusion permettent de créer des images photoréalistes ou artistiques à partir de simples descriptions textuelles. Cette technologie soulève des questions sur la créativité, le droit d'auteur et la désinformation."},
    {"titre": "Threads, le concurrent de Twitter (X) lancé par Meta", "date": "2023-07-05", "theme": "Actualité", "description": "Meta, la maison mère de Facebook et Instagram, a lancé Threads, une application de microblogging conçue pour concurrencer directement Twitter (désormais appelé X). L'application a connu un démarrage fulgurant en s'appuyant sur la base d'utilisateurs d'Instagram."},
    {"titre": "La technologie CRISPR et l'édition du génome", "date": "2023-12-08", "theme": "Actualité", "description": "Les autorités réglementaires britanniques et américaines ont approuvé le premier traitement médical basé sur la technologie d'édition de gènes CRISPR-Cas9. Ce traitement vise à guérir la drépanocytose, une maladie génétique du sang, ouvrant la voie à de nouvelles thérapies géniques."},
    {"titre": "Le projet de ville futuriste 'The Line' en Arabie Saoudite", "date": "2022-07-25", "theme": "Actualité", "description": "L'Arabie Saoudite a présenté les détails de son projet pharaonique 'The Line', une ville linéaire de 170 km de long, sans voiture et fonctionnant à 100% aux énergies renouvelables. Le projet, qui fait partie du plan Neom, suscite à la fois fascination et scepticisme."},
    {"titre": "Le retour du Concorde ? L'avion supersonique Boom Overture", "date": "2022-08-16", "theme": "Actualité", "description": "La start-up américaine Boom Supersonic développe l'Overture, un avion de ligne capable de voler à une vitesse supersonique, promettant de diviser par deux les temps de trajet transatlantiques. Plusieurs compagnies aériennes ont déjà passé des précommandes."},
    {"titre": "La crise énergétique en Europe", "date": "2022-09-01", "theme": "Actualité", "description": "Suite aux tensions géopolitiques, l'Europe a fait face à une crise énergétique majeure, avec une flambée des prix du gaz et de l'électricité. Cette situation a accéléré les efforts de transition vers les énergies renouvelables et la sobriété énergétique."},
    {"titre": "L'Inde devient le pays le plus peuplé du monde", "date": "2023-04-24", "theme": "Actualité", "description": "Selon les estimations des Nations Unies, l'Inde a dépassé la Chine pour devenir le pays le plus peuplé de la planète. Ce basculement démographique a des implications économiques et géopolitiques importantes pour le 21ème siècle."},
    {"titre": "Le développement de l'informatique quantique", "date": "2023-10-01", "theme": "Actualité", "description": "Des entreprises comme Google, IBM et des start-ups spécialisées continuent de faire des progrès significatifs dans le domaine de l'informatique quantique. Bien que son utilisation à grande échelle soit encore lointaine, l'ordinateur quantique promet de révolutionner la médecine, la science des matériaux et l'intelligence artificielle."}
]

# --- Gestion des Notes (Persistance) ---
RATINGS_FILE = "ratings.json"

def load_ratings():
    """Charge les notes depuis un fichier JSON."""
    if os.path.exists(RATINGS_FILE):
        try:
            with open(RATINGS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} # Retourne un dictionnaire vide si le fichier est corrompu ou vide
    return {}

def save_ratings(ratings):
    """Sauvegarde les notes dans un fichier JSON."""
    with open(RATINGS_FILE, 'w') as f:
        json.dump(ratings, f, indent=4)

# --- Initialisation de l'état de la session ---
if 'article_ratings' not in st.session_state:
    st.session_state.article_ratings = load_ratings()

# --- Fonctions ---

def trouver_reponses(question):
    """Trouve et classe les articles en fonction de la pertinence par rapport à une question."""
    mots_question = set(re.split(r'\W+', question.lower()))
    if '' in mots_question:
        mots_question.remove('')

    resultats = []
    for article in BASE_DE_DONNEES:
        contenu = (article["titre"] + " " + article["description"]).lower()
        mots_contenu = re.split(r'\W+', contenu)
        
        score = 0
        mots_communs_details = {}
        for mot in mots_question:
            count = mots_contenu.count(mot)
            if count > 0:
                score += count
                mots_communs_details[mot] = count

        if score > 0:
            resultats.append({"article": article, "score": score})
            # Affiche les détails dans la console du terminal
            print("\n--- 🔎 Article correspondant trouvé ---")
            print(f"Titre : {article['titre']}")
            print(f"Détails des mots en commun pour la requête \"{question}\":")
            for mot, count in mots_communs_details.items():
                print(f"  - Le mot '{mot}' apparaît {count} fois.")
            print("------------------------------------")

    resultats.sort(key=lambda x: x["score"], reverse=True)
    return resultats

def afficher_resultats_recherche(articles, num_to_show):
    """Affiche les résultats de la recherche avec un effet de fondu et des expanders."""
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
        st.warning("🤔 Aucun article ne correspond à votre recherche.")
        return

    time.sleep(0.01)

    with results_container.container():
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        meilleur_article = articles[0]
        score_text = f"(Score de pertinence : {meilleur_article['score']})"
        st.success(f"✅ **Meilleur résultat** {score_text}")
        with st.container(border=True):
            st.subheader(f"{meilleur_article['article']['titre']}")
            st.caption(f"Thème : {meilleur_article['article']['theme']} | Date : {meilleur_article['article']['date']}")
            st.write(meilleur_article['article']['description'])

        if len(articles) > 1:
            st.write("---")
            st.info("🔎 **Autres résultats similaires :**")
            for res in articles[1:num_to_show]:
                score_text = f"| Mots en commun : {res['score']}"
                expander_label = f"**{res['article']['titre']}** (Date : {res['article']['date']}) {score_text}"
                with st.expander(expander_label):
                    st.write(res['article']['description'])
        
        st.markdown('</div>', unsafe_allow_html=True)

def page_recherche(num_articles_to_show):
    """Contenu de la page de recherche par mots-clés."""
    st.header("🔍 Recherche par mots-clés")
    question = st.text_input("Posez votre question ou entrez des mots-clés ici :", key="search_query")

    if question:
        with st.spinner("🔍 Je recherche la réponse..."):
            reponses = trouver_reponses(question)

        st.sidebar.subheader("Trier les résultats")
        sort_option = st.sidebar.selectbox("Trier par :", ["Pertinence", "Date (plus récent)", "Date (plus ancien)"])

        if sort_option == "Date (plus récent)":
            reponses.sort(key=lambda x: datetime.strptime(x['article']['date'], '%Y-%m-%d'), reverse=True)
        elif sort_option == "Date (plus ancien)":
            reponses.sort(key=lambda x: datetime.strptime(x['article']['date'], '%Y-%m-%d'), reverse=False)
        
        afficher_resultats_recherche(reponses, num_articles_to_show)

def page_generale(num_articles_to_show):
    """Contenu de la page générale pour parcourir les articles."""
    st.header("📰 Parcourir les articles")

    st.sidebar.subheader("Options d'affichage")
    theme_filter = st.sidebar.radio("Filtrer par thème", ["Tous", "Sport", "Musique", "Jeux Vidéo", "Actualité"])
    sort_by = st.sidebar.radio("Trier par", ["Date (plus récent)", "Meilleures notes"])

    articles_a_afficher = list(BASE_DE_DONNEES)

    if theme_filter != "Tous":
        articles_a_afficher = [art for art in articles_a_afficher if art["theme"] == theme_filter]

    if sort_by == "Date (plus récent)":
        articles_a_afficher.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    elif sort_by == "Meilleures notes":
        articles_a_afficher.sort(key=lambda x: st.session_state.article_ratings.get(x['titre'], 0), reverse=True)

    if not articles_a_afficher:
        st.warning("Aucun article à afficher pour cette catégorie.")
    else:
        for i, article in enumerate(articles_a_afficher[:num_articles_to_show]):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(article['titre'])
                    st.caption(f"Thème : {article['theme']} | Date : {article['date']}")
                with col2:
                    note = st.number_input(
                        "Note", 
                        min_value=1, 
                        max_value=5, 
                        value=st.session_state.article_ratings.get(article['titre'], 3), 
                        key=f"note_{article['titre']}_{i}",
                        label_visibility="collapsed"
                    )
                    if st.session_state.article_ratings.get(article['titre']) != note:
                        st.session_state.article_ratings[article['titre']] = note
                        save_ratings(st.session_state.article_ratings)
                        st.rerun()
                
                st.write(article['description'])
                note_actuelle = st.session_state.article_ratings.get(article['titre'], 0)
                if note_actuelle > 0:
                    st.markdown(f"**Votre note : {'⭐' * note_actuelle}**")
                else:
                    st.markdown("_Pas encore noté_")
            st.write("")

# --- Logique principale de l'application ---

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisissez une page", ["Recherche par mots-clés", "Parcourir les articles"])
st.sidebar.divider()

st.sidebar.subheader("Paramètres d'affichage")
num_articles = st.sidebar.number_input("Nombre d'articles à afficher", min_value=1, max_value=50, value=5, step=1)
st.sidebar.divider()

if page == "Recherche par mots-clés":
    page_recherche(num_articles)
elif page == "Parcourir les articles":
    page_generale(num_articles)
