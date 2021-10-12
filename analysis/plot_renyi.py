import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import statistics
import numpy as np
import pandas as pd

LOC = os.getcwd() +'/'
print(LOC)

def plot_renyi_profile(output_directory, input_directory, factor):
    """
    Makes a renyi diversity profile using the table created by the R-script renyi_diversity.R

    Args:
        output_directory: String: A string with the path to the location of the output folder
        input_directory: String: A string with the path to the location of the input files.
        factor: String: A string containg the factor to use for the comparisons
    """
    x = [0,1,2,3,4,5,6,7,8,9,10]
    fig, ax = plt.subplots()

    factors, factor_dict = get_filenames_from_metafile(input_directory, factor)
    colors = cm.rainbow(np.linspace(0, 1,len(factors)))
    values_per_factor = [[] for x in range(len(factors))]

    with open(LOC+output_directory+"/renyi_diversity.tsv") as renyi_df:
        renyi_df.readline()
        for line in renyi_df.read().strip().split('\n'):
            y = []
            values = line.split('\t')
            sample_id = values[0]
            for n in values[1:]:
                y.append(float(n))
            factor = factor_dict[sample_id]
            factor_n = factors.index(factor)
            values_per_factor[factor_n].append(y)
            
            ax.plot(x, y, color = colors[factor_n], alpha = 0.4)
    
    for f, n in zip(values_per_factor, range(0,len(values_per_factor))):
        y_median = []
        for i in range(0,11):
            y_median.append(statistics.median(list(list(zip(*f))[i])))
        ax.plot(x, y_median, color = colors[n], alpha = 1, linewidth = 2.5, marker='o', markersize = 4)

    fig.savefig(output_directory+"/renyi_profile.png")
    plt.close()
    

def get_filenames_from_metafile(input_directory, factor):
    """
    Gets the filenames from the metadata files and stores each sample_id to a factor

    Args:
        input_directory: String: A string containing the path to the location of the input files
        factor: String A string containing the factor to use for the comparisons
    
    Returns:
        list(factors): A list with all the unique factors that occur in the metadata file
        factor_dict: dict: A dictionary which holds the sample ids that belong to each factor
    """
    df = pd.read_csv(input_directory+'/metadata.tsv', sep='\t')
    print(df)
    factor_dict = dict(zip(df.Sample, df[factor]))
    factors = set(factor_dict.values())
    
    return list(factors), factor_dict
