# Calcul_traits_to_arff

Ce script prend en charge un fichier json contenant les mentions et leur context droit et gauche.
Un exemple de fichier json est disponible au  https://github.com/Michele1996/Projet/edit/master/mentions.json

Ce fichier a été crée a en donnant un texte brut (.txt) au détecteur de mentions crée par Loic Grobol http://lattice.cnrs.fr/Grobol-Loic
Le lien a son detecteur: https://github.com/Evpok/neural-end-to-end-coref.

Fonctionnement:

* Les mentions au debut sont des listes de mots: ['"le"','"stylo"',]  donc au debut on  rends la mention une string sans caracteres speciaux: le stylo

*Pour chaque mentions donc on cherche a calculer les traits:
 - GENDRE
 - NOMBRE
 - GROUP PREPOSITIONNEL
 - ENTITE NOMMEE
 - DISTANCE EN NOMBRE DE MOTS
 - DISTANCE EN NOMBRE DE CARACTERES
 - DISTANCE EN NOMBRE DE PHRASES
 - TAUX D'INCLUSION D'UN MENTION DANS L'AUTRE
 - SI ELLE SONT IDENTIQUES ID_FORM
 - SI UNE EST PARTIE DE L'AUTRE SUB_FORM


En considerant les mentions et les phrases ou la mentions est presente on etiquette le texte entier
On prends separement les mentions et on les etiquettes avec un # suivi d'un nombre de mention: ex la stylo#1

Une fois le texte entier etiquetté on passe le texte au script mXS , detecteur de entités nommées crée par Damien Nouvel http://damien.nouvels.net/fr/mxs:

 import os
            os.system("cd /home/mike/mXS")  #on change de directory pour etre dans la directory de mXS
            os.system("echo \""+mots+"\" | ./bin/tagEtapeModelPLOP.sh > /mnt/c/Users/miche/Desktop/entity.txt") #on utilise mXS on donnant le texte entier etiquetté et on le sauvegarde dans entity.txt
            b=open('/mnt/c/Users/miche/Desktop/entity.txt')

Ex:

Emmanuel Macron est a la maison

Apres Etiquettage: Emmanuel Macron#1 est a la maison#2

Apres mXS : <pers> Emmanuel Macron</pers>#1 est a la maison#2
En utilisant la tokenisation par phrases de UdPipe http://ufal.mff.cuni.cz/udpipe,  on decoupe le texte en phrases,  et en suite on tokenise par mots.

La tokenisation nous donne un format similaire au XML avec des balise:

<!ELEMENT    corpus     (SENTENCE*)>
<!ELEMENT    SENTENCE   (NODE*)>
<!ATTLIST    SENTENCE    ord           CDATA        #REQUIRED
                         alloc         CDATA        #REQUIRED>
<!ELEMENT    NODE   (NODE*)>
<!ATTLIST    NODE        ord           CDATA        #REQUIRED
                         alloc         CDATA        #REQUIRED
                         form          CDATA        #REQUIRED
                         lem           CDATA        #REQUIRED
                         mi            CDATA        #REQUIRED  #Contient Gendre et nombre
                         si            CDATA        #REQUIRED   #peut etre  'root', 'case' et 'det'
                         sub           CDATA        #REQUIRED>

Grace aux nodes ELEMENT Et les attributes mi  qui contient le Gendre, le Nombre et  si qui contient le role du mots ex: root ou case on sait quel mot est la tete de la mention, on regarde le contenu de mi pour savoir son gendre et son nombre.
Pour le trait GROUPE PREPOSITIONNEL on regarde les fils du mot où le 'si' est root, et dans le cas ou il y a un mot où le 'si' est 'case' alors la mention est dans un groupe prepositionnel.

Pour les Entité Nommées On recherche dans le texte etiquetté et passé a mXS en lui enlevant la balise fermant </..>, une fois trouvé on regarde les caracteres a gauche pour voir si il y a une entité nommée detectée et donc la quelle.

Une fois avoir fait ca et avoir stoquée la mention et ses 4 premiers traits , avec une boucle for on boucle sur la liste des mentions et on calcul les meme traits de facon a avoir des couples de mentions et traits. Pour chaque couple on va ensuite calculer les traits:

- DISTANCE EN NOMBRE DE MOTS
 - DISTANCE EN NOMBRE DE CARACTERES
 - DISTANCE EN NOMBRE DE PHRASES
 - TAUX D'INCLUSION D'UN MENTION DANS L'AUTRE
 - SI ELLE SONT IDENTIQUES ID_FORM
 - SI UNE EST PARTIE DE L'AUTRE SUB_FORM

Dont toutes sont calcules a partire de operations basilaires sur chaines , donc comparaison, chercher le debut de chaque mentions et trouver les distances en mots, phrases et caracteres sauf le taux d'inclusion qui est calculé grace au module fuzzywuzzy:

from fuzzywuzzy import fuzz
fuzz.ratio("this is a test", "this is a test!")
 96
 
Finalement une fois trouvé tous les traits on utilise le module liarc-arff pour ecrire le fichier arff :

obj = {
                          'description': u'mention',
                          'relation':"men",
                          'attributes': [
                          ('gn', ['MASC', 'FEM']),
                          ('gn1', ['MASC', 'FEM']),
                          ('num1', ['SING','PLUR']),
                          ('num', ['SING','PLUR']),
                          ('en', ['PERS','LOC','ORG','FUNC']),
                          ('en1', ['PERS','LOC','ORG','FUNC']),
                          ('gp', ['CASE=YES', 'CASE=NO']),
                          ('gp1', ['CASE=YES', 'CASE=NO']),
                          ('id_form',['YES','NO']),
                          ('subform',['YES','NO']),
                          ('inc_rate','REAL'),
                          ('dis_men','REAL'),
                          ('dis_phrase','REAL'),
                          ('dis_char','REAL'),
                        ],
                         'data': listoflist,
                       }                  
                arff.dumps(obj)
