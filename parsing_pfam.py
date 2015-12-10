#!/usr/bin/env python

"""
Students: Anne, Diego, Raquel, Koen
Student number: 
Script for parsing a pfam tabular output file
"""
from sys import argv


def parsing(pfam_file):
    """Needs a pfam tabular output file and returns a txt file with query, target en E-value
    """
    pfam_file = open(pfam_file)
    outfile = open("parsed_out_pfam.txt", "w")
    pfam_dict = {}
    counter_proteins = 0
    for line in pfam_file:
        if not line.startswith("#"):
            columns = line.strip()
            columns = columns.split()
            if columns[2] not in pfam_dict:
                pfam_dict[columns[2]] = columns[2],columns[0], columns[4]
                counter_proteins += 1
                line = "%-20s: %-20s %-20s \n" %(columns[2], columns[0], columns[4])
                outfile.write(line)
    pfam_file.close()
    print counter_proteins
    return None

if __name__== "__main__":
     parsing(argv[1])