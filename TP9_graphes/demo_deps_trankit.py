from trankit import Pipeline
nlp = Pipeline('french')

file_path = '../Documents/TP8/projet/texte.txt'

with open(file_path, 'r', encoding='utf-8') as file:
     text = file.read() 

doc = nlp(text)
dep = []

for sentence in doc['sentences']: 
    sentence_tokens = []
    for token in sentence['tokens'] : 
        token_contenu = {
            'text': token['text'],
            'lemma': token.get('lemma', ' '),
            'pos' : token.get('upos', ' '),
            'head' : token.get('head', ' '),
            'deprel' : token.get('deprel', ' ')
        }
            
        sentence_tokens.append(token_contenu)
    dep.append(sentence_tokens)


for sentence in dep:
    for token in sentence:
        print(token)

