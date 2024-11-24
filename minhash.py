from __future__ import division

import pickle
from heapq import heapify,heappop,heappush
import random

totalShingles = 23880 #! Chia thanh 23880 Shingles!
pklHandler = open("docShingleDict.pkl", 'rb')
docShingleDict= pickle.load(pklHandler)
pklHandler.close()

def findRandomNos(k):
  randList = []
  randIndex = random.randint(0, totalShingles -1) 
  randList.append(randIndex) #! trong randList luc nay la cac index random 

  while k>0:
    while randIndex in randList: #! dam bao rang 
      randIndex = random.randint(0, totalShingles-1) 
    #1 sau vong while nay dam bao se khong bao gio random trung nhau. 
    randList.append(randIndex)
    k = k-1
  print("This is my randList: {}".format(randList))
  return randList
  

#! 25 is number of row in signature matrix!
randomNoA = findRandomNos(25)
randomNoB = findRandomNos(25)
#print("This is my random No A: {}".format(randomNoA))
#print("This is my random No B: {}".format(randomNoB))


docLowestShingleID = {} #! docLowestShingleID la signature matrix!
for doc in docShingleDict.keys():
  
  shingleIDSet = docShingleDict[doc]
  #print("shingleIDSet = {} for doc: {}".format(shingleIDSet, doc))
  #! Buoc nay de doc data trong file ShingleDict. <filenumber, List<int>IDNUMBER>
  lowestShingleID = []
  for x in range(0,25):
    listFx = [] #! listFx contain all hash Value
    for shingleID in shingleIDSet:
      hashValue = (randomNoA[x] * shingleID + randomNoB[x]) % totalShingles #! THIS IS MY HASH FUNCTION!
      listFx.append(hashValue)
    heapify(listFx) 
    lowestShingleID.append(heappop(listFx)) 
  docLowestShingleID[doc] = lowestShingleID #! docLowestShingleID la mot dict<fileNumber, linst<int>IDNUMBER> ma no la lowest ID
  #! luc nay docLowestShingleID se co value la hash function min nhat. Moi phan tu gom key va value, moi value la 1 list chua 25 gia tri hash.
print("This is doc lowest ShingleID: {}".format(docLowestShingleID))
#for doc in docLowestShingleID:
#  print doc, docLowestShingleID[doc]

def getFileNo(x):
  if x<10:
    x = "0" + str(x)
  else:
    x = str(x)
  
  return x

estimateMatrix = []
for x in range(0,100):
  doc1 = "file"+getFileNo(x)
  doc1LowestShingles = docLowestShingleID[doc1] #! we can call doc1LowestShingles is minhash signature
  col = []
  for y in range(0,100):
    doc2 = "file"+getFileNo(y)
    doc2LowestShingles = docLowestShingleID[doc2]
    count = 0
    for i in range(0,25):
      #! track number of value minHash signature equal
      if doc1LowestShingles[i] == doc2LowestShingles[i]:
        count = count + 1
        
    col.append(count/25)
  estimateMatrix.append(col)

#print("This is my estimateMatrix: {}".format(estimateMatrix))
  
print ("\nList of Documents with J(d1,d2) more than 0.5")
for x in range(0,50):
  file1 = "file" + getFileNo(x)
  for y in range(0,100):
    if estimateMatrix[x][y] > 0.5:
      file2 = "file" + getFileNo(y)
      if file1 != file2:
        shinglesSet1 = docShingleDict[file1]
        shinglesSet2 = docShingleDict[file2]
        print ("d1: " + file1 + " and d2: " + file2)
        print ("J(d1,d2): " + str(estimateMatrix[x][y])	)
        jaccard = (len(shinglesSet1.intersection(shinglesSet2)) / len(shinglesSet1.union(shinglesSet2)))
        print ("Jaccard coefficient: ", str(jaccard))
        #print 

docJaccard = {}

def pop(jaccardList):
  estimatedJaccardC, fileX = heappop(jaccardList)
  print (fileX)

print( "Three nearest neighbors for the first 10 files")

for x in range(0,10):
  file1 = "file" + getFileNo(x)
  estimatedJaccardList = []
  for y in range(0,100):
    file2 = "file" + getFileNo(y)
    if file1 != file2:
      heappush(estimatedJaccardList, (-estimateMatrix[x][y], file2))
  
  #print estimatedJaccardList
  print ("\n" + file1 + ":")
  for x in range(0,3):
    pop(estimatedJaccardList)
    
  


