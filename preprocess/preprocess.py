import os
from optparse import OptionParser

def process():
    options, args = parse_arguments()
    samples = get_filenames(options.dir)

    for sample in samples:
        print("===== %s =====" %(sample))
        check_output_folder(sample)
        pe_joining(sample, options.dir)
        adapter_trimming(sample)
        fastq_to_fasta(sample)
        remove_junk_files(sample)


def parse_arguments():
    """
    Parses the input options with OptionParser

    Returns:
        An OptionParser object with the options
    """
    parser = OptionParser()
    parser.add_option("-d", "--dir", help="full path to the .FastQ-files")
    
    return parser.parse_args()


def get_filenames(dir):
    """
    Loops through a directory and retrieves all filenames from it.

    Args:
        dir: A String with the full path to the directory off the FastQ-files.
    Returns:
        samples: A Set of sample name Strings.
    """
    directory = os.fsencode(dir)
    samples = set()

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        test = filename.split('_R')
        samples.add(test[0])
    
    return samples


def pe_joining(filename, dir):
    """
    Paired-end joins the forward (R1) and reverse (R2) reads using FLASH2.

    Args:
        filename: A string of the name of the sample
        dir: A string of the full path to the directory
    """
    r1_path = dir+'/'+filename+"_R1.fastq"
    r2_path = dir+'/'+filename+"_R2.fastq"
    commandline = "~/Documents/radboud/TCR_repertoire_analysis/preprocess/flash -m 10 -M 1000 -x 0.2 -o %s -O %s %s" % ("preprocess/output/"+filename+'/'+filename, r1_path, r2_path)

    print("===== Paired-end joining =====")
    fasta_pipe = os.popen(commandline)
    fasta_res = fasta_pipe.read()

    direc_string = ' '+"preprocess/output/"+filename+'/'
    os.system("rm "+ direc_string.join([direc_string+filename+".hist", filename+".hist.innie", filename+".hist.outie", filename+".histogram.innie", filename+".histogram.outie", filename+".histogram"]))

    pe_joining_loosly(filename)

    os.system("cat "+"preprocess/output/"+filename+'/'+filename+".extendedFrags.fastq "+"preprocess/output/"+filename+'/'+filename+"_loosly.extendedFrags.fastq > "+"preprocess/output/"+filename+'/'+filename+"_joined.fastq")


def pe_joining_loosly(filename):
    """
    Loosly (less stringent) paired-end joins the forward (R1) and reverse (R2) reads using FLASH2.

    Args:
        filename: A string of the name of the sample
        dir: A string of the full path to the directory
    """
    r1_name = filename+".notCombined_1.fastq"
    r2_name = filename+".notCombined_2.fastq"
    filename_loosly = filename+"_loosly"
    commandline = "~/Documents/radboud/FLASH/FLASH-1.2.11-Linux-x86_64/./flash -m 10 -M 1000 -x 0.4 -o %s -O %s %s" % ("preprocess/output/"+filename+'/'+filename_loosly, "preprocess/output/"+filename+'/'+r1_name, "preprocess/output/"+filename+'/'+r2_name)
    
    print("===== Paired-end joining (loosly) =====")
    fasta_pipe = os.popen(commandline)
    fasta_res = fasta_pipe.read()

    direc_string = ' '+"preprocess/output/"+filename+'/'
    os.system("rm "+ direc_string.join([direc_string+filename_loosly+".hist", filename_loosly+".hist.innie", filename_loosly+".hist.outie", filename_loosly+".histogram.innie", filename_loosly+".histogram.outie", filename_loosly+".histogram"]))


def adapter_trimming(filename):
    """
    Trimmes the adapter and primer sequences of from the DNA reads.

    Args:
        filename: A string of the name of the sample
    """
    commandline = "cutadapt -g file:preprocess/primers/primer_set5.fasta -a file:preprocess/primers/primer_set3.fasta -o %s %s" % ("preprocess/output/"+filename+'/'+filename+".fastq", "preprocess/output/"+filename+'/'+filename+"_joined.fastq")

    print("===== Trimming Primers/Adapters =====")
    fasta_pipe = os.popen(commandline)
    fasta_res = fasta_pipe.read()


def fastq_to_fasta(filename):
    """
    Converts file from Fastq to Fasta format.

    Args:
        filename: A string of the name of the sample
    """
    os.system("sed -n '1~4s/^@/>/p;2~4p' %s > %s " % ("preprocess/output/"+filename+'/'+filename+".fastq", "preprocess/output/"+filename+'/'+filename+'.fasta'))


def remove_junk_files(filename):
    """
    Removes junk (not needed) files.

    Args:
        filename: A string of the name of the sample
    """
    direc_string = ' '+"preprocess/output/"+filename+'/'
    os.system("rm "+ direc_string.join([direc_string+filename+".notCombined_1.fastq", filename+".notCombined_2.fastq", filename+".extendedFrags.fastq", filename+"_loosly.extendedFrags.fastq", filename+"_joined.fastq"]))


def check_output_folder(filename):
    """
    Checks if the output folder exists, otherwise creates it

    Args:
        filename: A string of the name of the sample
    """
    if not os.path.exists("preprocess/output/"+filename):
        os.makedirs("preprocess/output/"+filename)


if __name__ == '__main__':
    process()