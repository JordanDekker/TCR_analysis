import os

LOC = os.getcwd() + '/'
VDJTOOLS_CALL = "java -Xmx16G -jar "
VDJTOOLS_EXECUTABLE = VDJTOOLS_CALL + LOC+"/analysis/vdjtools/vdjtools-1.2.1.jar "


def create_VDJ_tables(dir, dir_out):
    """
    Creates VDJ counts tables from IMGT-3NT-files using VDJtools

    Args:
        dir: String: A string with the path to the location of the input directory with the IMGT-3NT files
        dir_out: String: A string with the path to the location of the output directory
    """
    for file in os.listdir(dir):
        filename = os.fsdecode(file)
        if filename.startswith("metadata"):
            os.system(VDJTOOLS_EXECUTABLE+"Convert -S imgthighvquest -m "+dir+'/'+filename+" vdjtools_tmp")
            with open(dir+'/'+filename, 'r') as meta_file:
                with open ("vdjtools_tmp.metadata.tsv", 'w') as new_metafile:
                    for line in meta_file.read().strip().split('\n'):
                        line = line.replace("sample.id", "Sample")
                        values = line.split('\t')
                        new_metafile.write('\t'.join(values[1:])+'\n')
    
    move_vdj_files(dir_out)

def move_vdj_files(dir_out):
    """
    Moves the created VDJ counts table to die ouput directory and removes not needed files created by VDJtools

    Args:
        dir_out: String: A string with the path to the location of the output directory
    """
    check_output_folder(LOC+dir_out)
    for file in os.listdir(LOC):
        filename = os.fsdecode(file)
        if filename.startswith("vdjtools_tmp"):
            new_filename = filename.replace("vdjtools_tmp.", '')
            os.system("mv "+LOC+filename+ " "+LOC+dir_out+'/'+new_filename)
        elif filename == "_vdjtools_error.log":
            os.system("rm "+filename)
        elif filename == "metadata.txt":
            os.system("rm "+filename)


def check_output_folder(directory_name):
    """
    Checks if the output folder exists, otherwise creates it
    """

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

#calculate_overlap_values("/home/your/Documents/radboud/TCR_repertoire_analysis/example_vdj_tables/")