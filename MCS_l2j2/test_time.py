import random
import time
import os

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
        return ((nb/(self.n*self.m))*100)
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
        
    def copy(self):
        new_grid = Grid(self.n, self.m)
        new_grid.grid = [row.copy() for row in self.grid]
        return new_grid

import random

def random_placement(small_rectangles ,big_rectangle, g, small_rectangles_place):
    if g.CalcDensity() == 100.0 or len(small_rectangles)==0:
        return g.CalcDensity()
    else:
        small_rectangles = sorted(small_rectangles, key=lambda r: r.width * r.height)
        xlen = g.m
        ylen = g.n
        len_sm = len(small_rectangles)
        list_coinHG = [] #On initialise les listes contenant les differents types de coins
        list_coinHD = []
        list_coinBG = []
        list_coinBD = []
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
            if n < 25 and list_coinHG: #Ici, on teste 25 fois les differents coins hauts gauches pour chaque rectangle si c'est possible de le placer
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
            elif n >= 75 and list_coinBD:  #Les 25 itérations des rectangles sont avec les coins BD
                pos = random.randint(0, len(list_coinBD)-1)
                y, x = list_coinBD[pos]
                x = x-sm.height+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin BD
                y = y-sm.width+1
                nbpos = 4
            else: #Après 100 itérations, si aucun coin n'existe on break
                break
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
        return g.CalcDensity()



def getCoins(grid):
    coin_HG=[]
    coin_BG=[]
    coin_HD=[]
    coin_BD=[]
    xlen = grid.m
    ylen = grid.n
    for i in range(0, xlen): #Pour chaques case dans Grid, on verifie si la case est pas un certain type de coin
            for y in range(0,ylen): #On verifie aussi si le coin n'existe pas deja dans la liste correspondante
                if grid.coinHG(i, y) == True:
                    if (i, y) not in coin_HG: 
                        coin_HG.append((i, y))
                if grid.coinHD(i, y) == True:
                    if (i, y) not in coin_HD: 
                        coin_HD.append((i, y))
                if grid.coinBG(i, y) == True:
                    if (i, y) not in coin_BG: 
                        coin_BG.append((i, y))
                if grid.coinBD(i, y) == True:
                    if (i, y) not in coin_BD: 
                        coin_BD.append((i, y))
    return coin_HG, coin_BG, coin_HD, coin_BD

from collections import defaultdict

import copy

def mcss(rectangles, big_rectangle, grid, n):
    best_density = 0
    best_grid = None
    best_placement = None

    for sim in range(n):
        placed_rectangles = []
        remaining_rectangles = copy.deepcopy(rectangles)  # Deep copy of the original rectangles list
        current_grid = grid.copy()

        while len(remaining_rectangles) != 0:
            densities = defaultdict(list)
            coin_HG, coin_BG, coin_HD, coin_BD = getCoins(current_grid)

            for i, rect in enumerate(remaining_rectangles):
                for coin in coin_HG:
                    y, x = coin
                    temp_rect = rect.copy()

                    remaining_rectangles_temp = copy.deepcopy(remaining_rectangles)

                    # Update the x and y attributes of the copied rectangle
                    temp_rect.x = x
                    temp_rect.y = y

                    if can_fit(big_rectangle, temp_rect, placed_rectangles):
                        new_grid = current_grid.copy()
                        placed_rectangles_temp = placed_rectangles.copy()
                        placed_rectangles_temp.append(temp_rect)
                        new_grid.update_by_rect(temp_rect.y, temp_rect.x, temp_rect.height, temp_rect.width, len(placed_rectangles_temp))
                        new_grid_temp = new_grid.copy()
                        
                        if len(remaining_rectangles) == 1:
                            density = new_grid.CalcDensity()
                        else:
                            density = random_placement(remaining_rectangles_temp[:i] + remaining_rectangles_temp[i + 1:], big_rectangle, new_grid_temp, placed_rectangles_temp.copy())
                        densities[density].append((i, temp_rect, new_grid))
                # Add loops for other coins (coin_BG, coin_HD, coin_BD) similarly
            if not densities:
                break

            max_density = max(densities.keys())
            i, new_rectangle, new_grid = random.choice(densities[max_density])

            placed_rectangles.append(new_rectangle)
            remaining_rectangles.pop(i)
            current_grid = new_grid

        if current_grid.CalcDensity() > best_density:
            best_density = current_grid.CalcDensity()
            best_grid = current_grid
            best_placement = placed_rectangles

    return best_density, best_grid, best_placement

