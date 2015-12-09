
#!/usr/bin/env python

"""
Students: Anne, Diego, Raquel, Koen
Student number: 
"""
from sys import argv
import os.path

def getSequencesfromGenes(genes,fasta_file):
    
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
