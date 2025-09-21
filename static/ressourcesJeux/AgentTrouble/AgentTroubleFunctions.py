from random import randint, choices, shuffle
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
cheminAssetsAgentTrouble="static/ressourcesJeux/AgentTrouble/assets/"

class Joueur():
    """Définit chaque joueur"""
    def __init__(self,numLieu,role,numero):
        """Création du joueur en lui attribuant son role, lieu, adresse mail et lien de carte"""
        self.numLieu=numLieu
        if self.numLieu=="??":
            self.nomLieu="??"
        else :
            if len(InfosLieux[self.numLieu])==2: #Si on a pas de nom alternatif (que le lieu n'a pas d'accents donc que son nom est le même que son dans le nom de fichier)
                self.nomLieu=InfosLieux[self.numLieu][0] 
            else :
                self.nomLieu=InfosLieux[self.numLieu][2] #Si un nom alternatif, on prend celui avec accents


        self.role=role
        self.num=numero
        if self.role=="ESPION" :
            self.carte=cheminAssetsAgentTrouble+"CartesJoueurs/Agent2.jpg"
        else :
            #On construit le lien de la carte grace aux infos du joueur
            texte1=InfosLieux[self.numLieu][0]
            texte2=self.role.replace("'", " ")
            texte2=texte2.replace("é", "e")
            texte2=texte2.replace("è", "e")
            texte2=texte2.replace("-", " ")
            self.carte=texte1+"_"+texte2
            self.carte=cheminAssetsAgentTrouble+"CartesJoueurs/"+self.carte+".png"

    def getInfos(self):
        return self.num, (self.nomLieu, self.role, self.carte)


    def test(self):
        print(self.nomLieu, self.role, self.num)


