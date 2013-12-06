#crib hand scorer
import os
import math
from random import randint, shuffle, random
from ast import literal_eval
import datetime

#os.chdir("/Users/mathishard/Desktop/Riddles/1/Crib")

def makeHandLookup():
    f = open('crib.txt')
    w = f.read()
    f.close()
    lookup = literal_eval(w)
    return lookup

def makeLookupDeck():
    lookup_deck = {}
    for char in "A23456789TJQK":
        for suit in "hsdc":
            if char.isdigit():
                lookup_deck[char+suit] = [char+suit,int(char),int(char)]
            elif char == 'A':
                lookup_deck[char+suit] = [char+suit,1,1]
            elif char == 'T':
                lookup_deck[char+suit]= [char+suit,10,10]
            elif char == 'J':
                lookup_deck[char+suit] = [char+suit,10,11]
            elif char == 'Q':
                lookup_deck[char+suit] = [char+suit,10,12]
            elif char == 'K':
                lookup_deck[char+suit] = [char+suit,10,13]
    return lookup_deck

# make a standard 52-card deck
def makeDeck():
    deck = []
    for char in "A23456789TJQK":
        for suit in "hsdc":
            if char.isdigit():
                deck.append([char+suit,int(char),int(char)])
            elif char == 'A':
                deck.append([char+suit,1,1])
            elif char == 'J':
                deck.append([char+suit,10,11])
            elif char == 'Q':
                deck.append([char+suit,10,12])
            elif char == 'K':
                deck.append([char+suit,10,13])
    return deck

# deal out |players| hands of |size| cards with optional cut 
def dealCards(deck,players,size,cut):
    hands =[]
    for i in range(players):
        h = []
        for j in range(size):
            h.append(deck.pop())
        hands.append(h)
    if cut:
        hands.append([deck.pop()])
    return hands

# print out hands
def printHand(cards,sort):
    chand = []
    for i in cards:
        chand.append(i)
    if sort:
        chand.sort(key = lambda x: x[2])
    hand = ''
    for i in chand:
        hand = hand + str(i[0])+", "
    hand = hand[:-2]
    return hand

# print scores
def printScore(scores,n):
    print "\nYou: "+str(scores[0])+ "  Computer: "+str(scores[1]) + n

# choose dealer
def chooseDealer(deck):
    pcut = [[0,0,0]]
    ocut = [[0,0,0]]
    raw_input("\nCut the deck to determine dealer. Press enter to continue.")
    while pcut[0][2] == ocut[0][2]:
        shuffle(deck)
        pcut = [deck[0]]
        ocut = [deck[1]]
    print "\nYour cut: "+ printHand(pcut,False)
    print "Computer's cut: "+ printHand(ocut,False)
    if pcut[0][2] < ocut[0][2]:
        print "Your deal!\n"
        return 0
    elif ocut[0][2] < pcut[0][2]:
        print "Computer's deal!\n"
        return 1
    else:
        chooseDealer(deck)

def makeComputerHands(hand,hands_lookup):
    hands = []
    for i in range(3):
        for j in range(i+1,4):
            for k in range(j+1,5):
                for l in range(k+1,6):
                    h = [hand[i],hand[j],hand[k],hand[l]]
                    h.sort(key = lambda x:x[0])
                    name = h[0][0]+h[1][0]+h[2][0]+h[3][0]
                    s = hands_lookup[name]
                    c = []
                    for l in range (6):
                        if hand[l] not in h:
                            c.append(hand[l])   
                    hands.append([h,c,s])
                    hands.sort(key = lambda x: x[2])
    return hands[14]
    
                

