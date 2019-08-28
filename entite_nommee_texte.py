def en_texte(mots):
   import os
   os.system("cd /home/mike/mXS")
   os.system("echo \""+mots+"\" | ./bin/tagEtapeModelPLOP.sh > /mnt/c/Users/miche/Desktop/entity.txt")
   file=open('/mnt/c/Users/miche/Desktop/entity.txt')
   texte_entite = str(file.read())
