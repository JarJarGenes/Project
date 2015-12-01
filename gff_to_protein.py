#!/usr/bin/env python
'''
Author: 
Student number: 
Script for gff file to protein > search for matches > return EC numbers
'''

from sys import argv
import subprocess

    
def gff_to_protein(gff_file, genome_db):
    """This is a function that needs a gff file and a genome file and returns proteins
    """
    protein_file = 'proteins.fasta'
    cmd = 'gff3_file_to_proteins.pl %s %s -o %s' % (gff_file, genome_db, protein_file)
    subprocess.check_output(cmd, shell=True)
    return protein_file
    
#def blastp(protein_file):
#    """This function needs a file with protein sequences and returns a file with matches
#    """
#    matches_file = 'matches.
    
    
    
if __name__ == '__main__':
    gff_to_protein(argv[1],argv[2])
    


