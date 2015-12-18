#!usr/bin/env python
"""
Authors: Raquel, Koen, Diego, Anna
Script: This is the Jar-Jar platform, here you can choose several options for treating
your data in an interactive way. Preprocessing, annotation, mapping and help are options.
"""
#modules
import subprocess
import os.path
import time

#Classes
class JarjarTools:
    """This is the main class which calls the subclass chosen from the options function
    """
        
    def __init__(self):
        """Initializes the platform, cleans the screen and prints the name
        """
        
        subprocess.check_call("clear",shell=True)
        print  'JARJAR PLATFORM\n'


    def options(self):
        """With this function we offer to the user several options to work with the data.

        User can choose between preprocess the data, mapping and annotation, exit or help.
        After choosing the script calls one of the subclasses
        """
        
        subprocess.check_call("clear",shell=True)
        choices = {1:"Preprocessing data",2:"Mapping and Annotation tools",0:"Exit",3:"Help",4:"Auto-run"}
        out = False
        while not out:
            for number, one_choice in choices.iteritems():
                print number, one_choice
            choice = raw_input("Choose one of the above: ")
            if choice == '1':
                quality_game()
            elif choice == '2':
                annotation_mapping_game()            
            elif choice == '3':
                help_user()
            elif choice == '4':
                autoRun()
            elif choice == '0':
                subprocess.check_call("clear",shell= True)
                print "Farewell, and may the force be with you."
                time.sleep(2)
                subprocess.check_call("clear",shell= True)
                out=True

                
    #Below are the functions that can be called from the subclasses.            
    def filelist(self,pattern,question):
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
        if len(filedict.keys()) == 0:
                print "You do not have the correct files. Program will return to previous menu"
                time.sleep(2)
                return False
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
        
        return '"'+choosefile+'"'

        

    def choice_yn(self,question):
        """Prompts a yes/no question, and waits for a "correct" answer
    
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


    def check_out(self,cmd):
        """Calls subprocess.check_output in the command line

        Argument:
        cmd, which is the chosen command line from the function that is calling this one.
        -- string type
		
        Output: Run the command line in the shell
	"""
	subprocess.check_output(cmd, shell=True)

    def check_call(self,cmd):
        """Calls subprocess.check_call in the command line

        Argument:
        cmd, which is the chosen command line from the function that is calling this one.
        -- string type        Output: Run the command line in the shell

        Output: Run the command line in the shell
        """
	subprocess.check_call(cmd, shell=True)

        
class quality_game(JarjarTools):
    
    def __init__(self):
        """Starts the quality interactive function. It automatically calls fastX function
        to check the quality of fastQ file

        The program will ask for fastq files, if the are not the the program could close
        
        Output: The script run the command line for the chosen program in the shell
        """
        
        print "\nWelcome to quality check\n"
        filedict = JarjarTools().filelist("*.f*q", "Please insert a number for your input file: ")
        input_file = filedict  # raw_input("Please insert a number for your input file: ")
        self.fastX(input_file)
   
    
    def fastX(self,fastq_string):
        """This is a function that returns a fastq file with trimmed reads

        Argument:
        The name of a fastQ file as a string type ?
        
        Output:
        """
        
        out_file = "trimmed_"+fastq_string
        cmd = 'fastq_quality_trimmer -t %s -i %s -o %s ' % ("25",fastq_string, out_file)    
        #If the file is already there it won't overwrite the old file
        if os.path.exists(out_file):
            choice = JarjarTools().choice_yn("Test_outfile.fastq output file exists, overwrite? (Y/N)\n: ")
            if choice:
                JarjarTools().check_call(cmd)
        else:
            JarjarTools().check_call(cmd)
            
        return out_file


class help_user(JarjarTools):
    """Inherits from JarjarTools, this will give a brief explanation
    to the user and the available options inside the platform again.

    Called from options in JarjarTools
    """
    
    def __init__(self):
        """Prints a small description of the platform and gives the different options again

        User has to choose between Quality check, annotation & mapping tools or exit.
        """ 
        stop = False
        while not stop:
            options = {0: "Exit", 1:"Quality check", 2: "Annotation & Mapping tools"}    
            print ("\nWELCOME TO JAR-JAR PLATFORM!\nThis platform is design as a "
                   "tool of tools, here you can choose between several option"
                   " for treating your data. Now, you can choose one of the following:\n")
            for number, option in options.items():
                print number, option
            user = raw_input("\nInsert a number from the list: ")
            if user == '0':
                stop = True
            elif user == '2':
                annotation_mapping_game()
            elif user == '1':
                quality_game()

                
class annotation_mapping_game(JarjarTools):
    """Inherits from JarjarTools, it starts an interactive function for choosing
    tools for annotation and mapping. Exit and help are also available.
    """
    
    def __init__(self):
        """Interactive funtion for choosing tools for annotation and mapping

        User has to choose between a list of tool for annotation and mapping

        Input: A number from the list of options
        Output: Run the chosen program and return to annotation and mapping options
        """
        
        print "\nWelcome to annotation & mapping\n"
        out = False    
        while not out:
            print "Choose one of the following tasks:\n"    
            tools = {1:'HiSat',2:"Cufflinks",3:"Cuffmerge",4: "CuffDiff", 5:"Tophat2",
                     6:"Bowtie", 7: "GetProteins", 8: "BlastProteins" ,9: "Help", 0: "Exit"}    
            for number, tool in tools.items():
                print number, tool
            tool = raw_input('\nWhat tool would you like to choose? ')
            JarjarTools().check_call('clear')
            #Each option calls a different function
            if tool == '1':
                self.hisat_build()
                self.hisat_align()
            elif tool == '2':
                self.cufflinks()
            elif tool == '3':
                self.cuffmerge()
            elif tool == '4':
                self.cuffdiff()
            elif tool == '5':
                self.tophat()
            elif tool == "6":
                self.bowtie()
            elif tool == "7":
                self.gtf_to_protein()
            elif tool == "8":
                self.blastp()
            elif tool == "9":
                self.help_lines()
            elif tool ==  "0":
                #When out is True, the program exits from annotation_game
                out = True
            else:
                print 'Thanks for using this interactive program!'


    def help_lines(self):
        """Prints a text with explanations for each tool
        """
        
        print 'help lines'
        help_lines = "This is a section where there will eventually be help\n"
        print help_lines

    
    def hisat_build(self):
        """ Creates index files of a (draft) genome in fasta format

        Input:
        Output:
        """
        
        build = False
        if os.path.isfile("build_index.1.ht2"):
            choice = JarjarTools().choice_yn("Some index files already exist, overwrite? Y|N: ")
            if choice:
                build = True
            else:
                return
        else:
            print "Index files do not exist, please create them"
            build = True
        genome = JarjarTools().filelist("*.f*a",'Number of file containing draft genome: ') 
        if not genome:
            return
        #Runs hisat-build
        if build:
            cmd = "hisat2-build -p 4 %s build_index" %genome
            print cmd
            JarjarTools().check_call(cmd)

        return

    
    def hisat_align(self):
        """ HiSat maps reads to the genome using the index files from HiSat-build.

        Input:
        Output:
        """
        
        print "Hisat needs the following files to function"
        print "- two files containing paired end read mate-pairs (example_1.fq & example_2.fq)"
        seq_1 = JarjarTools().filelist("*.f*q*",'Number of file containing _1 mate pair ends: ')
        JarjarTools().check_call('clear')
        seq_2 = JarjarTools().filelist("*.f*q*",'Number of file containing _2 mate pair ends: ')
        JarjarTools().check_call('clear')
        output = raw_input("please specify the name of the .sam output file (excluding extension): " )
        JarjarTools().check_call('clear')
        print "\nHisat will now start aligning reads to the genome\n"
        time.sleep(1)        
        cmd = "hisat2 --dta-cufflinks -p 4 -x build_index -1 %s -2 %s -S %s.sam" %(seq_1,seq_2,output)
        #cmd is printed so the user can see the command line that is being used
        print cmd
        JarjarTools().check_call(cmd)
        print "HiSat is done mapping the reads."
        print "Now it will create some files which you can use later on"        
        #create bam, sorted bam and bam index file
        command = "samtools view -bS %s.sam > %s.bam"%(output,output)
        JarjarTools().check_call(command)
        command = "samtools sort %s.bam %s.sorted"%(output,output)
        JarjarTools().check_call(command)
        command = "samtools index %s.sorted.bam"%output
        JarjarTools().check_call(command)    
        print "All files have been created, use igv.sh to load and view results!"
        
        return

    
    def cufflinks(self):
        """Runs cufflinks which generates predicted transcripts in a GTF file

        Input:
        Output:
        """
        
        endprogram = False
        while not endprogram:
            JarjarTools().check_call('clear')
            choice = JarjarTools().choice_yn("Welcome to cufflinks\n"
                                "--------------------------------------\n"
                                "For cufflinks you need a sam/bam file."
                                "\nAlready have it? press Y!\n"
                                "Type N for "
                                "'help' on how to get the correct files. ")   
            if choice:
                input_file = JarjarTools().filelist("*.sorted.?am",'Insert the number of the sam/bam file: ')
                out_folder = raw_input("Please specify the folder the results "
                                       "should be outputted to"
                                       "\n(Leave blank to use current folder): ")    
                if len(out_folder)!= 0:
                    folder = "-o "+out_folder
                else:
                    folder = "-o ./"                    
                cmd = 'cufflinks -q -p 4 --no-update-check %s %s' %(folder, input_file)
                starttime = time.time()
                JarjarTools().check_call(cmd)
                elapsedtime = time.time() - starttime
                print "Cufflinks took %s seconds to complete"%str(elapsedtime)
                choice = JarjarTools().choice_yn("Do you want to add the generated GTF file to the merge file? Y|N: ")
                if choice:
                    mergefile = open("gtfmerge.txt", "a")
                    mergefile.write("%s/transcripts.gtf"%out_folder)
                    mergefile.write("\n")
                    mergefile.close()
                endprogram = True                
            else:
                raw_input("You can use HiSat to generate a sam/bam file "
                "Run HiSat first to get the file\n"
                "Press return to exit")
                endprogram = True
    
        return

    
    def cuffmerge(self):
        """ Merges multiple GTF files into a single GTF file to be used in cuffdiff

        Input:
        Output:
        """
        
        choice = JarjarTools().choice_yn("run Cuffmerge? Y|N: ")
        if choice:
            cmd = "cuffmerge -p 4 gtfmerge.txt"
            JarjarTools().check_call(cmd)
            print "Cuffmerge ran succesfully, returning to previous screen"
            time.sleep(2)
        else:
            print "Cuffmerge didn't run. Returning to previous screen now"
            time.sleep(2)     
        return

    def cuffdiff(self):
        """ Runs cuffdiff and allows the user to choose files etc.

        Arguments:
        N/A

        Output:
        N/A
        """
        out_folder = raw_input("Please specify the folder the results "
                                       "should be outputted to"
                                       "\n(Leave blank to use current folder): ")    
        if len(out_folder)!= 0:
            folder = out_folder
        else:
            folder = "./"
            
        subprocess.check_call("clear",shell = True)
        print "Output folder set to: "+folder
        print "Reference .GTF file: "
        print "Files selected: " + "\n"

        gtf = str(JarjarTools.filelist(self,"*.g?f","What is your reference .gtf file? "))
        subprocess.check_call("clear",shell = True)
        print "Output folder set to: "+folder
        print "Reference .GTF file: "+gtf
        print "Files selected: " + "\n"
        filenumber = int(raw_input("How many files do you want to compare with each other (min. 2)? "))
        file_seperated = ""
        labels = ""
        for x in range(filenumber):
            subprocess.check_call("clear",shell = True)
            print "Output folder set to: "+folder
            print "Reference .GTF file: "+gtf
            print "Files selected: %s"%labels + "\n"
            filename = JarjarTools.filelist(self,"*.?am","Insert the number of file #%s and press return: "%str(x+1))
            file_seperated += " %s"%filename
            try:
                labels += filename[filename.rindex('/')+1:filename.index(".")]+","
            except ValueError:
                labels += filename+","

        labels = labels[:-1]
        print "Output folder set to: "+folder
        print "Reference .GTF file: "+gtf
        print "Files selected: %s"%labels + "\n" + "\n"
        
        
        cmd = "cuffdiff -o %s -L %s -p 4 %s%s"%(folder,labels,gtf,file_seperated)
        print "Cuffdiff will now run with these settings:"
        print cmd
        time.sleep(5)

        subprocess.check_call(cmd,shell=True)

        raw_input("Cufflinks is done running, press return to continue")
        return
    
    def tophat(self):
        """Calls the program tophat,    NOT COMPLETELY DEVELOPED

        Input:
        Output:
        """
        
        print "For tophat you need a file with indexes"
        name_indexes = raw_input('Name_indexes: ')
        reads_file = raw_input('Input file: ')
        cmd = 'tophat2 -o %s %s  %s' %(out_folder, name_indexes, reads_file)
        #(out_folder, name_indexes, reads_file)
        JarjarTools().check_call(cmd)
        return

    
    def bowtie(self):
        """ Calls the program bowtie,    NOT COMPLETELY DEVELOPED

        Input:
        Output:
        """
        
        phred_score, format_file = self.bowtie2_options()
        cmd = ('bowtie2 -x %s -%s --phred%s >%s'
               %(input_file,format_file, phred_score, out_folder))
        ##(out_folder(name_indexes),input_file(fastQ_file or fasta file respectively),format_file phred_score(64|33))
        JarjarTools().check_call(cmd)
        return

    
    def bowtie2_options(self):
        """Bowtie run options

        Input:
        Output:
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


    def gtf_to_protein(self):
        """This is a function that needs a gff file and a genome file and 
        returns proteins

        Input:
        Output:
        """
        scaffold_file = JarjarTools().filelist("*.fasta","Please select the correct scaffold number: ")
		
        gtf_filename = JarjarTools().filelist("*.gtf","Please select the correct gtf file number: ")
        if scaffold_file == False or gtf_filename == False:
            return
        init = gtf_filename.index('.') 
        gff_filename = gtf_filename[:init]+'.gff3'      
        cmd = 'TransDecoder-2.0/util/cufflinks_gtf_to_alignment_gff3.pl' \
        " %s > %s" % (gtf_filename, gff_filename )
        JarjarTools().check_out(cmd)        
        #Name for the protein file from the transdecoder
        protein_file_cat = 'protein_file_cat.fasta'
        print "Running..."
        print "Please wait..."        
        #Problems in the protein_file_Cat.fasta
        print scaffold_file
        cmd = 'TransDecoder-2.0/util/gff3_file_to_proteins.pl {0} {1} > {2}'\
        .format(gff_filename, scaffold_file, protein_file_cat)
        JarjarTools().check_out(cmd)
    
        return protein_file_cat

    
    def blastp(self):
        """This function needs a file with protein sequences and returns a 
        file with matches Let op Evalue 1E-5 en coverage!

        Input:
        Output:
        """
        protein_file_cat = JarjarTools().filelist("*.fasta","Please select a protein sequence fasta file")
        protein_file_arabidopsis = JarjarTools().filelist("*.fasta","Please select the arabidopsis transcriptome fasta file")
        init = protein_file_arabidopsis.index('.') 
        database = 'db_proteins_'+protein_file_arabidopsis[:init]
        #makeblastdb -in protein_file_arabidopsis.fasta -dbtype prot 
        #-out db_protein_file_genes.db
        cmd = 'makeblastdb -in %s -dbtype prot -out %s  '\
        % (protein_file_arabidopsis,database)
        JarjarTools().check_out(cmd)
        matches_file = 'matches.txt'
        #blastp -query protein_file_cat.fasta -db db_protein_file_genes.db 
        #-out matches.txt -outfmt 7 -evalue 1E-5
        cmd = 'blastp -query %s -db %s -out %s -outfmt 7 -evalue 1E-5' \
        % (protein_file_cat, database, matches_file)
        JarjarTools().check_out(cmd)
        print "Done."
        return matches_file 

