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
    """ Initial flow function, which allows for choosing what to do
    """
    
    subprocess.check_call("clear",shell=True)
    choices = {1:"Preprocessing data",2:"Mapping and Annotation tools",3:"Exit",0:"Help"}
    out = False
    while not out:
        for key, value in choices.iteritems():
            print key, value
        choice = raw_input("Choose one of the above: ")
        if choice == '1':
            quality_game()
        elif choice == '2':
            annotation_mapping()            
        elif choice == '0':
            help_user()    
        elif choice == '3':
            subprocess.check_call("clear",shell= True)
            print "Farewell, and may the force be with you."
            time.sleep(2)
            subprocess.check_call("clear",shell= True)
            out=True
            
def help_user():
    """ Lists help for the jarjar() function
    """
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
            annotation_mapping()
        elif user == '1':
            quality_game()

def quality_game():
    """Quality interactive program
    """
    print "\nWelcome to quality check\n"
    input_file = filelist("*.f*q","Please insert a number for your input file: ")
    fastX(input_file)
   

    
def fastX(fastq_string):
    """
    This is a function that returns a fastq file with trimmed reads
    """
    out_file = "trimmed_"+fastq_string
    cmd = 'fastq_quality_trimmer -t %s -i %s -o %s ' % ("25",fastq_string, out_file)    
    #If the file is already there it won't overwrite the old file
    if os.path.exists(out_file):
        choice = choice_yn("Test_outfile.fastq output file exists, overwrite? (Y/N)\n: ")
        if choice:
            subprocess.check_call(cmd,shell=True)
    else:
        subprocess.check_call(cmd,shell=True)
    return out_file

def annotation_mapping():
    """Interactive program for annotation and mapping
    """
    print "\nWelcome to annotation & mapping\n"
    out = False

    while not out:
        print "Choose one of the following tasks:\n"

        tools = {1:'HiSat',2:"Cufflinks",3:"Cuffmerge",4:"Tophat2",
                 5:"Bowtie", 6: "GetProteins", 7: "BlastProteins" ,8: "Help", 9: "Quit"}

        for number, tool in tools.items():
            print number, tool
        tool = raw_input('\nWhat tool would you like to choose? ')
        
        if tool == '1':
            subprocess.check_call("clear", shell = True)
            hisat_build()
            hisat_align()
        elif tool == '2':
            subprocess.check_call("clear", shell = True)
            cufflinks()
        elif tool == '3':
            subprocess.check_call("clear", shell = True)
            cuffmerge()
        elif tool == '4':
            subprocess.check_call("clear", shell = True)
            tophat()
        elif tool == "5":
            subprocess.check_call("clear", shell = True)
            bowtie()
        elif tool == "6":
            subprocess.check_call("clear", shell = True)
            gtf_to_protein()
        elif tool == "7":
            subprocess.check_call("clear", shell = True)
            blastp()
        elif tool == "8":
            subprocess.check_call("clear", shell = True)
            print ('help lines')
            help_lines = "This is a section where there will eventually be help"
            print help_lines
        elif tool ==  "9":
            out = True
        else:
            print 'Thanks for using this interactive program!'

def hisat_build():
    """ Creates index files of a (draft) genome in fasta format.
    """
    
    build = False
    if os.path.isfile("build_index.1.ht2"):
        overwrite = None
        choice = choice_yn("Some index files already exist, overwrite? Y|N: ")
        if choice:
            build = True
        else:
            return
    else:
        print "Index files do not exist, please create them"
        build = True
        
    genome = filelist("*.f*a",'Number of file containing draft genome: ')
    
    #Runs hisat-build
    if build:
        cmd = "hisat2-build -p 4 %s build_index" %genome
        print cmd
        subprocess.check_call(cmd, shell = True)
    return

def hisat_align():
    """ HiSat maps reads to the genome using the index files from HiSat-build.
    """
    
    print "Hisat needs the following files to function"
    print "- two files containing paired end read mate-pairs (example_1.fq & example_2.fq)"
    seq_1 = filelist("*.f*q*",'Number of file containing _1 mate pair ends: ')
    subprocess.check_call("clear", shell = True)
    seq_2 = filelist("*.f*q*",'Number of file containing _2 mate pair ends: ')
    subprocess.check_call("clear", shell = True)
    output = raw_input("please specify the name of the .sam output file (excluding extension): " )
    subprocess.check_call("clear",shell = True)
    print "\nHisat will now start aligning reads to the genome\n"
    time.sleep(1)
    
    cmd = "hisat2 --dta-cufflinks -p 4 -x build_index -1 %s -2 %s -S %s.sam" %(seq_1,seq_2,output)
    print cmd
    subprocess.check_call(cmd, shell = True)
    print "HiSat is done mapping the reads."
    print "Now it will create some files which you can use later on"
    
    #create bam, sorted bam and bam index file
    command = "samtools view -bS %s.sam > %s.bam"%(output,output)
    subprocess.check_call(command, shell = True)
    command = "samtools sort %s.bam %s.sorted"%(output,output)
    subprocess.check_call(command, shell = True)
    command = "samtools index %s.sorted.bam"%output
    subprocess.check_call(command, shell = True)

    print "All files have been created, use igv.sh to load and view results!"
    return

