import stanza
#stanza.download('fr') 
nlp = stanza.Pipeline(lang='fr', processors='tokenize,lemma,pos,ner')
def process_text(text):
# Traiter le texte avec Stanza
    doc = nlp(text)
# Afficher les résultats
    for sentence in doc.sentences:
        for word in sentence.words:
            
            print(word.text[0], word.lemma[1], word.pos[2])


texte = "je suis belle."
process_text(texte)