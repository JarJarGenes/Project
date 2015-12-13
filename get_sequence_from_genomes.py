
#!/usr/bin/env python

"""
Students: Anne, Diego, Raquel, Koen
Student number: 
"""
from sys import argv
import os.path

def getSequencesfromGenes(genes,fasta_file):
    """
	This is a function that generates a Fasta file from 
	a file that contains a list of the name of the sequences
	
	Input genes: File with a list of the name of the genes too look
	Input fasta_file: Fasta file of the sequences to look at
	Output: returns two arrays containing all the names and the sequences
	in order
	"""
    fasta_file  = open(fasta_file)
    genes       = open(genes)
    flag        = False
    flag2       = False
    nucleotides = ''
    name        = []
    seq         = []
    for gene in genes:
        gene = gene.strip()
	for line in fasta_file:  
            if line.startswith('>'):
                flag = False
                line = line.strip()
                line_id = line.rsplit('_')
                lenght = len(line_id)
                id_number = line_id[lenght-1]
                
                if gene == id_number:
                    name.append(line)
                    flag = True
                    if flag2:
                        seq.append(nucleotides)
                        nucleotides = ''
                        
            else:
                if flag:
                    line = line.strip()
                    nucleotides = nucleotides + line
                    nucleotides = nucleotides + "\n"
                    flag2= True
    
        fasta_file.seek(0) 
    seq.append(nucleotides)
	
    return name,seq

def generateFastaFile(name,seq):
	"""
	This is a function that generates a fasta file from the two arrays
	Input name: array containing all the name of the id of each sequences
	Input: seq: array containing all the sequences
	Output: creates a file named mia_genes.fasta with the selected id names and 
	sequences
	"""
    
	output = 'mia_genes.fasta'
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

    #print seq
if __name__== "__main__":
    
    name, seq = getSequencesfromGenes(argv[1],argv[2])
    generateFastaFile(name,seq)
