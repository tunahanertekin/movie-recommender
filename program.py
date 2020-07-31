import numpy as np
from scipy import spatial
from progressbar import ProgressBar

class User:
    def __init__(self, index, simRating):
        self.index = index
        self.simRating = simRating
    
class Movie:
    def __init__(self, index, weightedAverage):
        self.index = index
        self.weightedAverage = weightedAverage

class MovieInfo:
    def __init__(self, name, date, link):
        self.name = name
        self.date = date
        self.link = link
    
def getSparseMatrix(filename):
    

    SparseMatrix = [[0 for x in range(movieCount)] for y in range(userCount)] 

    with open("ml-100k/"+filename) as f:
        lines = [line.rstrip() for line in f]


    for i in lines:
        tempLine = i.split("\t")
        SparseMatrix[int(tempLine[0])-1][int(tempLine[1])-1] = int(tempLine[2])


    for movie in range(0,len(SparseMatrix[0])):
        movieRatingSum = 0
        voteCount = 0
        for user in range(0,len(SparseMatrix)):
            if SparseMatrix[user][movie]!=0:
                movieRatingSum = movieRatingSum + SparseMatrix[user][movie]
                voteCount = voteCount + 1

        for user in range(0,len(SparseMatrix)):
            if voteCount == 0:
                SparseMatrix[user][movie] = 2.5
            elif SparseMatrix[user][movie]==0:
                SparseMatrix[user][movie] = movieRatingSum/voteCount

    UsersAverageRatings = [ 0 for x in range(userCount)]
    for user in  range(0, len(SparseMatrix)):
        average = sum(SparseMatrix[user])/len(SparseMatrix[user])
        UsersAverageRatings[user] = average
        for movie in range(0, len(SparseMatrix[0])):
            SparseMatrix[user][movie] = SparseMatrix[user][movie]-average

    return SparseMatrix, UsersAverageRatings

def findWeightedAverageOfMovie(targetUserId, movieId, similarUsers):
    totalTop = 0
    totalDown = 0

    #applying formula
    for i in similarUsers:
        totalTop = totalTop + Sparse[i.index][movieId]*(1-i.simRating)
        totalDown = totalDown + (1-i.simRating)

    WeightedAverageOfMovie = totalTop/totalDown + UsersAverageRatings[targetUserId]

    return WeightedAverageOfMovie

def getSimilarUsers(targetUserId, kNN):
    Degrees = [User(0,0.0) for x in range(userCount)]

    for user in range(0, userCount):
        Degrees[user] = User(user, spatial.distance.cosine(Sparse[targetUserId], Sparse[user]))

    Degrees.sort(key=lambda User: User.simRating)
    Degrees.pop(0)#pop user himself

    return Degrees[:kNN]

def getFirstNMovies(targetUserId, kNN, n):
    MovieRecommendList = [ Movie(0,0.0) for x in range(movieCount)]
    SimilarUsers = getSimilarUsers(targetUserId, kNN)
    
    for movie in range(0, len(MovieRecommendList)):
        MovieRecommendList[movie].index = movie
        MovieRecommendList[movie].weightedAverage = findWeightedAverageOfMovie(targetUserId, movie, SimilarUsers)

    MovieRecommendList.sort(reverse=True, key=lambda Movie: Movie.weightedAverage)
    return MovieRecommendList[:n]

#Main Code Starts Here

print("DVD/Film Öneri Sistemi\n")
userCount = 943
movieCount = 1682

MovieInfoArr = [ MovieInfo('x','x','x') for x in range(movieCount)]

with open("ml-100k/u.item") as f:
    lines = [line.rstrip() for line in f]

for i in lines:
    tempLine = i.split("|")
    MovieInfoArr[int(tempLine[0])-1] = MovieInfo(tempLine[1], tempLine[2], tempLine[4])

print("1. Kullanıcıya En Çok Benzeyen Kullanıcıların Listesi")
print("2. Kullanıcının Bir Filme Vereceği Puan Tahmini")
print("3. Film Önerileri")
print("4. Test")
print("5. Çıkış")

choice = '0'

while choice != 5:
    print()
    choice = input("Seçim: ")
    print()
    if choice == '1':
        Sparse, UsersAverageRatings = getSparseMatrix("u1.base")
        targetUserId = int(input("Kullanıcı ID Numarası(0-943): "))
        kNN = int(input("kNN Derecesi(en benzer kaç kullanıcı seçilsin?): "))
        SimilarUsers = getSimilarUsers(targetUserId, kNN)
        print()
        for i in SimilarUsers:
            print(i.index," -> ",i.simRating)
    elif choice == '2': 
        Sparse, UsersAverageRatings = getSparseMatrix("u1.base")
        targetUserId = int(input("Kullanıcı ID Numarası(0-943): "))
        movieId = int(input("Film ID Numarası(0-1682): "))
        kNN = int(input("kNN Derecesi(en benzer kaç kullanıcı seçilsin?): "))
        SimilarUsers = getSimilarUsers(targetUserId, kNN)
        WA = findWeightedAverageOfMovie(targetUserId, movieId, SimilarUsers)
        print()
        print(targetUserId,"ID'li kullanıcının",movieId,"ID'li filme vereceği tahmini puan:", WA)
    elif choice == '3':
        Sparse, UsersAverageRatings = getSparseMatrix("u1.base")
        targetUserId = int(input("Kullanıcı ID Numarası(0-943): "))
        kNN = int(input("kNN Derecesi(en benzer kaç kullanıcı seçilsin?): "))
        howMany = int(input("Önerilecek film sayısı:"))
        MovieRecommendList = getFirstNMovies(targetUserId, kNN, howMany)
        print()
        for i in MovieRecommendList:
            print(i.index," -> ", MovieInfoArr[i.index].name)
    elif choice == '4':
        kNN = int(input("kNN Derecesi(en benzer kaç kullanıcı seçilsin?): "))
        dataset = input("Veri seti numarası(1-5):")
        
        
        #for dataset in range(1,6):
        #    for kNNX in range(1,6):
        ds = str(dataset)
        #kNN = kNNX*10
        Sparse, UsersAverageRatings = getSparseMatrix("u"+ds+".base")

        with open('ml-100k/u'+ds+'.test') as f:
            lines = [line.rstrip() for line in f]

        SumMSE = 0
        rowCount = 0
        activeUser = -1
        pbar = ProgressBar()

        for i in pbar(lines):
            tempLine = i.split("\t")
            if activeUser != tempLine[0]:
                tempSimilarUsers = getSimilarUsers(int(tempLine[0]), kNN)
                activeUser = tempLine[0]
            SumMSE = SumMSE + (findWeightedAverageOfMovie(int(tempLine[0]), int(tempLine[1]), tempSimilarUsers) - int(tempLine[2]))**2
            rowCount = rowCount + 1
            
        MSE = SumMSE/rowCount

        print()
        print("MSE(kNN = ",kNN,", dataset #",dataset,"):",MSE)
    elif choice=='5':
        print("done")
    else:
        print("wrong input")

exit()

