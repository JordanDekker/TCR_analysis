import os, time
from optparse import OptionParser
import pathlib

from analysis.immunarch import call_immunarch
from analysis.vdjtools import call_vdjtools
from analysis import plot_renyi

def main():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    options, args = parse_arguments()
    file_type = check_filetypes(options.dir)

    input_directory = options.dir.split('/')
    directory_name = [i for i in input_directory if i][-1]

    if options.dir[-1] == '/':
        options.dir = options.dir[:-1]
    
    if file_type == 1:
        analysis_from_IMGT_files(directory_name, timestr, options)
    if file_type == 2:
        analysis_from_VDJtables(directory_name, timestr, options)



def analysis_from_VDJtables(directory_name, timestr, options):
    """
    Start point for the analysis if the input directory contains VDJ table files

    Args:
        directory_name: String: The name of the directory, this is used as the name for the analysis
        timestr: String: A string containing the time of start running the script
        options: optparse.Values: A dict-like object with the input values from the user
    """
    check_output_folder(directory_name, timestr)
    output_directory = "output/"+directory_name+'_'+timestr
    
    if options.TRB:
        TRB_data_dir, TRB_output_dir = create_specific_gene_files(output_directory, "TRB", options)
        call_immunarch.read_vdj_tables(TRB_data_dir, TRB_output_dir, options.factor)
        plot_renyi.plot_renyi_profile(TRB_output_dir, TRB_data_dir, options.factor)

    if options.TRG:
        TRG_data_dir, TRG_output_dir = create_specific_gene_files(output_directory, "TRG", options)
        call_immunarch.read_vdj_tables(TRG_data_dir, TRG_output_dir, options.factor)
        plot_renyi.plot_renyi_profile(TRG_output_dir, TRG_data_dir, options.factor)

    if not options.TRB and not options.TRG:
        call_immunarch.read_vdj_tables(options.dir, output_directory, options.factor)
        plot_renyi.plot_renyi_profile(output_directory, options.dir, options.factor)


def analysis_from_IMGT_files(directory_name, timestr, options):
    """
    Start point for the analysis if the input directory contains IMGT-3NT files

    Args:
        directory_name: String: The name of the directory, this is used as the name for the analysis
        timestr: String: A string containing the time of start running the script
        options: optparse.Values: A dict-like object with the input values from the user
    """
    check_output_folder(directory_name, timestr+"_VDJtables")
    check_folder(directory_name+'_'+"_VDJtables")

    output_data_dir = directory_name+'_'+"_VDJtables"
    output_analysis_dir = "output/"+directory_name+'_'+timestr+"_VDJtables"
    
    call_vdjtools.create_VDJ_tables(options.dir, output_data_dir)

    options.dir = directory_name+'_'+"_VDJtables"

    if options.TRB:
        TRB_data_dir, TRB_output_dir = create_specific_gene_files(output_analysis_dir, "TRB", options)
        call_immunarch.read_vdj_tables(TRB_data_dir, TRB_output_dir, options.factor)
        plot_renyi.plot_renyi_profile(TRB_output_dir, TRB_data_dir, options.factor)
    
    if options.TRG:
        TRG_data_dir, TRG_output_dir = create_specific_gene_files(output_analysis_dir, "TRG", options)
        call_immunarch.read_vdj_tables(TRG_data_dir, TRG_output_dir, options.factor)
        plot_renyi.plot_renyi_profile(TRG_output_dir, TRG_data_dir, options.factor)
    
    if not options.TRB and not options.TRG:
        call_immunarch.read_vdj_tables(options.dir, output_analysis_dir, options.factor)
        plot_renyi.plot_renyi_profile(output_analysis_dir, options.dir, options.factor)



def create_specific_gene_files(output_directory, gene, options):
    """
    Creates VDJ counts tables for only one specific gene (TRB or TRG)

    Args:
        ouput_directory: String: A string with the path to the location of the output directory
        gene: String: Filter either on TRB or on TRG
        options: optparse.Values: A dict-like object with the input values from the user
    
    Returns:
        String with the path to the location of the newly created VDJ tables with only one gene type (TRG/TRB)
    """
    os.makedirs(output_directory+'/'+gene+"_data")
    output_data_dir = output_directory+'/'+gene+"_data/"

    os.makedirs(output_directory+'/'+gene+"_output")
    output_analysis_dir = (output_directory+'/'+gene+"_output/")

    for file in os.listdir(options.dir):
        filename = os.fsdecode(file)
        with open(options.dir+'/'+filename, 'r') as f:
            first_line = f.readline()
            if first_line.startswith("count"):
                with open(output_data_dir+filename, 'w') as output_file:
                    output_file.write(first_line)
                    for line in f.read().strip().split('\n'):
                        values = line.split('\t')
                        if options.productive:
                            if '_' not in values[3] and '*' not in values[3] and "TRB" in values[4]:
                                output_file.write(line+'\n')
                        elif not options.productive:
                            if gene in values[4]:
                                output_file.write(line+'\n')
            elif first_line.startswith("Sample"):
                with open(output_data_dir+"metadata.tsv", 'w') as output_file:
                    output_file.write(first_line)
                    for line in f.read().strip().split('\n'):
                        output_file.write(line+'\n')
    
    return output_data_dir, output_analysis_dir


def parse_arguments():
    """
    Parses the input options with OptionParser

    Returns:
        An OptionParser object with the options
    """
    parser = OptionParser()
    parser.add_option("-d", "--dir", help="path to the input directory")
    parser.add_option("-f", "--factor", help="path to the input directory", default = "Type")    
    parser.add_option("--TRB", help="Only use TRB genes", default = False, action = "store_true")
    parser.add_option("--TRG", help="Only use TRG genes", default = False, action = "store_true")
    parser.add_option("--productive", help="Only use producte clonotypes", default = False, action = 'store_true')

    return parser.parse_args()
    

def check_filetypes(dir):
    """
    Checks if the input directory consists of only VDJ table files or IMGT-3NT-files

    Args:
        dir: String: A string with the path to the directory which contains the input files
    
    Returns:
        1 or 2: int: Returns 1 if directory consists of IMGT-3NT-files. Returns 2 if the directory consists of VDJ count tables
    """
    directory = os.fsencode(dir)

    IMGT_type = False
    VDJ_table_type = False

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open(dir+'/'+filename) as f:
            first_line = f.readline()
            if first_line.startswith("count"):
                VDJ_table_type = True
            elif first_line.startswith("Sequence number"):
                IMGT_type = True
    
    if IMGT_type and VDJ_table_type:
        print("Use a directory with only IMGT High-V-Quest files or only VDJ counts table files")
        exit()

    if IMGT_type == False and VDJ_table_type == False:
        print("No useful files found in the directory.")
        exit()
    
    if IMGT_type:
        return 1
    elif VDJ_table_type:
        return 2
    

def check_output_folder(directory_name, timestr):
    """
    Checks if the output folder exists, otherwise creates it
    """

    if not os.path.exists('output/'+directory_name+'_'+timestr):
        os.makedirs('output/'+directory_name+'_'+timestr)

def check_folder(directory_name):
    """
    Checks if the output folder exists, otherwise creates it
    """

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

if __name__ == "__main__":
    main()

