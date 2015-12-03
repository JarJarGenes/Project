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
        "from your fasta file? (Press -1 to sequence the whole sequence" \
         "Press 0 to exit the program\n Warning! this may take a while"+\
         "depending on your file size!): ")
        if input_number_sequence > '0':
            flow_program(int(input_number_sequence))
            break
        elif input_number_sequence < '0':
            flow_program(0)
            break            
        else:
            print "#################################################" 
            print "Thanks for using this program, Beta version V1.0" 
            print "#################################################"             
            break

def flow_program(input_number_sequence):
    #Follows the main flow of the program
    #open the two files from the user for getting the N sequence
    small_fasta_file = ''
    protein_file_cat = ''    
    scaffold_file  = ''
    with open(argv[1]) as fh:
        scaffold_file    = fh.name
        index             = scaffold_file.rfind('/')
        scaffold_file    = scaffold_file[index:].replace('/','')
        small_fasta_file  = small_fasta_dataset(fh,scaffold_file,\
        input_number_sequence)
    """
    with open(argv[2]) as fh:
        gff_filename    = fh.name
        index           = gff_filename.rfind('/')
        gff_filename    = gff_filename[index:].replace('/','')+'.small'
        small_gff_dataset(fh,small_fasta_file,gff_filename)
    """
    
    with open(argv[2]) as fh:
        gtf_filename     = fh.name
        #index            = gtf_filename.rfind('/')
        #gtf_filename     = gtf_filename[index:].replace('/','')+'.small'
        protein_file_cat = gtf_to_protein(scaffold_file,gtf_filename)
    print protein_file_cat
 
    cmd = 'clear'
    print subprocess.check_output(cmd, shell=True)
    print "###########################################"
    print "######## LIST OF POSSIBLE FASTA FILES TO SELECT ########"
    print "###########################################"    
    cmd = 'ls *.fasta'
    print subprocess.check_output(cmd, shell=True)
    protein_file_arabidopsis = \
    raw_input("Please select the proteins file to blast: ")    
    blastp(protein_file_cat,protein_file_arabidopsis)
    
    
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
            
            if (input_number_sequence != 0):            
            
                for index in range(input_number_sequence):    
                    outfile.write(str(newlist[index]['name']))
                    outfile.write(str(newlist[index]['sequence']))                            
                outfile.close()
                print "File {0} succesfully generated!"\
                   .format(small_fasta_file)
            else:
                for index in range(len(newlist)):    
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
        if (input_number_sequence != 0):    
            
            for index in range(input_number_sequence):    
                outfile.write(str(newlist[index]['name']))
                outfile.write(str(newlist[index]['sequence']))                            
            outfile.close()
            print "File {0} succesfully generated!"\
            .format(small_fasta_file)
        else:
            for index in range(len(newlist)):    
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
        
def gtf_to_protein(scaffold_file,gtf_filename):
    """This is a function that needs a gff file and a genome file and 
    returns proteins
    """
    init = gtf_filename.index('.') 
    gff_filename = gtf_filename[:init]+'.gff3'    
    #TransDecoder-2.0/util/cufflinks_gtf_to_alignment_gff3.pl 
    #                   transcripts.gtf > transcripts.gff3    
    cmd = 'TransDecoder-2.0/util/cufflinks_gtf_to_alignment_gff3.pl' \
    " %s > %s" % (gtf_filename, gff_filename )  
    subprocess.check_output(cmd, shell=True)
    #Name for the protein file from the transdecoder
    protein_file_cat = 'protein_file_cat.fasta'
    print "Running..."
    print "Please wait..."
    #Problems in the protein_file_Cat.fasta
    print scaffold_file
    cmd = 'TransDecoder-2.0/util/gff3_file_to_proteins.pl {0} {1} > {2}'\
    .format(gff_filename, scaffold_file, protein_file_cat)
    subprocess.check_output(cmd, shell=True)

    return protein_file_cat        
    
        
def blastp(protein_file_cat, protein_file_arabidopsis):
    """This function needs a file with protein sequences and returns a 
    file with matches Let op Evalue 1E-5 en coverage! 
    """
    init = protein_file_arabidopsis.index('.') 
    database = 'db_proteins_'+protein_file_arabidopsis[:init]
    #makeblastdb -in protein_file_arabidopsis.fasta -dbtype prot 
    #-out db_protein_file_genes.db
    cmd = 'makeblastdb -in %s -dbtype prot -out %s  '\
    % (protein_file_arabidopsis,database)
    subprocess.check_output(cmd, shell=True)
    matches_file = 'matches.txt'
    #blastp -query protein_file_cat.fasta -db db_protein_file_genes.db 
    #-out matches.txt -outfmt 7 -evalue 1E-5
    cmd = 'blastp -query %s -db %s -out %s -outfmt 7 -evalue 1E-5' \
    % (protein_file_cat, database, matches_file)
    subprocess.check_output(cmd, shell=True)
    print "Done."
    return matches_file        
        
if __name__== "__main__":

    jarjargenes()