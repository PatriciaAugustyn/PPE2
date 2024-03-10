from pathlib import Path
from datetime import datetime
from typing import Optional



def filtre_category(item: dict, categorie_existe: Optional[set] = None)-> bool :
    if categorie_existe is None:
        print(f"Aucun élément trouvé pour la catégorie '{categorie_existe}'.")
        return True
    for categorie in item['category']:
        if categorie_existe.lower() in categorie.lower():
            #print(item)
            return True
        else:
            return False
   

def filtre_date(item: dict, date_debut: Optional[datetime.date] = None, date_fin: Optional[datetime.date] = None) -> bool:
    if date_debut is None and date_fin is None:
        return True  # Si aucune date n'est spécifiée, l'article passe le filtre
    try:
        #print(item['pubDate'])
        article_date = datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %Z").date()
        #print(article_date)
        if date_debut and date_fin:
            return date_debut <= article_date <= date_fin
        elif date_debut:
            return article_date >= date_debut
        elif date_fin:
            return article_date <= date_fin
    except (TypeError, ValueError) as e:
        # print(f"Error parsing date: {e}")
        pass
    return False


def filtre_source(item_or_path, source: Optional[str] = None) -> bool:
    if source is None:
        return True
    if isinstance(item_or_path, dict):
        item_source = item_or_path.get('source', '')
        if source.lower() in item_source.lower():
            return True
    elif isinstance(item_or_path, Path):
        if source.lower() in item_or_path.stem.lower():
            return True
    else:
        raise ValueError("L'argument doit être un dictionnaire représentant un item ou un objet Path.")
    return False



