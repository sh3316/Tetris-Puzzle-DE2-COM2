# ####################################################
# DE2-COM2 Computing 2
# Individual project
#
# Title: MAIN FILE EXAMPLE
# Authors: Liuqing Chen, Feng Shi, 
#          and Isaac Engel (13th September 2017)
# Last updated: 13th September 2017
# ####################################################

# Write or import your functions in this file

def Tetris(target):
    # determine number of rows and number of columns, respectively
    dimensionr = len(target)
    dimensionc = len(target[0])
    
    # if the number of rows is too small, terminate the program
    if dimensionr is 0:
        return []
    elif dimensionr is 1:
        return [(0,0)]
    
    solution = []
    # create lists to store information about each of the tiles
    # tilescoords: location of tile, tilesconnected: number of adjacent tiles, tilesdirections: direction of adjacent tiles
    tilescoords = []
    tilesconnected = []
    tilesdirections = []
    
    # set the solution matrix to default (all entries (0,0)) and iterate through the grid to gather information about each of the tiles
    for r in range(dimensionr):
        solution.append([])
        for c in range(dimensionc):
            # setting the entries of the solution matrix
            solution[r].append((0,0))
            if target[r][c] is 1:
                # store location of tiles
                tilescoords.append((r,c))
                count = 0
                directions = []
                # count the number of adjacent tiles and determine their location relative to the current tile
                if r != (dimensionr-1):
                    if target[r+1][c] == 1:
                        count+=1
                        directions.append('d')
                if r != 0:
                    if target[r-1][c] == 1:
                        count+=1
                        directions.append('u')
                if c != (dimensionc-1):
                    if target[r][c+1] == 1:
                        count+=1
                        directions.append('r')
                if c != 0:
                    if target[r][c-1] == 1:
                        count+=1
                        directions.append('l')
                # store the above information
                tilesconnected.append(count)
                tilesdirections.append(directions)

    tetriminos = []
    
    # while there are tiles with only 1 adjacent tile, repeatedly fit Tetris pieces starting at those tiles
    somethingdone = True
    # if there are too many tiles, reduce the number of repetitions
    loops=int(dimensionr/100)
    while(somethingdone and loops<13):
        loops+=1
        somethingdone = False
        # iterate through the tiles to find those with only 1 adjacent tile
        i=0
        while i<(len(tilescoords)):
            if i<len(tilescoords) and tilesconnected[i]==1:
                # find the row and column of such tiles
                row = tilescoords[i][0]
                col = tilescoords[i][1]
                #create list to store visited locations, which is needed to apply the Tetris piece fitting algorithm
                discovered = []
                # create list to hold information about the appropriate Tetris piece
                tetrimino = []
                # create stack to use for Tetris piece fitting algorithm, a variation of the maze searching algorithm
                stack = []
                # begin the Tetris piece fitting algorithm
                stack.append((row,col))
                discovered.append((row,col))
                while len(stack)>0:
#                    print("stack: ",stack,end=" / ")
                    coord = stack.pop() ###
