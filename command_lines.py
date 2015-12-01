#!usr/bin/env python
"""
Authors: Raquel, Koen, Diego, Anna
Script: Annotation
"""
#modules
from sys import argv
import subprocess
import os.path
import time
import itertools

#function
def jarjar():
    subprocess.check_call("clear",shell=True)
    choices = {1:"Quality check",2:"Annotation tools",3:"Exit",4:"Help"}
    out = False
    while not out:
        for key, value in choices.iteritems():
            print key, value
        usr = raw_input("Choose one of the above: ")
        if usr == '1':
            quality_game()
        elif usr == '2':
            annotation_game()            
        elif usr == '0':
            help_user()    
        elif usr == '3':
            print "May the force be with you"
            out=True
        
def help_user():
    stop = False
    while not stop:
        options = {1:"Quality check", 2: "Annotation tools", 3: "Exit"}    
        print ("\nWELCOME TO JAR-JAR PLATFORM!\nThis platform is design as a"
               "tool of tools, here you can choose between several option"
               "for treat your data. Choose one of the following:\n")
        for number, option in options.items():
            print number, option
        user = raw_input("\nInsert a number from the list: ")
        if user == '3':
            stop = True
        elif user == '2':
            annotation_game()
        elif user == '1':
            quality_game()

def quality_game():
    """Quality interactive program
    """
    print "\nWelcome to quality check\n"
    
    try:
        input_file = argv[1]
    except IndexError:
        input_file = raw_input("Please insert a name for your input file: ")
    input_file, out = input_file_checker(input_file)
    while not out:
        with open(input_file) as fh:
           filename = fh.name
           index = filename.rfind('/')
           filename = filename[index:].replace('/','')
           fastq_file = small_dataset(fh,filename)    
        fastX(fastq_file)
   

    
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
        subprocess.check_call(cmd,shell=True)
    return out_file

def annotation_game():
    """Interactive program for annotation
    """
    print "\nWelcome to annotation\n"
    out = False

    while not out:
        print "Choose one of the following tasks:\n"

        tools = {1:'Bowtie2',2:"Cufflinks",3:"Tophat2",
                 4:"HiSat", 5: "help", 6: "quit"}

        for number, tool in tools.items():
            print number, tool
        tool = raw_input('\nWhat tool would you like to choose? ')
        
        if tool == '1':
            subprocess.check_call("clear", shell = True)
            bowtie()
        elif tool == '2':
            subprocess.check_call("clear", shell = True)
            cufflinks()
        elif tool == '3':
            subprocess.check_call("clear", shell = True)
            tophat()
        elif tool == "4":
            subprocess.check_call("clear", shell = True)
            hisat_build()
            hisat_align()
        elif tool == "5":
            subprocess.check_call("clear", shell = True)
            print ('help lines')
            #bowtie2 indexes command line: 'bowtie2-build -f %s %s' %(FASTA_reference, name_indexes)
            #bowtie2 command line: 'bowtie2 -x %s -q or -f % --phred%d'    %(name_indexes,fastQ_file or fasta file respectively, phred_score(64|33))
            #tophat2 command line: 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
            #samtools command line(we need this for cufflinks): 'samtools view %s - %s' %(bam_file, out_sam_file)
            #cufflinks command line: 'cufflinks -o %s %s'%(out_folder, sam_file) [sam_file = 'accepted_hits.bam] 
        elif tool ==  "6":
            out = True

        else:
            print 'Thanks for using us'

def bowtie():
    phred_score, format_file = bowtie2_options()
    cmd = ('bowtie2 -x %s -%s --phred%s >%s'
           %(input_file,format_file, phred_score, out_folder))
    ##(out_folder(name_indexes),input_file(fastQ_file or fasta file respectively),format_file phred_score(64|33))
    return

def bowtie2_options():
    """Bowtie run options
    """
    check = True
    while check:
        phred_score = raw_input('What is your phred_score? (64 or 33)')
        format_file = raw_input("Which format are you using?"
                                "Please choose: 'q' (=fastQ) or 'f'(=fasta)")
        if phred_score == '64' or phred_score == '33':
            if format_file.lower() == 'q' or format_file.lower() == 'f':
                check = False
        else:
            print 'Phred score or format file no valid, try again'
    
    return phred_score, format_file

