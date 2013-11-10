#crib hand scorer
import os
from random import randint

os.chdir("/Users/mathishard/Desktop/Riddles/1/Crib")

cards = [[1,'s'],[2,'s'],[3,'s'],[4,'s'],[5,'s'],[6,'s'],[7,'s'],[8,'s'],[9,'s'],['T','s'],['J','s'],['Q','s'],['K','s'],[1,'c'],[2,'c'],[3,'c'],[4,'c'],[5,'c'],[6,'c'],[7,'c'],[8,'c'],[9,'c'],['T','c'],['J','c'],['Q','c'],['K','c'],[1,'h'],[2,'h'],[3,'h'],[4,'h'],[5,'h'],[6,'h'],[7,'h'],[8,'h'],[9,'h'],['T','h'],['J','h'],['Q','h'],['K','h'],[1,'d'],[2,'d'],[3,'d'],[4,'d'],[5,'d'],[6,'d'],[7,'d'],[8,'d'],[9,'d'],['T','d'],['J','d'],['Q','d'],['K','d']]

cardvals = {1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,'T':10,'J':11,'Q':12,'K':13}

current_player = 0
score = [0,0]
    

# PROCEDURES FOR DEALING OUT CARDS
def get_hand(l,taken,order):
    hand = []
    while len(hand)<l:
        newcard = randint(0,51)
        if not newcard in hand and not newcard in taken:
            hand.append(newcard)
    if order: hand.sort()
    return hand

def get_chand(hand,order):
    chand = []
    for i in range(0,len(hand)):
        chand.append(cards[hand[i]])
    if order: chand.sort(key = lambda x: x[0])
    return chand

#problem here with same cards being dealt to multiple hands
def deal_cards():
    taken = []
    phand = get_hand(6,taken,True)
    pchand = get_chand(phand,True)
    taken = taken + phand
    ohand = get_hand(6,taken,True)
    ochand = get_chand(ohand,True)
    taken = taken + ohand
    cut = get_hand(1,taken,True)
    ccut = get_chand(cut,False)
    taken = taken + cut
    return [pchand,ochand,ccut]

#PROCEDURE TO PRINT HANDS

def print_hand(chand):
    hand = ''
    for i in chand:
        hand = hand + str(i[0]) + str(i[1]) + ","
    hand = hand[:-1]
    return hand

# PROCEDURE FOR CHOOSING DEALER
def choose_dealer():
    raw_input("Cut the deck to determine dealer. Press enter to continue.")
    pcut = get_hand(1,[],False)
    ocut = get_hand(1,pcut,False)
    pccut = get_chand(pcut,False)
    occut = get_chand(ocut,False)
    print "Your cut: "+print_hand(pccut)
    print "Computer's cut: "+print_hand(occut)
    if cardvals[pccut[0][0]] < cardvals[occut[0][0]]:
        print "Your deal!\n"
        return 0
    elif cardvals[occut[0][0]] < cardvals[pccut[0][0]]:
        print "Computer's deal!\n"
        return 1
    else:
        choose_dealer()

#PROCEDURE FOR INPUTING CARD TO PLAY

def make_card(x,h):
    valid = False
    while not valid:
        c = []
        if len(x)!=2:
            print "Input invalid!"
            print "Your hand is "+print_hand(h)+'.'
            x = raw_input("Please choose a card to play: ")
        elif len(x) == 2:
            if x[0] in ['1','2','3','4','5','6','7','8','9']:
                c.append(int(x[0]))
            else:
                c.append(x[0])
            c.append(x[1])
            if not c in h:
                print "You don't have that card!"
                print "Your hand is "+print_hand(h)+'.'
                x = raw_input("Please choose a card to play: ")
            elif c in h:
                return c
                

#SCORING PROCEDURES

def check_flush(chand,cut,crib):
    if chand[0][1]==chand[1][1] and chand[0][1]==chand[2][1] and chand[0][1]==chand[3][1] and chand[0][1]==cut[0][1]:
        return 5
    elif chand[0][1]==chand[1][1] and chand[0][1]==chand[2][1] and chand[0][1]==chand[3][1] and crib==False:
        return 4
    else: return 0

def fifteens(chand,cut):
    fiftscore=0
    vals = []
    for i in range(0,len(chand)):
        if type(chand[i][0]) is int:
            vals.append(chand[i][0])
        else:
            vals.append(10)
    if type(cut[0][0]) is int:
        vals.append(cut[0][0])
    else:
        vals.append(10)
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
            if chand[i][0]==chand[j][0]:
                pairsscore+=2
    return pairsscore    

