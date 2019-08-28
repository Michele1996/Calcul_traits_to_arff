#! /usr/bin/env python3
import csv
import json
import sys
import re
import entite_nommee_texte
import nettoyage_texte
import pathlib as pa
import typing as ty
import rhinoscriptsyntax as rs
import torch
import Model
import spacy 

def smart_open(
    filename: str, mode: str = 'r', *args, **kwargs
) -> ty.Generator[ty.IO, None, None]:
    '''Open files and i/o streams transparently.'''
    if filename == '-':
        if 'r' in mode:
            stream = sys.stdin
        else:
            stream = sys.stdout
        if 'b' in mode:
            fh = stream.buffer  # type: ty.IO
        else:
            fh = stream
        close = False
    else:
        fh = open(filename, mode, *args, **kwargs)
        close = True

def main_entry_point(argv=None):
            filename = rs.OpenFileName("mention.json", filter)
            #Lecture du fichier json contenant les mentions
            if filename:
               with open(filename, 'r') as f:
                    results = json.load(f)
            i=0
            nlp = spacy.load("fr_core_news_md")
            #On initialise le model de udpipe pour le francais
            model = Model.Model('/mnt/c/Users/miche/Desktop/french-sequoia-ud-2.0-170801.udpipe')
            case=None
            lemma=""
            #On ouvre le fichier contenant le texte brut
            file = open('/mnt/c/Users/miche/Desktop/monfichier2.txt',encoding='latin-1',errors='ignore')
            #On ouvre aussi le fichier arff et on lui inscrit l'intete
            b = open("/mnt/c/Users/miche/Desktop/dete.arff", 'a', encoding='latin-1')
            list_of_list_data=[]
            import arff
            Stringa_comparaison=""
            Stringa_comparaison1=""
            uma1=""
            tk=0
            fi=None
            fo=None
            tktext=0
            #On lit le fichier et on cree la liste des phrases separées par un point
            lines=str(file.read())
            mots=lines
            list=lines.split(".")
            con = 0
            no=None
            texte_nettoye=""
            o=0
            
            u=0
            # On prende les mentions avec leur contexte droit et gauche"""
            res = results.copy()
            mention2=""
            nettoyage(results,texte_nettoye)
               
            for row in results:
                calcul_traits_non_rel(row,Stringa_comparaison)
                #On va faire la meme chose pour chaque couple de mentions. Donc mention1, mention2, mention1, mention3 ectt, double for
                for row2 in res:
                    calcul_traits_non_rel(row2, Stringa_comparaison1)
                    inc_rate=0
                    sub_form=""
                    dis_men=0
                    id_form=""
                    dis_phrase=0
                    dis_char=0
                    calcul_trait_rel(Stringa_comparaison, Stringa_comparaison1,inc_rate,sub_form,dis_men,id_form,dis_phrase,dis_char)
                    with smart_open("/mnt/c/Users/miche/Desktop/det.json", 'a', encoding='latin-1') as g :
                         data={"mention":[{"mention" : mention2 , "Entité Nommée": en ,"Gendre": gn ,"Nombre": num ,"GP": gp}]}
                     
                         json.dump(data,g,ensure_ascii=False, indent=4)
                         traits=[gn1,gn,en1,en,num1,num,gp1,gp,id_form, sub_form,inc_rate,dis_men,dis_phrase, dis_char]
                         list_of_list_data.append(traits)
                         
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
                         'data': list_of_list_data,
                       }                  
                arff.dumps(obj)  

if __name__ == '__main__':
    main_entry_point()