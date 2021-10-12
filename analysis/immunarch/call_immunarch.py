import os

def read_vdj_tables(mapLoc, output_dir, factor):
    print(mapLoc)
    print(output_dir)
    os.system("Rscript analysis/immunarch/start_immunarch.R " + mapLoc +" "+output_dir + " " + factor)