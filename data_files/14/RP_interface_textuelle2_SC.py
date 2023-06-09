import random
from tkinter import messagebox
import time


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other_rectangle):
        return self.x < other_rectangle.x + other_rectangle.height and self.x + self.height > other_rectangle.x and self.y < other_rectangle.y + other_rectangle.width and self.y + self.width > other_rectangle.y

    def __repr__(self):
        return f"Rectangle({self.x}, {self.y}, {self.width}, {self.height})"

    def copy(self):
        return Rectangle(self.x, self.y, self.width, self.height)

def can_fit(big_rectangle, small_rectangle, other_rectangles_place):
    for other_rectangle in other_rectangles_place:
        if small_rectangle.intersects(other_rectangle):
            return False
    return big_rectangle.x <= small_rectangle.x and big_rectangle.y <= small_rectangle.y and big_rectangle.x + big_rectangle.height >= small_rectangle.x + small_rectangle.height and big_rectangle.y + big_rectangle.width >= small_rectangle.y + small_rectangle.width


class Grid: # creation d'une classe creant une matrice pour une interface graphique simple du programme
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.grid = [[0 for j in range(n)] for i in range(m)]

        '''for i in range(n): // si on veut que les bordures du grand rectangle soient apparentes i.e. les rectangles
            self.grid[i][0] = 1 // de taille 1*1 en bordure ne se verront donc pas
            self.grid[0][i] = 1
            self.grid[n-1][i] = 1
            self.grid[i][n-1] = 1'''

    def __str__(self): # permet d'afficher la matrice : carré plein pour les valeurs égales à 1 sinon un carré vide
        d=0
        print(" L ", end="")
        for i in range (self.n):
            if(i%10==0):
                if (i==0):
                    print(i,end=" ")
                else :
                    print("!",end=" ")
                    d+=1
            else:
                print(i-d*10,end=" ")
        print(" ")
        print("H")
        return ('\n'.join([str(i%10) +"  "+ ' '.join([str(self.grid[i][j]) for j in range(0,self.n)]) for i in range(0,self.m)]))+('\n')


    def update_by_rect(self, x, y, n, m, value): # permet de mettre a jour la matrice en ajoutant les nouveaux rectangles 
        for i in range(x, m+x):
            for j in range(y, n+y):
                if value<10 :
                    self.grid[i][j] = value #value sera 1 si le rectangle est placé en premier, 2 si il a été placé en deuxième etc...
                else :
                    lettre={10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F', 16:'G', 17:'H', 18:'I', 19:'J', 20:'K', 21:'L', 22:'M', 23:'N', 24:'O', 25:'P', 26:'Q', 27:'R', 28:'S', 29:'T', 30:'U',31:'V', 32:'W', 33:'X', 34:'Y', 35:'Z'}
                    self.grid[i][j]=lettre[value] #ici on utilise les lettres de l'alphabet pour représenter les rectangles placés en dixième et plus

    def CalcDensity(self): # permet de calculer la densité des petits rectangles dans la BOX
        nb = 0
        for row in self.grid:
            for cell in row:
                if cell != 0:
                    nb +=1
        print((nb/(self.n*self.m))*100)
        return exit

    # Verifie pour les coordonnées données si le type de coin est bien valide

    def coinHG(self, x, y):
        if self.grid[x][y]==0:
            if x==0 and y>0:
                if self.grid[x][y-1]!=0 and self:
                    return True
            if x>0 and y==0:
                if self.grid[x-1][y]!=0 and self:
                    return True
            if x==0 and y==0:
                return True
            if x>0 and y>0:
                if self.grid[x-1][y]!=0 and self.grid[x][y-1]!=0:
                    return True
        return False

    def coinHD(self, x, y):
        if self.grid[x][y]==0:
            if x==0 and y==(self.n)-1:
                return True
            elif x==0 and y<(self.n)-1:
                if self.grid[x+1][y+1]!=0 and self:
                    return True
            elif x>0 and y==(self.m)-1:
                if self.grid[x-1][y]!=0 and self:
                    return True
            elif x<(self.m)-1 and y<(self.n)-1:
                if self.grid[x-1][y]!=0 and self.grid[x][y+1]!=0:
                    return True 
        else:
            return False
    
    def coinBG(self, x, y):
        if self.grid[x][y]==0:
            if x==(self.m)-1 and y==0:
                return True
            elif x<(self.m)-1 and y==0:
                if self.grid[x+1][y]!=0 and self:
                    return True
            elif x==(self.m)-1 and y>0:
                if self.grid[x][y-1]!=0 and self:
                    return True
            elif x<(self.m)-1 and y<(self.n)-1:
                if self.grid[x+1][y]!=0 and self.grid[x][y-1]!=0:
                    return True 
        else:
            return False

    def coinBD(self, x, y):
        if self.grid[x][y]==0:
            if x==(self.m)-1 and y<(self.n)-1:
                if self.grid[x][y+1]!=0 and self:
                    return True
            elif x==(self.m)-1 and y==(self.n)-1:
                return True
            elif x<(self.m)-1 and y==(self.n)-1:
                if self.grid[x+1][y]!=0 and self:
                    return True
            elif x<(self.m)-1 and y<(self.n)-1:
                if self.grid[x+1][y]!=0 and self.grid[x][y+1]!=0:
                    return True 
        else:
            return False


def main_player():
    x = int(input("Choississez un problème entre 1 et 10 (rentrez un entier entre 1 et 10):"))
    while x<1 or x>10:
        print("Vous n'avez pas tapé un entier entre 1 et 10")
        x = int(input("Choississez un problème entre 1 et 10 (rentrez un entier entre 1 et 10):"))
    fichier = str(x)+".txt"
    small_rectangles = []
    small_rectangles_place = []
    with open(fichier) as f:
        first_line = f.readline()
        a, b = [int(i) for i in first_line.split()]
        big_rectangle = Rectangle(0, 0, a, b)
        g = Grid(b, a)
        for line in f:
            a, b = [int(i) for i in line.split()]
            small_rectangles.append(Rectangle(0, 0, a, b))
    while len(small_rectangles)!=0:
        length_sr = len(small_rectangles)
        print(" Taille Grand Rectangle (hauteur x largeur): "+ str(g.m)+"x"+str(g.n))
        print(g)
        print("")
        _temp = input("Voulez vous placer un rectangle ou retirer le dernier rectangle posé ? P ou R")
        while _temp != "P" and _temp !="R":
            _temp = input("Veuillez rentrez P ou R : ")
            print(_temp)
        if len(small_rectangles_place)==0 and _temp=="R":
            print("Impossible der retirer car il n'y a pas de rectangles placés, veuillez poser un rectangle !")
            _temp = "P"
        if _temp == "P":
            for i in range(0, length_sr):
                print(str(i) +". "+"Rectangle de taille (hauteur x largeur) "+str(small_rectangles[i].width) + "x" + str(small_rectangles[i].height))
            A = int(input(" Tapez un nombre : "))
            while  A>length_sr-1 or A<0:
                A = int(input(" Tapez un nombre entre 0 et " + str(length_sr -1)+ ": "))
            k = int(input(" Renseigner le x : "))
            j = int(input(" Renseigner le y : "))

            sm = small_rectangles[A]
            sm.x=k
            sm.y=j
            if not can_fit(big_rectangle, sm, small_rectangles_place):
                print("rectangle de coordonnées x = " + str(sm.x) + ", y = " + str(sm.y) + ", hauteur = " + str(sm.width) + ", largeur = " + str(sm.height) + " ne peut pas être placé dans le grand rectangle ou chevauche un autre rectangle.")
            else:
                print(repr(sm))
                print("rectangle de coordonnées x = " + str(sm.x) + ", y = " + str(sm.y) + ", hauteur = " + str(sm.width) + ", largeur = " + str(sm.height) + " peut être placé dans le grand rectangle.")
                small_rectangles_place.append(Rectangle(k,j,sm.width,sm.height))
                g.update_by_rect(j, k, sm.height, sm.width, len(small_rectangles_place))
                del small_rectangles[A]
        elif _temp == "R":
            _temp_ret_sm = small_rectangles_place.pop(len(small_rectangles_place)-1)
            g.update_by_rect(_temp_ret_sm.y, _temp_ret_sm.x, _temp_ret_sm.height, _temp_ret_sm.width, 0)
            small_rectangles.append(_temp_ret_sm)
        
    dens=g.CalcDensity()
    print("La densité totale des petits rectangles dans la BOX est de : "+str(dens)+" %.")
  

def main_random():
    #Choisi un probleme au hasard parmis 3 fichiers
    fichint = random.randint(1, 10)
    print(str(fichint)+".txt")
    fichier = str(fichint)+".txt"
    small_rectangles = []
    small_rectangles_place = []
    with open(fichier) as f: #On recupere les valeurs du fichiers pour creer les objets pour les probleme
        first_line = f.readline()
        a, b = [int(i) for i in first_line.split()]
        big_rectangle = Rectangle(0, 0, a, b)
        g = Grid(b, a)
        for line in f:
            a, b = [int(i) for i in line.split()]
            small_rectangles.append(Rectangle(0, 0, a, b))
    xlen = g.m
    ylen = g.n
    len_sm = len(small_rectangles)
    print("Taille Grand Rectangle (largeur x hauteur): "+ str(g.n)+"x"+str(g.m))
    print("Taille des petits rectangles: ")
    for i in range (len_sm):
            print("n°"+str(i+1) +" "+ str(small_rectangles[i].width) +"x"+ str(small_rectangles[i].height))
    list_coinHG = [] #On initialise les listes contenant les differents types de coins
    list_coinHD = []
    list_coinBG = []
    list_coinBD = []
    first_rect = small_rectangles[len_sm-1] #On place d'abord le plus grand rectangle du probleme en haut a gauche
    small_rectangles_place.append(Rectangle(0,0,first_rect.width,first_rect.height))
    g.update_by_rect(0, 0, first_rect.height, first_rect.width, 1)
    del small_rectangles[len_sm-1]
    n = 0
    while len(small_rectangles)!=0 and n<100:
        len_sm = len(small_rectangles)
        print(g)
        choserect = random.randint(0, len_sm-1)  #On choisit un petit rectangle au hasard à placer
        rect = small_rectangles[choserect]
        for i in range(0, xlen): #Pour chaques case dans Grid, on verifie si la case est pas un certain type de coin
            for y in range(0,ylen): #On verifie aussi si le coin n'existe pas deja dans la liste correspondante
                if g.coinHG(i, y) == True:
                    if (i, y) not in list_coinHG: 
                        list_coinHG.append((i, y))
                if g.coinHD(i, y) == True:
                    if (i, y) not in list_coinHD: 
                        list_coinHD.append((i, y))
                if g.coinBG(i, y) == True:
                    if (i, y) not in list_coinBG: 
                        list_coinBG.append((i, y))
                if g.coinBD(i, y) == True:
                    if (i, y) not in list_coinBD: 
                        list_coinBD.append((i, y))
        nbpos = 0
        sm = rect
        if n < 25: #Ici, on teste 25 fois les differents coins hauts gauches pour chaque rectangle si c'est possible de le placer
            pos = random.randint(0, len(list_coinHG)-1)
            y, x = list_coinHG[pos]
            nbpos = 1
        elif n >= 25 and n < 50 and list_coinHD: #Les 25 itérations des rectangles sont avec les coins HD
            pos = random.randint(0, len(list_coinHD)-1)
            y, x = list_coinHD[pos]
            x = x-sm.height+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin HD 
            nbpos = 2
        elif n >= 50 and n < 75 and list_coinBG:  #Les 25 itérations des rectangles sont avec les coins BG
            pos = random.randint(0, len(list_coinBG)-1)
            y, x = list_coinBG[pos]
            y = y-sm.width+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin BG
            nbpos = 3
        elif n >= 75 and n < 100 and list_coinBD:  #Les 25 itérations des rectangles sont avec les coins BD
            pos = random.randint(0, len(list_coinBD)-1)
            y, x = list_coinBD[pos]
            x = x-sm.height+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin BD
            y = y-sm.width+1
            nbpos = 4
        else: #Bien sur on essaye de placer sur les coins non-hauts gauches uniquement si il en existe, sinon par defaut sur un coin HG
            pos = random.randint(0, len(list_coinHG)-1)
            y, x = list_coinHG[pos]
            nbpos = 1
        sm.x=x
        sm.y=y
        if not can_fit(big_rectangle, sm, small_rectangles_place):
            print("rectangle de coordonnées x = " + str(sm.x) + ", y = " + str(sm.y) + ", hauteur = " + str(sm.width) + ", largeur = " + str(sm.height) + " ne peut pas être placé dans le grand rectangle ou chevauche un autre rectangle.")
        else:
            print("rectangle de coordonnées x = " + str(sm.x) + ", y = " + str(sm.y) + ", hauteur = " + str(sm.width) + ", largeur = " + str(sm.height) + " peut être placé dans le grand rectangle.")
            small_rectangles_place.append(Rectangle(x,y,sm.width,sm.height))
            del small_rectangles[choserect]
            if nbpos == 1: #On verifie quel type de coin a été utilisé dans la liste pour pouvoir supprimer ce coin de la liste des coins
                g.update_by_rect(y, x, sm.height, sm.width, len(small_rectangles_place))
                del list_coinHG[pos]
            elif nbpos == 2:
                g.update_by_rect(y, x, sm.height, sm.width, len(small_rectangles_place))
                del list_coinHD[pos]
            elif nbpos == 3:
                g.update_by_rect(y, x, sm.height, sm.width, len(small_rectangles_place))
                del list_coinBG[pos]
            elif nbpos == 4:
                g.update_by_rect(y, x, sm.height, sm.width, len(small_rectangles_place))
                del list_coinBD[pos]
        n+=1
    print(g)
    print("\n")
    if len(small_rectangles)==0:
        print("C'est réussi, il reste aucun rectangle à placer")
    else :
        print("C'est raté, il reste "+str(len(small_rectangles))+" rectangle(s) à placer")
    print("densité totale :", end= " ")
    g.CalcDensity()




def dfs(rectangles, big_rectangle, rectangles_placed, grid, placed_indices):
    print(grid)
    # test fin récursion : tous lres rectangles ont été placé
    if len(rectangles_placed) == len(rectangles):
        return True

    # boucle qui test chaque rectangle non placé pour chaque appel récursif
    for l, rectangle in enumerate(rectangles):
        if l not in placed_indices:
            # On essaye de poser le rectangle dans chaque position de la grille possible
            for i in range(grid.m):
                for j in range(grid.n):
                    new_rectangle = Rectangle(rectangle.x, rectangle.y, rectangle.width, rectangle.height)
                    new_rectangle.x = j
                    new_rectangle.y = i
                    """ DEBUG
                    print(repr(new_rectangle))
                    print(".")
                    print(repr(big_rectangle))
                    print("..")
                    for p in rectangles_placed:
                        print(repr(p))
                    print("...")"""
                    if can_fit(big_rectangle, new_rectangle, rectangles_placed):
                        # placer le rectangle et update de la grille
                        rectangles_placed.append(new_rectangle)
                        placed_indices.append(l)
                        grid.update_by_rect(i, j, new_rectangle.height, new_rectangle.width, len(rectangles_placed))

                        # appel réursif
                        if dfs(rectangles, big_rectangle, rectangles_placed, grid, placed_indices):
                            return True

                        # Backtrack
                        rectangles_placed.pop()
                        placed_indices.pop()
                        grid.update_by_rect(i, j, new_rectangle.height, new_rectangle.width, 0)
            print(grid)
            # Impossible de placer le rectangle
            return False

    return True



def main_dfs():
    fichint = 7
    print(str(fichint)+"guillotine.txt")
    fichier = str(fichint)+"guillotine.txt"
    small_rectangles = []
    small_rectangles_place = []
    placed_indices = []
    with open(fichier) as f: #On recupere les valeurs du fichiers pour creer les objets pour les probleme
        first_line = f.readline()
        a, b = [int(i) for i in first_line.split()]
        big_rectangle = Rectangle(0, 0, a, b)
        g = Grid(b, a)
        for line in f:
            a, b = [int(i) for i in line.split()]
            small_rectangles.append(Rectangle(0, 0, a, b))
    sorted_rectangles = sorted(small_rectangles, key=lambda r: r.width * r.height, reverse=True)
    if(dfs(sorted_rectangles, big_rectangle, small_rectangles_place, g, placed_indices)):
        print("reussite !")
        print("")
        print(g)
        print("densité totale :", end= " ")
        g.CalcDensity()
    else:
        print("raté !")
        print(g)
        print("densité totale :", end= " ")
        g.CalcDensity()
    return None




def main():
        x = int(input("Tapez 1 pour résoudre un probème vous même ou 2 pour un problème aléatoire par l'ordinateur Random ou 3 pour dfs: "))
        while x<1 or x>3:
            print("Vous n'avez pas tapé un entier entre 1 et 2")
            x = int(input("Tapez 1 pour résoudre un probème vous même ou 2 pour un problème aléatoire par l'ordinateur Random : "))
        if x==1:
            if messagebox.askyesno("Regles RP", "Voulez lire les règles du RP ?")==True:
                messagebox.showinfo("Regles :", """Règles du Rectangle Packing

Le but est de placer plusieurs "petits" rectangles dans un plus grand rectangle appelé la BOX, tout cela sans chevauchement. 
Si l'on souhaite que la BOX soit 100% remplie des petits rectangles, alors on dit que l'on cherche un Perfect Rectangle Packing.

Premierement, pour connaitre le probleme que vous allez resoudre, vous en choisirez un parmis une base de problème créée.
Puis vous entrerez des coordonnees pour chaque rectangle à placer, elles feront références à la position du coin haut gauche de ce petit rectangle.
Le x fait référence à l'axe des abscisses (l'axe L), et le y lui à l'axe des ordonnées (l'axe H).

Bonne chance !""")
            main_player()
        if x==2:
            start_time = time.time()
            main_random()
            print("Effectué en %s secondes :" % (time.time() - start_time))
        if x==3:
            start_time = time.time()
            main_dfs()
            print("Effectué en %s secondes :" % (time.time() - start_time))




if __name__=="__main__":
     main()
     
