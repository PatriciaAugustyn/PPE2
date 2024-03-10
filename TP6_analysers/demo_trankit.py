import argparse
from trankit import Pipeline

# Charger le modèle Trankit pour le français 
nlp = Pipeline(lang='french', gpu=False)
# et ajouter les autres français ?
nlp.add('french-partut')
nlp.add('french-sequoia')

def process_data_and_write_output(text, output_file):
    # Analyser le texte
    data = nlp(text)

    # Ouvrir le fichier de sortie pour écriture
    with open(output_file, "w") as f_out:
        # Affichage des en-têtes
        #print("Token\tLemme\tPOS")
        # Écrire les en-têtes dans le fichier
        f_out.write("Token\tLemme\tPOS\n")

        # Parcourir chaque phrase dans 'sentences'
        for sentence in data['sentences']:
            # Parcourir chaque token dans 'tokens'
            for token in sentence['tokens']:
                # Récupérer les valeurs 'text', 'lemma' et 'upos' pour chaque token ; et si ne trouve pas, alors on prend une chaine de caractère vide comme valeur
                #token_text = token['text']
                token_text = token.get('text', '')
                #token_lemma = token['lemma']
                token_lemma = token.get('lemma', '')
                #token_upos = token['upos']
                token_upos = token.get('upos', '')
                
                # Afficher les informations
                #print(f"Token: {token_text}\tLemma: {token_lemma}\tPOS: {token_upos}")
                # Formater et afficher les informations
                #print(f"{token_text}\t{token_lemma}\t{token_upos}")
                
                # Formater les informations
                line = f"{token_text}\t{token_lemma}\t{token_upos}\n"
                # Écrire la ligne dans le fichier
                f_out.write(line)





def main():
    # Définition des arguments en ligne de commande
    parser = argparse.ArgumentParser(description="Analyse d'un fichier texte avec Trankit")
    parser.add_argument("input_file", help="Chemin du fichier d'entrée à analyser")
    parser.add_argument("output_file", help="Chemin du fichier de sortie pour stocker les résultats")
    args = parser.parse_args()

    # Lire le contenu du fichier d'entrée
    with open(args.input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Traitement des données et écriture dans le fichier de sortie
    process_data_and_write_output(text, args.output_file)




if __name__ == "__main__":
    main()