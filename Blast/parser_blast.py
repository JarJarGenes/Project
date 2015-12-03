#!usr/bin/env python
"""
Author: Diego, Anna, Koen & Raquel
Script: Blast parser
"""
import re
import os.path

def blast_parser(blast_result):
    """Given an output file from blast, format 7 (tab file),
    it returns a dictionary with query as key and hit name and identity as list of values.
    """
    my_blast =  open(blast_result)
    blast_dict = {}
    pat_query =  re.compile('Query: (\w+)') #Finds the name of the query
 #   pat_datab = re.compile('Database: (\w)') #Catches the name of the data base
    for line in my_blast:
        query_match = re.search(pat_query, line)
        if query_match:
            query = query_match.group(1)
            blast_dict[query] = []
            print query
        elif not line.startswith('#'):
            columns = line.strip().split('\t')
            blast_dict[query] += [[columns[0], columns[1]]]
    my_blast.close()
    return blast_dict

if __name__ == '__main__':
    out = False
    name_file = raw_input('Insert the name of your output blast file: ')
    while not out:
        if not os.path.exists(name_file):
            name_file = raw_input('The file looks like is not in this folder. Try again (0 to exit): ')
            if name_file == '0':
                out = True
    if not out:
        blast_dict = blast_parser(name_file)
