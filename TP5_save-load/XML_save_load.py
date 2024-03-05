from datastructures import Item, Corpus
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import List

def item_to_xml(item: Item) -> ET.Element:
    element = ET.Element("item")
    for field in item.__dataclass_fields__.keys():
        value = getattr(item, field)
        if isinstance(value, list):
            for v in value:
                sub_element = ET.SubElement(element, field)
                sub_element.text = v
        else:
            sub_element = ET.SubElement(element, field)
            sub_element.text = value
    return element

def corpus_to_xml(corpus: Corpus) -> ET.Element:
    root = ET.Element("corpus")
    for article in corpus.articles:
        root.append(item_to_xml(article))
    return root

def save_xml(corpus: Corpus, output_file: Path) -> None:
    xml_data = corpus_to_xml(corpus)
    tree = ET.ElementTree(xml_data)
    tree.write(str(output_file), encoding="utf-8", xml_declaration=True)

def load_xml(input_file: Path) -> Corpus:
    tree = ET.parse(str(input_file))
    root = tree.getroot()
    articles = []
    for item_element in root.findall("item"):
        item_data = {}
        for sub_element in item_element:
            if sub_element.tag not in item_data:
                item_data[sub_element.tag] = []
            item_data[sub_element.tag].append(sub_element.text)
        item = Item(**item_data)
        articles.append(item)
    return Corpus(articles=articles)

