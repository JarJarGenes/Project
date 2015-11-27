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
def jarjar():
    out = False
    while not out:
        usr = raw_input("Already know what you want? Press 1(qual) or 2(ann); Need help? Press 0 (3 to exit): ")
        if usr == '1':
            quality_game()
        elif usr == '2':
            annotation_game()            
        elif usr == '0':
            help_user()    
        elif usr == '3':
            print "--- Thanks for using us"
            out=True
        
def help_user():
    stop = False
    while not stop:
        options = {1:"Quality check", 2: "Annotation tools", 3: "Exit"}    
        print "\nWELCOME TO JAR-JAR PLATFORM!\nThis platform is design as a tool of tools, here you can choose between several option for treat your data. Choose one of the following:\n"
        for number, option in options.items():
            print number, option
        user = raw_input("\nInsert a number from the list: ")
        if user == '3':
            stop = True
        elif user == '2':
            annotation_game()
        elif user == '1':
            quality_game()
        
def run_my_program(cmd):
    """This functions runs a choosen tool in the linux command line
    """
    print cmd
    #subprocess.check_call(cmd, shell=True)
def bowtie2_options():
    """Bowtie run options
    """
    check = True
    while check:
        phred_score = raw_input('What is your phred_score? (64 or 33)')
        format_file = raw_input('Which format are you using? Please choose: "q" (=fastQ) or "f"(=fasta) ')
        if phred_score == '64' or phred_score == '33':
            if format_file.lower() == 'q' or format_file.lower() == 'f':
                check = False
        else:
            print 'Phred score or format file no valid, try again'
    
    return phred_score, format_file
        
def annotation_game():
    """Interactive program
    """
    print "\nWelcome to annotation\n"
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
    while not os.path.exists(input_file):
        print 'Your input file seems that doesn\'t exists'
        input_file = raw_input('Input file name: ')
    out = False
    while not out:
        print "Choose one of the following tasks:\n"
        tools = {1:'Bowtie2',2:"Cufflinks",3:"Tophat2",4:"help", 5: "quit"}
        for number, tool in tools.items():
            print number, tool
        tool = raw_input('\nWhat tool would you like to choose? ')    
        if tool == '1':
            phred_score, format_file = bowtie2_options()
            cmd = 'bowtie2 -x %s -%s --phred%s >%s' %(input_file,format_file, phred_score, out_folder)
            ##(out_folder(name_indexes),input_file(fastQ_file or fasta file respectively),format_file phred_score(64|33))
        elif tool == '2':
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
                else:
                    cmd = False                                
            ##%(out_folder, sam_file) #[sam_file = 'accepted_hits.bam]
        elif tool == '3':
            print "For tophat you nedd a file with indexes"
            name_indexes = raw_input('Name_indexes: ')
            reads_file = input_file
            cmd = 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
            #(out_folder, name_indexes, reads_file)
        elif tool == "4":
            print ('help lines')
            cmd = False
            #bowtie2 indexes command line: 'bowtie2-build -f %s %s' %(FASTA_reference, name_indexes)
            #bowtie2 command line: 'bowtie2 -x %s -q or -f % --phred%d'    %(name_indexes,fastQ_file or fasta file respectively, phred_score(64|33))
            #tophat2 command line: 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
            #samtools command line(we need this for cufflinks): 'samtools view %s - %s' %(bam_file, out_sam_file)
            #cufflinks command line: 'cufflinks -o %s %s'%(out_folder, sam_file) [sam_file = 'accepted_hits.bam]
        elif tool ==  "5":
            out = True
            cmd = False
        if cmd:
            run_my_program(cmd)
        else:
            print 'Thanks for using us'

def quality_game():
    """Quality interactive program
    """
    print "\nWelcome to quality check\n"
    try:
        input_file = argv[1]
    except IndexError:
        input_file = raw_input("Please inser a name for your input file: ")
    while not os.path.exists(input_file):
        print 'Your input file seems that doesn\'t exists'
        input_file = raw_input('Input file name: ')
    with open(input_file) as fh:
       filename = fh.name
       index = filename.rfind('/')
       filename = filename[index:].replace('/','')
       fastq_file = small_dataset(fh,filename)    
    fastX(fastq_file)
   
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
        else: #Maybe this is redundant?
            pass
    else:
        subprocess.check_call(cmd,shell=True)
    return out_file

if __name__ == '__main__':    
    jarjar()
    
    
    
