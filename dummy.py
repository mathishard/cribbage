from ast import literal_eval
import os
os.chdir("/Users/mathishard/Desktop/Riddles/1/Crib")

f = open('crib.txt')

w = f.read()
f.close()

lookup = literal_eval(w)
print "done"
print lookup['AcAdAhAs']
