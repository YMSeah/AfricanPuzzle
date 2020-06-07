from functools import lru_cache

#Grid-square Status Codes:{-1:impossible (conflicting)
#0:blank,1:filled,
#2:bottom-left filled,3:top-right filled,
#4:top-left filled,5:bottom-right filled}

#Piece orientation Status Codes:1 normal,2-4 are rotate cw 90deg.5 flipped r-l,6-8 are 5 rotate cw 90deg

@lru_cache(None)
def rotate(pieceLetter,orientation): #Returns a 4x4 grid containing the piece
    piece=pieces[pieceLetter] #rotated to the orientation. "pieceLetter" is a string eg. 'a'.
    #flip r-l
    flip={0:0,1:1,2:5,5:2,3:4,4:3}
    image=[[0 for _ in range(4)] for _ in range(4)]
    if orientation>4:
        for i in range(4):
            for j in range(4):
                image[i][j]=flip[piece[i][3-j]]
        piece=image
        orientation-=4

    #rotate90
    rotateDict={0:0,1:1,2:4,3:5,4:3,5:2}
    for _ in range(1,orientation):
        image=[[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                image[i][j] = rotateDict[piece[3-j][i]]
        piece=image
    #shift left
    leftCol=0
    while True:
        ok=True
        for i in range(4):
            if piece[i][leftCol]!=0:
                ok=False
                break
        if ok==False:
            break
        leftCol+=1
    image2=[[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(leftCol,4):
            image2[i][j-leftCol]=piece[i][j]
    piece=image2
    #shift up
    topRow=0
    while True:
        ok=True
        for i in range(4):
            if piece[topRow][i]!=0:
                ok=False
                break
        if ok==False:
            break
        topRow+=1
    image2=[[0 for _ in range(4)] for _ in range(4)]
    for i in range(topRow,4):
        for j in range(4):
            image2[i-topRow][j]=piece[i][j]
    piece=image2
    return piece
        
def deepCopy(grid): #Creates a deep copy of the 6x6 grid.
    grid2=[[0 for _ in range(6)] for __ in range(6)]
    for i in range(6):
        for j in range(6):
            grid2[i][j]=grid[i][j]
    return grid2

#Grid-square Status Codes:{-1:impossible (conflicting)
#0:blank,1:filled,
#2:bottom-left filled,3:top-right filled,
#4:top-left filled,5:bottom-right filled}

pieces={
'a':[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 4, 0, 0],
     [1, 2, 0, 0]],
'b':[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [5, 2, 0, 0],
     [3, 4, 0, 0]],
'c':[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [5, 1, 1, 2]],
'd':[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 5, 0, 0],
     [5, 1, 0, 0]],
'e':[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [2, 0, 0, 0],
     [1, 1, 4, 0]],
'f':[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [5, 1, 4, 0]],
'g':[[0, 0, 0, 0],
     [0, 5, 0, 0],
     [5, 1, 0, 0],
     [3, 4, 0, 0]]
}

possibleOrientations={'a':[1,2,3,4], #remove symmetries
                      'b':[1],
                      'c':[1,2,3,4],
                      'd':[1,2,3,4],
                      'e':[1,2,3,4,5,6,7,8],
                      'f':[1,2,5,6],
                      'g':[1,2,3,4,5,6,7,8]}

orientationMatches={(0,0):0,(0,1):1,(0,2):2,(0,3):3,(0,4):4,(0,5):5, #Given 2 orientation statuses on same grid square, return the resulting grid square status.
                    (1,0):1,(1,1):-1,(1,2):-1,(1,3):-1,(1,4):-1,(1,5):-1,
                    (2,0):2,(2,1):-1,(2,2):-1,(2,3):1,(2,4):-1,(2,5):-1,
                    (3,0):3,(3,1):-1,(3,2):1,(3,3):-1,(3,4):-1,(3,5):-1,
                    (4,0):4,(4,1):-1,(4,2):-1,(4,3):-1,(4,4):-1,(4,5):1,
                    (5,0):5,(5,1):-1,(5,2):-1,(5,3):-1,(5,4):1,(5,5):-1}


grid=[[0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0]]

def neatPrint(grid): #Prints the 6x6 grid neatly.
    for i in range(6):
        s=''
        for j in range(6):
            s=s+str(grid[i][j])
        print(s)
    print('\n')

def showLaidPieces(laidPieces): #Prints a 6x6 grid displaying all the laid pieces.
    grid=[[0 for _ in range(6)] for _ in range(6)]
    for piece,orientation,i,j in laidPieces:
        p=rotate(piece,orientation)
        for a in range(4):
            for b in range(4):
                if p[a][b]==1:
                    grid[i+a][j+b]=piece
                if p[a][b]==2 or p[a][b]==3:
                    grid[i+a][j+b]='\\'
                if p[a][b]==4 or p[a][b]==5:
                    grid[i+a][j+b]='/'
    neatPrint(grid)

def stickToGrid(g,piece,orientation,i,j): #Put piece onto grid. Updates grid.
    p=rotate(piece,orientation)
    for a in range(4):
        for b in range(4):
            pieceVal=p[a][b]
            if (i+a>=6 or j+b>=6): #out of grid
                if pieceVal!=0: #piece is out of grid
                    return False
                continue
            g[i+a][j+b]=orientationMatches[(g[i+a][j+b],pieceVal)]
            if g[i+a][j+b]==-1: #piece conflicts with grid
                return False
    return True

def layPiece(grid,laidPieces,piecesLeft): #Recursively lays a piece on grid,
    #starting with 1st blank space on the smallest row (and smallest column).
    if len(piecesLeft)==0: #complete
        possibleSolutions.append(laidPieces)
#        print(laidPieces)
#        grids.append(grid) #for testing
#        pLeft.append(piecesLeft) #for testing
        return
    for i in range(6): #Identify 1st blank space (i,j)
        ok=True
        for j in range(6):
            if grid[i][j]!=1: #Not completely filled. 1st blank space.
                ok=False
                break
        if ok==False:
            break
    for piece in piecesLeft:
        for orientation in possibleOrientations[piece]:
            g=deepCopy(grid)
            ok=stickToGrid(g,piece,orientation,i,j)
            if ok:
                laidPieces2=laidPieces.copy()
                piecesLeft2=piecesLeft.copy()
                laidPieces2.append([piece,orientation,i,j])
                piecesLeft2.remove(piece)
                layPiece(g,laidPieces2,piecesLeft2)
            
#grids=[]#for testing
#pLeft=[]#for tesing
#counts=[0]

########### To Run Code #########
laidPieces=[] #[[piece,orientation,i,j]]
piecesLeft=list('gabcdef'*2)
possibleSolutions=[] #store laidPieces
layPiece(grid,laidPieces,piecesLeft)

#The code will take very long to complete. To end prematurely, press ctrl-c. Some solutions would have been generated.
#To see a solution, run "showLaidPieces(possibleSolutions[solutionNumber])".
solutionNumber=5
#print(possibleSolutions) #all possible solutions
showLaidPieces(possibleSolutions[solutionNumber]) #show 1 solution