def cufflinks():
    endprogram = False
    while not endprogram:
        subprocess.check_call("clear",shell=True)
        warning = raw_input("Welcome to cufflinks\n"
                            "--------------------------------------\n"
                            "For cufflinks you need a sam/bam file."
                            "\nAlready have it? press 1!\n"
                            "Press 0 for "
                            '"help" on how to get the correct files. ')

        if warning == '1':
            sbamfiles = subprocess.check_output('find *.sorted.?am',shell=True)
            sbamlist = sbamfiles.split()
            key = 0
            filedict = {}
            for elem in sbamlist:
                filedict[key]=elem
                key += 1
        
            print "List of potential sam/bam files:\n","-"*20
            for number, elem in filedict.items():
                print number, elem
            print "-"*20,"\n"
    
            input_file = raw_input('Insert the number of the sam/bam file: ')
            input_file = filedict[int(input_file)]
            out_folder = raw_input("Please specify the folder the results "
                                   "should be outputted to"
                                   "\n(Leave blank to use current folder): ")
            if len(out_folder)!= 0:
                out_folder = "-o "+out_folder
            else:
                out_folder = "-o ./"
            cmd = 'cufflinks %s %s' %(out_folder, input_file)
            
            subprocess.check_call(cmd, shell = True)
            endprogram = True
        elif warning == '0':
            cont = raw_input("You can use HiSat to generate a sam/bam file "
                             "Run HiSat first to get the file\n"
                             "Press return to exit")
            endprogram = True
        else:
            print "That's not 1 or 0!"
    return

def tophat():
    print "For tophat you need a file with indexes"
    name_indexes = raw_input('Name_indexes: ')
    reads_file = input_file
    cmd = 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
    #(out_folder, name_indexes, reads_file)
    return

def hisat_build():
    
    build = False
    if os.path.isfile("build_index.1.ht2"):
        overwrite = None
        while overwrite not in ["Y","N","y","n"]:
            overwrite = raw_input("Some index files already exist, overwrite? Y|N: ")
        if overwrite.upper() == "Y":
            build = True
        else:
            return
    else:
        print "Index files do not exist, please create them"
        build = True
        
    files = subprocess.check_output("find *.fasta", shell = True)
    filelist = files.split()
    key = 0
    filedict = {}
    for elem in filelist:
        filedict[key]=elem
        key += 1
        
    print "List of potential genome files:\n","-"*20
    for number, elem in filedict.items():
        print number, elem
    print "-"*20,"\n"
    
    genome = raw_input('Number of file containing draft genome: ')
    genome = filedict[int(genome)]

    #Runs hisat-build
    if build:
        cmd = "hisat2-build %s build_index" %genome
        print cmd
        subprocess.check_call(cmd, shell = True)
    return

def hisat_align():
    
    print "Hisat needs the following files to function"
    print "- two files containing paired end read mate-pairs (example_1.fq & example_2.fq)"

    files = subprocess.check_output("find *.fastq",shell = True)
    #files += subprocess.check_output("find *.fq",shell = True)
    filelist = files.split()
    key = 0
    filedict = {}
    for elem in filelist:
        filedict[key]=elem
        key += 1
    
    print "List of potential fastq files:\n","-"*20
    for number, elem in filedict.items():
        print number, elem
    print "-"*20,"\n"
        
    seq_1 = raw_input('Number of file containing _1 mate pair ends: ')
    seq_1 = filedict[int(seq_1)]
    seq_2 = raw_input('Number of file containing _2 mate pair ends: ')
    seq_2 = filedict[int(seq_2)]            

    output = raw_input("please specify the name of the .sam output file (excluding extension): " )
    subprocess.check_call("clear",shell = True)
    print "\nHisat will now start aligning reads to the genome\n"
    time.sleep(3)
    cmd = "hisat2 --dta-cufflinks -x build_index -1 %s -2 %s -S %s.sam" %(seq_1,seq_2,output)
    print cmd
    subprocess.check_call(cmd, shell = True)

    #create bam, sorted bam and bam index file
    command = "samtools view -bS %s.sam > %s.bam"%(output,output)
    subprocess.check_call(command, shell = True)
    command = "samtools sort %s.bam %s.sorted"%(output,output)
    subprocess.check_call(command, shell = True)
    command = "samtools index %s.sorted.bam"%output
    subprocess.check_call(command, shell = True)

    print "All files have been created, use igv.sh to load and view results!"
    return
            
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

if __name__ == '__main__':    
    jarjar()
