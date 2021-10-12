# Clonal homeostasis
imm_hom <- repClonality(immdata$data,
                        .method = "homeo",
                        .clone.types = c(Small = .0001, Medium = .001, Large = .01, Hyperexpanded = 1))
output_file <- paste(output_dir, sep="", "/clonality_homeostasis.tsv")
write.table(imm_hom, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the clonal homeostasis plot
p1 <- vis(imm_hom)

# Save the clonal homeostasis plot
output_png <- paste(output_dir, sep="", "/clonality_homeostasis.png")
png(filename=output_png)
plot(p1)
dev.off()


# Least prolific clonotypes
imm_rare <- repClonality(immdata$data, .method = "rare")
output_file <- paste(output_dir, sep="", "/rare_clonality.tsv")
write.table(imm_rare, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the least prolific clonotypes plot
p2 <- vis(imm_rare)

# Save the least prolific clonotypes plot
output_png <- paste(output_dir, sep="", "/rare_clonality.png")
png(filename=output_png)
plot(p2)
dev.off()


# Top N clonotypes
imm_top <- repClonality(immdata$data, .method = "top", 
                        .head = c(10, 100, 1000, 3000, 10000, 40000))
output_file <- paste(output_dir, sep="", "/top_n_clonality.tsv")
write.table(imm_top, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the top N clonotypes
p3 <- vis(imm_top)

# Save the top N clonotypes
output_png <- paste(output_dir, sep="", "/top_n_clonality.png")
png(filename=output_png)
plot(p3)
dev.off()