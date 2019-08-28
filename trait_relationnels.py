def calcul_trait_rel(Stringa_comparaison, Stringa_comparaison1,inc_rate,sub_form,dis_men,id_form,dis_phrase,dis_char):
                    
                    #Comparaison string si identique
                    if Stringa_comparaison == Stringa_comparaison1:
                       id_form='YES'
                    else:
                       id_form='NO'
                    comparaison = Stringa_comparaison.split('#')
                    comparaison1= Stringa_comparaison1.split('#')
                    #Calcul du trait distance en numb de mention grace aux etiquettes #1, #2 ect
                    dis_men= int(comparaison1[1])-int(comparaison[1])
                    kl=0
                    kl1=0
                    linea=0
                    linea1=0
                    #Calcul distance en phrase grace a la liste des phrase, on cherche les mentions dans les phrases
                    for line in list:
                        if Stringa_comparaison in line:
                           linea = kl
                        else:
                           kl=kl+1
                    for line1 in list:
                        if Stringa_comparaison in line1:
                           linea1 = kl1
                        else:
                           kl1=kl1+1
                    dis_phrase= linea1 - linea
                    #Calcul de la distance en char grace au texte etiquetté, on cherche la pos initiale de chaque mention
                    it = texte_nettoye.find(Stringa_comparaison1)
                    it1=texte_nettoye.find(Stringa_comparaison)
                    dis_char=it-it1
                    #Calcul trait subform, string in string
                    if Stringa_comparaison1 in Stringa_comparaison:
                       sub_form='YES'
                    else:
                       sub_form='NO'
                    #Calcul inc_rate grace au module fuzzy, calcul ratio mention in une autre mention
                    from fuzzywuzzy import fuzz
                    inc_rate=fuzz.ratio(Stringa_comparaison1, Stringa_comparaison)