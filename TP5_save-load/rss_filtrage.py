import xml.etree.ElementTree as ET
from datastructures import Item, Corpus
from pathlib import Path
from rss_reader import module_re, module_etree, module_feedparser
from datetime import datetime, timezone
from typing import List

def afficher_resultats(corpus, args):
    """Affiche les résultats du corpus ou de la filtration sur la console."""

    # Si les catégories sont spécifiées, imprimer les catégories
    if args.category:
        print("Categories: ", args.category)

    # Parcourir chaque élément du corpus
    for item in corpus:
        formatted_guid = str(item.guid) if item.guid is not None else ""
        formatted_title = str(item.title) if item.title is not None else ""
        formatted_link = str(item.link) if item.link is not None else ""
        formatted_description = str(item.description) if item.description is not None else ""
        formatted_pubdate = str(item.pubdate) if item.pubdate is not None else ""
        formatted_category = str(item.category) if item.category is not None else ""
        print(f"GUID: {formatted_guid}")
        print(f"Title: {formatted_title}")
        print(f"Link: {formatted_link}")
        print(f"Description: {formatted_description}")
        print(f"Pubdate: {formatted_pubdate}")
        print(f"Category: {formatted_category}")
        print("-" * 50)

def filtrer_articles_par_category(liste_articles_uniq, category_choisi):
    articles_choisis = []
    for article in liste_articles_uniq:
        if category_choisi in article.category:
            articles_choisis.append(article)
    return articles_choisis

def choix_filtrage(corpus, args):
    if isinstance(corpus, list):
        if args.category is not None:
            corpus = filtrer_articles_par_category(corpus, args.category)

        if args.date and (args.date_debut or args.date_fin):
            date_debut = datetime.strptime(args.date_debut, '%a, %d %b %Y %H:%M:%S %z') if args.date_debut else None
            date_fin = datetime.strptime(args.date_fin, '%a, %d %b %Y %H:%M:%S %z') if args.date_fin else None
            corpus = filtrer_articles_par_date(corpus, date_debut, date_fin)
        return Corpus(articles=corpus)
    else:
        return corpus

def parcourir_corpus(dossier, args) -> Corpus:
    """Parcourir les fichiers dans le dossier donné en argument"""

    # Mettre tous les fichiers du dossier dans une liste
    dossier = Path(dossier)
    fichiers = list(dossier.glob('**/*.xml'))

    # Liste des articles uniques à retourner
    liste_articles_uniq = []
    titres_uniq = set()

    """
    Lire chaque fichier.xml, mettre les items dans une liste, si le titre d'un item n'existe pas dans la liste
    des articles uniques, l'y ajouter ; si la catégorie est différente, ajouter la catégorie dans la liste des
    catégories
    """

    for fichier in fichiers:
        liste_fichier = []
        liste_fichier.append(fichier)
        if args.re is True:
            liste_articles = module_re(liste_fichier)
        elif args.etree is True:
            try:
                liste_articles = module_etree(liste_fichier)
            except ET.ParseError:
                pass
        elif args.feedparser is True:
            liste_articles = module_feedparser(liste_fichier)

        # Ajouter des nouveaux articles
        for article_data in liste_articles:
            if article_data['title'] not in titres_uniq:
                item = Item(**article_data)
                liste_articles_uniq.append(item)
                titres_uniq.add(article_data['title'])

            # Si l'article existe mais avec une catégorie différente, ajouter la nouvelle catégorie
            else:
                for article_existant in liste_articles_uniq:
                    if article_data['title'] == article_existant.title:
                        if article_data['category'][0] not in article_existant.category:
                            article_existant.category.append(article_data['category'][0])

    return Corpus(articles=liste_articles_uniq)


def convertir_date(date_string):
    #utiliser différents formats de date pour le filtrage
    formats_date = [
        "%Y-%m-%dT%H:%M:%S%z",  # Format ISO 8601
        "%a, %d %b %Y %H:%M:%S %z",  # Format "Mon, 12 Feb 2024 21:14:09 +0100"
        "%a, %d %b %Y %H:%M:%S GMT",  # Format "Tue, 30 Jan 2024 21:57:41 GMT"
        "%a, %d %b %Y %H:%M:%S %Z",  # Format "Tue, 30 Jan 2024 21:57:41 UTC"
        "%Y-%m-%d",  # Format "2024-01-30"
    ]

    #Essayer chaque format de date jusqu'à ce que l'un d'eux fonctionne
    for format_date in formats_date:
        try:
            date_object = datetime.strptime(date_string, format_date)
            return date_object
        except ValueError:
            pass

    #Si aucun format de date ne fonctionne, retourner None ou lever une exception
    return None


def filtrer_articles_par_date(articles, date_debut=None, date_fin=None):
    #fonction qui filtre les articles selon les dates de début et de fin si elles sont spécifiées
    articles_filtres = []

    #extraction de la date et conversion en type datetime
    for article in articles:
        if 'pubdate' in article:
            article_date_str = article['pubdate']
            article_date = convertir_date(article_date_str)

            # Convertir article_date en timezone UTC si elle n'a pas de timezone
            if article_date is not None and article_date.tzinfo is None:
                article_date = article_date.replace(tzinfo=timezone.utc)

            #filtrage en fonction des dates données en argument
            if date_debut and date_fin and article_date is not None:
                if date_debut <= article_date <= date_fin:
                    articles_filtres.append(article)
            elif date_debut and article_date is not None:
                if article_date >= date_debut:
                    articles_filtres.append(article)
            else:
                articles_filtres.append(article)

    return articles_filtres
