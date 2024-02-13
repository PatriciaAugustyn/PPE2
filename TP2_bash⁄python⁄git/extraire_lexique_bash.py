import sys

def lecture_corpus(fichiers):
    contenu = []
    for fichier in fichiers:
        try:
            with open(fichier, "r", encoding='utf-8') as doc:
                lecture = doc.read()
                contenu.append(lecture)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {fichier}: {e}")
    return contenu

def lire_contenu():
    for ligne in sys.stdin:
        print(ligne.strip())

def chemins_vers_fichiers():
    chemins = sys.stdin.read().strip().split('\n')
    for chemin in chemins:
        print(chemin)

def main():
    # Vérifie si au moins une option est passée
    if len(sys.argv) < 2:
        print("L'utilisation de ce programme : python3 extraire_lexique_bash.py <option> [corpus]")
        print("--choix1 : python3 extraire_lexique_bash.py --choix1 Corpus/*.txt")
        print("--choix2 : cat Corpus/*.txt | python3 extraire_lexique_bash.py --choix2")
        print("--choix3 :  ls Corpus/*.txt | python extraire_lexique_bash.py --choix3")

        sys.exit(1)
    option = sys.argv[1]

    if option == '--choix1':
        fichiers = sys.argv[2:]
        if not fichiers:
            print("Erreur: Aucun fichier spécifié pour l'option --choix1")
            sys.exit(1)
        contenu = lecture_corpus(fichiers)
        for texte in contenu:
            print(texte)
    elif option == '--choix2':
        lire_contenu()
    elif option == '--choix3':
        chemins_vers_fichiers()
    else:
        print("Les options possibles sont '--choix1', '--choix2' et '--choix3'")
        sys.exit(1)

if __name__ == "__main__":
    main()
