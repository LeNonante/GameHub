from random import *
import os

cheminAssetsInsider="static/ressourcesJeux/Insider/assets/"

def GenererPartieInsider(NbJoueurs):
    """ Fonction qui genere une partie d'insider en créant envoyant un dico de la forme :
    {Num manche : ([role J1, role J2, etc], MotManche1) """
    #On récupere et mélange les mots
    fichier = open(cheminAssetsInsider+"MOTS.txt",'r')
    lecture=fichier.readlines()
    fichier.close()
    shuffle(lecture)
    #On récup le nombre de mot necessaire pour chaque manche
    ListeMots=[]
    for i in range(NbJoueurs):
        ListeMots.append(lecture[i])
    #on genere les roles de chaque manche
    DicoInfoManche={}
    for i in range(NbJoueurs):
        #On creer la liste des roles (Nombre de safe + 1 traitre)
        listeRoles=["Safe"]*(NbJoueurs-2)
        listeRoles.append("Traitre")
        shuffle(listeRoles)
        listeRoles.insert(i,"Maitre")
        DicoInfoManche[i]=(listeRoles,ListeMots[i])
    return DicoInfoManche