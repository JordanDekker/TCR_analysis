##############################################################################
# R script that calls different TR analysis using immunarch 
##############################################################################

library(immunarch)

#Filepath to the count .tsv file.
args <- commandArgs(trailingOnly = TRUE)
output_dir <- args[2]
factor <- args[3]

immdata <- repLoad(args[1])
source("analysis/immunarch/basic_analysis.R")
source("analysis/immunarch/clonal_overlap.R")
source("analysis/immunarch/diversity.R")
source("analysis/immunarch/clonality.R")
source("analysis/immunarch/renyi_diversity.R")
source("analysis/immunarch/gene_usage.R")