# discard to crib
def discard(hands,dealer,ldeck,hands_lookup):
    phand = hands[0]
    ohand = hands[1]
    cut = hands[2]
    if dealer == 0:
        print "It is your crib."
    else:
        print "It is the computer's crib."
    discarded = 0
    crib = []
    d = makeComputerHands(ohand,hands_lookup)
    ohand = d[0]
    for i in range(2):
        crib.append(d[1][i])
    '''
    for i in range(2): #computer randomly discards to crib -- to be amended with A.I. some day
        card = ohand[randint(0,5-i)]
        crib.append(card)
        ohand.remove(card) 
    '''
    while discarded < 2:
        print "\nYour hand is "+ printHand(phand,True)
        discard = raw_input("Choose a card for the crib: ")
        if discard not in ldeck:
            print "Input invalid!"
        elif ldeck[discard] not in phand:
            print "You don't have that card!"
        elif ldeck[discard] in phand:
            crib.append(ldeck[discard])
            phand.remove(ldeck[discard])
            discarded +=1
    crib.sort(key = lambda x: x[2])
    return [phand,ohand,crib,cut]  

# END GAME PROCEDURE

def endGame(scores,players):
    if players == 0:
        with open('scores.txt','a') as f:
            f.write(str(datetime.date.today()) + "\t" + str(scores[0])+'\t'+str(scores[1])+'\n')
        print "You win! Final score "+str(scores[0])+'-'+str(scores[1])+'.\n'
        if scores[1] < 61:
            print "You double-skunked the computer!\n"
        elif scores[1] < 91:
            print "You skunked the computer!\n"        
    else:
        with open('scores.txt','a') as f:
            f.write(str(datetime.date.today()) + "\t" + str(scores[0])+'\t'+str(scores[1])+'\n')
        print "You lose. Final score "+str(scores[0])+'-'+str(scores[1])+'.\n'
        if scores[0] < 61:
            print "You were double-skunked by the computer!\n"
        elif scores[0] < 91:
            print "You were skunked by the computer!\n"
    again = raw_input("Would you like to play again? Y/N ")
    if again == 'Y' or again == 'y':
        main()
    else:
        exit()

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

# PROCEDURES FOR PEGGING

# ISSUES:
# -last player doesn't always peg points for go, specifically if the last player is the only one to play cards (maybe resolved?)

# check if pegging is allowed with the hand you have

def pegAllowed(history,hand):
    if hand == []: return False
    for c in hand:
        h=[]
        for i in history:
            h.append(i)
        h.append(c)
        sums = 0
        for d in h:
            sums+=d[1]
        if sums <= 31:
            return True
    return False

# check if sum of history is 15

def checkFifteens(history,p):
    sums = 0
    for h in history:
        sums+=h[1]
    if sums == 15: 
        if p:
            print "Fifteen two!\n"
        return 2
    else: return 0  

# check if sum of history is 31
# might be unnecessary
'''
def checkThirtyOne(history):
    sums = 0
    for h in history:
        sums+=h[1]
    if sums == 31: 
        print "31 makes 2!\n"
        return 2
    else: return 0 '''

# check to see if tail of history is a set

def checkSets(history,p):
    l=len(history)
    matches = 0
    match = history[l-1][2]
    if l <= 1:
        return 0
    elif l == 2:
        if history[1][2] == history[0][2]:
            if p:
                print "For two!"
            return 2
        else:
            return 0
    elif l == 3:
        if history[1][2] == history[0][2] and history[2][2] == history[0][2]:
            if p:
                print "For six!"
            return 6
        elif history[1][2] == history[2][2]:
            if p:
                print "For two!"
            return 2
        else:
            return 0
    elif l >= 4:
        if history[l-1][2] == history[l-2][2] and history[l-1][2] == history[l-3][2] and history [l-1][2] == history[l-4][2]:
            if p:
                print "For twelve!"
            return 12
        elif history[l-1][2] == history[l-2][2] and history[l-1][2] == history[l-3][2]:
            if p:
                print "For six!"
            return 6
        elif history[l-1][2] == history[l-2][2]:
            if p:
                print "For two!"
            return 2
        else:
            return 0 
            '''
    else:
        for i in range(2,l):
            if history[l-1][2] == history[l-i][2]:
                matches += 1
            else:
                break
        if matches == 0:
            return matches
        elif matches == 1:
            print "For two!"
            return 2
        elif matches == 2:
            print "For six!"
            return 6
        elif matches == 3:
            print "For 12!"
            return 12'''

