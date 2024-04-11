import stanza

stanza.download('fr')
nlp = stanza.Pipeline('fr', processors='tokenize, lemma, pos, depparse')

with open('texte.txt', 'r') as texte:
    doc = nlp(texte.read())
    sent_list = []
    tokens_list = []
    for sentence in doc.sentences:
        for token in sentence.words:
            tokens_list.append(
                [token.text, 
                token.lemma, 
                token.pos, 
                token.id, 
                token.text, 
                token.head, 
                sentence.words[token.head-1].text if token.head > 0 else "root", 
                token.deprel,
                ])
            if token.text == "." or token.text == "!":
                sent_list.append(tokens_list)
                tokens_list = []
    print(sent_list)

""" with open('texte.txt', 'r') as texte:
    doc = nlp(texte.read())
    tokens_list = []
    for sentence in doc.sentences:
        for word in sentence.words:             
            tokens_list.append({
                'text':word.text,
                'lemma':word.lemma,
                'pos':word.upos,
                'id':word.id,
                'head id':word.head,
                'head text':sentence.words[word.head-1].text if word.head > 0 else "root",
                'deprel':word.deprel,
            }) 
    print(tokens_list) """


""" #pour récupérer le gouverneur/dépendant et la nature de chaque token , j'ai utilisé 
'id':word.id,
'head id':word.head,
'head text':sentence.words[word.head-1].text if word.head > 0 else "root",
'deprel':word.deprel, """


""" def analyze_deps_stanza(text: str) -> str:
    with open('texte.txt', 'r') as texte:
        doc = nlp(texte.read())
        tokens_list = []
        for sentence in doc.sentences:
            for word in sentence.words:             
                tokens_list.append([word.id, word.text, word.head, sentence.words[word.head-1].text if word.head > 0 else "root", word.deprel,
                ])
    return tokens_list """