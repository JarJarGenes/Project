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
    pat = "\t%s:(\w+)" %file_with_names[:3]
    pattern = re.compile(pat)
    records = []
    for line in open(file_txt):
        records += re.findall(pattern,line)
    return records
    
def get_seq(records, file_with_names, output_name):
    """Using a list of genes from kegg it downloads the files with the AA and N sequences and parses it.
    It writes in one file called 'my_seq.txt', then it takes the labels and sequences. This file is overwritten
    and deleted at the end of the operation.
    
    Input: List of parsed gene names from kegg
    Output: -A file with all the seqs in order, first protein seq and then aa seq.
            -A dictionary with all the sequences
            -Two dictionaries, one with nucleotide seq and the other one with prot seq
            -Two file with the seqs splitted
    """
    print 'Getting sequences now...'
    my_file = open(output_name, 'w')
    N_dict = {}
    A_dict = {}
    my_dict = {}
    seq = ''
    for each_name in records:
        cmd = ('wget -O my_seq.txt http://www.genome.jp/dbget-bin/www_bget?-f+%s+%s')%(file_with_names[:3],each_name)       
        subprocess.check_call(cmd, shell=True)
        start = False
        pat = re.compile('\(A|N\)')
        for line in open('my_seq.txt'):            
            match = re.search(pat,line)
            if start:
                if match or line.startswith('<'):
                    my_dict[label] = seq
                    my_file.write('>'+label+'\n'+seq+'\n')
                    if match:
                        if line.startswith('<!-- '):
                            line = line.strip().split('>>'); print line;label = line[1]; seq = ''
                        else: label = line.strip(); seq = ''
                    else: start = False
                else:
                    seq += line.strip()
            elif match:
                if line.startswith('<!-- '):
                    line = line.strip().split('>>'); print line;label = line[1]; seq = ''
                else: label = line.strip(); seq = ''
                start = True
        
        N_file = open('N_seqs.fasta','w')
        A_file = open('A_seqs.fasta','w')
        for label, seq in my_dict.items():
            if '(N)' in label:
                N_file.write('>'+label[1:]+'\n'+seq+'\n')
                N_dict[label] = seq
            elif '(A)' in label:
                A_file.write('>'+label+'\n'+seq+'\n')
                A_dict[label] = seq
        subprocess.check_call('rm my_seq.txt', shell=True)
    N_file.close()
    A_file.close()
    my_file.close()
    print '------------------DONE'
    print '--------------------------------------Thanks for using us :)'
    return my_dict, N_dict, A_dict

def get_list(name_path, out):
    cmd = 'wget http://rest.kegg.jp/link/genes/%s' %name_path
    finished = False
    while not finished:
        try:
            e = subprocess.check_call(cmd, shell=True)
            if e == 0:
                finished = True
        except subprocess.CalledProcessError:
            print 'Looks like the name you gave is not valid, try again or 0 to exit.'
            name_path = raw_input('Name of the path: ')
            if name_path == '0':
                print 'here'
                finished = True
                out = True
    return out, name_path
    
if __name__ == '__main__':
    out = False
    got_it = False
    try:
        file_with_names = argv[1]
    except IndexError:
        while not out and not got_it:
            usr = raw_input("Do you have your gene list from kegg? (Y|N) ")
            if usr.lower() == 'y':
                file_with_names = raw_input('Name of your file: ')
                got_it = True
            elif usr.lower() == 'n':
                usr = raw_input("We can get it for you if you know the name of the pathway or you can check it in kegg.jp (we will wait for you).\n1 I know the path, get it for me please\n0 I changed my mind(exit)\n Insert a number: ")       
                if usr == '1':
                    name_path = raw_input('Now you can insert the name, the format must be like this: example = map00902 ("monoterpenoid pathway") or ath00901 ("Arabidopsis thaliana, path: map00901")(0 to exit)\n\nName of the path: ')
                    if name_path != '0':
                        out, name_path = get_list(name_path, out)
                        file_with_names = name_path
                        got_it = True
                    elif name_path == '0':
                        out = True
                elif usr == '0':
                    out = True
            if not out:
                if got_it:
                    continue
                while not os.path.exists(file_with_names):
                    print 'Your file doesn\'t seem to exist.\nCheck the name and insert again the name (press 0 to exit).\nDo you need the gene list?(press 1 to help).'
                    cmd = subprocess.check_output('ls',shell=True)
                    print cmd
                    file_with_names = raw_input('Name of your file: ')
                    got_it = True
                    if file_with_names == '0':
                        out = True
    if not out and got_it:
        try:
            output_name = argv[2]
        except IndexError:
            output_name = 'sequences.fasta'
        print file_with_names, 'here'
        records = get_name(file_with_names)   
        all_seqs, N_seqs, A_seqs = get_seq(records,file_with_names, output_name)
    else:
        print '--------------------------------------Thanks for using us :)'
