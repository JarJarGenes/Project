#!/usr/bin/env python
"""
Author: Koen Hoogendoorn
Script description: Splits concatenated FastQ files,
and outputs the split files to inputname_1.fastq and inputname_2.fastq
"""

#IMPORTS
from __future__ import division
from sys import argv
import time

#Classes & Functions
def splitfile(filename,reads = float("inf")):
    """ Splits a fastq file that has concatenated reads into two files

    Arguments:
    filename -- str, name of the fastqfile (excluding extension)
    reads -- float, number of reads to split
    Output:
    N/A
    """
    openfile = open(filename+".fastq")
    out_1 = open(filename+"_1.fastq","w")
    out_2 = open(filename+"_2.fastq","w")
    counter = 0
    for line in openfile:
        counter +=1
        
        if counter > reads*4:
            break
        
        line = line.strip()
        if line.startswith("@") or line.startswith("+"):
            out_1.write(line)
            out_1.write("\n")
            out_2.write(line)
            out_2.write("\n")
        elif line != "\n":
            length = len(line)
            split = length/2
            part1 = line[:int((length/2))]
            part2 = line[int((length/2)):]
            out_1.write(part1+"\n")
            out_2.write(part2+"\n")

    openfile.close()
    out_1.close()
    out_2.close()

    print "Done!"
    
#Main
if __name__ == "__main__":
    start_time = time.time()
    input_filename = argv[1]
    try:
        reads = float(argv[2])
        splitfile(input_filename,reads)
    except IndexError:
        splitfile(input_filename)
    print("program took %s seconds to run" % (time.time() - start_time))
