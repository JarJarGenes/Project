#!/usr/bin/env python

"""
Student:Anne Tjallingii
Student number: 911024836020
Script for pfam
"""

from sys import argv
import subprocess
import os

def pfam(fasta_no_matches, HMM_database):
    """This function takes a fasta file with protein sequences and returns a file with domains
    input file HMM_database = Pfam-A.hmm 
    """  
    out_file = "pfam_output.txt"
    cmd = 'hmmscan --cpu %s -E %s --tblout %s %s %s > /dev/null' % (4, 0.0001, out_file, HMM_database, fasta_no_matches)
    if os.path.exists("pfam_output.txt"):
        check = raw_input( "Pfam output file exists, overwrite? (Y/N)\n: ")
        if check == "Y" or check == "y":
            subprocess.check_call(cmd,shell=True)
        else:
            pass
    else:
        subprocess.check_call(cmd,shell=True)
    return out_file

if __name__ == "__main__":
    pfam(argv[1],argv[2])
    
    