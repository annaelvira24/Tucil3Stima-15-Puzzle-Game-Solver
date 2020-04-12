from BranchAndBound import *

idxRow = 0
idxCol = 0
inputfile = input("Masukkan file .txt yang ingin diuji ")
print(">> Kondisi awal Puzzle:")
initialMatrix = filetoMatrix(inputfile)
printMatrix(initialMatrix)
print(">> Nilai fungsi Kurang untuk tiap ubin :")
kurang = (countInversi(initialMatrix))
idxRow, idxCol = searchEmptyBlock(initialMatrix, idxRow, idxCol)
X = defineX(idxRow, idxCol)

print(">> Nilai sigma kurang =", kurang)
print(">> Nilai sigma kurang ditambah X =", kurang + X)
print()

if ((kurang + X)%2 != 0):
    print("Puzzle is Unsolvable :(")
else:
    print("Puzzle is Solvable :D")
    print()

    tStart = perf_counter()
    solveBnB(initialMatrix, idxRow, idxCol, finalMatrix)
    tStop = perf_counter()

    print(">> Waktu eksekusi =", tStop - tStart, "sekon")
