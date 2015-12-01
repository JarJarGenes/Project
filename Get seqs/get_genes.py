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
import os.path

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
    print records
    return records
    
def get_seq(records, output_name):
    """Using a list of genes from kegg it downloads the files with the AA and N sequences and parses it.
    It writes in one file called 'my_seq.txt', then it takes the labels and sequences. This file is overwritten
    and deleted at the end of the operation.
    
    Input: List of parsed gene names from kegg
    Output: -A file with all the seqs in order, first protein seq and then aa seq.
            -A dictionary with all the sequences
            -Two dictionaries, one with nucleotide seq and the other one with prot seq
            -Two file with the seqs splitted
    """
    my_file = open(output_name, 'w')
    N_dict = {}
    A_dict = {}
    my_dict = {}
    seq = ''
    for each_name in records:
        cmd = ('wget -O my_seq.txt http://www.genome.jp/dbget-bin/www_bget?-f+ath+%s')%each_name       
        subprocess.check_call(cmd, shell=True)
        start = False
        pat = re.compile('\(A|N\)')
        for line in open('my_seq.txt'):            
            match = re.search(pat,line)
            if start:
                if match or line.startswith('<'):
                    my_dict[label] = seq
                    my_file.write('>'+label+'\n'+seq+'\n')
                    if match: label = line.strip(); seq = ''
                    else: start = False
                else:
                    seq += line.strip()
            elif match:
                label = line.strip()
                start = True
        
        N_file = open('N_seqs.fasta','w')
        A_file = open('A_seqs.fasta','w')
        for label, seq in my_dict.items():
            if '(N)' in label:
                N_file.write('>'+label+'\n'+seq+'\n')
                N_dict[label] = seq
            elif '(A)' in label:
                A_file.write('>'+label+'\n'+seq+'\n')
                A_dict[label] = seq   
        subprocess.check_call('rm my_seq.txt', shell=True)
    print '------------------DONE'
    N_file.close()
    A_file.close()
    my_file.close()
    return my_dict, N_dict, A_dict
    
if __name__ == '__main__':
    file_with_names = argv[1]
    while not os.path.exists(file_with_names):
        cmd = subprocess.check_output('ls',shell=True)
        print cmd
        file_with_names = raw_input('Your program doesn\'t seem to exist.\nCheck the name and insert again the name: ')
    try:
        output_name = argv[2]
    except IndexError:
        output_name = 'Sequences.fasta'
    records = get_name(file_with_names)   
    all_seqs, N_seqs, A_seqs = get_seq(records, output_name)
    
    
