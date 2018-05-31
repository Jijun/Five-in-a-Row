# -*- coding: utf-8 -*-
"""
Created on Thu May 17 10:56:45 2018

@author: Pi-314159265
"""

########## Five in a Row ##########

import copy
import sys
import math

import time
y = time.time()

class rearrange:
    def __init__(self, og_board, board_size):
        self.ogBoard = og_board
        self.boardSize = board_size

    # Row Analysis.
    def Row(self):
        return self.ogBoard

    # Column Analysis.
    def Col(self):
        Col = []
        for wi in range(0, self.boardSize):
            col = []
            for si in range(0, self.boardSize):
                col.append(self.ogBoard[si][wi])
            Col.append(col)
        return Col

    # Diagonal Analysis
    def Dia(self):
        Dia = []
        for wi in range(0, self.boardSize - 1):
            dia = []
            si = 0
            while wi != -1:
                dia.append(self.ogBoard[wi][si])
                si += 1
                wi -= 1
            Dia.append(dia)
        for wi in range(0, self.boardSize):
            dia = []
            si = self.boardSize - 1
            while wi != self.boardSize:
                dia.append(self.ogBoard[si][wi])
                si -= 1
                wi += 1
            Dia.append(dia)
        return Dia

    # Anti-Diagonal Analysis
    def Ada(self):
        Ada = []
        for si in range(0, self.boardSize):
            ada = []
            wi = 0
            while si != self.boardSize:
                ada.append(self.ogBoard[si][wi])
                si += 1
                wi += 1
            Ada.append(ada)
        Ada = Ada[::-1]
        for wi in range(1, self.boardSize):
            ada = []
            si = 0
            while wi != self.boardSize:
                ada.append(self.ogBoard[si][wi])
                si += 1
                wi += 1
            Ada.append(ada)
        return Ada

# The base score of the stone at each point.
def scoreIndexList(List):
    indexList = [0] * len(List)
    i_test = 0
    for i in range(0, len(List)):
        if List[i] != 0 and i >= i_test:
            twoIndex = 0
            zeroIndex = 0
            negIndex = 0
            i_test = i
            stop = "no"
            while i_test < len(List) and stop == "no":
                if List[i_test] == List[i]:
                    twoIndex += 1
                elif i_test + 1 < len(List):
                    if List[i_test + 1] == List[i] and List[i_test] == 0:
                        zeroIndex += 1
                    else:
                        stop = "yes"
                else:
                    stop = "yes"
                i_test += 1
            if stop == "yes":
                i_test -= 1
            if i <= 0 or List[i - 1] != 0:
                negIndex += 1
            if i_test >= len(List) or List[i_test] != 0:
                negIndex += 1
            if negIndex == 2:
                negIndexJ = 2.5
            else:
                negIndexJ = negIndex
            scoreIndex = float(abs(5 ** (twoIndex - negIndexJ) + 0.9 * negIndex - 0.8 * zeroIndex))
            for indexListi in range(i, i_test):
                indexList[indexListi] = int(scoreIndex * 10)
    scoreList = list(map(lambda l, L: l * L, List, indexList))
    return scoreList

# Add new scores to the original score list.
def AddScore(sB, SB):
    for sb in range(0, len(SB)):
        for sbi in range(0, len(SB[sb])):
            if sB[sb][sbi] != 0:
                sB[sb][sbi] = sB[sb][sbi] + 3 * SB[sb][sbi]
            else:
                sB[sb][sbi] = SB[sb][sbi]
    return sB
   
