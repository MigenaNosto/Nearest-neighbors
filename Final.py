import sys
import os
import random
import time
import tkinder as tk




#MyReadDataRoutine() will create a frozenset for the words found in a doc
#and then add it to a list , the wordsets
def MyReadDataRoutine():
    wordsets=[] #list of frozenset
    word_list=[]
    keep=[]
    i=0
    #i increases when we are done with the first fset
    while i<numDocuments:
        word_list.append(tuple(f.readline().split())) #add the word to the word_list
        if word_list[-1][0]!=(i+1): #this checks if i just read the first word of the next doc,which we will always do
            keep=word_list[-1] #keep the last word that was read
            word_list=word_list[:-1] #and delete it
            fword=frozenset(tuple(word_list)) #create the frozenset
            wordsets.append(fword) #and add it to the wordset
            word_list.clear() #empty the word_list so that it is readey for the next fset
            word_list.append(keep) #add the first word of the next fset we just read
            i=i+1

    return wordsets


# MyJacSimWihSets() will find the jaccard simillarity of two documents
# with 2 for loops iterating through the worset and finding common wordIds
def MyJacSimWihSets(docID1, docID2):
    k=0
    q=0
    interSectionCount=0 #keep track of common words
    i=3

    for i in wordsets[docID1-1]: #iterate through the frozenset of docID1
        i_marks=iter(i) #iterate through each tuple found in the frozenset 1
        next(i_marks) #read the firsttoken of the tuple, it represents the docID1, we do not need it
        wordID1=next(i_marks) #and keep track of each wordID in this frozenet
        for j in wordsets[docID2-1]:#iterate through the frozenset of docID2
            j_marks=iter(j) #iterate through each tuple found in the frozenset 2
            next(j_marks)#read the firsttoken of the tuple, it represents the docID2, we do not need it
            wordID2=next(j_marks) #and keep track of each wordID in this frozenet
            if wordID1==wordID2:
                interSectionCount=interSectionCount+1 # same wordIds just found
    #print('interSectionCount in MyJacSimWihSets is :', interSectionCount)
    simWithSets= interSectionCount /(len(wordsets[docID1-1]) + len(wordsets[docID2-1]) - interSectionCount ) # |𝐴 ∪ 𝐵| = |𝐴| + |𝐵| − |𝐴 ∩ 𝐵|



# MyJacSimWithOrderedLists will find the jaccard simillarity of two documents, sorting each frozenset and
# using two pointers, one for each frozenset and comparing to find common words
def MyJacSimWithOrderedLists(docID1, docID2):
        pos1=0 #pointer to frozenset of docID1
        pos2=0 #pointer to frozenset of docID2
        interSectionCount=0 #keep track of common words
        L1=sorted(wordsets[docID1-1]) #now frosenset 1 is sorted and with no multiple numbers
        L2=sorted(wordsets[docID2-1]) #now frosenset 2 is sorted and with no multiple numbers
        len1=len(L1)
        len2=len(L2)

        #while both pointers are showing to some tuple of each frosenset
        while pos1<len1 and pos2<len2:
            i_marks=iter(L1[pos1]) #iterate through each tuple found in the frozenset 1
            next(i_marks) #read the first token of the tuple, it represents the docID1, we do not need it
            wordID1=next(i_marks) #and keep track of each wordID in this frozenet 1
            j_marks=iter(L2[pos2]) #iterate through each tuple found in the frozenset 2
            next(j_marks) #read the firsttoken of the tuple, it represents the docID2, we do not need it
            wordID2=next(j_marks) #and keep track of each wordID in this frozenet 2
            if wordID1==wordID2: # if common wordid is found increase interSectionCount and move both pointers
                interSectionCount=interSectionCount+1
                pos1+=1
                pos2+=1
            else: #move the pointer showing to the smaller wordid
                if wordID1<wordID2:
                    pos1+=1
                else:
                    pos2+=1

        simWithOrderedLists= interSectionCount /(len(wordsets[int(docID1)-1]) + len(wordsets[docID2-1]) - interSectionCount ) # |𝐴 ∪ 𝐵| = |𝐴| + |𝐵| − |𝐴 ∩ 𝐵|

        return simWithOrderedLists


