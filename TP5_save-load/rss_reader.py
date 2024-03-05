import re
import feedparser
import xml.etree.ElementTree as ET
import argparse
from tabulate import tabulate
from typing import List
from datastructures import Item

def module_re(chemins: List[str], date_debut=None, date_fin=None) -> List[Item]:
    liste_infos = []
    for chemin in chemins:
        rss_flux = open(chemin).read()

        liste_items = re.findall(r"<item>([\s\S]*?)<\/item>", rss_flux)

        for element in liste_items:
            item_dict = {}

            if matches:= re.search(r"<guid>([\s\S]*?)<\/guid>", element):
                item_dict['guid'] = matches.group(1)
            else:
                item_dict['guid'] = ''
            if matches:= re.search(r"<title>([\s\S]*?)<\/title>", element):
                item_dict['title'] = matches.group(1)
            else:
                item_dict['title'] = ''
            if matches:= re.search(r"<link>([\s\S]*?)<\/link>", element):
                item_dict['link'] = matches.group(1)
            else:
                item_dict['link'] = ''
            if matches:= re.search(r"<description>([\s\S]*?)<\/description>", element):
                item_dict['description'] = matches.group(1)
            else:
                item_dict['description'] = ''
            if matches:= re.search(r"<category>([\s\S]*?)<\/category>", element):
                category = []
                category.append(matches.group(1))
                item_dict['category'] = category
            else:
                category = ['']
                item_dict['category'] = category
            if matches:= re.search(r"<pubDate>([\s\S]*?)<\/pubDate>", element):
                item_dict['pubdate'] = matches.group(1)
            else:
                item_dict['pubdate'] = ''

            liste_infos.append(item_dict)

    return liste_infos


def module_etree(chemins: List[str], date_debut=None, date_fin=None) -> List[Item]:
    liste_infos = []
    for chemin in chemins:
        tree = ET.parse(chemin)
        root = tree.getroot()

        for child in root.findall('.//item'):
            item_dict = {}

            item_dict['guid'] = child.find('guid').text if child.find('guid') is not None else ''
            item_dict['title'] = child.find('title').text if child.find('title') is not None else ''
            item_dict['description'] = child.find('description').text if child.find('description') is not None else ''
            item_dict['pubdate'] = child.find('pubDate').text if child.find('pubDate') is not None else ''
            category = []
            category.append(child.find('category').text if child.find('category') is not None else '')
            item_dict['category'] = category
            item_dict['link'] = child.find('link').text if child.find('link') is not None else ''

            if item_dict['description'] is not None:
                item_dict['description'] = re.sub('\s+', ' ', item_dict['description']).strip()

            item_dict['title'] = re.sub('\s+', ' ', item_dict['title']).strip()
            item_dict['link'] = re.sub('\s+', ' ', item_dict['link']).strip()

            liste_infos.append(item_dict)

    return liste_infos


def module_feedparser(chemins: List[str], date_debut=None, date_fin=None) -> List[Item]:
    liste_infos = []
    for chemin in chemins:
        # Parsing du fichier et initialisation de la liste de résultats
        flux = feedparser.parse(chemin)

        # Extraction des métadonnées de chaque entrée
        for entry in flux.entries:
            item_dict = {}

            item_dict['guid'] = entry.get('guid', '')
            item_dict['title'] = entry.get('title', '')
            item_dict['link'] = entry.get('link', '')
            item_dict['description'] = entry.get('description', '')
            category = []
            category.append(entry.get('category', ''))
            item_dict['category'] = category
            item_dict['pubdate'] = entry.get('published', '')

            liste_infos.append(item_dict)

    return liste_infos

def choix_utilisateur(args) -> List[Item]:
    if args.re is not None:
        return module_re(args.re)
    elif args.etree is not None:
        return module_etree(args.etree)
    elif args.feedparser is not None:
        return module_feedparser(args.feedparser)


def main():
    parser = argparse.ArgumentParser(description="Un script qui lit le fichier xml dont le chemin est donné en argument, et qui retourne le texte et les métadonnées des item du flux RSS.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--re', nargs='+', metavar='FILENAME', help="Utilisez cette option pour que le fichier xml soit parsé avec RegEx")
    group.add_argument('--etree', nargs='+', metavar='FILENAME', help="Utilisez cette option pour que le fichier xml soit parsé avec etree")
    group.add_argument('--feedparser', nargs='+', metavar='FILENAME', help="Utilisez cette option pour que le fichier xml soit parsé avec feedparser")
    args = parser.parse_args()

    liste_items = choix_utilisateur(args)
    # print(liste_items)
    headers = ["GUID", "Titre", "Lien", "Description", "Categorie", "Date de publication"]
    data = []
    for item in liste_items:
        data.append([item.guid, item.title, item.link, item.description, item.category, item.pubdate])
    print(tabulate(data, headers=headers, tablefmt="grid", maxcolwidths=20))
    # print(data)

if __name__ == '__main__':
    main()
