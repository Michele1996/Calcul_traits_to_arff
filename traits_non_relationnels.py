def calcul_traits_non_rel(row, Stringa_comparaison):
                mention2= str(row['content']).replace('[','').replace(']','').replace('\'','').replace(',','').replace('<start>','').replace('<end>','').replace('\"','').replace("\"m\" ","m'").replace("\"qu\" il","qu'il").replace("\"l\" ","l'").replace("  "," ").replace("\"d\" ","d'").replace("\"n\" ","n'").replace("m ","m'").replace("d ","d'").replace("l ","l'").replace("qu  ","qu'").replace("-","")
                mention2= mention2.replace("*","\'")
                sen = []
                bool=False
                sen.append(mention2[0])       # put first letter in list. First letter doesn't need a space.
                for char in mention2[1::]:         # begin iteration after first letter
                   if char.islower():
                      sen.append(char) # if character is lower add to list
                   elif char.isupper():
                      if bool== True:
                         sen.append("\'") # then add the upper case character to list 
                         sen.append(char) # then add the upper case character to list  
                      else:
                         sen.append("-") # if character is upper add a space to list
                         sen.append(char) # then add the upper case character to list 
                   elif char==" ":
                      sen.append(" ")
                   elif char=="\'":
                      bool=True  
                   result = ''.join(sen)    # use () join to convert the list to a string
                mention2=result
                #On donc a nouveau une etiquette a les mentions et on les cherches dans le texte etiquetté
                #mention2 sera la mention, uma22 la mention etiquetté et uma1 la phrase qui contient la mention
                if mention2!="":
                   mention2_etiquette=mention2+"#"+str(tk)
                   
                   tk=tk+1
       	        for line in list:
                    if mention2 in line:
                       phrase_contenant_mention=line
                       list.remove(line)
                       fi=True
                    if fi:
                       break
                
                if mention2=="m":
                   mention2="m'"
                if mention2=="qu":
                   mention2="qu'"
               # On initialise gp a NO et on utilise udpipe pour tokenizer les mentions
                gp1 = "CASE=NO"
                sentences = model.tokenize(mention2)
                
                #on lance donc le parseur et le tagger de udpipe et on recuper les resultats dans un format matxin similaire a XML avec des balises.
                for s in sentences:
                   model.tag(s)
                   model.parse(s)
                
                conllu=model.write(sentences,"matxin")
                #On prends l'arborescence et on fait la tokenisation par que de la phrase avec la mention
               
                # Une fois trouvé la tete de la mention, on cherche dans la meme ligne , les elements: gendre nombre 
                #Pour le gp, on regarde les fils de l'element tete de la mention, si la ligne : "si=case" est trouvée alors la mention est dans un gp
                i1=0
                cas1=0
                
               
                i=0
                cas=0
                conllu = str(conllu).split("\n")
                kas=0
                en1 =""
                gn1=""
                num1=""
                el = texte_nettoye.find(mention2_etiquette)
                
                gm=model.tokenize(texte_nettoye[el-4:el+len(mention2_etiquette)])
                for n in gm:
                    model.tag(n)
                    model.parse(n)
                gm = model.write(gm,"matxin")
                gm=gm.split("\n")
                if case:
                  
                   for k in gm:
                         
                       if "si=\"root\"" in k:
                          kas=i1
                       
                      
                       if "si=\"case\"" in k and i1==(kas+1):
                          gp="CASE=YES"
                       
                       i1=i1+1
                
                texte=texte.replace("' ","'")
                #Pour l'entité nommée on reprends la mention etiquetté et on la recherche dans le texte etiquetté et passé a mXS : texte
                #On recherche la mention et on regarde a sa gauche pour trouver la balise <func>,<org> etc...
                Stringa_comparaison=mention2_etiquette
                uma5=mention2
                print(uma5)
                if "'" in uma5[:2]:
                   uma5=mention2[2:]
                if " " in uma5[:3]:
                   uma5=mention2[3:]
                elif " " in uma5[:4]:
                   uma5=mention2[4:]
                print(uma5)
                entity = texte.find(uma5)
                print(entity)
                ent=texte[entity-7:entity]
                print(ent)
                if "func" in ent:
                    en="FUNC"
                if "pers" in ent:
                    en="PERS"
                if "loc" in ent:
                    en="LOC"
                if "org" in ent:
                    en="ORG"
                if case:
                   if mention2 in stringa and str(con-1) in stringa:
                      gp="CASE=YES"
                for c in conllu:
                    ca=c.find("lem=")
                    lem=c[ca:].split(" ")
                    lemt=lem[0]
                    if '>' not in lemt:
                       
                       lemt1=lemt.split("=")
                       
                       if len(lemt1) > 1:
                          lemma=lemt1[1].replace("\"","")
                    if "si=\"root\"" in c:
                       cas=i
                      
                      
                       if 'Gender=Fem' in c:
                          gn="FEM"
                       if 'Gender=Masc' in c:
                          gn="MASC"
                       if 'Number=Sing' in c:
                          num="SING"
                       if 'Number=Plur' in c:
                          num="PLUR"
                    if "si=\"case\"" in c and i==(cas+1):
                       gp="CASE=YES"
                       stringa=mention2_etiquette
                       case=True
                    i=i+1
                        
               
                
                     
                
     
                
           
                
                #Une fois fait on enleve des metions les mentions non correctes, c'est a dire les mentions ou la tete est un verb ou une ponctoition
                doc1 = nlp(mention2)
                
                if mention2 == "":
                   mention2="aa"
                skip = None
                for token in doc1:
                    
                    if "PUNCT" in token.tag_ or ("VERB" in token.tag_ and "ROOT" in token.dep_):
                       skip = True
                  
                    
                       
                if skip:
                   row['left_context'] =""
                   row['content']=""
                   row['right_context']
                mention2=mention2.replace('é','e')
                #on ecris les resultats dans le fichier arff et dans le fichier json
                with smart_open("/mnt/c/Users/miche/Desktop/det.json", 'a', encoding='latin-1') as g :
                     data={"mention":[{"mention" : mention2 , "Entité Nommée": en1 ,"Gendre": gn1 ,"Nombre": num1 ,"GP": gp1}]}
                     
                     json.dump(data,g,ensure_ascii=False, indent=4)
                     
                    
                #On va faire la meme chose pour chaque couple de mentions. Donc mention1, mention2, mention1, mention3 ectt, double for
