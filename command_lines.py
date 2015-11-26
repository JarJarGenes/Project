#!usr/bin/env python
"""
Authors: Raquel, Koen, Diego, Anna
Script: Annotation
"""
#modules
from sys import argv
import subprocess
import os.path

#function
def run_my_program(cmd):
    """This functions runs a choosen tool in the linux command line
    """
    print cmd
    #e = subprocess.check_call(cmd, shell=True)
def bowtie2_options():
    """Bowtie run options
    """
    check = True
    while check:
        phred_score = raw_input('What is your phred_score? (64 or 33)')
        format_file = raw_input('Which format are you using? (q = fastQ, f= fasta')
        if phred_score == '64' or phred_score == '33':
            if format_file.lower() == 'q' or format_file.lower() == 'f':
                check = False
        else:
            print 'Phred score or format file no valid, try again'
    
    return phred_score, format_file

if __name__ == '__main__':
    """Interactive program
    """
    try:
        out_folder = argv[1]
        input_file = argv[2]
    except IndexError:
        print 'Name for your output folder and input file are requiered'
        out_folder = raw_input('Output folder name: ')
        input_file = raw_input('Input file name: ')
    if os.path.exists(out_folder):
        overwrite = raw_input('Your output folder already exist, overwrite? (Y|N)')
        if overwrite.upper() == 'N':
            out_folder = raw_input('Output folder name: ')
    if not os.path.exists(input_file):
        print 'Your input file seems that doesn\'t exists'
        input_file = raw_input('Input file name: ')
    out = False
    while not out:
        tool = raw_input('What tool would you like to choose? (Choices: "Bowtie2", "Cufflinks", "TopHat2", "help", "quit") ')    
        if tool.lower() == 'bowtie2':
            phred_score, format_file = bowtie2_options()
            cmd = 'bowtie2 -x %s -%s --phred%s >%s' %(input_file,format_file, phred_score, out_folder)
                    ##(out_folder(name_indexes),input_file(fastQ_file or fasta file respectively),format_file phred_score(64|33))
        elif tool.lower() == 'cufflinks':
            warming = raw_input('For cufflinks you need a sam file, run bowtie2 first if you need a bam file. Already have it(should be your input file!)? Write "continue" or "help" to get the correct files. ')
            if warming == 'continue':
                input_file = raw_input('Insert again the name of your sam file: ')
                cmd = 'cufflinks -o %s %s' %(out_folder, input_file) #[sam_file = 'accepted_hits.bam]
            else:
                cont = raw_input('You can use bowtie2 to create a bam file and then samtools to get the sam file, do you still want to continue?(Y|N) ')
                if cont.lower() == 'y' or cont.lower() == 'yes':
                    phred_score, format_file = bowtie2_options()
                    cmd = 'bowtie2 -x %s -%s --phred%s >%s' %(input_file,format_file, phred_score, out_folder)
                    run_my_program(cmd)
                    print 'Check the name of your bam file and choose cufflinks again'
                    cmd = 'ls -lh'
                    run_my_program(cmd)
                    bam_file = raw_input('Name of your bam file: ')
                    cmd = 'samtools view %s - %s' %(bam_file, out_folder)  
                    run_my_program(cmd)                                  
            ##%(out_folder, sam_file) #[sam_file = 'accepted_hits.bam]
        elif tool.lower() == 'tophat2':
            name_indexes = raw_input('Name_indexes: ')
            reads_file = input_file
            cmd = 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
            #(out_folder, name_indexes, reads_file)
        elif tool.lower() == 'help' or tool.lower() == 'h':
            print ('help lines')
            cmd = False
            #bowtie2 indexes command line: 'bowtie2-build -f %s %s' %(FASTA_reference, name_indexes)
            #bowtie2 command line: 'bowtie2 -x %s -q or -f % --phred%d'    %(name_indexes,fastQ_file or fasta file respectively, phred_score(64|33))
            #tophat2 command line: 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
            #samtools command line(we need this for cufflinks): 'samtools view %s - %s' %(bam_file, out_sam_file)
            #cufflinks command line: 'cufflinks -o %s %s'%(out_folder, sam_file) [sam_file = 'accepted_hits.bam]
        elif tool.lower() ==  'quit':
            out = True
            cmd = False
        if cmd:
            run_my_program(cmd)
    else:
        print 'Thanks for using us'