### MCS VERSION 2 ###
"""def mcs(rectangles, big_rectangle, grid, n):
    best_density = 0
    best_grid = None
    best_placement = None

    placed_rectangles = []
    remaining_rectangles = copy.deepcopy(rectangles)
    current_grid = grid.copy()

    while len(remaining_rectangles) != 0:
        densities = defaultdict(list)
        coin_HG, coin_BG, coin_HD, coin_BD = [],[],[],[]

        for i, rect in enumerate(remaining_rectangles):
            coin_HG, coin_BG, coin_HD, coin_BD = getCoins(current_grid)
            for sim in range(n):
                temp_rect = rect.copy()
                if sim < n/4 and coin_HG: #Ici, on teste 25 fois les differents coins hauts gauches pour chaque rectangle si c'est possible de le placer
                    pos = random.choice(coin_HG)
                    y, x = pos
                elif sim >= n/4 and sim < n/2 and coin_HD: #Les 25 itérations des rectangles sont avec les coins HD
                    pos = random.choice(coin_HD)
                    y, x = pos
                    x = x-temp_rect.height+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin HD 
                elif sim >= n/2 and sim < n/3 and coin_BG:  #Les 25 itérations des rectangles sont avec les coins BG
                    pos = random.choice(coin_BG)
                    y, x = pos
                    y = y-temp_rect.width+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin BG
                elif sim >= 75 and sim < 100 and coin_BD:  #Les 25 itérations des rectangles sont avec les coins BD
                    pos = random.choice(coin_BD)
                    y, x = pos
                    x = x-temp_rect.height+1 #On modifie les coordonnées de placement pour pouvoir les placer de facon != pour un coin BD
                    y = y-temp_rect.width+1

                remaining_rectangles_temp = copy.deepcopy(remaining_rectangles)

                temp_rect.x = x
                temp_rect.y = y

                if can_fit(big_rectangle, temp_rect, placed_rectangles):
                    new_grid = current_grid.copy()
                    placed_rectangles_temp = placed_rectangles.copy()
                    placed_rectangles_temp.append(temp_rect)
                    new_grid.update_by_rect(temp_rect.y, temp_rect.x, temp_rect.height, temp_rect.width, len(placed_rectangles_temp))
                    new_grid_temp = new_grid.copy()
                            
                    if len(remaining_rectangles) == 1:
                        density = new_grid.CalcDensity()
                    else:
                        density = random_placement(remaining_rectangles_temp[:i] + remaining_rectangles_temp[i + 1:], big_rectangle, new_grid_temp, placed_rectangles_temp.copy())
                    densities[density].append((i, temp_rect, new_grid))
        if not densities:
            break

        max_density = max(densities.keys())
        i, best_rectangle, new_grid = random.choice(densities[max_density])

        placed_rectangles.append(best_rectangle)
        remaining_rectangles.pop(i)
        current_grid = new_grid

    return placed_rectangles, current_grid, current_grid.CalcDensity(), remaining_rectangles"""



import concurrent.futures

def simulate(sim, rect, n, coin_HG, coin_HD, coin_BG, coin_BD, remaining_rectangles, big_rectangle, placed_rectangles, current_grid, i):
    temp_rect = rect.copy()
    if sim < n/4 and coin_HG:
        pos = random.choice(coin_HG)
        y, x = pos
    elif sim >= n/4 and sim < n/2 and coin_HD:
        pos = random.choice(coin_HD)
        y, x = pos
        x = x - temp_rect.height + 1
    elif sim >= n/2 and sim < 3*n/4 and coin_BG:  # Change this condition
        pos = random.choice(coin_BG)
        y, x = pos
        y = y - temp_rect.width + 1
    elif sim >= 3*n/4 and coin_BD:  # Change this condition
        pos = random.choice(coin_BD)
        y, x = pos
        x = x - temp_rect.height + 1
        y = y - temp_rect.width + 1
    else:
        return None, None

    if not coin_BD and not coin_BG and not coin_HD and not coin_HG:
        return None, None

    remaining_rectangles_temp = copy.deepcopy(remaining_rectangles)

    temp_rect.x = x
    temp_rect.y = y

    if can_fit(big_rectangle, temp_rect, placed_rectangles):
        new_grid = current_grid.copy()
        placed_rectangles_temp = placed_rectangles.copy()
        placed_rectangles_temp.append(temp_rect)
        new_grid.update_by_rect(temp_rect.y, temp_rect.x, temp_rect.height, temp_rect.width, len(placed_rectangles_temp))
        new_grid_temp = new_grid.copy()
                            
        if len(remaining_rectangles) == 1:
            density = new_grid.CalcDensity()
        else:
            density = random_placement(remaining_rectangles_temp[:i] + remaining_rectangles_temp[i + 1:], big_rectangle, new_grid_temp, placed_rectangles_temp.copy())
    
        return density, (i, temp_rect, new_grid)
    else:
        return None, None

