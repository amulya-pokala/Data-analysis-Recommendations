from math import sqrt

import csv                          # a module in python. There is no need to install this
movieFile = open('movies.csv')      # opening a csv file. For excel files we can use openPYXL
movieReader = csv.reader(movieFile)  # creating a reader object on movieFile
movieDict={}                        # a dictionary to store the movie id as the key and the value as a list of movie name and it's genres
for row in movieReader:             # iterating through movieReader
    li=[row[1]]                     # li contains movie name and genres for each movie id and is appended to the dict value 
    genre=""            
    for i in range(0,len(row[2])):    # itearting through string of genres for each movie id
        if (row[2])[i]!='|':            # when we encounter a  '|', we understand that reading a genre has been
                                        #completed  and if more genres are there we need to read them
            genre=genre+(row[2])[i]     # appending each character
            
        
        else:
            li.append(genre)            # appending genre to a list
            genre=""                    
    movieDict[row[0]]=li                


# printing the key and values of the dictionary
'''for key,value in movieDict.items():
    print key,value
    print '\n'
'''


userFile = open('ratings.csv')     
userReader = csv.reader(userFile)
count=0
userDict={}
for row in userReader:
    if count==0:
        count=count+1
        continue
    
    if int(row[0]) not in userDict:
        userDict[int(row[0])]={}
        (userDict[int(row[0])])[int(row[1])]=float(row[2])
    else:
       (userDict[int(row[0])])[int(row[1])]=float(row[2])

"""for key,value in userDict.items():  # uncomment them to see what is there in userDict
    print key,value
    print '\n'"""


#getting similarity score
def pear(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    # Find the number of elements
    n = len(si)
    # if they are no ratings in common, return 0
    if n == 0:
        return 0
    # Add up all the preferences
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    # Sum up the squares
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    # Sum up the products
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den
    return r

#sorting based on rating in descending order
def func(input):
    return input[1]

# Gets recommendations for a person by using a weighted average
#  of every other user's rankings
def getRecom(prefs, person, similar=pear):
    totals = {}
    simSums = {}
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        sim = similar(prefs, person, other)
        # ignore scores of zero or lower
        if sim <= 0:
            continue
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    # Create the normalized list

    rank = [(str(item), total / simSums[item]) for item, total in totals.items()]
    # Return the sorted list
    rank.sort(key=func)
    rank.reverse()
    return rank


user=input('Enter user to generate recomendations: ')
#generate recomendations
ans=getRecom(userDict,user)
count=0;

#printing movies along with their score in descending order
for i in ans:
    for j in movieDict:
        if i[0]==j:
            if(count<10):
                count=count+1
                print i[0],movieDict[j],i[1]
            else:
                break





outputFile = open('output.csv', 'w')
fieldNames=['Movie Id','Movie Name','Rating']
outputWriter = csv.DictWriter(outputFile, fieldnames=fieldNames)
count=0
outputWriter.writeheader()
for i in ans:
    for j in movieDict:
        if i[0]==j:
            if count<10:
                count+=1
                
                outputWriter.writerow({'Movie Id':i[0],'Movie Name':movieDict[j],'Rating':int(i[1])})
                
            else:
                break
outputFile.close()
            