#create_random_hash_function() ....creates a random hash function.
def create_random_hash_function(p=2**33-355, m=2**32-1):
    a=random.randint(1,p-1)
    b=random.randint(0,p-1)
    return lambda x: 1+(((a * x + b) % p) % m)


#randomHash_dict() create a dictionary of hashed items
def randomHash_dict():
    h=create_random_hash_function() #create a new hash fanction
    randomHash= {  j:h(j) for j in range(W)} #add each key:its hashed number in a dictionary
    myHashKeysOrderedByValues = sorted(randomHash, key = randomHash.get)
    myHash = {myHashKeysOrderedByValues[x]:x for x in range(W)} #sort the dictionary based on the value
    return myHash

#MyMinHash() creates a list of lists containing the docIds for each wordID and then it creates the SIG array
def MyMinHash(documentsList, k):
    wordlist=[] #list of lists containing the docIds

    for i in range(W): #create an empty list of lists wordlist
        wordlist.append([])
    for i in range(numDocuments): #find each frozenset in wordset
        for j in wordsets[i]:#find each word in frozenset
            j_marks=iter(j)
            doc=next(j_marks) #keep docID of tuple
            word=next(j_marks) #keep wordID of tuple
            wordlist[int(word)-1].append(int(doc)) #add the docID found in the list shown by wordId in wordlist

    #SIG is signature array
    SIG = [[ '_' for j in range(numDocuments)] for i in range(k)]
    h = [ randomHash_dict() for i in range(k)] #create a list of premutations

    for row in range(W) : #shows to each row-word in wordlist
        for docid in wordlist[row]: #shows in each docid of each word in wordlist
            for i in range(k): #for each premutation
                if SIG[i][docid-1]=='_': #if certain cell of SIG is empty fill it
                    SIG[i][docid-1]=h[i][row] #with the right hashed value from h list
                elif h[i][row]<SIG[i][docid-1]:# certain cell of SIG has a number smaller than the hashed value found
                    SIG[i][docid-1]=h[i][row] #replace it

    return SIG


#MySigSim() compares the signatures of each doc and computes
#their similarity
def MySigSim(docID1,docID2,numPermutations):

    list_sig1=[]
    list_sig2=[]
    pos=0
    interSectionCount=0

    #create the sigantures of each doc
    for i in range(numPermutations):#iterate through SIG[] with certain docIDs
        list_sig1.append(SIG[i][docID1]) #sigantures of doc1
        list_sig2.append(SIG[i][docID2]) #sigantures of doc2

    Sorted_sig1=sorted(list_sig1) #now dignature of doc1 is sorted and with no multiple numbers
    Sorted_sig2 = sorted(list_sig2) #now dignature of doc2 is sorted and with no multiple numbers
    len1=len(Sorted_sig1)
    len2=len(Sorted_sig2)

    #while the pointer is showing to some num of each signature
    while pos<len1 and pos<len2:

        if Sorted_sig1[pos]==Sorted_sig2[pos]: #if same premutation in signatures is found
            interSectionCount=interSectionCount+1 #increase interSectionCount
        pos+=1 #move position by 1

    SigSim = interSectionCount/numPermutations



    return SigSim



