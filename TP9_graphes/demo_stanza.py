import stanza

stanza.download('fr')
nlp = stanza.Pipeline('fr', processors='tokenize, lemma, pos')

with open('texte.txt', 'r') as texte:
    doc = nlp(texte.read())

for sentence in doc.sentences:
    for token in sentence.tokens:
        print(f"Forme: {token.text}, Lemme: {token.words[0].lemma}, POS: {token.words[0].upos}")