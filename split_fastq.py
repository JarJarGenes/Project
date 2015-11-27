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
def splitfile(filename):
    """ Splits a fastq file that has concatenated reads into two files

    Arguments:
    filename -- str, name of the fastqfile (including extension)

    Output:
    N/A
    """
    openfile = open(filename)
    out_1 = open(filename.strip(".fastq")+"_1.fastq","w")
    out_2 = open(filename.strip(".fastq")+"_2.fastq","w")
    counter = 0
    while counter <1000:
        for line in openfile:
            line = line.strip()
            counter += 1
            if line.startswith("@") or line.startswith("+"):
                out_1.write(line)
                out_1.write("\n")
                out_2.write(line)
                out_2.write("\n")
            else:
                length = len(line)
                part1 = line[:(length/2)+1]
                part2 = line[(length/2):]
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
    splitfile(input_filename)
    print("program took %s seconds to run" % (time.time() - start_time))
