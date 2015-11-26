#!/usr/bin/env python

"""
Students: Anne, Diego, Raquel, Koen
Student number: 
Script for reading a fasta file and producing trimmed reads
"""

from sys import argv
import os.path
import subprocess

def small_dataset(input_file):
    """
    """
    counter = 0
    fastq_string = ''     
    
    for line in input_file:

        if line.startswith('@'):  
            counter +=1                    
        if counter > 4000: #To take small samples
            break                    
        fastq_string+=line        

    fastq_file = 'SRR1271857.fastq'
    outfile = open(fastq_file,'w')
    outfile.write(fastq_string)
    outfile.close()

    return fastq_file
    
def fastX(fastq_string):
    """This is a function that returns a fastq file with trimmed reads
    """
    
    out_file = 'test_outfile.fastq'
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
       fastq_file = small_dataset(fh)
   """
   directory = 'SRP041695/SRR1271857.fastq'
   with open(directory) as fh:
       fastq_string = small_dataset(fh)
   """
   fastX(fastq_file)
   