def mcs(rectangles, big_rectangle, grid, n):

    placed_rectangles = []
    remaining_rectangles = copy.deepcopy(rectangles)
    current_grid = grid.copy()

    while len(remaining_rectangles) != 0:
        densities = defaultdict(list)
        coin_HG, coin_BG, coin_HD, coin_BD = [], [], [], []

        for i, rect in enumerate(remaining_rectangles):
            coin_HG, coin_BG, coin_HD, coin_BD = getCoins(current_grid)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(simulate, sim, rect, n, coin_HG, coin_HD, coin_BG, coin_BD, remaining_rectangles, big_rectangle, placed_rectangles, current_grid, i) for sim in range(n)]

            for future in concurrent.futures.as_completed(futures):
                density, placement_info = future.result()
                if density != None:
                    densities[density].append(placement_info)

        if not densities:
            break

        max_density = max(densities.keys())
        i, best_rectangle, new_grid = random.choice(densities[max_density])

        placed_rectangles.append(best_rectangle)
        remaining_rectangles.pop(i)
        current_grid = new_grid


    return placed_rectangles, current_grid, current_grid.CalcDensity()

import sys
import os
import random

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def main_mcs(fich):
    fichier = fich
    small_rectangles = []
    try:
        with open(fichier) as f:
            first_line = f.readline()
            a, b = [int(i) for i in first_line.split()]
            big_rectangle = Rectangle(0, 0, a, b)
            g = Grid(b, a)
            for line in f:
                a, b = [int(i) for i in line.split()]
                small_rectangles.append(Rectangle(0, 0, a, b))
            sorted_rectangles = sorted(small_rectangles, key=lambda r: r.width * r.height, reverse=True)
            start_time = time.time()
            a, b, c = mcs(sorted_rectangles, big_rectangle, g, 50)
            end_time =time.time() - start_time
            print(end_time)
            print(c)
            return end_time, c
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)


def main():
    for i in range(1,4):
        if i == 1:
            for j in range(10, 11):
                fichier = "data_files/"+str(j)+".txt"
                file1 = open("tests_temps0_pb"+str(j)+".txt", "w")
                file1.write("Fonction  probleme  temps densité\n")
                for n in range(0, 5):
                    x, y = main_mcs(fichier)
                    file1.write("mcs"+" "+str(x)+" "+str(y)+"\n")
                file1.close()
        elif i == 2:
            for j in range(9, 10):
                fichier = "data_files/12/"+str(j)+"guillotine.txt"
                file1 = open("tests_temps12_pb"+str(j)+".txt", "w")
                file1.write("Fonction  temps densité\n")
                for n in range(0, 3):
                    x, y = main_mcs(fichier)
                    file1.write("mcs n12"+" "+str(x)+" "+str(y)+"\n")
                file1.close()
        elif i == 3:
            for j in range(9, 10):
                fichier = "data_files/13/"+str(j)+"guillotine.txt"
                file3 = open("tests_temps13_pb"+str(j)+"guillotine.txt", "w")
                file3.write("Fonction  temps densité\n")
                for n in range(0, 3):
                    x, y = main_mcs(fichier)
                    file3.write("mcs n13"+" "+str(x)+" "+str(y)+"\n")
                file3.close()
        elif i == 4:
            for j in range(2, 10):
                fichier = "data_files/14/"+str(j)+"guillotine.txt"
                file4 = open("tests_temps14_pb"+str(j)+"guillotine.txt", "w")
                file4.write("Fonction temps densité\n")
                for n in range(0, 3):
                    x, y = main_mcs(fichier)
                    file4.write("mcs n12"+" "+str(x)+" "+str(y)+"\n")
                file4.close()
        elif i == 5:
            for j in range(0, 10):
                fichier = "data_files/15/"+str(j)+"guillotine.txt"
                file5 = open("tests_temps15_pb"+str(j)+"guillotine.txt", "w")
                file5.write("Fonction  temps densité\n")
                for n in range(0, 3):
                    x, y = main_mcs(fichier)
                    file5.write("mcs n15"+" "+str(x)+" "+str(y)+"\n")
                file5.close()
        elif i == 6:
            for j in range(0, 10):
                fichier = "data_files/16/"+str(j)+"guillotine.txt"
                file6 = open("tests_temps16_pb"+str(j)+"guillotine.txt", "w")
                file6.write("Fonction  temps densité\n")
                for n in range(0, 3):
                    x, y = main_mcs(fichier)
                    file6.write("mcs n16"+" "+str(x)+" "+str(y)+"\n")
                file6.close()


if __name__=="__main__":

     main()