class autoRun(JarjarTools):
    
    filenames = ["SRR127157_complete.fastq","SRR127158.fastq","SRR127159.fastq"]
    
    def splitFastQ(self):
    """Splits a fastq file that has concatenated reads into two files

    Arguments:
    filename -- str, name of the fastqfile (excluding extension)
    
    Output:
    N/A
    """
    path = "/local/data/BIF30806_2015_2/project/RNAseq/SRP041695/"
    
    for filename in filenames:
        openfile = open(path+filename)
        out_1 = open(os.path.splitext(filename)[0]+"_1.fastq","w")
        out_2 = open(os.path.splitext(filename)[0]+"_2.fastq","w")
        
        for line in openfile:
            line = line.strip()
            if line.startswith("@") or line.startswith("+"):
                out_1.write(line)
                out_1.write("\n")
                out_2.write(line)
                out_2.write("\n")
            elif line != "\n":
                length = len(line)
                split = length/2
                part1 = line[:int((length/2))]
                part2 = line[int((length/2)):]
                out_1.write(part1+"\n")
                out_2.write(part2+"\n")
    
        openfile.close()
        out_1.close()
        out_2.close()
    return

    def runtools(self):
        logfile(self,"SplitFastQ","Started")
        splitFastQ(self)
        logfile(self,"SplitFastQ","Completed")
        genome = "cro_scaffold.min_1000bp.fasta"
        logfile(self,"HiSat2-build","Started")
        subprocess.check_call("hisat2-build -p 4 %s genome_index" %genome)
        logfile(self,"HiSat2-build","Completed")
        logfile(self,"HiSat2-align","Started")
        for filename in filenames:
            file_1 = os.path.splitext(filename)[0]+"_1.fastq
            file_2 = os.path.splitext(filename)[0]+"_2.fastq
            cmd = "hisat2 --dta-cufflinks -p 4 "
            cmd += "-x genome_index -1 %s -2 %s -S %s.sam"%(file_1,file_2,os.path.splitext(filename)[0])
            subprocess.check_call(cmd,shell=True)
        logfile(self,"HiSat2-align","Completed")
        logfile(self,"Samtools","Started")
        for filename in filenames:
            filenm = os.path.splitext(filename)[0]
        command = "samtools view -bS %s.sam > %s.bam"%(filenm,filenm)
        JarjarTools().check_call(command)
        command = "samtools sort %s.bam %s.sorted"%(filenm,filenm)
        JarjarTools().check_call(command)
        command = "samtools index %s.sorted.bam"%filenm
        JarjarTools().check_call(command)
        logfile(self,"Samtools","Completed")
        logfile(self,"Cufflinks","Started")
        for filename in filenames:
            inputname = os.path.splitext(filename)[0]+".sorted.bam"
            folder = "Cufflinks_"+os.path.splitext(filename)[0]
            cmd = 'cufflinks -q -p 4 --no-update-check %s %s' %(folder, inputname)
            s= open("cuffmerge.txt", "a")
            s.write(folder+"/transcripts.gtf\n")
            s.close
        logfile(self,"Cufflinks","Completed")
        logfile(self,"Cuffmerge","Started")
        command = "cuffmerge -p 4 cuffmerge.txt"
        JarjarTools().check_call(command)
        if os.path.isfile("cuffmerge.txt"):
            subprocess.check_call("rm cuffmerge.txt",shell = True)
        logfile(self,"Cuffmerge","Completed")
        logfile(self,"Cuffdiff","Started")
        output = "Cuffdiff"
        file_seperated = ""
        gtf = "filtered_gtf.gtf"
        for filename in filenames:
            file_seperated+= " %s.sorted.bam"%os.path.splitext(filename)[0]
        cmd = "cuffdiff -o %s -p 4 %s%s"%(output,gtf,file_seperated)
        return
    
    def logfile(self,program,state):
        log = open("log.txt","a")
        log.write("["+time.strftime('%H:%M:%S')+"]\t")
        log.write(program+"\t"+state+"\n")
        log.close()
        return

    def checkfiles(self):
        return
    

if __name__ == '__main__':    
    JarjarTools().options()

