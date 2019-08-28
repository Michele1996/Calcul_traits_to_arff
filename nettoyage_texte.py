def nettoyage(results, texte_nettoye):
    for row1 in results:
        save=" "
        # mention2 sera la seule mention. row1 est la mention dans son context, donc on cherche a avoir row[content] qui est la mention en lui enlevant les caracteres superflues """
        mention2= str(row1['content']).replace('[','').replace(']','').replace('\'','').replace(',','').replace('<start>','').replace('<end>','').replace('\"','').replace("\"m\" ","m'").replace("\"qu\" il","qu'il").replace("\"l\" ","l'").replace("  "," ").replace("\"d\" ","d'").replace("\"n\" ","n'").replace("m ","m'").replace("d ","d'").replace("l ","l'").replace("qu  ","qu'").replace("-","")
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
            #Result est donc la mention reconstruite"""
            mention2=result
                
           if mention2 in "":
              mention2="-------------"
           if mention2=="m":
              mention2="m'"
           if mention2 in "n":
              mention2=="n'"
           if mention2 =="en":
              mention2=" en "
                
           control="#"+str(tktext)
          # On etiquette les mentions trouvees avec un #plus un nombre"""
           if mention2 in lines:
                   
              uma3=mention2+"#"+str(tktext)
              lines=lines.replace(mention2,uma3,1)
              op=lines.find(uma3)
              si=si+lines[:op]
              lines=lines[op:]
                   
              tktext=tktext+1
           elif mention2 in lines.replace("#"+str(tktext-1),""):
              ti =mention2.split(" ")
              for ti2 in ti:
                  if ti2 in mention2:
                     o=o+1
                  if o==len(ti):
                     lines.find(ti2)
                     lines=lines.replace(ti2,ti2+control)
                     tktext=tktext+1
            
           texte_nettoye=texte_nettoye+lines