def nobs(chand,cut):
    for i in range (0,4):
        if chand[i][0]=='J' and chand[i][1] == cut[0][1]:
            return 1
    return 0    

def runs(hand,cut):
    chand = []
    for i in hand: chand.append(i)
    chand.append(cut[0])
    runsscore=0
    fives=False
    fours=False
    vals=[]
    for i in range(0,5):
        if type(chand[i][0]) is int:
            vals.append(chand[i][0])
        elif chand[i][0]=='T':
            vals.append(10)
        elif chand[i][0]=='J':
            vals.append(11)  
        elif chand[i][0]=='Q':
            vals.append(12)
        elif chand[i][0]=='K':
            vals.append(13)
    vals.sort()
#   first check for a run of 5
    if vals[4]-vals[3]==1 and vals[3]-vals[2]==1 and vals[2]-vals[1]==1 and vals[1]-vals[0]==1:
        runsscore += 5
        fives = True

#   next check for runs of 4
    if fives==False:
        for i in range (0,2):
            for j in range (i+1,3):
                for k in range (j+1,4):
                    for l in range (k+1,5):
                        if vals[l]-vals[k]==1 and vals[k]-vals[j]==1 and vals[j]-vals[i]==1:
                            runsscore += 4
                            fours = True

#   finally check for runs of 3
    if not fives and not fours:
        for i in range (0,3):
            for j in range (i+1,4):
                for k in range (j+1,5):
                    if vals[k]-vals[j]==1 and vals[j]-vals[i]==1:
                        runsscore +=3

    return runsscore

# SCORE ENTIRE HAND

def score_hand(chand,cut,crib):
    return check_flush(chand,cut,crib)+fifteens(chand,cut)+pairs(chand,cut)+nobs(chand,cut)+runs(chand,cut)

# PROCEDURES FOR PEGGING

# check if pegging is allowed with the hand you have

def peg_allowed(history,hnd):
    if hnd == []: return False
    for c in hnd:
        h=[]
        for i in history:
            h.append(i)
        h.append(c)
        sums = 0
        for i in range(0,len(h)):
            if type(h[i][0]) is int:
                sums+=h[i][0]
            else:
                sums+=10
        if sums <= 31:
            return True
    return False

# check if sum of history is 15

def check_fifteens(history):
    sums = 0
    for i in range(0,len(history)):
        if type(history[i][0]) is int:
            sums+=history[i][0]
        else:
            sums+=10
    if sums == 15: 
        print "Fifteen two!\n"
        return 2
    else: return 0  

# check if sum of history is 31

def check_thirty_one(history):
    sums = 0
    for i in range(0,len(history)):
        if type(history[i][0]) is int:
            sums+=history[i][0]
        else:
            sums+=10
    if sums == 31: 
        print "31 makes 2!\n"
        return 2
    else: return 0  

# check to see if tail of history is a set

def check_sets(history):
    l=len(history)
    if l <= 1: 
        return 0
    if l >= 4:
        if history[l-1][0] == history[l-2][0] and history[l-2][0] == history[l-3][0] and history[l-3][0] == history[l-4][0]:
            print "The royal!\n"
            return 12
        elif history[l-1][0] == history[l-2][0] and history[l-2][0] == history[l-3][0]:
            print "For six!\n"
            return 6
        elif history[l-1][0] == history[l-2][0]:
            print "For two!\n"
            return 2
        else: return 0
    if l >= 3:
        if history[l-1][0] == history[l-2][0] and history[l-2][0] == history[l-3][0]:
            print "For six!\n"
            return 6
        elif history[l-1][0] == history[l-2][0]:
            print "For two!\n"
            return 2
        else: return 0
    if l >= 2:
        if history[l-1][0] == history[l-2][0]:
            print "For two!\n"
            return 2
        else: return 0
    else: return 0

#check to see if history ends in a run

