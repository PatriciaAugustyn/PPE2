import argparse, textwrap
import re
import xml.etree.ElementTree as ET
import feedparser

def lecture_fichier_flux_r1(path):
    '''Cette fonction permet de lire le fichier xml dont le chemin est donné en
    argument, et qui retourne le texte et les métadonnées des item du flux RSS.'''

    with open(path, "r", encoding="utf-8") as fichier:
        xml = fichier.read()

        # On veut cibler notre regex sur ce qui est seulement a l'intérieur des balises <title></title> et <description></description> : donc ()
        regex_titre = re.findall(r"<title>(.*)</title>", xml)
        regex_description = re.findall(r"<description>(.*)</description>", xml)

        # Les résultats : rendre la visualisation des données plus visible
        print("\nLe texte entre les balises <title></title> :\n")
        for titre in regex_titre:
            print(titre.strip())

        print("\nLe texte entre les balises <description></description> :\n")
        for description in regex_description:
            print(description.strip())

        # Bonus :
        regex_date = re.findall(r"<pubDate>(.*)</pubDate>", xml)
        regex_lien = re.findall(r"<link>(.*)</link>", xml)
        regex_categorie = re.findall(r"<category>(.*)</category>", xml)

        print("\nLe texte entre les balises <pubDate></pubDate> :\n")
        for date in regex_date:
            print(date.strip())

        print("\nLe texte entre les balises <link></link> :\n")
        for lien in regex_lien:
            print(lien.strip())

        print("\nLe texte entre les balises <category></category> :\n")
        for categorie in regex_categorie:
            print(categorie.strip())

def lecture_fichier_flux_r2(path):
     #doit donner le contenu des titres et descriptions
    #liste de titre/ liste de description et liste de méta donnée? 
    tree = ET.parse(path)
    root = tree.getroot()
    title = []
    description =[]
    date = []
    category = []

    for channel in root.findall('channel'):
        for item in channel.findall('item'):
            date.append(item.findtext('pubDate'))
            title.append(item.findtext('title'))
            category.append(item.findtext('category'))
            description.append(item.findtext('description'))
        print(category)
    return channel, title, category, description 

def lecture_fichier_flux_r3(path):
    try:
        feed = feedparser.parse(path)
        print("\nLe texte entre les balises <title></title> :\n")
        for entry in feed.entries:
            print(entry.title.strip())

        print("\nLe texte entre les balises <description></description> :\n")
        for entry in feed.entries:
            print(entry.description.strip())

        print("\nLe texte entre les balises <pubDate></pubDate> :\n")
        for entry in feed.entries:
            print(entry.published.strip())

        print("\nLe texte entre les balises <link></link> :\n")
        for entry in feed.entries:
            print(entry.link.strip())

        print("\nLe texte entre les balises <category></category> :\n")
        for entry in feed.entries:
            if 'tags' in entry:
                for tag in entry.tags:
                    print(tag.term.strip())

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def main():
    parser = argparse.ArgumentParser(description = "Lancement de le fonction r1 : python3 rss_reader.py -r r1 sample.xml\nLancement de le fonction r2 : python3 rss_reader.py -r r2 sample.xml\nLancement de le fonction r3 : python3 rss_reader.py -r r2 sample.xml", usage='use "python %(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter, epilog="Merci d'avoir lu notre manuel ! Passez une excellente journée/soirée !")

    parser.add_argument("chemin_fichier_xml", help="Il faut ajouter le chemin vers votre fichier XML : python3 rss_reader.py [chemin_fichier_xml]")
    parser.add_argument("-r", "--role", 
                        choices=["r1", "r2", "r3"], 
                        help=textwrap.dedent('''Il existe 3 fonctions pour ce programme : 
                                             
-r1 : cette fonction permet d'utiliser le module re
-r2 : cette fonction permet d'utiliser le module etree
-r3 : cette fonction permet d'utiliser le module feedparser'''))


    args = parser.parse_args()
    path = args.chemin_fichier_xml
    
    if args.role == "r1":
        lecture_fichier_flux_r1(path)
    elif args.role == "r2":
        lecture_fichier_flux_r2(path)
    elif args.role == "r3":
        lecture_fichier_flux_r3(path)
    else:
        raise ValueError("Veuillez préciser le rôle ;) ")
    

if __name__ == '__main__':
    main()
    print("FINI")

# Lancement de le fonction r1 : python3 rss_reader.py -r r1 sample.xml
# Lancement de le fonction r2 : python3 rss_reader.py -r r2 sample.xml
# Lancement de le fonction r3 : python3 rss_reader.py -r r2 sample.xml