#                    print("coord: ",coord,end=" / ")
#                    print("discovered: ",discovered)
                    tetrimino.append((coord[0],coord[1]))
                    # if we have a complete Tetris piece, stop the algorithm
                    if len(tetrimino)==4:
                        break
                    # otherwise, keep building a Tetris piece as long as there are adjacent tiles
                    if coord[0]!=0 and (coord[0]-1,coord[1]) not in discovered and (coord[0]-1,coord[1]) in tilescoords:
                        discovered.append((coord[0]-1,coord[1]))
                        stack.insert(0,(coord[0]-1,coord[1]))
                        #stack.append((coord[0]-1,coord[1]))
                    if coord[1]!=0 and (coord[0],coord[1]-1) not in discovered and (coord[0],coord[1]-1) in tilescoords:
                        discovered.append((coord[0],coord[1]-1))
                        stack.insert(0, (coord[0],coord[1]-1))
                        #stack.append((coord[0],coord[1]-1))
                    if coord[1]!=dimensionc-1 and (coord[0],coord[1]+1) not in discovered and (coord[0],coord[1]+1) in tilescoords:
                        discovered.append((coord[0],coord[1]+1))
                        stack.insert(0,(coord[0],coord[1]+1))
                        #stack.append((coord[0],coord[1]+1))
                    if coord[0]!=dimensionr-1 and (coord[0]+1,coord[1]) not in discovered and (coord[0]+1,coord[1]) in tilescoords:
                        discovered.append((coord[0]+1,coord[1]))
                        stack.insert(0,(coord[0]+1,coord[1]))
                        #stack.append((coord[0]+1,coord[1]))
                # if we successfully ended up with a complete Tetris piece, store information about the Tetris piece
                # forget about the now used tiles afterwards
                if len(tetrimino)==4:
                    somethingdone = True
                    # for each tile in Tetris piece, remove it from the lists holding tile information so that we don't consider them afterwards
                    for n in tetrimino:
                        index = tilescoords.index(n)
                        tilescoords.pop(index)
                        tilesconnected.pop(index)
                        affected=tilesdirections.pop(index)
                        for x in affected:
                            if x=='u':
                                updex = tilescoords.index((n[0]-1,n[1]))
                                tilesdirections[updex].remove('d')
                                tilesconnected[updex]-=1
                            elif x=='d':
                                downdex = tilescoords.index((n[0]+1,n[1]))
                                tilesdirections[downdex].remove('u')
                                tilesconnected[downdex]-=1
                            elif x=='l':
                                leftdex = tilescoords.index((n[0],n[1]-1))
                                tilesdirections[leftdex].remove('r')
                                tilesconnected[leftdex]-=1
                            elif x=='r':
                                rightdex = tilescoords.index((n[0],n[1]+1))
                                tilesdirections[rightdex].remove('l')
                                tilesconnected[rightdex]-=1
                    tetriminos.append(tetrimino)
                    i-=1
                # if we have a Tetris piece that is missing a tile, fill it up first and undergo the above process
                elif len(tetrimino)==3:
                    somethingdone = True
                    filledup=False
                    for k in range(3):
                        n = tetrimino[k]
                        affected = tilesdirections[tilescoords.index(n)]
                        # find an empty space to be an 'excess' tile if not yet done
                        if not filledup:
                            if 'u' not in affected and n[0]!=0 and target[n[0]-1][n[1]]==0:
                                filledup=True
                                tetrimino.append((n[0]-1,n[1]))
                            elif 'd' not in affected and n[0]!=dimensionr-1 and target[n[0]+1][n[1]]==0:
                                filledup=True
                                tetrimino.append((n[0]+1,n[1]))
                            elif 'l' not in affected and n[1]!=0 and target[n[0]][n[1]-1]==0:
                                filledup=True
                                tetrimino.append((n[0],n[1]-1))
                            elif 'r' not in affected and n[1]!=dimensionc-1 and target[n[0]][n[1]+1]==0:
                                filledup=True
                                tetrimino.append((n[0],n[1]+1))
                    # if Tetris piece is now complete, remove the tiles from the lists holding tile info so that we don't consider them afterwards
                    if filledup and len(tetrimino)==4:
                        for k in range(3):
                            n=tetrimino[k]
                            index = tilescoords.index(n)
                            tilescoords.pop(index)
                            tilesconnected.pop(index)
                            affected=tilesdirections.pop(index)
                            for x in affected:
                                if x=='u':
                                    updex = tilescoords.index((n[0]-1,n[1]))
                                    tilesdirections[updex].remove('d')
                                    tilesconnected[updex]-=1
                                elif x=='d':
                                    downdex = tilescoords.index((n[0]+1,n[1]))
                                    tilesdirections[downdex].remove('u')
                                    tilesconnected[downdex]-=1
                                elif x=='l':
                                    leftdex = tilescoords.index((n[0],n[1]-1))
                                    tilesdirections[leftdex].remove('r')
                                    tilesconnected[leftdex]-=1
                                elif x=='r':
                                    rightdex = tilescoords.index((n[0],n[1]+1))
                                    tilesdirections[rightdex].remove('l')
                                    tilesconnected[rightdex]-=1
                        tetriminos.append(tetrimino)
                        i-=1
            i+=1
    #handle tiles with more than one adjacent tiles
    i=0
    while i<(len(tilescoords)):
        if i<len(tilescoords) and tilesconnected[i]>1:
            # find the row and column of such tiles
            row = tilescoords[i][0]
            col = tilescoords[i][1]
            # create stack to use for Tetris piece fitting algorithm, a variation of the maze searching algorithm
            stack = []
            #create list to store visited locations, which is needed to apply the Tetris piece fitting algorithm
            discovered = []
            # create list to hold information about the appropriate Tetris piece
            tetrimino = []
            # begin the Tetris piece fitting algorithm
            stack.append((row,col))
            discovered.append((row,col))
            while len(stack)>0:
                coord = stack.pop() ###
                tetrimino.append((coord[0],coord[1]))
                # if we have a complete Tetris piece, stop the algorithm
                if len(tetrimino)==4:
                    break
                # otherwise, keep building a Tetris piece as long as there are adjacent tiles
                if coord[0]!=0 and (coord[0]-1,coord[1]) not in discovered and (coord[0]-1,coord[1]) in tilescoords:
                    discovered.append((coord[0]-1,coord[1]))
                    stack.insert(0,(coord[0]-1,coord[1]))
                if coord[1]!=0 and (coord[0],coord[1]-1) not in discovered and (coord[0],coord[1]-1) in tilescoords:
                    discovered.append((coord[0],coord[1]-1))
                    stack.insert(0, (coord[0],coord[1]-1))
                if coord[1]!=dimensionc-1 and (coord[0],coord[1]+1) not in discovered and (coord[0],coord[1]+1) in tilescoords:
                    discovered.append((coord[0],coord[1]+1))
                    stack.insert(0,(coord[0],coord[1]+1))
                if coord[0]!=dimensionr-1 and (coord[0]+1,coord[1]) not in discovered and (coord[0]+1,coord[1]) in tilescoords:
                    discovered.append((coord[0]+1,coord[1]))
                    stack.insert(0,(coord[0]+1,coord[1]))
            # if we successfully ended up with a complete Tetris piece, store information about the Tetris piece
            # forget about the now used tiles afterwards
            if len(tetrimino)==4:
                somethingdone = True
                # for each tile in Tetris piece, remove it from the lists holding tile information so that we don't consider them afterwards
                for n in tetrimino:
                    index = tilescoords.index(n)
                    tilescoords.pop(index)
                    tilesconnected.pop(index)
                    affected=tilesdirections.pop(index)
                    for x in affected:
                        if x=='u':
                            updex = tilescoords.index((n[0]-1,n[1]))
                            tilesdirections[updex].remove('d')
                            tilesconnected[updex]-=1
                        elif x=='d':
                            downdex = tilescoords.index((n[0]+1,n[1]))
                            tilesdirections[downdex].remove('u')
                            tilesconnected[downdex]-=1
                        elif x=='l':
                            leftdex = tilescoords.index((n[0],n[1]-1))
                            tilesdirections[leftdex].remove('r')
                            tilesconnected[leftdex]-=1
                        elif x=='r':
                            rightdex = tilescoords.index((n[0],n[1]+1))
                            tilesdirections[rightdex].remove('l')
                            tilesconnected[rightdex]-=1
                tetriminos.append(tetrimino)
                i-=1
            # if we have a Tetris piece that is missing a tile, fill it up first and undergo the above process
            elif len(tetrimino)==3:
                somethingdone = True
                filledup=False
                for k in range(3):
                    n = tetrimino[k]
                    affected = tilesdirections[tilescoords.index(n)]
                    # find an empty space to be an 'excess' tile if not yet done
                    if not filledup:
                        if 'u' not in affected and n[0]!=0 and target[n[0]-1][n[1]]==0:
                            filledup=True
                            tetrimino.append((n[0]-1,n[1]))
                        elif 'd' not in affected and n[0]!=dimensionr-1 and target[n[0]+1][n[1]]==0:
                            filledup=True
                            tetrimino.append((n[0]+1,n[1]))
                        elif 'l' not in affected and n[1]!=0 and target[n[0]][n[1]-1]==0:
                            filledup=True
                            tetrimino.append((n[0],n[1]-1))
                        elif 'r' not in affected and n[1]!=dimensionc-1 and target[n[0]][n[1]+1]==0:
                            filledup=True
                            tetrimino.append((n[0],n[1]+1))
                # if Tetris piece is now complete, remove the tiles from the lists holding tile info so that we don't consider them afterwards
                if filledup and len(tetrimino)==4:
                    for k in range(3):
                        n=tetrimino[k]
                        index = tilescoords.index(n)
                        tilescoords.pop(index)
                        tilesconnected.pop(index)
                        affected=tilesdirections.pop(index)
                        for x in affected:
                            if x=='u':
                                updex = tilescoords.index((n[0]-1,n[1]))
                                tilesdirections[updex].remove('d')
                                tilesconnected[updex]-=1
                            elif x=='d':
                                downdex = tilescoords.index((n[0]+1,n[1]))
                                tilesdirections[downdex].remove('u')
                                tilesconnected[downdex]-=1
                            elif x=='l':
                                leftdex = tilescoords.index((n[0],n[1]-1))
                                tilesdirections[leftdex].remove('r')
                                tilesconnected[leftdex]-=1
                            elif x=='r':
                                rightdex = tilescoords.index((n[0],n[1]+1))
                                tilesdirections[rightdex].remove('l')
                                tilesconnected[rightdex]-=1
                    tetriminos.append(tetrimino)
                    i-=1
        i+=1
    #wrap up by cleaning up tiles with one adjacent tile one last time
    while i<(len(tilescoords)):
        if i<len(tilescoords) and tilesconnected[i]==1:
            # find the row and column of such tiles
            row = tilescoords[i][0]
            col = tilescoords[i][1]
            # create stack to use for Tetris piece fitting algorithm, a variation of the maze searching algorithm
            stack = []
            #create list to store visited locations, which is needed to apply the Tetris piece fitting algorithm
            discovered = []
            # create list to hold information about the appropriate Tetris piece
            tetrimino = []
            # begin the Tetris piece fitting algorithm
            stack.append((row,col))
            discovered.append((row,col))
            while len(stack)>0:
                coord = stack.pop() ###
                tetrimino.append((coord[0],coord[1]))
                # if we have a complete Tetris piece, stop the algorithm
                if len(tetrimino)==4:
                    break
                # otherwise, keep building a Tetris piece as long as there are adjacent tiles
                if coord[0]!=0 and (coord[0]-1,coord[1]) not in discovered and (coord[0]-1,coord[1]) in tilescoords:
                    discovered.append((coord[0]-1,coord[1]))
                    stack.insert(0,(coord[0]-1,coord[1]))
                if coord[1]!=0 and (coord[0],coord[1]-1) not in discovered and (coord[0],coord[1]-1) in tilescoords:
                    discovered.append((coord[0],coord[1]-1))
                    stack.insert(0, (coord[0],coord[1]-1))
                if coord[1]!=dimensionc-1 and (coord[0],coord[1]+1) not in discovered and (coord[0],coord[1]+1) in tilescoords:
                    discovered.append((coord[0],coord[1]+1))
                    stack.insert(0,(coord[0],coord[1]+1))
                if coord[0]!=dimensionr-1 and (coord[0]+1,coord[1]) not in discovered and (coord[0]+1,coord[1]) in tilescoords:
                    discovered.append((coord[0]+1,coord[1]))
                    stack.insert(0,(coord[0]+1,coord[1]))
            # if we successfully ended up with a complete Tetris piece, store information about the Tetris piece
            # forget about the now used tiles afterwards
            if len(tetrimino)==4:
                somethingdone = True
                # for each tile in Tetris piece, remove it from the lists holding tile information so that we don't consider them afterwards
                for n in tetrimino:
                    index = tilescoords.index(n)
                    tilescoords.pop(index)
                    tilesconnected.pop(index)
                    affected=tilesdirections.pop(index)
                    for x in affected:
                        if x=='u':
                            updex = tilescoords.index((n[0]-1,n[1]))
                            tilesdirections[updex].remove('d')
                            tilesconnected[updex]-=1
                        elif x=='d':
                            downdex = tilescoords.index((n[0]+1,n[1]))
                            tilesdirections[downdex].remove('u')
                            tilesconnected[downdex]-=1
                        elif x=='l':
                            leftdex = tilescoords.index((n[0],n[1]-1))
                            tilesdirections[leftdex].remove('r')
                            tilesconnected[leftdex]-=1
                        elif x=='r':
                            rightdex = tilescoords.index((n[0],n[1]+1))
                            tilesdirections[rightdex].remove('l')
                            tilesconnected[rightdex]-=1
                tetriminos.append(tetrimino)
                i-=1
            # if we have a Tetris piece that is missing a tile, fill it up first and undergo the above process
            elif len(tetrimino)==3:
                somethingdone = True
                filledup=False
                for k in range(3):
                    n = tetrimino[k]
                    affected = tilesdirections[tilescoords.index(n)]
                    # find an empty space to be an 'excess' tile if not yet done
                    if not filledup:
                        if 'u' not in affected and n[0]!=0 and target[n[0]-1][n[1]]==0:
                            filledup=True
                            tetrimino.append((n[0]-1,n[1]))
                        elif 'd' not in affected and n[0]!=dimensionr-1 and target[n[0]+1][n[1]]==0:
                            filledup=True
                            tetrimino.append((n[0]+1,n[1]))
                        elif 'l' not in affected and n[1]!=0 and target[n[0]][n[1]-1]==0:
                            filledup=True
                            tetrimino.append((n[0],n[1]-1))
                        elif 'r' not in affected and n[1]!=dimensionc-1 and target[n[0]][n[1]+1]==0:
                            filledup=True
                            tetrimino.append((n[0],n[1]+1))
                # if Tetris piece is now complete, remove the tiles from the lists holding tile info so that we don't consider them afterwards
                if filledup and len(tetrimino)==4:
                    for k in range(3):
                        n=tetrimino[k]
                        index = tilescoords.index(n)
                        tilescoords.pop(index)
                        tilesconnected.pop(index)
                        affected=tilesdirections.pop(index)
                        for x in affected:
                            if x=='u':
                                updex = tilescoords.index((n[0]-1,n[1]))
                                tilesdirections[updex].remove('d')
                                tilesconnected[updex]-=1
                            elif x=='d':
                                downdex = tilescoords.index((n[0]+1,n[1]))
                                tilesdirections[downdex].remove('u')
                                tilesconnected[downdex]-=1
                            elif x=='l':
                                leftdex = tilescoords.index((n[0],n[1]-1))
                                tilesdirections[leftdex].remove('r')
                                tilesconnected[leftdex]-=1
                            elif x=='r':
                                rightdex = tilescoords.index((n[0],n[1]+1))
                                tilesdirections[rightdex].remove('l')
                                tilesconnected[rightdex]-=1
                    tetriminos.append(tetrimino)
                    i-=1
        i+=1
    # determine shape of tetriminos and mark on solution grid
    tetriminoshape=[]
    for a in tetriminos:
        # determine the leftmost coordinate of a tetrimino
        minc=min([a[0][1],a[1][1],a[2][1],a[3][1]])
        # determine the topmost coordinate among tiles of the same tetrimino that has that leftmost coordinate
        minctetris = []
        for b in a:
            if b[1]==minc:
                minctetris.append(b[0])
        # in this case, minr would not necessarily be the smallest row coordinate among all the tiles
        minr=min(minctetris)
        # determine the shape id
        if (minr+1,minc) in a:
            if (minr+2,minc) in a:
                if (minr+3,minc) in a:
                    tetriminoshape.append(2)
                elif (minr+2,minc+1) in a:
                    tetriminoshape.append(4)
                elif (minr+1,minc+1) in a:
                    tetriminoshape.append(12)
                elif (minr, minc+1) in a:
                    tetriminoshape.append(10)
                else:
                    tetriminoshape.append(-1)
            elif (minr+1,minc+1) in a:
                if (minr+1,minc+2) in a:
                    tetriminoshape.append(11)
                elif (minr+2,minc+1) in a:
                    tetriminoshape.append(17)
                elif (minr,minc+1) in a:
                    tetriminoshape.append(1)
                else:
                    tetriminoshape.append(-1)
            elif (minr,minc+1) in a:
                if (minr,minc+2) in a:
                    tetriminoshape.append(7)
                elif (minr-1,minc+1) in a:
                    tetriminoshape.append(19)
                else:
                    tetriminoshape.append(-1)
        elif (minr,minc+1) in a:
            if (minr,minc+2) in a:
                if (minr,minc+3) in a:
                    tetriminoshape.append(3)
                elif (minr-1,minc+2) in a:
                    tetriminoshape.append(5)
                elif (minr+1,minc+2) in a:
                    tetriminoshape.append(9)
                elif (minr-1,minc+1) in a:
                    tetriminoshape.append(13)
                elif (minr+1,minc+1) in a:
                    tetriminoshape.append(15)
                else:
                    tetriminoshape.append(-1)
            elif (minr+1,minc+1) in a:
                if (minr+2,minc+1) in a:
                    tetriminoshape.append(6)
                elif (minr-1,minc+1) in a:
                    tetriminoshape.append(14)
                elif (minr+1,minc+2) in a:
                    tetriminoshape.append(18)
                else:
                    tetriminoshape.append(-1)
            elif (minr-1,minc+1) in a:
                if (minr-2,minc+1) in a:
                    tetriminoshape.append(8)
                elif (minr-1,minc+2) in a:
                    tetriminoshape.append(16)
                else:
                    tetriminoshape.append(-1)
            else:
                tetriminoshape.append(-1)

    # mark the Tetris pieces in the solution matrix
    i=0
    while i<len(tetriminos):
        # check if the Tetris piece at hand has four distinct tiles. If not, remove it
        if len(tetriminos[i])<4 or len(tetriminos[i])!=len(set(tetriminos[i])):
            tetriminos.pop(i)
            i-=1
            continue
        # record in solution
        solution[tetriminos[i][0][0]][tetriminos[i][0][1]]=(tetriminoshape[i],i+1)
        solution[tetriminos[i][1][0]][tetriminos[i][1][1]]=(tetriminoshape[i],i+1)
        solution[tetriminos[i][2][0]][tetriminos[i][2][1]]=(tetriminoshape[i],i+1)
        solution[tetriminos[i][3][0]][tetriminos[i][3][1]]=(tetriminoshape[i],i+1)
        i+=1