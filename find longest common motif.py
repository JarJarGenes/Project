#!/usr/bin/env python
"""
Author: Koen Hoogendoorn
"""

#IMPORTS
from sys import argv
import re
import random

#Classes & Functions

def parsefile(fastafile):
    """ Grabs the raw sequence from a fasta file
    """
    sequences = fastafile.split(">")
    sequences = sequences[1:]
    seqlist = []
    for elem in sequences:
        #name = elem[:elem.index("\n")]
        sequence = elem[elem.index("\n"):]
        sequence = sequence.replace("\n","")
        seqlist.append(sequence)
    return seqlist

def findshortestsequence(sequencelist):
    """ finds the shortest sequence in the list of sequences
    """
    shortestelement = sequencelist[0]
    for element in sequencelist:
        if len(element) < len(shortestelement):
            shortestelement = element
    print shortestelement
    return shortestelement

def motiffinder(shortestelement,sequencelist):
    """ Finds the longest common motif
    """
    currentmotif = ""
    start=0
    score = 0
    while start< len(shortestelement):
        end=1
        while end <= len(shortestelement)-start:
            
            matchingseqs = []
            for elem in sequencelist:
                if shortestelement[start:start+end] not in elem:
                    break
                else:
                    matchingseqs.append(elem)
                    if len(matchingseqs) == len(seqlist):
                        if len(shortestelement[start:start+end]) > len(currentmotif):
                               currentmotif = shortestelement[start:start+end]
                               print currentmotif

                               
            
            end+=1
        start+=1
    
    
                
    print "final motif = ",currentmotif               
    return currentmotif

if __name__ == "__main__":
    o = open(argv[1])
    output = open("output.txt",'w')
    inputstr = o.read()
    seqlist = parsefile(inputstr)
    s= findshortestsequence(seqlist)
    l = motiffinder(s,seqlist)
    for elem in seqlist:
        output.write("%s\n\n"%elem)
    o.close()
    output.close()
