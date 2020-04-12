import copy
from queue import PriorityQueue
from time import perf_counter 

#down, left, up, right
moveRow= [1, 0, -1, 0] 
moveCol= [0, -1, 0, 1]

# state akhir matriks
finalMatrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

#kelas node (simpul)
class Node:
    def __init__(self, parent, matrix, row, col, cost, level):
        self.parent = parent
        self.matrix = copy.deepcopy(matrix)
        self.row = row
        self.col = col
        self.cost = cost
        self.level = level

#priority entry, untuk mngeatur priority queue
class PriorityEntry(object):
    def __init__(self, priority, data, navigation):
        self.navigation = navigation
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

# Fungsi ini membaca matriks dari file eksternal dan mengembalikan matriks hasil pembacaan
# file eksternal tersebut
def filetoMatrix(file):
    matrix = []
    with open(file) as f:
        for item in f:
            matrix.append([int(i) for i in item.split()])
    return matrix

# I.S. Matriks terdefinisi
# F.S. Matriks tercetak pada layar dengan format tampilan 15-puzzle game
def printMatrix(matrix):
    print("|-------|-------|-------|-------|")
    for i in range(4): 
        print("|", end = " ")
        for j in range(4): 
            if(matrix[i][j] != 16):
                print(" ",matrix[i][j],"\t|", end = " ") 
            else:
                print("  \t|", end = " ")
        print() 
        print("|-------|-------|-------|-------|")

# Fungsi untuk menghitung nilai total fungsi kurang dan menampilkan nilai fungsi kurang
# untuk setiap ubin
def countInversi(matrix):
    arraytemp = []
    arrayCountInversi = [0 for i in range (17)]
    for i in range (4):
        for j in range (4):
            arraytemp.append(matrix[i][j])
    
    inversiTotal = 0;
    for i in range (16):
        inversi = 0
        for j in range (i, 16):
            if(arraytemp[i] > arraytemp[j]):
                inversi += 1
                inversiTotal+=1;
        arrayCountInversi[arraytemp[i]] = inversi

    for i in range (1, 17):
        print("Ubin", i, "=", arrayCountInversi[i])

    return inversiTotal

# Fungsi untuk mencari nilai X
def defineX(row, col):
    if((row+col)%2 == 1):
        return 1
    else:
        return 0;

# Fungsi untuk mencari posisi ubin kosong pada koordinat matriks
def searchEmptyBlock(matrix, row, col):
    found = False
    i = 0
    while (not found and i < 4):
        j = 0
        while (not found and j < 4):
            if(matrix[i][j] == 16):
                found = True
            else:
                j+=1
        
        i+=1
    row = i-1
    col = j

    return (row, col)


# I.S. child dan parent berupa node yang terdefinisi
# F.S. Arah pergerakan dari parent ke child note tercetak di layar
def printNavigation(child, parent):
    if(child.row - parent.row == 1):
        print(">> down")
    elif(child.col - parent.col == -1):
        print(">> left")
    elif(child.row - parent.row == -1):
        print(">> up")
    elif(child.col - parent.col == 1):
        print(">> right")

# Fungsi untuk mengalokasikan node baru
def allocNode(matrix, row, col, newrow, newcol, level, parent): 
    node = Node(parent, matrix, row, col, 0, level)
    
    #swapping
    temp = node.matrix[row][col]
    node.matrix[row][col] = node.matrix[newrow][newcol]
    node.matrix[newrow][newcol] = temp

    node.row = newrow
    node.col = newcol

    return node 

# Memeriksa kotak kosong masih berada pada koordinat matriks yang valid
def isSafe(x, y):
    return (x >= 0 and x < 4 and y >= 0 and y < 4)

# Menghitung cost atau g(i) untuk simpul tertentu
def calculateCost(initialMat, finalMat):
    cost = 0
    for i in range (4):
        for j in range (4):
            if(initialMat[i][j] != 16 and initialMat[i][j] != finalMat[i][j]):
                cost += 1
    
    return cost

# I.S. node terdefinisi mungkin None
# F.S. navigasi dan matriks seluruh jalur tercetak pada layar
def printPath(node):
    if(node.parent is None):
        print("Langkah penyelesaian:", end="")
    else:
        printPath(node.parent)
        print()
        printNavigation(node, node.parent)
        printMatrix(node.matrix)

# algortima penyelesaian persoalan dengan menggunakan branch and bound
def solveBnB(initialMat, row, col, finalMat):
    countNode = 0
    pq = PriorityQueue()

    root = allocNode(initialMat, row, col, row, col, 0, None)
    countNode += 1
    root.cost = calculateCost(initialMat, finalMat)
    rootEntry = PriorityEntry(root.level + root.cost, root, None)
    pq.put(rootEntry)

    while (not (pq.empty())):
        # Find a live node with least estimated cost 
        min = pq.get().data
    
        if (min.cost == 0) :
            printPath(min)
            print(">> Jumlah simpul yang dibangkitkan = ", countNode)
            break
        
        else: 
            for i in range (4): 
                if (((min.parent is None) or (min.col + moveCol[i]!=min.parent.col and min.row + moveRow[i]!=min.parent.row)) 
                and (isSafe(min.row + moveRow[i], min.col + moveCol[i]))):
                    child = allocNode(min.matrix, min.row, min.col, min.row + moveRow[i], min.col + moveCol[i], min.level + 1, min)
                    countNode += 1
                    child.cost = calculateCost(child.matrix, finalMat)
                    childEntry = PriorityEntry(child.level + child.cost, child, i)
  
                    pq.put(childEntry)



