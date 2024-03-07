from dataclasses import dataclass
from xml.etree import ElementTree as ET
from pathlib import Path

import datetime
import json
import pickle

from dateutil import parser as dateparser


@dataclass
class Item:
    id : str  # élément guid (globally unique identifier) de l'item, sert à la déduplication
    source : str
    title : str
    description : str
    date : datetime.date
    categories : set[str]


@dataclass
class Corpus:
    # attention ! La liste ne gère pas en soit les guid (donc la déduplication).
    # Il faut soit :
    #    - faire une étape de déduplication en amont et supposer que cette liste est dédupliquée
    #    - changer le type vers dict[str, Item] où la clé (str) sera le guid de l'item.
    items : list[Item]


def save_xml(corpus : Corpus, output_file: Path) -> None:
    root = ET.Element("corpus")
    for item in corpus.items:
        item_e = ET.SubElement(root, "item")

        id_e = ET.SubElement(item_e, "id")
        id_e.text = item.id

        source_e = ET.SubElement(item_e, "source")
        source_e.text = item.source

        title_e = ET.SubElement(item_e, "title")
        title_e.text = item.title

        description_e = ET.SubElement(item_e, "description")
        description_e.text = item.description

        date_e = ET.SubElement(item_e, "date")
        if item.date is not None:
            date_e.text = datetime.date.isoformat(item.date)

        categories_e = ET.SubElement(item_e, "categories")
        for cat in sorted(item.categories):
            cat_e = ET.SubElement(categories_e, "category")
            cat_e.text = cat

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


def load_xml(input_file: Path) -> Corpus:
    root = ET.parse(input_file)
    corpus = Corpus([])

    for item in list(root.getroot()):
        item_date = item.find("date")
        if item_date is not None and item_date.text:
            item_date = dateparser.parse(item_date.text + " 00:00:00+00:00")
        else:
            item_date = None

        categories = set()
        for cat in list(item.find("categories")):
            categories.add(cat.text)

        corpus_item = Item(
            id = item.find("id").text,
            source = item.find("source").text,
            title = item.find("title").text,
            description = item.find("description").text,
            date = item_date,
            categories = categories
        )
        corpus.items.append(corpus_item)

    return corpus


def save_json(corpus : Corpus, output_file: Path) -> None:
    data = []
    for item in corpus.items:
        if item.date is not None:
            the_date = datetime.date.isoformat(item.date)

        current = {
            "id": item.id,
            "source": item.source,
            "title": item.title,
            "description": item.description,
            "date": the_date,
            "categories": sorted(item.categories)  # toujours avoir la même sérialisation (set n'est pas trié)
        }
        data.append(current)

    with open(output_file, "w") as output_stream:
        json.dump(data, output_stream, indent=2)


def load_json(input_file: Path) -> Corpus:
    corpus = Corpus([])
    with open(input_file, "rb") as input_stream:
        corpus.items = [
            Item(
                id=it["id"], 
                source=it["source"],
                title=it["title"],
                description=it["description"],
                date=it["date"] and datetime.date.fromisoformat(it["date"]),  # voir main.py pour syntaxe
                categories=set(it["categories"])
            )
            for it in json.load(input_stream)
        ]
    return corpus


def save_pickle(corpus : Corpus, output_file: Path) -> None:
    with open(output_file, "wb") as output_stream:
        pickle.dump(corpus, output_stream)


def load_pickle(input_file: Path) -> Corpus:
    with open(input_file, "rb") as input_stream:
        return pickle.load(input_stream)


name2saver = {
    "xml": save_xml,
    "json": save_json,
    "pickle": save_pickle,
}

name2loader = {
    "xml": load_xml,
    "json": load_json,
    "pickle": load_pickle,
}
