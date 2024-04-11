import spacy
from spacy import displacy

def analyze_deps_spacy(file_path: str):
    nlp = spacy.load("fr_core_news_sm")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    doc = nlp(text)
    analyzed_data = []

    for sent in doc.sents:
        sentence_tokens = []
        for token in sent:
            token_data = {
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "dep": token.dep_,
                "head": token.head.text,
                "head_pos": token.head.pos_,
                "children": [{
                    "text": child.text,
                    "lemma": child.lemma_,
                    "pos": child.pos_,
                    "dep": child.dep_
                } for child in token.children]
            }
            sentence_tokens.append(token_data)
        analyzed_data.append(sentence_tokens)

    return analyzed_data

# Afficher les dépendances sous forme de graphe
def display_dependencies(file_path: str):
    nlp = spacy.load("fr_core_news_sm")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    doc = nlp(text)
    displacy.serve(doc, auto_select_port=True, style="dep")

# Exemple d'utilisation pour analyser les dépendances 
file_path = "example.txt"
result = analyze_deps_spacy(file_path)
for i, sent in enumerate(result):
    print(f"Sentence {i+1}:")
    for token in sent:
        print(token)
    print()

# Exemple d'utilisation pour afficher les dépendances sous forme de graphe
# uncomment the following 2 lines if you want to have a link in terminal, where the arcs are displayed
#file_path = "example.txt"
#display_dependencies(file_path)
# to stop using the link (port), Ctrl+C in terminal