def check_runs(history):
    #convert to integers to check sequence
    run = 0
    seq = []
    l = len(history)
    for i in range(0,l):
        if type(history[i][0]) is int:
            seq.append(history[i][0])
        elif history[i][0] == 'T':
            seq.append(10)
        elif history[i][0] == 'J':
            seq.append(11)
        elif history[i][0] == 'Q':
            seq.append(12)
        elif history[i][0] == 'K':
            seq.append(13)
    # print seq
    # check run of 7
    if l >= 3:
        work = seq[l-3:l]
        work.sort()
        if work[2] - work[1] == 1 and work[1] - work[0] == 1:
            print "For a run of three!\n"
            run = 3
    if l >= 4:
        work = seq[l-4:l]
        work.sort()
        if work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            print "For a run of four!\n"
            run = 4
    if l >= 5:
        work = seq[l-5:l]
        work.sort()
        if work[4] - work[3] == 1 and work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            print "For a run of five!\n"
            run = 5
    if l >= 6:
        work = seq[l-6:l]
        work.sort()
        if work[5] - work[4] == 1 and work[4] - work[3] == 1 and work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            print "For a run of six!\n"
            run = 6
    if l >= 7:
        work = seq[l-7:l]
        work.sort()
        if work[6] - work[5] == 1 and work[5] - work[4] == 1 and work[4] - work[3] == 1 and work[3] - work[2] == 1 and work[2] - work[1] == 1 and work[1] - work[0] == 1:
            print "For a run of SEVEN!!\n"
            run = 7
    return run


#check whole score history

def check_hist(history):
    return check_sets(history)+check_fifteens(history)+check_runs(history)

#computer peg play

def cpeg(history,hand):
    if hand == []:
        print "Opponent cannot play."
        return [0,hand,history,True]
    for card in hand:
        if peg_allowed(history,hand):
            history.append(card)
            hand.remove(card)
            print "Opponent plays "+print_hand([history[-1]])+".\n"
            return [check_hist(history),hand,history,False]
    print "Opponent cannot play."
    return [0,hand,history,True]

def add_card(card):
    if type(card[0]) is int:
        return card[0]
    else: return 10

def peg(phand,ohand,pscore,oscore,c):
    d = (c+1)%2
    player_hand = []
    opponent_hand = []
    for i in phand: player_hand.append(i)
    for i in ohand: opponent_hand.append(i)
    pgo = False
    cgo = False
    playedlast = 0
    history = []
    total = 0
    while player_hand !=[] or opponent_hand !=[]:
        print "\nYour score: ",pscore
        print "Opponent's score: ",oscore
        print "Running total: ",total
        print "Cards played: " + print_hand(history)
        if d == 0:
            if player_hand == []:
                print "You have no cards left."
                pgo = True
                playedlast = 1
            elif peg_allowed(history,player_hand):
                print "Your cards: "+ print_hand(player_hand)
                pegable = False
                while not pegable:
                    play = make_card(raw_input("Choose a card to play: "),player_hand)
                    if peg_allowed(history,[play]):
                        history.append(play)
                        player_hand.remove(play)
                        pscore+=check_hist(history)
                        total+=add_card(play)
                        pegable = True
                    else: print "You can't play that card!"
                playedlast = 0
            else:
                print "Your cards: "+ print_hand(player_hand)
                print "You cannot play."
                pgo = True
            d = 1
        if d == 1: 
            if opponent_hand == []:
                print "Opponent cannot play."
                cgo = True
                playedlast = 0
            else:
                c = cpeg(history,opponent_hand)
                oscore += c[0]
                opponent_hand = c[1]
                history = c[2]
                cgo = c[3]
                if not cgo:
                    total+=add_card(history[-1])
                    playedlast=1
                #else:
                    #print "Opponent cannot play.\n"
            d = 0
        if (pgo and cgo):
            if playedlast == 0:
                d = 0
                if total == 31: pscore+=2
                if total != 31: pscore+=1
            elif playedlast == 1:
                d = 1
                if total == 31: oscore+=2
                if total != 31: oscore+=1
            history = []
            total = 0
    if playedlast == 0 and not (pgo and cgo):
        if total == 31: pscore+=2
        if total != 31: pscore+=1
    elif playedlast == 1 and not (pgo and cgo):
        if total == 31: oscore+=2
        if total != 31: oscore+=1
    return [pscore,oscore]

#print peg([[5,'s'],[6,'s'],['J','s'],['K','s']], [[1,'s'],[2,'s'],['Q','s'],['T','s']],0,0,0)
    


#PROCEDURE FOR DISCARDING DEALT HAND TO FORM CRIB

