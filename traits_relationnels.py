def calcul_trait_rel(fuzz,mention1_comparaison, mention2_comparaison,list,texte_etiquette):
                    inc_rate=0
                    sub_form=""
                    dis_men=0
                    id_form=""
                    dis_phrase=0
                    dis_char=0
                   
                    #Comparaison string si identique
                    if mention1_comparaison == mention2_comparaison:
                       id_form='YES'
                    else:
                       id_form='NO'
                    token_mention1=mention1_comparaison.split("#")
                    token_mention2=mention2_comparaison.split("#")
                    comparaison = token_mention1[0]+"#"+token_mention1[1]
                    comparaison1= token_mention2[0]+"#"+token_mention2[1]
                 
                    #Calcul du trait distance en numb de mention grace aux etiquettes #1, #2 ect
                    if len(comparaison1) >1 and len(comparaison) >1:
                       dis_men= int(token_mention1[1])-int(token_mention2[1])
                    
                    kl=0
                    kl1=0
                    linea=0
                    linea1=0
                    list1=list.copy()
                    #Calcul distance en phrase grace a la liste des phrase, on cherche les mentions dans les phrases
                    for line in list:
                        
                        if comparaison in line:
                           linea = kl
                           
                        
                        else:
                           kl=kl+1
                    for line1 in list1:
                        if comparaison1 in line1:
                           linea1 = kl1
                        else:
                           kl1=kl1+1
                    
                    dis_phrase= linea1 - linea
                    #Calcul de la distance en char grace au texte etiquetté, on cherche la pos initiale de chaque mention
                    it = texte_etiquette.find(comparaison)
                    it1=texte_etiquette.find(comparaison1)
                    dis_char=it-it1
                    #Calcul trait subform, string in string
                    if token_mention2[0] in token_mention1[0]:
                       sub_form='YES'
                    else:
                       sub_form='NO'
                    #Calcul inc_rate grace au module fuzzy, calcul ratio mention in une autre mention
                    
                    inc_rate=fuzz.ratio(token_mention2, token_mention1)
                    return [inc_rate,sub_form,dis_men,id_form,dis_phrase,dis_char]