import random

def Guillotine_par2(nb, size):
    list_rect = []
    x = size
    y = size
    list_rect.append([x, y])
    n = 16

    file = open(str(nb) + "guillotine.txt", "w")
    file.write(str(x) + " " + str(y) + "\n")
    i = 0
    while i < n-1:
        nb = random.randint(0, len(list_rect) - 1)
        xory = random.randint(0,1)
        if xory == 1:
            if (list_rect[nb][0]-1)>1:
                xrand = random.randint(1, list_rect[nb][0]-1)
                list_rect.append([list_rect[nb][0]-xrand, list_rect[nb][1]])
                list_rect.append([(list_rect[nb][0])-(list_rect[nb][0]-xrand), list_rect[nb][1]])
                if len(list_rect) > 2:
                    del list_rect[nb]
                i+=1
        else:
            if (list_rect[nb][1]-1)>1:
                yrand = random.randint(1, list_rect[nb][1]-1)
                list_rect.append([list_rect[nb][0], list_rect[nb][1]-yrand])
                list_rect.append([list_rect[nb][0], list_rect[nb][1]-(list_rect[nb][1]-yrand)])
                if len(list_rect) > 2:
                    del list_rect[nb]
                i += 1
    print(list_rect)
        
    for i in range (0,len(list_rect)):
        file.write(str(list_rect[i][0]) + " " + str(list_rect[i][1]) + "\n")

    file.close()

def main():
    for i in range(0,10):
        Guillotine_par2(i, 30)

if __name__=="__main__":
    main()
