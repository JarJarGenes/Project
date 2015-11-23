#!/usr/bin/env python
"""
Author: Koen Hoogendoorn
"""

#IMPORTS
from sys import argv

#Classes & Functions
def findsequences(inputstring):
    """ Find all the sequences in the input file,
        and stores every sequence in a list.
    """
    inputstring = inputstring.replace("\n","")
    seqlist = inputstring.split(">")
    seqlist = seqlist[1:]
    return seqlist

def findgccontent(sequencelist):
    """ Finds the GC-content of a sequence, and stores it in a dictionary.
    """
    gcdict = {}
    gccontent = 0.00
    sequence = ""
    sequenceName = ""
    for element in sequencelist:
        sequence = element[13:]
        sequenceName = element[:13]
        gccontent = (float(sequence.count("G"))+float(sequence.count("C")))/float(len(sequence))*100.00
        gcdict[sequenceName] = gccontent
    return gcdict

def findmaxgc(gcdictionary):
    """ Finds the maximum gc content sequence and returns its name and gc content
    """
    highestnumber = 0.00
    for name,gc in gcdictionary.items():
        if gc > highestnumber:
            highestnumber = gc
            highestname = name
        else:
            pass
    return highestname,highestnumber
            
#Main
if __name__ == "__main__":
    o = open(argv[1])
    output = open("output.txt",'w')
    inputstr = o.read()
    out = findsequences(inputstr)
    print out
    gccontent = findgccontent(out)
    print gccontent
    out1,out2 = findmaxgc(gccontent)
    print out1,out2
    output.write("%s\n%.6f" %(out1,out2))
    output.close()
    o.close()
