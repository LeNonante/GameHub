from random import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os

cheminAssetsInsider="static/ressourcesJeux/Insider/assets/"

def LancerPartieInsider(NbJoueurs,code):
    """ Fonction qui lance une partie d'insider en créant les cartes et en renvoyant le role de chaque joueur en fonction de la manche"""
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
    fontMot = ImageFont.truetype("arial.ttf", 150)
    fontCode = ImageFont.truetype("arial.ttf", 24)

    for i in range(NbJoueurs):
        ImageFondTraitre=Image.open("assets/Insider/assets/cartes/TraitreVierge.png")
        drawTraitre = ImageDraw.Draw(ImageFondTraitre)
        ImageFondSafe=Image.open("assets/Insider/assets/cartes/SafeVierge.png")
        drawSafe = ImageDraw.Draw(ImageFondSafe)
        ImageFondMaitre=Image.open("assets/Insider/assets/cartes/MaitreVierge.png")
        drawMaitre = ImageDraw.Draw(ImageFondMaitre)

        #On creer la liste des roles (Nombre de safe + 1 traitre)
        listeRoles=["Safe"]*(NbJoueurs-2)
        listeRoles.append("Traitre")
        shuffle(listeRoles)
        listeRoles.insert(i,"Maitre")
        DicoInfoManche[i]=(listeRoles,ListeMots[i])

        #On genere chaque cartes
        _, _, w, h = drawTraitre.textbbox((0, 0), ListeMots[i], font=fontMot) #On calcule la taille du texte
        drawTraitre.text(((1920-w)/2, 830), ListeMots[i], (0,0,0), font=fontMot)#On ecrit les mots sur les deux cartes
        drawMaitre.text(((1920-w)/2, 830), ListeMots[i], (0,0,0), font=fontMot)

        #On ecrit le code et le num de la manche sur chaque carte
        drawMaitre.text((0,0), code+"-"+str(i+1), (0,0,0), font=fontCode)
        drawTraitre.text((0,0), code+"-"+str(i+1), (0,0,0), font=fontCode)
        drawSafe.text((0,0), code+"-"+str(i+1), (0,0,0), font=fontCode)

        #On l'enregistre
        ImageFondTraitre.save("assets/Insider/assets/cartes/Traitre"+code+str(i)+".png","PNG")
        ImageFondMaitre.save("assets/Insider/assets/cartes/Maitre"+code+str(i)+".png","PNG")
        ImageFondSafe.save("assets/Insider/assets/cartes/Safe"+code+str(i)+".png","PNG")
    return DicoInfoManche


def CleanPartieInsider(NbJoueurs, code):
    """Supprime toutes les cartes d'une partie"""
    try :
        for i in range(NbJoueurs):
            os.remove("assets/Insider/assets/cartes/Safe"+code+str(i)+".png")
            os.remove("assets/Insider/assets/cartes/Maitre"+code+str(i)+".png")
            os.remove("assets/Insider/assets/cartes/Traitre"+code+str(i)+".png")

    #Si les fichiers sont introuvables, on passe
    except FileNotFoundError:
        pass

