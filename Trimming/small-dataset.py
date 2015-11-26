#!/usr/bin/env python

"""
Students: Anne, Diego, Raquel, Koen
Student number: 
Script for reading a fasta file and producing trimmed reads
"""

from sys import argv
import os.path
import subprocess

def small_dataset(input_file,filename):
    """
    Description: function that gets the first 4000 sequences in the input FastQ file
    Input: FastQ file sequence
    Output: Generates an output fastQ file with the 4000 sequences
    Return: String with the name of the output fastq file name
    """
    counter = 0
    fastq_string = ''     
    
    for line in input_file:

        if line.startswith('@'):  
            counter +=1                    
        if counter > 4000: #To take small samples
            break                    
        fastq_string+=line        
    #Generates the fastq file with the string that stored the 4000 sequences of the FastQ file
    fastq_file = filename
    outfile = open(fastq_file,'w')
    outfile.write(fastq_string)
    outfile.close()

    return fastq_file
    
def fastX(fastq_string):
    """
    This is a function that returns a fastq file with trimmed reads
    """
    out_file = 'test_outfile_'+fastq_string
    #cmd = 'fastq_quality_trimmer -t %s -i %s -o %s ' % (25,'../yeast/CENPK_RNA_1.fastq', out_file)
    cmd = 'fastq_quality_trimmer -t %s -i %s -o %s ' % (25,fastq_string, out_file)    
    #If the file is already there it won't overwrite the old file
    if os.path.exists(out_file):
        check = raw_input( "Test_outfile.fastq output file exists, overwrite? (Y/N)\n: ")
        if check == "Y" or check == "y":
            subprocess.check_call(cmd,shell=True)
        else:
            pass
    else:
        subprocess.check_call(cmd,shell=True)
    return out_file
    
if __name__== "__main__":


   with open(argv[1]) as fh:
       filename = fh.name
       index = filename.rfind('/')
       filename = filename[index:].replace('/','')
       fastq_file = small_dataset(fh,filename)
   fastX(fastq_file)
   
