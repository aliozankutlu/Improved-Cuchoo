from random import uniform
from random import randint 
import math

# gr17 : optimal value2085
inputMatrix = [[0, 633, 257,  91, 412, 150,  80, 134, 259, 505, 353, 324,  70, 211, 268, 246, 121],
[633,   0, 390, 661, 227, 488, 572, 530, 555, 289, 282, 638, 567, 466, 420, 745, 518],
[257, 390,   0, 228, 169, 112, 196, 154, 372, 262, 110, 437, 191,  74,  53, 472, 142],
[ 91, 661, 228,   0, 383, 120,  77, 105, 175, 476, 324, 240,  27, 182, 239, 237,  84],
[412, 227, 169, 383,   0, 267, 351, 309, 338, 196,  61, 421, 346, 243, 199, 528, 297],
[150, 488, 112, 120, 267,   0,  63,  34, 264, 360, 208, 329,  83, 105, 123, 364,  35],
[ 80, 572, 196,  77, 351,  63,   0,  29, 232, 444, 292, 297,  47, 150, 207, 332,  29],
[134, 530, 154, 105, 309,  34,  29,   0, 249, 402, 250, 314,  68, 108, 165, 349,  36],
[259, 555, 372, 175, 338, 264, 232, 249,   0, 495, 352,  95, 189, 326, 383, 202, 236],
[505, 289, 262, 476, 196, 360, 444, 402, 495,   0, 154, 578, 439, 336, 240, 685, 390],
[353, 282, 110, 324,  61, 208, 292, 250, 352, 154,   0, 435, 287, 184, 140, 542, 238],
[324, 638, 437, 240, 421, 329, 297, 314,  95, 578, 435,   0, 254, 391, 448, 157, 301],
[ 70, 567, 191,  27, 346,  83,  47,  68, 189, 439, 287, 254,   0, 145, 202, 289,  55],
[211, 466,  74, 182, 243, 105, 150, 108, 326, 336, 184, 391, 145,   0,  57, 426,  96],
[268, 420,  53, 239, 199, 123, 207, 165, 383, 240, 140, 448, 202,  57,   0, 483, 153],
[246, 745, 472, 237, 528, 364, 332, 349, 202, 685, 542, 157, 289, 426, 483,   0, 336],
[121, 518, 142,  84, 297,  35,  29,  36, 236, 390, 238, 301,  55,  96, 153, 336,   0]] 
distanceMatrix = inputMatrix

# Levy ucusunun hesaplanması 
def levyFlight(u):
    return math.pow(u,-1.0/3.0)
#  Levy ucusunun hesaplanması icin kullanılan uniform deger
def randF():
    return uniform(0.0001,0.9999)

# Amac fonksiyon degerinin hesaplanmasi
def calculateDistance(path):
    index = path[0]
    distance = 0
    for nextIndex in path[1:]:
        distance += distanceMatrix[index][nextIndex]
        index = nextIndex
    return distance+distanceMatrix[path[-1]][path[0]];

# swap operatoru
def swap(sequence,i,j):
    temp = sequence[i]
    sequence[i]=sequence[j]
    sequence[j]=temp

# twoOptMove operatoru
def twoOptMove(nest,a,c):
    nest = nest[0][:]
    swap(nest,a,c)
    return (nest,calculateDistance(nest))

# doubleBridgeMove operatoru
def doubleBridgeMove(nest,a,b,c,d):
    nest = nest[0][:]
    swap(nest,a,b)
    swap(nest,b,d)
    return (nest , calculateDistance(nest))

# parametre atamalari
numNests = 9
pa = int(0.2*numNests)
pc = int(0.6*numNests)
maxGen = 300

# yuva sayısı
n = 199
# yuvalar arrayi
nests = []

# yuvaların ve yuvalara ait amac fonksiyonu degerlerinin atanmasi
initPath=range(0,n)
index = 0
for i in range(numNests):
    if index == n-1:
        index = 0
    swap(initPath,index,index+1)
    index+=1
    nests.append((initPath[:],calculateDistance(initPath)))
# amac fonksiyonu degerlerine göre yuvaların sıralanmasi
nests.sort(key=lambda tup: tup[1])
for t in range(maxGen):
    # Akilli guguk kusu degerlendirmesini pc oranında uygulanması
    cuckooNest = nests[randint(0,pc)]
    # Büyük perturbasyon degeri icin doubleBridgeMove isleminin uygulanmasi
    if(levyFlight(randF())>2):
        cuckooNest = doubleBridgeMove(cuckooNest,randint(0,n-1),randint(0,n-1),randint(0,n-1),randint(0,n-1))
    else:
    # Kücük perturbasyon degeri icin twoOptMove isleminin uygulanmasi
        cuckooNest = twoOptMove(cuckooNest,randint(0,n-1),randint(0,n-1))
   
    # n yuva icerisinden rassal olarak yuvanın secilmesi     
    randomNestIndex = randint(0,numNests-1)
    # iyilik kontrolu
    if(nests[randomNestIndex][1]>cuckooNest[1]):
        nests[randomNestIndex] = cuckooNest
    # pa oranında yuvalara degisimin yapılmasi    
    for i in range(numNests-pa,numNests):
        nests[i] = twoOptMove(nests[i],randint(0,n-1),randint(0,n-1))
    nests.sort(key=lambda tup: tup[1])	   
# en iyi yuva sonucu : [en kısa yol], mesafe 
print ("en iyi yuva sonucu : [en kısa yol], mesafe")	
print(nests[0])