def checkRuns(history,p):
    #convert to integers to check sequence
    seq = []
    l = len(history)
    for i in range(0,l):
        seq.append(history[i][2])
    if l >= 7:
        work = seq[l-7:l]
        work.sort()
        if work[6] - work[5] == 1 and work[5] - work[4] == 1 and work[4] - work[3] == 1 and work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            if p:
                print "For a run of SEVEN!!\n"
            return 7
    if l >= 6:
        work = seq[l-6:l]
        work.sort()
        if work[5] - work[4] == 1 and work[4] - work[3] == 1 and work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            if p:
                print "For a run of six!\n"
            return 6
    if l >= 5:
        work = seq[l-5:l]
        work.sort()
        if work[4] - work[3] == 1 and work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            if p:
                print "For a run of five!\n"
            return 5
    if l >= 4:
        work = seq[l-4:l]
        work.sort()
        if work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            if p:
                print "For a run of four!\n"
            return 4
    if l >= 3:
        work = seq[l-3:l]
        work.sort()
        if work[2] - work[1] == 1 and work[1] - work[0] == 1:
            if p:
                print "For a run of three!\n"
            return 3
    return 0    
    
# check whole score history

def checkHist(history,p):
    return checkSets(history,p)+checkFifteens(history,p)+checkRuns(history,p)

# total history values

def totalHistory(history):
    t = 0
    for i in history:
        t += i[1]
    return t

# pegging play

# computer peg A.I. (work in progress)
def cplay(history,hand,card):
    history.append(card)
    hand.remove(card)
    print "Opponent plays "+printHand([history[-1]],False)+"."
    if hand == []:
        return [checkHist(history,True),hand,history,True,True]
    else:
        return [checkHist(history,True),hand,history,False,True]

# check to see if hand has a pair in it, and if so, return the card to play as well. This is to attempt to peg for 6.
# a problem is that if you have 3 or 4 of a kind, it will still play one of those cards, but that's not a huge problem really.
# also, it's predictable for the computer to ALWAYS lead a pair card, so I'm going to weight it so the computer does it some percent
# of the time. Say 70% for now. Also also, don't want to just play an ace because that's suspicious.

def checkForPair(hand):
    l = len(hand)
    r = random()
    if r < 0.7:
        for i in range(l-1):
            for j in range(i+1,l):
                if hand[i][2] == hand[j][2] and hand[i][2] != 1 and hand[i][2] !=5:
                    return [True,i]
    return [False,0]  

def checkForNonTen(hand):
    for i in hand:
        if i[1] != 10:
            return [True,0] #if there's a non-ten or face card, return true, but don't play the index
    return [False,0] #if there are only tens or faces, just play the first one

def checkSmall(hand):
    l = len(hand)
    for i in range(l):
        if hand[i][1] < 5 and 1 < hand[i][1]: # don't want to lead an ace because those are better for pegging
            return [True,i] # if there's a small card, return true and the index to play
    return [False,0] #if not, return false

def checkSevenFive(hand):
    l = len(hand)
    for i in range(l):
        if hand[i][1] != 7 and hand[i][1] != 5:
            return [True,i]
    return [False,0]

def playLead(history,hand): # procedure for leading for pegging, problem with leading 5 if lowest
    if len(hand) == 1: #if there's only one card in the hand, then obviously just play that
        return cplay(history,hand,hand[0])
    else: # if there are two or more cards, computer must decide what to do
        only_fives = True # check for non-fives
        for i in hand: 
            if i[1] != 5:
                only_fives = False
        if only_fives:
            return cplay(history,hand,hand[0])
        pair = checkForPair(hand) # is there a pair?
        if pair[0]:
            return cplay(history,hand,hand[pair[1]])
        non_tens = checkForNonTen(hand)
        if not non_tens[0]: #if only tens, play whatever
            return cplay(history,hand,hand[0])
        else: # now computer still has to decide which card to play
            small = checkSmall(hand) # do we have a card smaller than 5?
            if small[0]: # if small card other than an ace, play it
                return cplay(history,hand,hand[small[1]])
            else: # otherwise, lead a non-seven and non-five if possible
                sevenorfive = checkSevenFive(hand) # is there a non-seven?
                return cplay(history,hand,hand[sevenorfive[1]])

