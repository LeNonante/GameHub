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
            if len(InfosLieux[self.numLieu])==2:
                self.nomLieu=InfosLieux[self.numLieu][0]
            else :
                self.nomLieu=InfosLieux[self.numLieu][2]


        self.role=role
        self.num=numero
        if self.role=="ESPION" :
            self.carte="https://i.ibb.co/pyRJh7D/Agent.jpg"
        else :
            #On construit le lien de la carte grace aux infos du joueur
            texte1=InfosLieux[self.numLieu][0]
            texte2=self.role.replace("'", " ")
            texte2=texte2.replace("é", "e")
            texte2=texte2.replace("è", "e")
            texte2=texte2.replace("-", " ")
            self.carte=texte1+"-"+texte2
            self.carte=DicoLiensCartes[self.carte]

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

DicoLiensCartes={
    'Ambassade-Ambassadeur':'https://iili.io/dugrNLv.png',
    'Ambassade-Conseiller culturel':'https://iili.io/dugreBR.png',
    'Ambassade-Conseiller scientifique':'https://iili.io/dugrk1p.png',
    'Ambassade-Correspondant informatique':'https://iili.io/dugrvrN.png',
    'Ambassade-Secretaire':'https://iili.io/dugrU7t.png',
    'Ambassade-attache de defense':'https://iili.io/dugrgkX.png',
    'Ambassade-conseiller economique':'https://iili.io/dugrrpn.png',
    'Avion-Agent de vente':'https://iili.io/dugr6Is.png',
    'Avion-Co pilote':'https://iili.io/dugrPhG.png',
    'Avion-Hotesse de l air':'https://iili.io/dugriQf.png',
    'Avion-Passager':'https://iili.io/dugrQEl.png',
    'Avion-Pilote':'https://iili.io/dugrZ42.png',
    'Avion-Preparateur des plateaux repas':'https://iili.io/dugrD2S.png',
    'Avion-Stewart':'https://iili.io/dugrbY7.png',
    'Banque-Analyste financier':'https://iili.io/dugrmv9.png',
    'Banque-Client':'https://iili.io/dugrppe.png',
    'Banque-Client dans le rouge':'https://iili.io/dug49Tu.png',
    'Banque-Conseiller':'https://iili.io/dug4Hhb.png',
    'Banque-Directeur':'https://iili.io/dug4JQj.png',
    'Banque-Guichetier':'https://iili.io/dug42Cx.png',
    'Banque-Trade':'https://iili.io/dug43EQ.png',
    'Base militaire-Assistant administratif':'https://iili.io/dug4f3B.png',
    'Base militaire-Chauffeur Poids Lourd':'https://iili.io/dug4qYP.png',
    'Base militaire-Colonel':'https://iili.io/dug4Bv1.png',
    'Base militaire-Infirmiere':'https://iili.io/dug4CyF.png',
    'Base militaire-Maitre chien':'https://iili.io/dug4oTg.png',
    'Base militaire-Operateur reseau':'https://iili.io/dug4xja.png',
    'Base militaire-Pilote d avion':'https://iili.io/dug4zZJ.png',
    'Bateau pirate-Capitaine':'https://iili.io/dug4TCv.png',
    'Bateau pirate-Chef de la carte au tresor':'https://iili.io/dug4A4p.png',
    'Bateau pirate-Cuisinier':'https://iili.io/dug453N.png',
    'Bateau pirate-Gerant des voiles':'https://iili.io/dug47aI.png',
    'Bateau pirate-Maitre Artilleur':'https://iili.io/dug4Yvt.png',
    'Bateau pirate-Matelot':'https://iili.io/dug4ayX.png',
    'Bateau pirate-Prisonnier':'https://iili.io/dug4lun.png',
    'Boite de nuit-Barman':'https://iili.io/dug40js.png',
    'Boite de nuit-Client':'https://iili.io/dug41ZG.png',
    'Boite de nuit-Client Bourre':'https://iili.io/dug4Gnf.png',
    'Boite de nuit-DJ':'https://iili.io/dug4MG4.png',
    'Boite de nuit-Danseur':'https://iili.io/dug4XF2.png',
    'Boite de nuit-Responsable Lumieres':'https://iili.io/dug4haS.png',
    'Boite de nuit-Videur':'https://iili.io/dug4j87.png',
    'Carnaval-Deguise en Mousquetaire':'https://iili.io/dug4N99.png',
    'Carnaval-Deguise en Obelix':'https://iili.io/dug4Oue.png',
    'Carnaval-Deguise en Pirate':'https://iili.io/dug4ewu.png',
    'Carnaval-Deguise en SUper Heros':'https://iili.io/dug4kZb.png',
    'Carnaval-Deguise en loup':'https://iili.io/dug48nj.png',
    'Carnaval-Deguise en table basse':'https://iili.io/dug4SMx.png',
    'Carnaval-Deguisement oublie':'https://iili.io/dug4rFV.png',
    'Casino-Banquier':'https://iili.io/dug44cB.png',
    'Casino-Croupier':'https://iili.io/dug4i91.png',
    'Casino-Directeur':'https://iili.io/dug4sAF.png',
    'Casino-Joueur gagnant':'https://iili.io/dug4Lwg.png',
    'Casino-Joueur perdant':'https://iili.io/dug4toJ.png',
    'Casino-Responsable securite':'https://iili.io/dug4DMv.png',
    'Casino-Tricheur':'https://iili.io/dug4bPR.png',
    'Centre de Thalasso-Client':'https://iili.io/dug4pFp.png',
    'Centre de Thalasso-Dieteticien':'https://iili.io/dug4ycN.png',
    'Centre de Thalasso-Estheticien':'https://iili.io/dug69SI.png',
    'Centre de Thalasso-Kinesitherapeute':'https://iili.io/dug6J9t.png',
    'Centre de Thalasso-Maitre nageur':'https://iili.io/dug63ts.png',
    'Centre de Thalasso-Masseur':'https://iili.io/dug6CKl.png',
    'Centre de Thalasso-Receptionniste':'https://iili.io/dug6zH7.png',
    'Cirque-Acrobate':'https://iili.io/dug6IR9.png',
    'Cirque-Cavalier':'https://iili.io/dug6uDu.png',
    'Cirque-Clown':'https://iili.io/dug67ix.png',
    'Cirque-Dompteur de tigre':'https://iili.io/dug6lUB.png',
    'Cirque-Jongleur':'https://iili.io/dug6GOF.png',
    'Cirque-Magicien':'https://iili.io/dug6XWJ.png',
    'Cirque-Responsable billeterie':'https://iili.io/dug6wfR.png',
    'Croisades-Archer':'https://iili.io/dug6OUN.png',
    'Croisades-Chevalier':'https://iili.io/dug6vRt.png',
    'Croisades-Ecuyer':'https://iili.io/dug6gxs.png',
    'Croisades-Garde':'https://iili.io/dug64sf.png',
    'Croisades-Paysan':'https://iili.io/dug6sg2.png',
    'Croisades-Prêtre':'https://iili.io/dug6Z57.png',
    'Croisades-Seigneur':'https://iili.io/dug6Dbe.png',
    'Ecole-Agent d entretient':'https://iili.io/dug6ysj.png',
    'Ecole-Directeur':'https://iili.io/dugPJ0Q.png',
    'Ecole-Eleve':'https://iili.io/dugP3dB.png',
    'Ecole-Infirmiere':'https://iili.io/dugPKe1.png',
    'Ecole-Professeur':'https://iili.io/dugPnLJ.png',
    'Ecole-Remplacant':'https://iili.io/dugPIgp.png',
    'Ecole-Responsable cantine':'https://iili.io/dugPA7I.png',
    'Fete d entreprise-Alternant':'https://iili.io/dugPRet.png',
    'Fete d entreprise-Apprenti':'https://iili.io/dugPcLG.png',
    'Fete d entreprise-Assistant administratif':'https://iili.io/dugP0Bf.png',
    'Fete d entreprise-PDG':'https://iili.io/dugPErl.png',
    'Fete d entreprise-Salarie licencie':'https://iili.io/durFiZb.png',
    'Fete d entreprise-Scretaire':'https://iili.io/dugPXp9.png',
    'Fete d entreprise-Stagiaire':'https://iili.io/dugPwhu.png',
    'Garage-Apprenti':'https://iili.io/dugPeBj.png',
    'Garage-Carrosier':'https://iili.io/dugPvrQ.png',
    'Garage-Client':'https://iili.io/dugPS2V.png',
    'Garage-Fournisseur d huile':'https://iili.io/dugPgkP.png',
    'Garage-Gerant':'https://iili.io/durFPwu.png',
    'Garage-Technicien en pneumatique':'https://iili.io/dugPiQa.png',
    'Garage-Vendeur automobile':'https://iili.io/dugPZ4R.png',
    'Hopital-Agent de maintenance':'https://iili.io/dugPbYN.png',
    'Hopital-Cardiologue':'https://iili.io/dugi9TX.png',
    'Hopital-Cuisinier':'https://iili.io/dugiHjn.png',
    'Hopital-Medecin chef':'https://iili.io/dugi2CG.png',
    'Hopital-Patient':'https://iili.io/dugiF44.png',
    'Hopital-Sage femme':'https://iili.io/dugiqa2.png',
    'Hopital-Urgentiste':'https://iili.io/dugiCy7.png',
    'Hotel-Agent d entretient':'https://iili.io/dugixje.png',
    'Hotel-Bagagiste':'https://iili.io/dugiTCb.png',
    'Hotel-Barman':'https://iili.io/dugiuGj.png',
    'Hotel-Client':'https://iili.io/dugiA6x.png',
    'Hotel-Cuisinier':'https://iili.io/dugi53Q.png',
    'Hotel-Directeur':'https://iili.io/dugi7aV.png',
    'Hotel-Receptionniste':'https://iili.io/dugiY8B.png',
    'Pacquebot-Capitaine':'https://iili.io/dugiayP.png',
    'Pacquebot-Naufrage seccouru':'https://iili.io/dugilu1.png',
    'Pacquebot-Passager clandestin':'https://iili.io/dugi0wF.png',
    'Pacquebot-Passager de 1ere classe':'https://iili.io/dugi1Zg.png',
    'Pacquebot-Passager de 2nd classe':'https://iili.io/dugiGna.png',
    'Pacquebot-Pecheur':'https://iili.io/dugiMMJ.png',
    'Pacquebot-Scientifique':'https://iili.io/dugiV6v.png',
    'Parc d attraction-Caissier':'https://iili.io/dugihap.png',
    'Parc d attraction-Cuisinier':'https://iili.io/dugij8N.png',
    'Parc d attraction-Mascotte':'https://iili.io/dugiN9I.png',
    'Parc d attraction-Operateur de manege':'https://iili.io/dugiOut.png',
    'Parc d attraction-Technicien de maintenance':'https://iili.io/dugiewX.png',
    'Parc d attraction-Visiteur':'https://iili.io/dugi8ns.png',
    'Parc d attraction-nettoyage':'https://iili.io/dugiSMG.png',
    'Plage-Animateur de club':'https://iili.io/dugiUPf.png',
    'Plage-Barman':'https://iili.io/dugirF4.png',
    'Plage-Moniteur de ski nautique':'https://iili.io/dugi6S2.png',
    'Plage-Plongeur':'https://iili.io/dugii9S.png',
    'Plage-Surfeur':'https://iili.io/dugisA7.png',
    'Plage-Touriste':'https://iili.io/dugiLN9.png',
    'Plage-Vendeur ambulant':'https://iili.io/dugiQte.png',
    'Poste de police-Inspecteur':'https://iili.io/dugitou.png',
    'Poste de police-Lieutenant':'https://iili.io/dugiDMb.png',
    'Poste de police-Medecin legiste':'https://iili.io/dugibPj.png',
    'Poste de police-Policier':'https://iili.io/dugipKx.png',
    'Poste de police-Prisonnier':'https://iili.io/dugiycQ.png',
    'Poste de police-Procureur':'https://iili.io/dugs9SV.png',
    'Poste de police-Secretaire':'https://iili.io/dugsJHB.png',
    'Restaurant-Barman':'https://iili.io/dugsdAP.png',
    'Restaurant-Chef':'https://iili.io/dugs3DF.png',
    'Restaurant-Client':'https://iili.io/dugsKog.png',
    'Restaurant-Critique culinaire':'https://iili.io/dugsfVa.png',
    'Restaurant-Livreur':'https://iili.io/dugsqiJ.png',
    'Restaurant-Serveur':'https://iili.io/dugsnlR.png',
    'Restaurant-Sommelier':'https://iili.io/dugsTNt.png',
    'Sous marin-Cuisinier':'https://iili.io/dugsuDX.png',
    'Sous marin-Mecanicien':'https://iili.io/dugs5Vs.png',
    'Sous marin-Meteorologiste':'https://iili.io/dugs7iG.png',
    'Sous marin-Navigateur':'https://iili.io/dugsaff.png',
    'Sous marin-Plongeur':'https://iili.io/dugscl4.png',
    'Sous marin-Soldat':'https://iili.io/dugs1J2.png',
    'Sous marin-Technicien':'https://iili.io/dugsERS.png',
    'Station Polaire-Biologiste':'https://iili.io/dugsGO7.png',
    'Station Polaire-Chef d expedition':'https://iili.io/dugsMb9.png',
    'Station Polaire-Electricien':'https://iili.io/dugsWxe.png',
    'Station Polaire-Plombier':'https://iili.io/dugshib.png',
    'Station Polaire-Scientifique':'https://iili.io/dugswfj.png',
    'Station Polaire-Technicien':'https://iili.io/dugsN0x.png',
    'Station Polaire-Veterinaire':'https://iili.io/dugskJV.png',
    'Station Spatiale-Astronaute':'https://iili.io/dugsv5B.png',
    'Station Spatiale-Astronome':'https://iili.io/dugs8OP.png',
    'Station Spatiale-Chef communication':'https://iili.io/dugsSb1.png',
    'Station Spatiale-Electricien':'https://iili.io/dugsrWg.png',
    'Station Spatiale-Pilote':'https://iili.io/dugs4sa.png',
    'Station Spatiale-Soudeur':'https://iili.io/dugsPqJ.png',
    'Station Spatiale-Technicien':'https://iili.io/dugsi0v.png',
    'Studio de cinema-Acteur':'https://iili.io/dugssgR.png',
    'Studio de cinema-Cascadeur':'https://iili.io/dugsQJp.png',
    'Studio de cinema-Chef decorateur':'https://iili.io/dugsZ5N.png',
    'Studio de cinema-Costumier':'https://iili.io/dugsteI.png',
    'Studio de cinema-Doublure':'https://iili.io/dugsmzX.png',
    'Studio de cinema-Producteur':'https://iili.io/dugspXn.png',
    'Studio de cinema-Realisateur':'https://iili.io/dugsyss.png',
    'Supermarche-Agent d entretient':'https://iili.io/dugLHqG.png',
    'Supermarche-Agent de securite':'https://iili.io/dugLJ1f.png',
    'Supermarche-Caissier':'https://iili.io/dugLdg4.png',
    'Supermarche-Client':'https://iili.io/dugL3dl.png',
    'Supermarche-Directeur':'https://iili.io/dugLF72.png',
    'Supermarche-Fournisseur':'https://iili.io/dugLKeS.png',
    'Supermarche-Voleur':'https://iili.io/dugLBI9.png',
    'Theatre-Accessoiriste':'https://iili.io/dugLCXe.png',
    'Theatre-Comedien':'https://iili.io/dugLnLu.png',
    'Theatre-Metteur en scene':'https://iili.io/dugLxqb.png',
    'Theatre-Responsable Lumieres':'https://iili.io/dugLIrx.png',
    'Theatre-Responsable Son':'https://iili.io/dugLudQ.png',
    'Theatre-Spectateur':'https://iili.io/dugLRkB.png',
    'Theatre-Technicien':'https://iili.io/dugL5mP.png',
    'Train-Agent de nettoyage':'https://iili.io/dugLYI1.png',
    'Train-Conducteur':'https://iili.io/dugLahF.png',
    'Train-Controlleur':'https://iili.io/dugLcLg.png',
    'Train-Passager de 1ere classe':'https://iili.io/dugL0Ba.png',
    'Train-Passager de 2nd classe':'https://iili.io/dugL1EJ.png',
    'Train-Technicien':'https://iili.io/dugLM2R.png',
    'Train-Voyageur sans ticket':'https://iili.io/dugLV7p.png',
    'Universite-Agent d entretient':'https://iili.io/dugLWkN.png',
    'Universite-Bibliothecaire':'https://iili.io/dugLXpI.png',
    'Universite-Chercheur':'https://iili.io/dugLwhX.png',
    'Universite-Directeur':'https://iili.io/dugLv4f.png',
    'Universite-Etudiant':'https://iili.io/dugLS24.png',
    'Universite-Infirmiere':'https://iili.io/dugLUYl.png',
    'Universite-Professeur':'https://iili.io/dugLgv2.png',
    'Zoo-Animateur':'https://iili.io/dugLrpS.png',
    'Zoo-Chef animalier':'https://iili.io/dugL6T7.png',
    'Zoo-Dompteur':'https://iili.io/dugLiQe.png',
    'Zoo-Fauconnier':'https://iili.io/dugLLCu.png',
    'Zoo-Soigneur':'https://iili.io/dugLQEb.png',
    'Zoo-Veterinaire':'https://iili.io/dugLZ4j.png',
    'Zoo-Visiteur':'https://iili.io/dugLD3x.png'
}

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
            17:["Garage",["Apprenti","Gérant","Client","Technicien en pneumatique","Carrosier","Vendeur automobile","Fournisseur d'huile"]],
            18:["Fete d entreprise",["PDG","Stagiaire","Apprenti","Alternant","Assistant administratif","Scrétaire","Salarié licencié"],"Fête d'entreprise"],
            19:["Ecole",["Eleve","Professeur","Infirmière","Directeur","Agent d'entretient","Responsable cantine","Remplacant"]],
            20:["Croisades",["Chevalier","Archer","Ecuyer","Paysan","Garde","Seigneur","Prêtre"]],
            21:["Casino",["Croupier","Joueur gagnant","Joueur perdant","Tricheur","Directeur","Responsable sécurité","Banquier"]],
            22:["Carnaval",["Déguisé en loup","Déguisé en Mousquetaire","Déguisé en Pirate","Déguisement oublié","Déguisé en SUper-Héros","Déguisé en Obélix","Déguisé en table-basse"]],
            23:["Boite de nuit",["Videur","DJ","Danseur","Barman","Client Bourré","Client","Responsable Lumières"]],
            24:["Bateau pirate",["Capitaine","Matelot","Cuisinier","Maitre Artilleur","Chef de la carte au trésor","Prisonnier","Gérant des voiles"]],#??
            25:["Base militaire",["Colonel","Pilote d'avion","Maitre-chien","Chauffeur Poids-Lourd","Opérateur réseau","Infirmière","Assistant administratif"]],
            26:["Banque",["Directeur","Client","Conseiller","Analyste financier","Client dans le rouge","Trade","Guichetier"]],
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