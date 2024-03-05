from datastructures import Item, Corpus
from pathlib import Path
from typing import Any
from dataclasses import asdict, is_dataclass
import json

def dataclass_to_dict(obj: Any) -> Any:
    if is_dataclass(obj):
        return {k: dataclass_to_dict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(v) for v in obj]
    else:
        return obj

def save_json(corpus: Corpus, output_file: Path) -> None:
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(dataclass_to_dict(corpus), json_file, ensure_ascii=False, indent=4)

def load_json(input_file: Path) -> Corpus:
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    print(type(data))
    print(data)
    articles = [Item(**article) for article in data['articles']]
    return Corpus(articles=articles)
