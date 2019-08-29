#! /usr/bin/env python3
import csv
import json
import sys
import Model
import re
import entite_nommee_texte
import etiquettage_texte
import traits_non_relationnels
import traits_relationnels
import pathlib as pa
import typing as ty
import torch

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
            filename = "/mnt/c/Users/miche/Desktop/Stage/detectedT.json"
            #Lecture du fichier json contenant les mentions
            if filename:
               with open(filename, 'r') as f:
                    results = json.load(f)
            
            i=0
            
            #On ouvre le fichier contenant le texte brut
            file = open('/mnt/c/Users/miche/Desktop/monfichier2.txt',encoding='latin-1',errors='ignore')
            #On ouvre aussi le fichier arff et on lui inscrit l'intete
            b = open("/mnt/c/Users/miche/Desktop/dete.arff", 'a', encoding='latin-1')
            list_of_list_data=[]
            import arff
           
            tk=0
            
            #On lit le fichier et on cree la liste des phrases separées par un point
            lines=str(file.read())
            mots=lines
            list=lines.split(".")
            con = 0
            no=None
            texte_etiquette=""
            o=0
            texte_entite=""
            u=0

            en1 =""
            gn1=""
            num1=""
            gp1="CASE=NO"

            en =""
            gn=""
            num=""
            gp="CASE=NO"
            # On prende les mentions avec leur contexte droit et gauche"""
            res = results.copy()
            
            lis1=list.copy()
            mention2=""
            texte_etiquette=etiquettage_texte.etiquettage(results,lines)
            lis=texte_etiquette.split(".")
            sys_tag=""
            sys_tag1=""
            texte_entite=entite_nommee_texte.en_texte(mots)
            j=0
            from fuzzywuzzy import fuzz
            model = Model.Model('/mnt/c/Users/miche/Desktop/french-sequoia-ud-2.0-170801.udpipe')
            nlp = spacy.load("fr_core_news_md")
            for row in results:
                sys_tag=row["sys_tag"]
                list_traits_non_rel=traits_non_relationnels.calcul_traits_non_rel(nlp,model,row,list,texte_etiquette,texte_entite)
                if len(list_traits_non_rel[4])>0:
                   num=list_traits_non_rel[0]
                   gp=list_traits_non_rel[1]
                   en=list_traits_non_rel[2]
                   gn=list_traits_non_rel[3]
                   mention1_comparaison=list_traits_non_rel[4]+"#"+str(i)
                
                   print(sys_tag)
                   i=i+1
                   j=0
                   #On va faire la meme chose pour chaque couple de mentions. Donc mention1, mention2, mention1, mention3 ectt, double for
                   for row2 in res:
                       sys_tag1=row2["sys_tag"]
                       list_traits_non_rel1=traits_non_relationnels.calcul_traits_non_rel(nlp,model,row2,lis1,texte_etiquette,texte_entite)
                       if len(list_traits_non_rel1[4])>0:
                          num1=list_traits_non_rel1[0]
                          gp1=list_traits_non_rel1[1]
                          en1=list_traits_non_rel1[2]
                          gn1=list_traits_non_rel1[3]
                          mention2_comparaison=list_traits_non_rel1[4]+"#"+str(j)
                          j=j+1
                       
                          
                          list_traits_rel=traits_relationnels.calcul_trait_rel(fuzz,mention1_comparaison, mention2_comparaison,lis,texte_etiquette)
                          inc_rate=list_traits_rel[0]
                          sub_form=list_traits_rel[1]
                          dis_men=list_traits_rel[2]
                          id_form=list_traits_rel[3]
                          dis_phrase=list_traits_rel[4]
                          dis_char=list_traits_rel[5]
                          
                          traits=[gn1,gn,en1,en,num1,num,gp1,gp,id_form, sub_form,inc_rate,dis_men,dis_phrase, dis_char,sys_tag,sys_tag1]
                    
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
                          ('sys_tag',['PR','N']),
                          ('sys_tag1',['PR','N']),
                        ],
                         'data': list_of_list_data,
                       }                  
                
            arf=arff.dumps(obj)  
            b.write(arf)
                
if __name__ == '__main__':
    main_entry_point()