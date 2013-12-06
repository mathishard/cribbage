# make lookup tables for 

import os
from math import ceil
from ast import literal_eval

#os.chdir("/Users/mathishard/Desktop/Riddles/1/Crib")

def makeDeck():
    deck = []
    for char in "A23456789TJQK":
        for suit in "hsdc":
            if char.isdigit():
                deck.append([char+suit,int(char),int(char)])
            elif char == 'A':
                deck.append([char+suit,1,1])
            elif char == 'T':
                deck.append([char+suit,10,10])
            elif char == 'J':
                deck.append([char+suit,10,11])
            elif char == 'Q':
                deck.append([char+suit,10,12])
            elif char == 'K':
                deck.append([char+suit,10,13])
    return deck

# SCORING PROCEDURES

def scorePoints(scores,player,points):
    scores[player]+=points
    if scores[player] > 120:
        endGame(scores,player)
    else:
        return scores

def checkFlush(chand,cut,iscrib):
    if chand[0][0][1]==chand[1][0][1] and chand[0][0][1]==chand[2][0][1] and chand[0][0][1]==chand[3][0][1] and chand[0][0][1]==cut[0][0][1]:
        return 5
    elif chand[0][0][1]==chand[1][0][1] and chand[0][0][1]==chand[2][0][1] and chand[0][0][1]==chand[3][0][1] and iscrib==False:
        return 4
    else: return 0

def fifteens(chand,cut):
    fiftscore=0
    vals = []
    for i in range(0,len(chand)):
        vals.append(chand[i][1])
    vals.append(cut[0][1])
    for i in range (0,4):
        for j in range (i+1,5):
            if vals[i]+vals[j]==15:
                fiftscore+=2
    for i in range (0,3):
        for j in range (i+1,4):
            for k in range (j+1,5):
                if vals[i]+vals[j]+vals[k]==15:
                    fiftscore+=2
    for i in range (0,2):
        for j in range (i+1,3):
            for k in range (j+1,4):
                for l in range (k+1,5):
                    if vals[i]+vals[j]+vals[k]+vals[l]==15:
                        fiftscore+=2
    if vals[0]+vals[1]+vals[2]+vals[3]+vals[4]==15:
        fiftscore+=2
    return fiftscore

def pairs(hand,cut):
    chand = []
    for i in hand: chand.append(i)
    chand.append(cut[0])
    chand.append(cut)
    pairsscore=0
    for i in range (0,4):
        for j in range (i+1,5):
            if chand[i][2]==chand[j][2]:
                pairsscore+=2
    return pairsscore  

def nobs(chand,cut):
    for i in range (0,4):
        if chand[i][0][0]=='J' and chand[i][0][1] == cut[0][0][1]:
            return 1
    return 0

def runs(hand,cut):
    chand = []
    for i in hand: chand.append(i)
    chand.append(cut[0])
    chand.sort(key = lambda x:x[2])
    runsscore=0
    fives=False
    fours=False
#   first check for a run of 5
    if chand[4][2] - chand[3][2] == 1 and chand[3][2] - chand[2][2] == 1 and chand[2][2] - chand[1][2] == 1 and chand[1][2] - chand[0][2] == 1:
        runsscore += 5
        fives = True

#   next check for runs of 4
    if fives==False:
        for i in range (0,2):
            for j in range (i+1,3):
                for k in range (j+1,4):
                    for l in range (k+1,5):
                        if chand[l][2] - chand[k][2] == 1 and chand[k][2]-chand[j][2] == 1 and chand[j][2]-chand[i][2] == 1:
                            runsscore += 4
                            fours = True

#   finally check for runs of 3
    if not fives and not fours:
        for i in range (0,3):
            for j in range (i+1,4):
                for k in range (j+1,5):
                    if chand[k][2]-chand[j][2] == 1 and chand[j][2]-chand[i][2] == 1:
                        runsscore +=3

    return runsscore    

# SCORE ENTIRE HAND

def scoreHand(chand,cut,crib):
    return checkFlush(chand,cut,crib)+fifteens(chand,cut)+pairs(chand,cut)+nobs(chand,cut)+runs(chand,cut)

# GENERATE BEST CHOICE FROM SIX CARD HAND

deck = makeDeck()

scores = {}

for i in range(49):
    for j in range(i+1,50):
        for k in range(j+1,51):
            for l in range(k+1, 52):
                hand = [deck[i],deck[j],deck[k],deck[l]]
                hand.sort(key = lambda x: x[0])
                hands = hand[0][0]+hand[1][0]+hand[2][0]+hand[3][0]
                score = []
                for m in range(52):
                    if not deck[m] in hand:
                        score.append(scoreHand(hand,[deck[m]],False))
                scores[hands] = ceil(100*sum(score)/float(len(score)))/100
                
f = open('crib.txt','w')                                
f.write(str(scores))

f.close()