def cufflinks():
    """Runs cufflinks which generates predicted transcripts in a GTF file
    """
    
    endprogram = False
    while not endprogram:
        subprocess.check_call("clear",shell=True)
        choice = choice_yn("Welcome to cufflinks\n"
                            "--------------------------------------\n"
                            "For cufflinks you need a sam/bam file."
                            "\nAlready have it? press Y!\n"
                            "Type N for "
                            '"help" on how to get the correct files. ')

        if choice:
            input_file = filelist("*.sorted.?am",'Insert the number of the sam/bam file: ')
            out_folder = raw_input("Please specify the folder the results "
                                   "should be outputted to"
                                   "\n(Leave blank to use current folder): ")

            if len(out_folder)!= 0:
                folder = "-o "+out_folder
            else:
                folder = "-o ./"
                
            cmd = 'cufflinks -q -p 4 --no-update-check %s %s' %(folder, input_file)
            starttime = time.time()
            subprocess.check_call(cmd, shell = True)
            elapsedtime = time.time() - starttime
            print "Cufflinks took %s seconds to complete"%str(elapsedtime)
            add_to_merge = choice_yn("Do you want to add the generated GTF file to the merge file? Y|N: ")
            if choice:
                mergefile = open("gtfmerge.txt", "a")
                mergefile.write("%s/transcripts.gtf"%out_folder)
                mergefile.write("\n")
                mergefile.close()
            endprogram = True
            
        else:
            cont = raw_input("You can use HiSat to generate a sam/bam file "
                             "Run HiSat first to get the file\n"
                             "Press return to exit")
            endprogram = True

    return

def cuffmerge():
    """ Merges multiple GTF files into a single GTF file to be used in cuffdiff
    """
    choice = choice_yn("run Cuffmerge? Y|N: ")
    if choice:
        cmd = "cuffmerge -p 4 gtfmerge.txt"
        subprocess.check_call(cmd, shell = True)
        print "Cuffmerge ran succesfully, returning to previous screen"
        time.sleep(2)
    else:
        print "Cuffmerge didn't run. Returning to previous screen now"
        time.sleep(2)     
    return

def tophat():
    """We're not using it
    """
    
    print "For tophat you need a file with indexes"
    name_indexes = raw_input('Name_indexes: ')
    reads_file = input_file
    cmd = 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
    #(out_folder, name_indexes, reads_file)
    return

def bowtie():
    """ We're not using it
    """
    
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

def gtf_to_protein():
    """This is a function that needs a gff file and a genome file and 
    returns proteins
    """
    scaffold_file = filelist("*.fasta","Please select the correct scaffold number: ")
    gtf_filename = ("*.gtf","Please select the correct gtf file number: ")
    init = gtf_filename.index('.') 
    gff_filename = gtf_filename[:init]+'.gff3'      
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

def blastp():
    """This function needs a file with protein sequences and returns a 
    file with matches Let op Evalue 1E-5 en coverage! 
    """
    protein_file_cat = filelist("*.fasta","Please select a protein sequence fasta file")
    protein_file_arabidopsis("*.fasta","Please select the arabidopsis transcriptome fasta file")
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

def choice_yn(question):
    """ Prompts a yes/no question, and waits for a "correct" answer

    Arguments:
    question -- str, a question that can be answered with yes or no

    Output:
    choice -- bool, True = Yes, False = No
    """
    
    choice = None
    while choice not in ["y","n","Y","N"]:
        choice = raw_input(question)
        if choice not in ["y","n","Y","N"]:
            print "That is not an option..."
    if choice in ["y","Y"]:
        choice = True
    else:
        choice = False
    return choice

def filelist(pattern,question):
    """Displays a list of files matching the extension pattern on the screen

    Arguments:
    pattern -- str, A pattern recognised by the "find" function of linux.
    question -- str, A question to be asked to the user to further specify
                     which file to choose.

    Output:
    choosefile -- str, name of the chosen file
    """
    
    files = subprocess.check_output("find . -name '%s'"%pattern,shell = True)
    filelist = files.split("\n")
    filelist = filelist[:-1]
    key = 0
    filedict = {}
    for elem in filelist:
        filedict[key]= elem.lstrip("./")
        key += 1
    
    print "List of potential files:\n","-"*20
    for number, elem in filedict.items():
        print number, elem
    print "-"*20,"\n"
    print "\n\n"
    filenum = raw_input(question)
    
    while int(filenum) not in filedict.keys():
        print "That file does not exist, choose a new one.\n"
        filenum = raw_input(question)

    choosefile = filedict[int(filenum)]
    
    return choosefile

if __name__ == '__main__':    
    jarjar()