#BryteForce() finds the NumNeighbors closest neighbors for all doc
#with jaccard or signature similarity for each doc (1...numDocuments-1)
#we used MyJacSimWithOrderedLists because its the fastest one
def BruteForce(len_of_list,choose_Sim,numPermutations):

    finalAvg=0
    final_Sum_of_Avg=0

    for docid1 in range(len_of_list):
        dist_dic = {} #dict to keep distance of each document from docid1
        myNeighborsDict={}#this will be the sorted by value version of sig_dist_dic
        Sum=0 #keep track of similarities of docid1 with its first NumNeighbours neighbours

        #when this for is finished dist_dic will be filled with distances from docID1 to each docid2
        for docid2 in range(len_of_list):
            if docid1 != docid2: #avoiding doc1
                if choose_Sim==0: #if we want jaccard similarity
                    seconds0 = time.time() #keep track of time before finding jaccard sim
                    Sim= MyJacSimWithOrderedLists(docid1,docid2)
                    seconds1 = time.time()#keep track of time after Jaccard sim
                else:#if we want signature similarity
                    seconds0 = time.time()#before finding Signature sim
                    Sim = MySigSim(docid1, docid2, numPermutations)
                    seconds1 = time.time()#keep track of time after finding Signature sim


                Seconds = seconds1- seconds0 #total time for one similarity comparison
                dist = 1 - Sim #find distance between docid1 and docid2
                dist_dic.update({docid2: dist}) #fill dictionary with keys=docid, value=distacne of docid2 from docid1
                if docid2<len_of_list:#find the sum of similarity for the first NumNeighbors neighbours with docid1
                    Sum = Sum+ Sim

        #create a list that keeps the sorted keys based on their values
        dic_orderedByValues= sorted(dist_dic, key=dist_dic.get)

        for t in range(NumNeighbors):
            Mykey = dic_orderedByValues[t]#find the key from sorted list
            myValue = dist_dic.get(Mykey) #now find te value of the previous key from jac_dist_dic
            myNeighborsDict.update({Mykey: myValue}) #this will have the first NumNeighbors neighbors by distance
        if t!=0:
            AvgSim= Sum/t #average jaccard simsilarity for some docid1 with the first NumNeighbors neighbours
        else:
            AvgSim=Sum

        final_Sum_of_Avg = final_Sum_of_Avg + AvgSim #final jaccard similarity for all docid1 to their neighbors
    finalAvg = final_Sum_of_Avg/float(numDocuments) #final average jaccard similarity

    return finalAvg






#LSH() finds the NumNeighbors closest neighbors for all doc
#with jaccard or signature similarity for each doc (1...numDocuments-1)
def LSH(SIG, rowsPerBand):

    LSHdicts ={}
    row=0
    counter=0
    docID=0
    hashLSH= create_random_hash_function()
    value=0
    value_list=[]
    sorted_LSH_dict={}
    AvgSim=0
    i=0
    flag=0
    while i< k: #make sure we do not read more lines than those that SIG has
        if docID<numDocuments: #in this case there are more docid sig to be read for this band
            if row < rowsPerBand: #there are more rows to be read for this signature of this doc
                value = SIG[row][docID]
                value_list.append(value) #make the list that keeps the signature for this docid
                row=row+1 #keep track of the rows ....do not read other band
                i=i+1
            else:#there are no more rows for this band
                valueTuple = tuple(value_list)
                t1= hash(valueTuple)
                LSHdicts.update({docID : hashLSH(t1)})#populate the dic that keeps docids as keys and their hashed signature as value
                value_list = []
                docID=docID +1
        else:#there are no more signatures for this band
            docID=0
            row=0
            value_list = []

            #sort the dict by values
            sorted_LSH_dict ={k: v for k, v in sorted(LSHdicts.items(), key=lambda item: item[1])}

            sorted_LSH_dict_LIST = list(sorted_LSH_dict.items())#create a list from the sorted dict
            #

            #iterate through the list of the sorted dict in order to find same hashed values
            for i in range(len(sorted_LSH_dict_LIST)):
                same_bucket=[] #keep docid with the same hashed value

                same_bucket.append(sorted_LSH_dict_LIST[i][0])

                for j in range(len(sorted_LSH_dict_LIST)):
                    if i!=j:
                        if sorted_LSH_dict_LIST[i][1]==sorted_LSH_dict_LIST[j][1]:
                            same_bucket.append(sorted_LSH_dict_LIST[j][0])#we found docid2 with the same hashed value as the docid1
                if len(same_bucket)>(NumNeighbors-1):#if docid1 has more neighbors than neighbours-1 then compare them
                    flag=1
                    AvgSim =AvgSim+ BruteForce(len(same_bucket),choose_Sim,numPermutations) #keep track of the average similarity that BruteForce returns
    if flag==0: #in this case no docid hade more than neigbors-1 neighbors...inform user and change rowsPerBand
        return 1


    print("AvgSim is:",  AvgSim/numBands)







 window = tk.Tk()
 
