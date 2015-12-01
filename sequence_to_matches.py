#!/usr/bin/env python

"""
Students: Anne, Diego, Raquel, Koen
Student number: 
Script for reading a fasta file and producing trimmed reads
"""
from sys import argv
import subprocess
import os.path

def jarjargenes():
    #Function that asks for a number of sequences
    #
    print "--- Welcome to JarJarGenes for getting the \n N sequence of a"+\
    " Fasta file and/or GFF3 File ---"
    out = False   
    while not out:
        input_number_sequence = raw_input("How many sequences do you want "+\
        "from your fasta file? (Press 0 to exit): ")
        if input_number_sequence > '0':

            flow_program(int(input_number_sequence))
            break
        elif input_number_sequence == '0':
            print "--- Thanks for using JarJar for getting small "+\
            "fasta datasets---"
            out = True

def flow_program(input_number_sequence):
    #Follows the main flow of the program
    #open the two files from the user for getting the N sequence
    small_fasta_file = ''
    fasta_filename  = ''
    gff_filename    = ''
    with open(argv[1]) as fh:
        fasta_filename    = fh.name
        index             = fasta_filename.rfind('/')
        fasta_filename    = fasta_filename[index:].replace('/','')+'.small'
        small_fasta_file  = small_fasta_dataset(fh,fasta_filename,\
        input_number_sequence)
    
    with open(argv[2]) as fh:
        gff_filename    = fh.name
        index           = gff_filename.rfind('/')
        gff_filename    = gff_filename[index:].replace('/','')+'.small'
        small_gff_dataset(fh,small_fasta_file,gff_filename)
        
    protein_file = gff_to_protein(gff_filename,fasta_filename)

    
    cmd = 'clear'
    print subprocess.check_output(cmd, shell=True)
    print "###########################################"
    print "######## LIST OF POSSIBLE FASTA FILES TO SELECT ########"
    print "###########################################"    
    cmd = 'ls *.fasta'
    print subprocess.check_output(cmd, shell=True)
    protein_file_genes = \
    raw_input("Please select the proteins file to blast: ")    
    blastp(protein_file,protein_file_genes)
    
    
def small_fasta_dataset(input_file,small_fasta_file,input_number_sequence):
    """
    Description: function that gets the first 4000 sequences in the input 
    Fasta file
    Input: Fasta file sequence
    Output: Generates an output fastQ file with the 4000 sequences
    Return: String with the name of the output fastq file name
    """
    counter     = 0
    flag        = 0
    index       = 0 
    nucleotides = ''
    dictionary_sequence = []
    
    for line in input_file:

        if line.startswith('>'):  
            #dictionary_sequence.append({'name':line.replace(">","")})                   
            dictionary_sequence.append({'name':line})                               
            counter +=1   
            if flag == 1:  
                dictionary_sequence[index]['sequence'] = nucleotides
                dictionary_sequence[index]['lenght'] = len(nucleotides)
                nucleotides = ''
                index=index+1
                flag = 0                
        else:
            flag = 1
            nucleotides = nucleotides + line        
                
    dictionary_sequence[index]['sequence'] = nucleotides
    dictionary_sequence[index]['lenght']   = len(nucleotides)   
    #Generates the fastq file with the string that stored the 4000 
    #sequences of the FastQ file       
    if os.path.exists(small_fasta_file):
        check = raw_input( "{0} file exists, overwrite? (Y/N)\n: "\
        .format(small_fasta_file))
        if check == "Y" or check == "y":
            newlist = sorted(dictionary_sequence,reverse=True, \
            key=lambda k: k['lenght'])     
            outfile = open(small_fasta_file,'w')    
        
            for index in range(input_number_sequence):    
                outfile.write(str(newlist[index]['name']))
                outfile.write(str(newlist[index]['sequence']))                            
            outfile.close()
            print "File {0} succesfully generated!"\
               .format(small_fasta_file)
        
        else:
            pass
    else:
        newlist = sorted(dictionary_sequence,reverse=True, \
        key=lambda k: k['lenght'])     
        outfile = open(small_fasta_file,'w')    
        
        for index in range(input_number_sequence):    
            outfile.write(str(newlist[index]['name']))
            outfile.write(str(newlist[index]['sequence']))                            
        outfile.close()
        print "File {0} succesfully generated!"\
        .format(small_fasta_file)
    return small_fasta_file
    
def small_gff_dataset(input_gff_file,small_fasta_file,small_gff_filename):    

    small_fasta_file    = open(small_fasta_file)
    scaffold_list       = []     
    scaffold_string     = ''    

    for line in small_fasta_file:
        if line.startswith('>'): 
            line = line.replace('>','')
            line = line.replace('\n','')
            scaffold_list.append(line)
    count = 0    
        
    for index in range(len(scaffold_list)):
        for line in input_gff_file: 
            if count == 0:
                scaffold_string = line
                count +=1
            line = line.split()
            if line[0] == scaffold_list[index]:
                scaffold_string = scaffold_string + '\t'.join(line)+'\n'    
        #For read a file more than once
        input_gff_file.seek(0)
        
    #Generates the fastq file with the string that stored the 4000 
    #sequences of the FastQ file        
    if os.path.exists(small_gff_filename):
        check = raw_input( "{0} file exists, overwrite? (Y/N)\n: "\
        .format(small_gff_filename))
        if check == "Y" or check == "y":
              outfile = open(small_gff_filename,'w')    
              outfile.write(str(scaffold_string))
              outfile.close()
              print "File {0} succesfully generated!"\
               .format(small_gff_filename)
        else:
            pass
    else:
        outfile = open(small_gff_filename,'w')    
        outfile.write(str(scaffold_string))
        outfile.close()    
        print "File {0} succesfully generated!"\
        .format(small_gff_filename)
    
    return small_gff_filename
        
def gff_to_protein(gff_file, genome_db):
    """This is a function that needs a gff file and a genome file and 
    returns proteins
    """
    protein_file = 'protein_file_cat.fasta'
    print "Debugging..."
    print gff_file
    print genome_db
    cmd = 'TransDecoder-2.0/util/gff3_file_to_proteins.pl {0} {1} > {2}'\
    .format(gff_file, genome_db, protein_file)
    subprocess.check_output(cmd, shell=True)
    return protein_file        
        
        
def blastp(protein_file_cat, protein_file_genes):
    """This function needs a file with protein sequences and returns a 
    file with matche Let op Evalue 1E-5 en coverage! 
    """
    cmd = 'makeblastdb -in %s'% (protein_file_genes)
    matches_file = 'matches.txt'
    cmd = 'blastp -query %s -db %s -out %s -evalue 1E-5' \
    % (protein_file_cat.fasta, protein_file_genes, matches_file)
    subprocess.check_output(cmd, shell=True)
    return matches_file        
        
if __name__== "__main__":

    jarjargenes()