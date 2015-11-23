#!/usr/bin/env python
"""
Author: Koen Hoogendoorn
"""

#IMPORTS
from sys import argv
import re

#Classes & Functions

def parsefile(fastafile):
    """ Grabs the raw sequence from a fasta file
    """
    ## ADD EXTRA COMMENT
    ## Extra Extra COMMENT
    sequences = fastafile.split(">")
    sequences = sequences[1:]
    nameseqlist = []
    for elem in sequences:
        sequence = elem[elem.index("\n"):]
        sequence = sequence.replace("\n","")
        nameseqlist.append(sequence)
    return seqlist

def findshortestsequence(sequencelist):
    """ Checks whether the first or last characters of one sequence match the last or first characters from the second sequence
    """
    shortestelement = sequencelist[0]
    for element in sequencelist:
        if len(element) < len(shortestelement):
            shortestelemenet = element
    return shortestelement

def motiffinder(shortestelement,sequencelist):
    """ Returns the sequences that overlap at their ends in a pairwise manner
    """
    score = 0
    currentmotif = ""
    for x in range(len(shortestelement)):
        for y in range(len(shortestelement)-x)):
            for elem in sequencelist:
                if shortestelement[x:x+y] in elem:
                    score +=1
                else:
                    break
            if score == len(sequencelist):
                currentmotif = shortestelement[x:x+y]
                
                   
    return currentmotif

if __name__ == "__main__":
    o = open(argv[1])
    output = open("output.txt",'w')
    inputstr = o.read()
    seqlist = parsefile(inputstr)
    s= findshortestsequence(seqlist)
    l = motiffinder(s,seqlist)
    print l  
    o.close()
    output.close()

