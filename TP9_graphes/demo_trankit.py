from trankit import Pipeline

# "Initialiser le pipeline Trankit pour le français"
p = Pipeline('french')

with open('texte_trankit.txt', 'r', encoding='utf-8') as file:
    doc_text = file.read()  

# Analyser le texte pour les parties du discours et la lemmatisation
pos_tagged_doc = p.posdep(doc_text, is_sent=False)

for sentence in pos_tagged_doc['sentences']:
    for token in sentence['tokens']:
        if 'expanded' in token:
            print(f"Expanded from: {token['text']}")
            for expanded_token in token['expanded']:
                token_text = expanded_token['text']
                token_pos = expanded_token.get('upos', 'N/A')
                token_lemma = expanded_token.get('lemma', token_text)  
                print(f" Expanded Token: {token_text}, POS: {token_pos}, Lemma: {token_lemma}")
        else:
            token_text = token['text']
            token_pos = token['upos']
            token_lemma = token.get('lemma', token_text)
            print(f"Token: {token_text}, POS: {token_pos}, Lemma: {token_lemma}")