class Plateau():
    """Classe qui gère le plateau"""
    def __init__(self,lieux,code):
        #Contiendra les 30 cartes des lieux a afficher
        self.lieux=lieux
        self.ImageFond=Image.open(cheminAssetsAgentTrouble+"Plateau.png")

        self.coordsY={  4:10, 3:440, 2:870, 1:1300, 0:1730} #Contient les coordonées Y des endroits du plateau ou placer le lieu en fonction de du quotient de sa divition par 6
        self.coordsX={  5:58, 4:688, 3:1318, 2:1948, 1:2578, 0:3208} #Contient les coordonées X des endroits du plateau ou placer le lieu en fonction de son numéro modulo 5

        for i in lieux:
            #On recupere l'image de la carte
            carte = Image.open(cheminAssetsAgentTrouble+"CartePlateau/"+str(i)+".png")
            #On la redimesionne pour l'image
            carte_redimensionnee = carte.resize((575, 420))
            #On retrouve les coordonnées de la carte et la colle sur le plateau
            x= self.coordsX[i%6]
            y= int(self.coordsY[i//6])
            self.ImageFond.paste(carte_redimensionnee, (x, y), carte_redimensionnee)
            #On écrit le code
            #fontCode = ImageFont.truetype("arial.ttf", 24)
            #draw = ImageDraw.Draw(self.ImageFond)
            #draw.text((0, 0),code,(0,0,0),font=fontCode)

        #On enregistre l'image
        #self.ImageFond.save(cheminAssetsAgentTrouble+"temp/Plateau_"+code+".png","PNG")
        #On transforme l'image en bytes pour l'enregistrer en BLOB dans la DB
        buffer = BytesIO()
        self.ImageFond.save(buffer, format="PNG")
        self.image_bytes = buffer.getvalue()
    
    def getBytes(self):
        return self.image_bytes
        

    def placer(self,liste):
        """Reset le plateau et place les cartes de la liste en paramètre"""
        self.reset()
        for i in liste:
            self.cartes[i].label.place( x= int(self.coordsX[i%6])*ratio , y= int(self.coordsY[i//6])*ratio)




class Manche():
    """Clase qui gère chaque manche"""

    def __init__(self,nbJoueurs,code,nombrelieux):
        #On recupere le code
        self.code=code

        #On melange les numéros de lieux et récupère les N premiers (N=Nombre de lieux) pour avoir un plateau aléatoire
        self.lieux=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,28, 29]
        shuffle(self.lieux)
        self.lieux=self.lieux[:nombrelieux]
        #On prend un lieu aléatoire dans la liste pour le lieu de la manche
        self.lieu=self.lieux[randint(0,nombrelieux-1)]

        #On creer la liste et crrer les objest joueurs
        self.joueurs=[]
        self.espion=randint(0,nbJoueurs-1) #On choisi le joueurs espion

        #on recupere les roles liés au lieu et les mélange
        self.roles=InfosLieux[self.lieu][1]
        shuffle(self.roles)

        #Pour les joueurs avant l'espion
        for i in range(self.espion):
            #On crée les objets joueurs et ecrit dans les logs
            self.joueurs.append(Joueur(self.lieu,self.roles[i],i))

        #On creer l'objet joueur de l'espion et ecrit les logs
        self.joueurs.append(Joueur("??","ESPION",self.espion))

        #Pour les joueurs avant l'espion
        for i in range(self.espion+1,nbJoueurs):
            #On crée les objets joueurs et ecrit dans les logs
            self.joueurs.append(Joueur(self.lieu,self.roles[i-1],i))

        self.plateau = Plateau(self.lieux,self.code)
        self.plateauBytes = self.plateau.getBytes()

    def getInfos(self):
        dicoInfos={}#Dico de la forme numJoueur : (lieu, role, carte)
        for j in self.joueurs :
            num, infos = j.getInfos()
            dicoInfos[num]=infos
        return dicoInfos
    
    def getPlateau(self):
        return self.plateauBytes
    
    def test(self):
        """Fonction de test qui affiche les elements de la manche"""
        print(self.code, self.lieu,self.espion,self.roles)
        for i in self.joueurs:
            i.test()

#de la forme : numLieu : [NomLieu, [Roles], NomLieuAvecAccents (optionnel)]
InfosLieux={0:["Zoo",["Soigneur","Visiteur","Dompteur","Fauconnier","Chef animalier","Veterinaire","Animateur"],"Zoo"],
            1:["Universite",["Professeur","Etudiant","Agent d'entretient","Chercheur","Directeur","Infirmière","Bibliothécaire"],"Université"],
            2:["Train",["Controlleur","Voyageur sans ticket","Conducteur","Technicien","Agent de nettoyage","Passager de 1ère classe","Passager de 2nd classe"],"Train"],
            3:["Theatre",["Comédien","Spectateur","Responsable Lumières","Responsable Son","Technicien","Metteur en scène","Accessoiriste"],"Théâtre"],
            4:["Centre de Thalasso",["Masseur","Maitre nageur","Client","Estheticien","Kinésithérapeute","Diététicien","Réceptionniste"],"Centre de Thalasso"],
            5:["Supermarche",["Caissier","Client","Directeur","Voleur","Agent d'entretient","Agent de sécurité","Fournisseur"],"Supermarché"],
            6:["Studio de cinema",["Acteur","Réalisateur","Producteur","Cascadeur","Doublure","Costumier","Chef décorateur"],"Studio de cinéma"],
            7:["Station Polaire",["Scientifique","Chef d'expedition","Technicien","Electricien","Plombier","Biologiste","Veterinaire"]],
            8:["Station Spatiale",["Astronaute","Technicien","Astronome","Electricien","Pilote","Soudeur","Chef communication"]],
            9:["Sous marin",["Soldat","Mecanicien","Technicien","Cuisinier","Navigateur","Meteorologiste","Plongeur"],"Sous-marin"],
            10:["Restaurant",["Serveur","Client","Chef","Critique culinaire","Livreur","Barman","Sommelier"]],
            11:["Poste de police",["Policier","Prisonnier","Procureur","Lieutenant","Secrétaire","Inspecteur","Médecin légiste"]],
            12:["Plage",["Touriste","Vendeur ambulant","Barman","Animateur de club","Moniteur de ski nautique","Surfeur","Plongeur"]],
            13:["Parc d attraction",["Visiteur","Opérateur de manège","Technicien de maintenance","nettoyage","Mascotte","Cuisinier","Caissier"],"Parc d'attraction"],
            14:["Pacquebot",["Capitaine","Passager clandestin","Passager de 1ère classe","Passager de 2nd classe","Pecheur","Naufragé seccouru","Scientifique"]],
            15:["Hotel",["Directeur","Client","Réceptionniste","Agent d'entretient","Cuisinier","Barman","Bagagiste"],"Hôtel"],
            16:["Hopital",["Médecin chef","Patient","Urgentiste","Cardiologue","Sage femme","Cuisinier","Agent de maintenance"],"Hôpital"],
            17:["Garage",["Apprenti","Gérant","Client","Technicien en pneumatique","Carrossier","Vendeur automobile","Fournisseur d'huile"]],
            18:["Fete d entreprise",["PDG","Stagiaire","Apprenti","Alternant","Assistant administratif","Secrétaire","Salarié licencié"],"Fête d'entreprise"],
            19:["Ecole",["Eleve","Professeur","Infirmière","Directeur","Agent d'entretient","Responsable cantine","Remplacant"]],
            20:["Croisades",["Chevalier","Archer","Ecuyer","Paysan","Garde","Seigneur","Prêtre"]],
            21:["Casino",["Croupier","Joueur gagnant","Joueur perdant","Tricheur","Directeur","Responsable sécurité","Banquier"]],
            22:["Carnaval",["Déguisé en loup","Déguisé en Mousquetaire","Déguisé en Pirate","Déguisement oublié","Déguisé en Super-Héros","Déguisé en Obélix","Déguisé en table-basse"]],
            23:["Boite de nuit",["Videur","DJ","Danseur","Barman","Client Bourré","Client","Responsable Lumières"]],
            24:["Bateau pirate",["Capitaine","Matelot","Cuisinier","Maitre Artilleur","Chef de la carte au trésor","Prisonnier","Gérant des voiles"]],#??
            25:["Base militaire",["Colonel","Pilote d'avion","Maitre-chien","Chauffeur Poids-Lourd","Opérateur réseau","Infirmière","Assistant administratif"]],
            26:["Banque",["Directeur","Client","Conseiller","Analyste financier","Client dans le rouge","Trader","Guichetier"]],
            27:["Avion",["Pilote","Co-pilote","Passager","Stewart","Hotesse de l'air","Agent de vente","Préparateur des plateaux repas"]],
            28:["Ambassade",["Ambassadeur","Secrétaire","Correspondant informatique","attaché de défense","conseiller économique","Conseiller culturel","Conseiller scientifique"]],
            29:["Cirque",["Acrobate","Magicien","Dompteur de tigre","Clown","Responsable billeterie","Cavalier","Jongleur"]],
}


def genererPartieAgentTrouble(NbJoueurs,NbLieux,code):
    """Fonction qui lance une manche"""
    #On creer la manche
    manche=Manche(NbJoueurs, code, NbLieux)
    imagePlateau=manche.getPlateau()
    return manche.getInfos(), imagePlateau