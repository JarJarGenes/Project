#!/usr/bin/env python

"""
Student:Anne Tjallingii
Student number: 911024836020
Script for using Blast and parsing blast. Returns a list with proteins that match with arabidopsis.
"""

from sys import argv
import subprocess
import os

def blastp_arabidopsis(fasta_no_matches, Arabidopsis_database):
    """This function takes a fasta file with protein sequences and returns a file with matches with the arabidopsis
    """  
    out_file = "blastp_arabidopsis_output.txt"
    cmd = 'blastp -query %s -db %s -evalue %s -outfmt %s -max_target_seqs %s -out %s' % (fasta_no_matches, Arabidopsis_database, 1E-5, 6, 1, out_file)
    if os.path.exists("blastp_arabidopsis_output.txt"):
        check = raw_input( "Blast output file exists, overwrite? (Y/N)\n: ")
        if check == "Y" or check == "y":
            subprocess.check_call(cmd,shell=True)
        else:
            pass
    else:
        subprocess.check_call(cmd,shell=True)
    return out_file
    
def parsing_blastp(blast_arabidopsis):
    blast_arabidopsis = open(blast_arabidopsis)
    outfile = open("parsed_output_blastp.txt", "w")
    blast_dict = {}
    count = 0
    for lines in blast_arabidopsis:
        columns = lines.strip().split()
        if columns[0] not in blast_dict:
            blast_dict[columns[0]] = columns[0], columns[1], columns[10]
            count += 1
            line = "%-20s: %-20s %-20s \n" % (columns[0], columns[1], columns[10])
            outfile.write(line)
    outfile.close()
    print count
    return None
            

if __name__ == "__main__":
    blast_output = blastp_arabidopsis(argv[1],argv[2])
    parsing_blastp(blast_output)