name = input("Enter name of document:")
f = open(name +'.txt','r')
D= int(f.readline())
W= int(f.readline())
NNZ=int(f.readline())

numDocuments= int(input("Give number of documents, whick must be less than "+ str(D)+":" ))
while numDocuments > D: #chck for logical numDocuments
    numDocuments= int(input("Give number of documents, whick must be less than "+ str(D)+":" ))
wordsets=MyReadDataRoutine()
NumNeighbors=int(input("Give a small number of neighbors: "))
k= int(input("Give number of permutations:"))
randomHash_dict()
SIG = MyMinHash(wordsets, int(k))
choose_Sim=int(input("Choose between Jaccard and Signature similarity. Press 0 for jaccard and 1 for signature:"))
if choose_Sim==1: #Signature similarity
    numPermutations= int(input("Choose the num of permutations, you want to work with: "))
    while(numPermutations>k): #check for logical numPermutations
        numPermutations= int(input("Choose the num of permutations, you want to work with: "))
else:
    numPermutations=0# Jaccard similarity we do not need numPermutations
choose_method=int(input("Choose between BrudeForse and LSH method. Press 0 for BrudeForse and 1 for LSH:"))

if choose_method==1: #LSH

    rowsPerBand = int(input("Give number of rows per band:"))
    numBands = int(k)/int(rowsPerBand)
    s=(1/numBands) ** (1/rowsPerBand)
    q=0
    timeforlsh=0
    lsh_second1= time.time()#Keep time for LSH computaion
    lshret=LSH(SIG, rowsPerBand)
    lsh_second2= time.time()
    timeforlsh=lsh_second2-lsh_second1
    while lshret==1 : #if LSH return 1 then no docid hade enough neigbors ... need to change rowsPerBand
        print("The number of rows per band is too big.")
        q=int(input("If you want to let the computer choose an apropriate of number of rows per band press 1. If you want to choose a new one press 0. "))
        if q==0:
            rowsPerBand = int(input("Give number of rows per band:"))
        elif q==1:
            rowsPerBand=rowsPerBand/2
            if rowsPerBand == 0:
                rowsPerBand=1
                break

        else :
            print("You must choose 1 for computer or 0.")
        numBands = int(k)/rowsPerBand
        s=(1/numBands) ** (1/rowsPerBand)
        lsh_second1= time.time()
        lshret=LSH(SIG, rowsPerBand)
        lsh_second2= time.time()
        timeforlsh=lsh_second2-lsh_second1
    print("ExecTime for LSH is:",timeforlsh)
    if q==1:
        print("The rowsPerBand that the computer chose is ,",rowsPerBand)

else:


    sec1= time.time()
    AvgSim= BruteForce(numDocuments,choose_Sim,numPermutations)
    print("AvgSim is", AvgSim)
    sec2= time.time()
    seconds= sec2-sec1
    print("ExecTime for BruteForce is", seconds)


a=int(input("If you want to compute the Jaccard similarity for certain documents press 1, else press 0. "))
if a==1:
    docID1=int(input('Give random docID1, which must be from 1 to '+str(numDocuments) +': '))
    docID2=int(input('Give random docID2, which must be from 1 to '+str(numDocuments)+': '))
    while docID1>numDocuments or docID2>numDocuments: #check for logical docid and docid2
        print('You gave wrong docID1 or docID2.')
        docID1=int(input('Give random docID1, which must be from 1 to '+str(numDocuments)+': '))
        docID2=int(input('Give random docID2, which must be from 1 to '+str(numDocuments)+': '))
    seconds0 = time.time() #keep track of MyJacSimWihSets computation time
    MyJacSimWihSets(docID1,docID2)
    seconds1 = time.time()#keep track of MyJacSimWithOrderedLists computation time
    MyJacSimWithOrderedLists(docID1, docID2)
    seconds2 = time.time()
    time_for_sets=seconds1-seconds0
    time_for_orderedLists=seconds2-seconds1
    e=int(input("If you want to compute the Signature similarity, press 1 "))
    if e==1:
        numPermutations=int(input("Give num of permutations to work with, which must be equal or less than the num of premutations: "))
        MySigSim(docID1-1,docID2-1,numPermutations)


f.close()
