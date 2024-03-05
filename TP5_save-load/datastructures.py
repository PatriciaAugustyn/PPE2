from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree as ET

@dataclass
class Item:
    guid: str
    title: str
    link: str
    description: str
    pubdate: str
    category: List[str]

    def __post_init__(self):
        if not hasattr(self, '_data'):
            self._data = {
                'guid': self.guid,
                'title': self.title,
                'link': self.link,
                'description': self.description,
                'category': self.category,
                'pubdate': self.pubdate,
            }

@dataclass
class Corpus:
    articles: List[Item]

    def __init__(self, articles):
        self.articles = articles

    def __iter__(self):
        return iter(self.articles)
