#!usr/bin/env python
"""
Author: Raquel, Koen, Anna & Diego
Script: With a file with the names of the genes from kegg,
it parses the downloaded files with the sequences
"""
#Import modules
import re
import subprocess
from sys import argv

#Functions
def get_name(file_txt):
    """With the list of genes obteined as following:
    Use kegg API: http://rest.kegg.jp/link/<target_db>/<source_db>[/<option>]
    [link -> find related entries by using database cross-references]
    i.e: /link/genes/hsa00010 or /link/hsa/hsa00010   List of human genes in pathway hsa00010
    Gets the names of the genes inside the file
    
    Input: Kegg list
    Output: List of gene names
    """    
    pattern = re.compile("\tath:(\w+)")
    records = []
    for line in open(file_txt):
        records += re.findall(pattern,line)
    
    return records
    
def get_seq(records, output_name):
    """Using a list of genes from kegg it downloads the files with the AA and N sequences and parses it.
    It writes in one file called 'my_seq.txt', then it takes the labels and sequences. This file is overwritten
    and deleted at the end of the operation.
    
    Input: List of parsed gene names from kegg
    Output: -A file with all the seqs in order, first protein seq and then aa seq.
            -A dictionary with all the sequences
            -Two dictionaries, one with nucleotide seq and the other one with prot seq
    """
    my_file = open(output_name, 'w')
    for each_name in records:
        cmd = ('wget -O my_seq.txt http://www.genome.jp/dbget-bin/www_bget?-f+ath+%s')%each_name       
        subprocess.check_call(cmd, shell=True)
        start = False
        my_dict = {}
        seq = ''
        pat = re.compile('\(A|N\)')
        for line in open('my_seq.txt'):            
            match = re.search(pat,line)
            if start:
                if match or line.startswith('<'):
                    my_dict[label] = seq
                    my_file.write(label+'\n'+seq+'\n')
                    if match: label = line.strip(); seq = ''
                    else: start = False
                else:
                    seq += line.strip()
            elif match:
                label = line.strip()
                start = True
        N_dict = {}
        A_dict = {}
        for label, seq in my_dict.items():
            if '(N)' in label:
                N_dict[label] = seq
            elif '(A)' in label:
                A_dict[label] = seq           
    print '------------------DONE'
    subprocess.check_call('rm my_seq.txt', shell=True)    
    my_file.close()
    return my_dict, N_dict, A_dict
    
if __name__ == '__main__':
    file_with_names = argv[1]
    try:
        output_name = argv[2]
    except IndexError:
        output_name = 'Sequences.fasta'
    records = get_name(file_with_names)   
    all_seqs, N_seqs, A_seqs = get_seq(records, output_name)
    
    
