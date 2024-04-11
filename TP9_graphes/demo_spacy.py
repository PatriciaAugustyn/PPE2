import spacy

nlp = spacy.load('fr_core_news_sm')

with open('example.txt', 'r', encoding='utf-8') as texte:
    doc = nlp(texte.read())

for token in doc:
    print(f"Forme: {token.text}, Lemme: {token.lemma_}, POS: {token.pos_}")
