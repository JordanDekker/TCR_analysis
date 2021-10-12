# Number of clonotypes per group
imm_gu <- geneUsage(immdata$data, "HomoSapiens.TRBV", "count", .norm = T)
output_file <- paste(output_dir, sep="", "/gene_usage.tsv")
write.table(exp_vol, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the number of clonotypes plot
p1 <- vis(imm_gu, .by = factor, .meta = immdata$meta)

# Save the number of clonotypes plot
output_png <- paste(output_dir, sep="", "/gene_usage.png")
png(filename=output_png)
plot(p1)
dev.off()