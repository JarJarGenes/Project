#!usr/bin/env python
"""
Author: Diego, Anna, Koen & Raquel
Script: Blast parser
"""
import re
from sys import argv
import os.path

def blast_parser(blast_result):
    
    """
    Result output from the TransDecoder Blastp     
    Input "matches.txt"    
    Given an output file from blast, format 7 (tab file),
    it returns a dictionary with query as key and hit name and identity as list of values.
    """
    my_blast =  open(blast_result)
    blast_dict = {}
    pat_query =  re.compile('Query: (\w+)') #Finds the name of the query
    flag = True    
    matches = 0
    no_matches = 0
    string_no_matches = ''
    for line in my_blast:
        query_match = re.search(pat_query, line)
        if query_match:
            query = query_match.group(1)
            blast_dict[query] = []
            flag = True

        elif not line.startswith('#'):
            columns = line.strip().split('\t')
            
            if flag:
                if columns[2] == '100.00':                
                    blast_dict[query] += [[columns[1], columns[2]]]
                    #print blast_dict[query]
                    flag = False                
                    matches += 1
                else:
                    blast_dict[query] += [[columns[1], columns[2]]]
                    string_no_matches +=  columns[0]
                    string_no_matches += '\n'    
                          
                    no_matches +=1
                    flag = False                    
                        
    my_blast.close()    
    
    #print "Matches: {0}".format(matches)
    #print "No matches: {0} ".format(no_matches)
    print string_no_matches    
    return string_no_matches

def generateFileNoMatches(no_matches):
    
    genes = 'no_matches.txt'
    with open(genes,"a+") as no_matches_file_fasta:
        
        no_matches_file_fasta.write(no_matches)
    return genes

def getSequencesfromGenes(genes,fasta_file):
    
    fasta_file  = open(fasta_file)
    genes       = open(genes)
    flag        = False
    flag2       = False
    nucleotides = ''
    name        = []
    seq         = []
    
    count = 0
    label = "Proccessing, please wait"
    for gene in genes:
        gene = gene.strip()
        print label    
	for line in fasta_file:  
     
            if line.startswith('>'):
                flag = False
                line = line.strip()
                id_number = line.split()
                id_number = id_number[0]
                id_number = id_number.replace(">","")  
                
                if gene == id_number:
                    name.append(line)
                    flag = True
                    if flag2:                        
                        #print id_number     
                        #print gene
                        #print line                        
                        #print nucleotides
                        seq.append(nucleotides)                                                
                        nucleotides = ''
                        count +=1
            else:
                if flag:
                    line = line.strip()
                    nucleotides = nucleotides + line
                    nucleotides = nucleotides + "\n"
                    flag2= True
        fasta_file.seek(0) 
        label = label +"."
    seq.append(nucleotides)
    return name,seq
    
def generateFastaFile(name,seq):
    output = 'no_matches_genes.fasta'
    if not os.path.isfile(output):

        with open(output,"a+") as file_fasta:
            
            for index in range(len(name)):

                file_fasta.write(name[index])
                file_fasta.write("\n")
                file_fasta.write(seq[index])
                #file_fasta.write("\n")

        print 'Success! Fasta file generated!'
    else:
        print 'Nothing happened, Text file already exists!'

if __name__ == '__main__':
    
    """
    name_file  = argv[1]
    no_matches = blast_dict = blast_parser(name_file)
    genes      = generateFileNoMatches(no_matches)
    cmd        = 'ls -lh'
    subprocess.check_output(cmd, shell=True)
    fasta_file = raw_input("Select which file to search in...")
    getSequencesfromGenes(genes,fasta_file)
    """
    name, seq = getSequencesfromGenes(argv[1],argv[2])
    generateFastaFile(name,seq)