def playCard(history,hand): # computer plays a non-lead card
# first determine the points that would be earned by playing each card
    plays = []
    for card in hand:
        if pegAllowed(history,[card]): # if cards can be played, first check to see if points are available. If so, greedily play for most points.
            h = []
            for i in history:
                h.append(i)
            h.append(card)
            score = checkHist(h,False)
            plays.append([card,score])
    plays.sort(key = lambda x: x[1])
    if plays == []: # if there are no legal plays
        print "Opponent cannot play."
        return [0,hand,history,True,False] # [points earned, hand remaining, history, if 'go', if played]
    elif plays[-1][1] != 0: # do this if you can get points. Fix so that tries for 15 if there are multiple 2-point options?
        return cplay(history,hand,plays[-1][0])
    else: # but what if you can't get points? For now, avoid totaling 5 or 21 or 10. This can be improved.
        shuffle(hand) #so that it doesn't always play the lowest card possible
        for card in hand:
            if pegAllowed(history,[card]):
                if totalHistory(history) + card[1] == 31:
                    return cplay(history,hand,card)
        for card in hand:
            if pegAllowed(history,[card]):
                if totalHistory(history) + card[1] != 10 and totalHistory(history) + card[1] != 21 and totalHistory(history) + card[1] !=5 and card[1] != 5: #avoid 21 and 10 and 5
                    return cplay(history,hand,card)
        #if it's impossible to avoid 21 and 10 and 5, total to 10 first
        for card in hand:
            if pegAllowed(history,[card]):
                if totalHistory(history) + card[1] == 10:
                    return cplay(history,hand,card)
        for card in hand:
            if pegAllowed(history,[card]):
                if totalHistory(history) + card[1] == 21 and card[1] != 5:
                    return cplay(history,hand,card)
        for card in hand: #then just play the highest card possible
            hand.sort(reverse = True)
            if pegAllowed(history,[card]):
                return cplay(history,hand,card)
        
#issues: will lead a 5 when a 5 is its lowest card
def cpeg(history,hand): #this is the A.I. which determines the card played by the computer
    if hand == []: #if no cards, obviously it can't play
        print "Opponent has no cards to play."
        return [0,hand,history,True,False]
    elif history == []: #i.e., the computer has to lead play
        return playLead(history,hand)
    else:
        return playCard(history,hand)
'''    for card in hand: # this is if not leading. For now, just maximize immediate points and avoid totaling 10 or 21. Maybe in future institute lookup table?
        if pegAllowed(history,[card]):
            return cplay(history,hand,card)
#            history.append(card)
#            hand.remove(card)
#            print "Opponent plays "+printHand([history[-1]],False)+"."
            if hand == []:
                return [checkHist(history),hand,history,True,True]
            else:
                return [checkHist(history),hand,history,False,True]
    print "Opponent cannot play."
    return [0,hand,history,True,False] '''

def ppeg(history,hand,ldeck):
    if hand == []:
        print "You have no cards left to play."
        return [0,hand,history,True,False]
    elif pegAllowed(history,hand):
        print "Your cards: "+ printHand(hand,True)
        pegable = False
        while not pegable:
            play = raw_input("Choose a card to play: ")
            if play not in ldeck:
                 print "Invalid input!"
            elif ldeck[play] not in hand:
                print "You don't have that card!"
            else:
                if pegAllowed(history,[ldeck[play]]):
                    history.append(ldeck[play])
                    hand.remove(ldeck[play])
                    pegable = True
                    if hand == []:
                        return [checkHist(history,True),hand,history,True,True]
                    else:
                        return [checkHist(history,True),hand,history,False,True]
    print "You cannot play."
    return [0,hand,history,True,False]

