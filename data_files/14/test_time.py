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
                self.grid[i][j] = value

    def CalcDensity(self): # permet de calculer la densité des petits rectangles dans la BOX
        nb = 0
        for row in self.grid:
            for cell in row:
                if cell != 0:
                    nb +=1
        return (nb/(self.n*self.m))*100
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

  

def main_random(n):

    #Choisi un probleme au hasard parmis 3 fichiers
    fichint = n
    fichier = str(fichint)+"guillotine.txt"
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
        if can_fit(big_rectangle, sm, small_rectangles_place):
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
    print("\n")
    if len(small_rectangles)==0:
        print("C'est réussi, il reste aucun rectangle à placer")
    else :
        print("C'est raté, il reste "+str(len(small_rectangles))+" rectangle(s) à placer")
    print("densité totale :", end= " ")
    print(g.CalcDensity())
    return g.CalcDensity()

def dfs(rectangles, big_rectangle, rectangles_placed, grid, placed_indices, n):
    # test fin récursion : tous lres rectangles ont été placé
    if len(rectangles_placed) == len(rectangles):
        print("nombres d'appels récursifs :" + str(n))
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

                    if can_fit(big_rectangle, new_rectangle, rectangles_placed):
                        # placer le rectangle et update de la grille
                        rectangles_placed.append(new_rectangle)
                        placed_indices.append(l)
                        grid.update_by_rect(i, j, new_rectangle.height, new_rectangle.width, len(rectangles_placed))

                        # appel réursif
                        if dfs(rectangles, big_rectangle, rectangles_placed, grid, placed_indices, n+1):
                            return True

                        # Backtrack
                        rectangles_placed.pop()
                        placed_indices.pop()
                        grid.update_by_rect(i, j, new_rectangle.height, new_rectangle.width, 0)
            # Impossible de placer le rectangle
            return False
    print("nombres d'appels récursifs :" + str(n))

    return True

def main_dfs(n):
    fichint = n
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

    if(dfs(sorted_rectangles, big_rectangle, small_rectangles_place, g, placed_indices, 1)):
        print("reussite !")
        print("")
        print("densité totale :", end= " ")
        print(g.CalcDensity())
    else:
        print("raté !")
        print("densité totale :", end= " ")
        print(g.CalcDensity())
    return g.CalcDensity()

def main():
    for i in range(0, 10):
        file1 = open("tests_temps14"+str(i)+".txt", "w")
        file1.write("Fonction  probleme  temps\n")
        for n in range(0, 10):
            start_time1 = time.time()
            x = main_random(n)
            time_ = time.time()-start_time1
            print(time_)
            file1.write("random"+" "+str(n)+" "+str(time_)+" "+str(x)+"\n")
        for n in range(0, 10):
            start_time2 = time.time()
            y = main_dfs(n)
            time_ = time.time()-start_time2
            print(time_)
            file1.write("dfs"+" "+str(n)+" "+str(time_)+" "+str(y)+"\n")
        file1.close()
    i1 = 0
    i2 = 0
    i3 = 0
    i4 = 0
    i5 = 0
    i6 = 0
    i7 = 0
    i8 = 0
    i9 = 0
    i10 = 0
    j1 = 0
    j2 = 0
    j3 = 0
    j4 = 0
    j5 = 0
    j6 = 0
    j7 = 0
    j8 = 0
    j9 = 0
    j10 = 0
    for i in range(0,10):
        file_ = "tests_temps14"+str(i)+".txt"
        with open(file_, 'r') as f:
            for line in f:
                components = line.strip().split()
                if components[0] == 'random':
                    if components[1] == '0':
                        i1 += float(components[2])
                    if components[1] == '1':
                        i2 += float(components[2])
                    if components[1] == '2':
                        i3 += float(components[2])
                    if components[1] == '3':
                        i4 += float(components[2])
                    if components[1] == '4':
                        i5 += float(components[2])
                    if components[1] == '5':
                        i6 += float(components[2])
                    if components[1] == '6':
                        i7 += float(components[2])
                    if components[1] == '7':
                        i8 += float(components[2])
                    if components[1] == '8':
                        i9 += float(components[2])
                    if components[1] == '9':
                        i10 += float(components[2])
                elif components[0] == 'dfs':
                    if components[1] == '0':
                        j1 += float(components[2])
                    if components[1] == '1':
                        j2 += float(components[2])
                    if components[1] == '2':
                        j3 += float(components[2])
                    if components[1] == '3':
                        j4 += float(components[2])
                    if components[1] == '4':
                        j5 += float(components[2])
                    if components[1] == '5':
                        j6 += float(components[2])
                    if components[1] == '6':
                        j7 += float(components[2])
                    if components[1] == '7':
                        j8 += float(components[2])
                    if components[1] == '8':
                        j9 += float(components[2])
                    if components[1] == '9':
                        j10 += float(components[2])
    file1 = open("MoyRandDfs14.txt", "w")
    file1.write("moyenne des temps effectués par random sur le probleme 0 comportant 14 rectangles :"+str(i1/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 1 comportant 14 rectangles :"+str(i2/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 2 comportant 14 rectangles :"+str(i3/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 3 comportant 14 rectangles :"+str(i4/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 4 comportant 14 rectangles :"+str(i5/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 5 comportant 14 rectangles :"+str(i6/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 6 comportant 14 rectangles :"+str(i7/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 7 comportant 14 rectangles :"+str(i8/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 8 comportant 14 rectangles :"+str(i9/10.0)+"\n")
    file1.write("moyenne des temps effectués par random sur le probleme 9 comportant 14 rectangles :"+str(i10/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 0 comportant 14 rectangles :"+str(j1/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 1 comportant 14 rectangles :"+str(j2/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 2 comportant 14 rectangles :"+str(j3/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 3 comportant 14 rectangles :"+str(j4/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 4 comportant 14 rectangles :"+str(j5/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 5 comportant 14 rectangles :"+str(j6/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 6 comportant 14 rectangles :"+str(j7/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 7 comportant 14 rectangles :"+str(j8/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 8 comportant 14 rectangles :"+str(j9/10.0)+"\n")
    file1.write("moyenne des temps effectués par dfs sur le probleme 9 comportant 14 rectangles :"+str(j10/10.0)+"\n")  
    file1.close()          

if __name__=="__main__":

     main()