# Create the score board.
def scoreBoard(Row, Col, Dia, Ada):
    size = len(Row)
    sB = []
    for row in Row: # Reversed Row.
        sB.append(scoreIndexList(row))
    COL = [] # Reversed Column.
    SB = []
    for col in range(0, size):
        COL.append(scoreIndexList(Col[col]))
    for COLi in range(0, len(COL)):
        SB.append([item[COLi] for item in COL])
    AddScore(sB, SB)
    DIA = [] # Reversed Diagonal
    SB = []
    SBss = [0] * size
    for dia in Dia:
        DIA.append(scoreIndexList(dia))
    for sizei in range(size):
        SBss[sizei] = DIA[sizei][sizei]
    SB.append(SBss)
    for diai in range(1, size):
        starti = 0
        diaii = diai
        SBs = [0] * size
        while starti != size - diaii:
            SBs[starti] = DIA[diai][starti]
            starti += 1
            diai += 1
        diaiii = size - diaii
        temp_size = size
        while diaiii != size:
            SBs[diaiii] = DIA[temp_size][size - 1 - diaii]
            diaiii += 1
            temp_size += 1
        SB.append(SBs)
    AddScore(sB, SB)
    ADA = [] # Reversed Anti-Diagonal
    SB = []
    sbs = [1] * size
    for ada in Ada:
        ADA.append(scoreIndexList(ada))
    for ada_i in range(size - 1, 2 * size - 1):
        sbs[ada_i + 1 - size] = ADA[ada_i][0]
    SB.append(sbs)
    for adai in range(size - 2, -1, -1):
        SBs = [0] * size
        ADAi = 0
        ADAi2 = adai
        while adai != size - 1:
            SBs[ADAi] = ADA[adai][ADAi]
            ADAi += 1
            adai += 1
        adai2 = size - 1 - ADAi2
        while adai2 != size:
            SBs[adai2] = ADA[adai2 + ADAi2][size - 1 - ADAi2]
            adai2 += 1
        SB.append(SBs)
    AddScore(sB, SB)
    return sB

# Calculate the score based on the score board.
def score(ogBoard, size):
    reArr = rearrange(ogBoard, size)
    sB = scoreBoard(reArr.Row(), reArr.Col(), reArr.Dia(), reArr.Ada())
    del reArr
    score_L = []
    for scoreL in sB:
        for scores in scoreL:
            score_L.append(scores)
    scoreL_noZero = list(filter((0).__ne__, score_L))
    neg_score = sum(negScore for negScore in scoreL_noZero if negScore < 0)
    pos_score = sum(posScore for posScore in scoreL_noZero if posScore > 0)
    return pos_score + neg_score

# Create new lists based on the next possible move.
def nBoards(boardStructure, side):
    zeroPos = []
    nextBoards = []
    for bSi in range(len(boardStructure)):
        for bsi in range(len(boardStructure[bSi])):
            zeropos = []
            if boardStructure[bSi][bsi] == 0:
                zeropos.append(bSi)
                zeropos.append(bsi)
            zeroPos.append(zeropos)
    zeroPos = list(filter(None, zeroPos))
    for pos in zeroPos:
        nextBoard = copy.deepcopy(boardStructure)
        nextBoard[pos[0]][pos[1]] = side
        nextBoards.append(nextBoard)
    return nextBoards    

# Recessive calls to find the next step.
def nextStep(board, depth, side, size):
    if depth > 2:
        nextBoard = nBoards(board, side)
        boardScore = []
        for next_board in nextBoard:
            boardScore.append(nextStep(next_board, depth - 1, side * -1, size))
        if side > 0:
            return max(boardScore)
        else:
            return min(boardScore)
    elif depth == 2:
        global scoreStandard
        scoreStandard = -math.inf
        nextBoard = nBoards(board, side)
        for next_board in nextBoard:
            nextStep(next_board, depth - 1, side * -1, size)
        return scoreStandard
    else:
        if scoreStandard == -math.inf:
            boardScore = []
            nextBoard = nBoards(board, side)
            for next_board in nextBoard:
                boardScore.append(score(next_board, size))
            scoreStandard = max(boardScore)
        else:
            boardScore = []
            nextBoard = nBoards(board, side)
            for nBi in range(len(nextBoard)):
                sC_t = score(nextBoard[nBi], size)
                if sC_t >= scoreStandard:
                    break
                else:
                    boardScore.append(sC_t)
            if len(boardScore) == len(nextBoard):
                scoreStandard = max(boardScore)

''' 15 * 15
boardStructure = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
'''
'''
boardSize = int(input("Please enter the size of the board (side length): "))
while boardSize < 5:
    boardSize = int(input("Please enter the size of the board (side length): "))
'''
depth = int(input("Please enter the depth (must be plural and non-negative): "))

boardSize = 9

nextBoards = nBoards(boardStructure, 1)
nextMvScoreList = []
for nextBoard in nextBoards:
    boardScore = nextStep(nextBoard, depth, -1, boardSize)
    nextMvScoreList.append(boardScore)
nextMvScore = max(nextMvScoreList)
nextMv = nextMvScoreList.index(nextMvScore)
print(nextMv)

start = 0
k = []
for board in boardStructure:
    start = start + board.count(0)
    k.append(start)
for ki in range(len(k)):
    if k[ki] >= nextMv:
        if ki != 0:
            print(ki + 1, nextMv - k[ki - 1] + 1)
        else:
            print("Row 1: {:}".format(nextMv + 1))
        print(time.time() - y)
        sys.exit()
