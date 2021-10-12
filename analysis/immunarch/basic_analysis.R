
# Number of clonotypes per group
exp_vol <- repExplore(immdata$data, .method = "volume")
output_file <- paste(output_dir, sep="", "/number_clonotypes.tsv")
print("1")
write.table(exp_vol, file=output_file, quote=FALSE, sep='\t', col.names = NA)
print("2")
#Create the number of clonotypes plot
p1 <- vis(exp_vol, .by = factor, .meta = immdata$meta)

# Save the number of clonotypes plot
output_png <- paste(output_dir, sep="", "/number_clonotypes.png")
png(filename=output_png)
plot(p1)
dev.off()


# Number of clonotypes per group
exp_cnt <- repExplore(immdata$data, .method = "count")
output_file <- paste(output_dir, sep="", "/clonotype_abundance.tsv")
write.table(exp_cnt, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the number of clonotypes plot
p2 <- vis(exp_cnt, .by = factor, .meta = immdata$meta)

# Save the number of clonotypes plot
output_png <- paste(output_dir, sep="", "/clonotype_abundance.png")
png(filename=output_png)
plot(p2)
dev.off()


# Number of clonotypes per sample
exp_vol <- repExplore(immdata$data, .method = "volume")
output_file <- paste(output_dir, sep="", "/clonotypes_per_sample.tsv")
write.table(exp_vol, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the number of clonotypes per sample plot
p3 <- vis(exp_vol)

# Save the number of clonotypes per sample plot
output_png <- paste(output_dir, sep="", "/clonotypes_per_sample.png")
png(filename=output_png)
plot(p3)
dev.off()


# CDR3 distribution 
exp_len <- repExplore(immdata$data, .method = "len", .col = "aa")
sample_counts <- vector(mode = "list", length = length(exp_vol$Sample))
names(sample_counts) <- exp_vol$Sample
for (i in 1:length(exp_vol$Sample)){
  sample_counts[[i]] <- exp_vol$Volume[[i]]
}
for(i in 1:nrow(exp_len)) {
  sample <- exp_len$Sample[[i]]
  sample_size <- sample_counts[[sample]]
  exp_len$Count[[i]] <- exp_len$Count[[i]] / sample_size * 100
}
output_file <- paste(output_dir, sep="", "/cdr3_distribution.tsv")
write.table(exp_len, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the CDR3 dsitribtuion plot
p4 <- vis(exp_len[exp_len$Length <= 20, ], .by = factor, .meta = immdata$meta)

# Save the CDR3 dsitribtuion plot
output_png <- paste(output_dir, sep="", "/cdr3_distribution.png")
png(filename=output_png)
plot(p4)
dev.off()