def discard(pchand,ochand,currentp):
    if currentp == 0:
        print "It is your crib."
    else:
        print "It is the computer's crib."
    discarded = 0
    crib = []
    for i in range(2):
        card = ochand[randint(0,5-i)]
        crib.append(card)
        ochand.remove(card)   
    while discarded == 0:
        d=[]
        print "\nYour hand is "+ print_hand(pchand)
        discard = raw_input("Choose a card for the crib: ")
        if len(discard)!=2:
            print "Input invalid!"
        elif discard[0] in ['1','2','3','4','5','6','7','8','9','10']:
            d.append(int(discard[0]))
            d.append(discard[1])
            if  [d[0],d[1]] in pchand:
                crib.append([d[0],d[1]])
                pchand.remove([d[0],d[1]])
                discarded = 1
        else:
            d = discard
            if  [d[0],d[1]] in pchand:
                crib.append([d[0],d[1]])
                pchand.remove([d[0],d[1]])
                discarded = 1
    while discarded == 1:
        d=[]
        print "\nYour hand is "+ print_hand(pchand)
        discard = raw_input("Choose a second card for the crib: ")
        if len(discard)!=2:
            print "Input invalid!"
        elif discard[0] in ['1','2','3','4','5','6','7','8','9']:
            d.append(int(discard[0]))
            d.append(discard[1])
            if  [d[0],d[1]] in pchand:
                crib.append([d[0],d[1]])
                pchand.remove([d[0],d[1]])
                discarded = 2
        else:
            d = discard
            if [d[0],d[1]] in pchand:
                crib.append([d[0],d[1]])
                pchand.remove([d[0],d[1]])
                discarded = 2  
    crib.sort(key = lambda x: x[0])
    return [pchand,ochand,crib]  

def main():
    score = [0,0]
    current_player = 0
    print "Welcome to Cribbage.\n"
    current_player = choose_dealer()
    while score[0] < 61 and score[1] < 61:
        print "You: " + str(score[0]) + ", Computer: " + str(score[1])
        hands = deal_cards()
        player_hand = hands[0]
        opponent_hand = hands[1] 
        cut = hands[2]
        split = discard(player_hand,opponent_hand,current_player)
        player_hand = split[0]
        opponent_hand = split[1]
        crib = split[2]
        print "Your hand: " + print_hand(player_hand)
        # print "Opponent: " + print_hand(opponent_hand)
        # print "Crib: " + print_hand(crib)    
        print "Cut: " + print_hand(cut)+"\n"
        if cut[0][0] == 'J':
            print "His nobs!"
            score[current_player]+=2
            print "You: " + str(score[0]) + ", Computer: " + str(score[1])
        pegs = peg(player_hand,opponent_hand,score[0],score[1],current_player)
        score[0] = pegs[0]
        score[1] = pegs[1]
        print "Player: " + print_hand(player_hand)
        print "Opponent: " + print_hand(opponent_hand)
        print "Crib: " + print_hand(crib)
        print "Cut: " + print_hand(cut)
        phscore = score_hand(player_hand,cut,False)
        chscore = score_hand(opponent_hand,cut,False)
        cscore = score_hand(crib,cut,True)
        print "Player hand score: ", phscore
        print "Opponent hand score: ", chscore
        print "Crib score: ", cscore
        score[0] += phscore
        score[1] += chscore
        score[current_player] += cscore
        current_player = (current_player + 1)%2
    print score

main()


class memoize:
    def __init__(self, function):
        self.function = function
        self.memoized = {}

    def __call__(self, x,y,z,w,c):
        try:
            return self.memoized[str(x)+','+str(y)+','+str(z)+','+str(w)+','+str(c)]
        except KeyError:
            self.memoized[str(x)+','+str(y)+','+str(z)+','+str(w)+','+str(c)] = self.function(x,y,z,w,c)
            return self.memoized[str(x)+','+str(y)+','+str(z)+','+str(w)+','+str(c)]

@memoize
def crib_score(x,y,z,w,c):
    crib=False
    chand=get_chand([x,y,z,w])
    cut = cards[c]
    return check_flush(chand,cut,crib)+pairs(chand,cut) + nobs(chand,cut) + runs(chand,cut) + fifteens(chand,cut)


#POPULATE EV SPREADSHEET TEXT FILE
'''
f = open('crib.txt','w')

for i in range (0,49):
    for j in range (i+1,50):
        for k in range (j+1,51): 
            for l in range (k+1,52):
                scores=[]
                for m in range (52):
                    if not m in [i,j,k,l]:
                        scores.append(crib_score(i,j,k,l,m))
                f.write(str(cards[i])+str(cards[j])+str(cards[k])+str(cards[l])+" " + str(sum(scores)/float(len(scores)))+"\n")

f.close()
'''


 