# this is still broken re: 31 = 2 and if last player plays 2+ cards in a row or only one card or is it? Seems to be resolved.
def peg(phand,ohand,dealer,scores,ldeck):
    player_hand = []
    computer_hand = []
    history = []
    running_total = 0
    d = dealer + 0
    played_last = dealer
    cgo = False
    pgo = False
    for i in phand:
        player_hand.append(i)
    for i in ohand:
        computer_hand.append(i)
    while player_hand !=[] or computer_hand !=[]:
        if player_hand == []:
            pgo = True
        if computer_hand == []:
            cgo = True
#        print "\nYour score: ",scores[0]
#        print "Computer's score: ",scores[1]
        printScore(scores, "  Running total: "+str(totalHistory(history))) 
        if history != []:
            print "Cards played: " + printHand(history,False)
        if d == 0: 
            c = cpeg(history,computer_hand)
            scorePoints(scores,1,c[0])
            computer_hand = c[1]
            history = c[2]
            cgo = c[3]
            played = c[4]
            if played:
                played_last = 1
#            if not cgo:
            running_total = totalHistory(history)
            d = 1
            if computer_hand == []:
                cgo = True
        elif d==1:
            p = ppeg(history,player_hand,ldeck)
            scorePoints(scores,0,p[0])
            player_hand = p[1]
            history = p[2]
            pgo = p[3]
            played = p[4]
            if played:
                played_last = 0
            running_total = totalHistory(history)
            d = 0
            if player_hand == []:
                pgo = True
        if cgo and pgo:
            if running_total == 31:
                print "Go for two!"
                scorePoints(scores,played_last,2)
            else:
                print "Go for one!"
                scorePoints(scores,played_last,1)
            history = []
            running_total = 0
            cgo = False
            pgo = False
            d = (played_last)
    return scores
                
                

            
def main():
    hand_lookup = makeHandLookup()   
    ldeck = makeLookupDeck()
    gameOver = False
    score = [0,0]
    deck = makeDeck()
    dealer = chooseDealer(deck)
    while not gameOver: 
        print "You: "+str(score[0])+"  Computer: "+str(score[1])
        deck = makeDeck()
        shuffle(deck)
        hands = dealCards(deck,2,6,True)
        hands = discard(hands,dealer,ldeck,hand_lookup)
        phand = hands[0]
        ohand = hands[1]
        crib = hands[2]
        cut = hands[3]
        print "\nYour hand: " + printHand(phand,True)
#        print "Computer's hand: " + printHand(ohand,True)
#        if dealer == 0:
#            print "Your crib: " + printHand(crib,True)
        print "Cut: " + printHand(cut,False)
        if cut[0][2] == 11:
            print "His nobs!"
            scorePoints(score,dealer,2)
            printScore(score,"")
        peg(phand,ohand,dealer,score,ldeck)
        printScore(score,'')
        if dealer == 0: 
            print "\nComputer's hand: " + printHand(ohand,True) + ' for ' + str(scoreHand(ohand,hands[3],False))+ ' points.'
            print "Your hand: " + printHand(phand,True) + ' for ' + str(scoreHand(phand,hands[3],False))+ ' points.'
            print "Your crib: " + printHand(crib,True) + ' for ' + str(scoreHand(crib,hands[3],False))+ ' points.'
            print "Cut: " + printHand(cut,False)
            scorePoints(score,1,scoreHand(ohand,hands[3],False))
            scorePoints(score,0,scoreHand(phand,hands[3],False))
            scorePoints(score,0,scoreHand(crib,hands[3],True))
            dealer = 1
        else:
            print "\nYour hand: " + printHand(phand,True) + ' for ' + str(scoreHand(phand,hands[3],False))+ ' points.'
            print "Computer's hand: " + printHand(ohand,True) + ' for ' + str(scoreHand(ohand,hands[3],False))+ ' points.'
            print "Computer's crib: " + printHand(crib,True) + ' for ' + str(scoreHand(crib,hands[3],False))+ ' points.'
            print "Cut: " + printHand(cut,False)
            scorePoints(score,0,scoreHand(phand,hands[3],False))
            scorePoints(score,1,scoreHand(ohand,hands[3],False))
            scorePoints(score,1,scoreHand(crib,hands[3],True))
            dealer = 0

main()
