# Korrigan : Vole 2 cartes choisies au hasard dans la main d'un adversaire.
# Elfe : utilise le pouvoir d'une carte deja présente devant lui
# Farfadet : Echange toutes les cartes de son peuple conte contre celles d'un autre joueur.
# Gnome : Pioche des ?? cartes supplémentaires.
# Lutin : Echange la main contre celle d'un adversaire.
# Dryade : Vole une carte deja posée par un adversaire (devant soi ? ou dans sa main ?)
# Fée : Annule le pouvoir d'une carte jouée par un adversaire. (peut etre utilisé pour annuler une fée, puis re annulé etc...)

#Revoir poiuvoir Dryade et Gnome
#revoir nb de chaque race dans la pioche (dico dans init partie)
import random   


class Carte():
    def __init__(self, nom, pouvoir):
        self.nom = nom
        self.pouvoir = pouvoir
        self.image = None  # Placeholder pour l'image de la carte
    def getNom(self):
        return self.nom
    def getPouvoir(self):
        return self.pouvoir
    def getImage(self):
        return self.image

class Korrigan(Carte):
    def __init__(self):
        super().__init__("Korrigan", "Vole 2 cartes choisies au hasard dans la main d'un adversaire.")

class Elfe(Carte):
    def __init__(self):
        super().__init__("Elfe", "Utilise le pouvoir d'une carte déjà présente devant lui.")

class Farfadet(Carte):
    def __init__(self):
        super().__init__("Farfadet", "Échange toutes les cartes de son peuple contre celles d'un autre joueur.")

class Gnome(Carte):
    def __init__(self):
        super().__init__("Gnome", "Pioche des ?? cartes supplémentaires.")

class Lutin(Carte):
    def __init__(self):
        super().__init__("Lutin", "Échange la main contre celle d'un adversaire.")

class Dryade(Carte):
    def __init__(self):
        super().__init__("Dryade", "Vole une carte déjà posée par un adversaire. (et en fait quoi avec ?)")

class Fee(Carte):
    def __init__(self):
        super().__init__("Fée", "Annule le pouvoir d'une carte jouée par un adversaire. (peut s'accumuler)")


class Partie():
    def __init__(self, dico_partie, liste_joueurs):
        self.dico=dico_partie

        if dico_partie=={} : #Si la partie n'a jamais été sauvegardée (vient d'etre créee), on créé tout
            #CREATION DE LA PIOCHE
            dico_repartition = { #Nombre de cartes de chaque race
                "Korrigan": 10,
                "Elfe": 10,
                "Farfadet": 10,
                "Gnome": 10,
                "Lutin": 10,
                "Dryade": 10,
                "Fee": 10
            }

            self.dico['pioche'] = []
            for race in dico_repartition:
                for _ in range(dico_repartition[race]): #Pour chaque race, on ajoute le nombre de cartes correspondant
                    self.dico['pioche'].append(race) #On utilise globals() pour récupérer la classe correspondant au nom de la race
            random.shuffle(self.dico['pioche'])

            #CREATION DES JOUERUS
            dico_joueurs={} #dico qui contient tous les joueurs (eux memes sont des dicos)
            for i in liste_joueurs:
                print(i)
                dico_j={}
                dico_j['main']=[]
                dico_j['peuple']=[]
                dico_joueurs[i]=dico_j
            self.dico['joueurs']=dico_joueurs
            #chaque joueur pioche 5 cartes
            for i in liste_joueurs:
                self.piocheCarte(i, nb=5)
            
            self.dico['actif_player']=liste_joueurs[0]#On definit  quel joueur c'est de jouer

    def piocheCarte(self, nom_joueur, nb=1):
        nb = min(len(self.dico['pioche']), nb)  # on prend le minimum entre le nombre de cartes demandées et le nombre de cartes restantes dans la pioche
        for i in range(nb):
            carte=self.dico['pioche'].pop(0)
            self.dico['joueurs'][nom_joueur]['main'].append(carte)

    def distribuerCartes(self, nb=5):
        for nom_joueur in self.joueurs:
            self.piocheCarte(nb, nom_joueur)
    
    def joueurCarte(self, nom_joueur, index_carte):
        #EFFET CARTE
        carte = self.dico['joueurs'][nom_joueur]['main'].pop(index_carte)
        self.dico['joueurs'][nom_joueur]['peuple'].append(carte)


    def echangerMain(self, nom_joueur1, nom_joueur2):
        temp=self.dico['joueurs'][nom_joueur1]['main']
        self.dico['joueurs'][nom_joueur1]['main'] = self.dico['joueurs'][nom_joueur2]['main']
        self.dico['joueurs'][nom_joueur2]['main'] = temp

    
    def echangerPeuple(self, nom_joueur1, nom_joueur2):
        temp=self.dico['joueurs'][nom_joueur1]['peuple']
        self.dico['joueurs'][nom_joueur1]['peuple'] = self.dico['joueurs'][nom_joueur2]['peuple']
        self.dico['joueurs'][nom_joueur2]['peuple'] = temp

    def getDict(self):
        return self.dico
    
    

p = Partie({},["ee","ff"])
p.joueurCarte("ee",1)
print(p.getDict())
p.echangerMain("ee","ff")
p.echangerPeuple("ee","ff")
print(p.getDict())