# Chao1 diversity
div_chao <- repDiversity(immdata$data, "chao1")
output_file <- paste(output_dir, sep="", "/chao1_diversity.tsv")
write.table(div_chao, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create Chao1 diversity per group
p1 <-vis(div_chao, .by = factor, .meta = immdata$meta)

# Save Chao1 diversity per group
output_png <- paste(output_dir, sep="", "/chao1_diversity.png")
png(filename=output_png)
plot(p1)
dev.off()


# D50 diversity
div_d50 <- repDiversity(immdata$data, "d50")
output_file <- paste(output_dir, sep="", "/d50_diversity.tsv")
write.table(div_chao, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create D50 diversity per group
p2 <-vis(div_d50, .by = factor, .meta = immdata$meta)

# Save D50 diversity per group
output_png <- paste(output_dir, sep="", "/d50_diversity.png")
png(filename=output_png)
plot(p2)
dev.off()


# D10 diversity
div_d10 <- repDiversity(immdata$data, "dxx", .perc = 10)
output_file <- paste(output_dir, sep="", "/d10_diversity.tsv")
write.table(div_chao, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create D50 diversity per group
p3 <-vis(div_d10, .by = factor, .meta = immdata$meta)

# Save D50 diversity per group
output_png <- paste(output_dir, sep="", "/d10_diversity.png")
png(filename=output_png)
plot(p3)
dev.off()

# Gini diversity
div_gini <- repDiversity(immdata$data, "gini")
output_file <- paste(output_dir, sep="", "/gini_diversity.tsv")
write.table(div_chao, file=output_file, quote=FALSE, sep='\t', col.names = NA)


# D10 diversity
div_d10 <- repDiversity(immdata$data, "dxx", .perc = 10)
output_file <- paste(output_dir, sep="", "/d10_diversity.tsv")
write.table(div_chao, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create D50 diversity per group
p3 <-vis(div_d10, .by = factor, .meta = immdata$meta)

# Save D50 diversity per group
output_png <- paste(output_dir, sep="", "/d10_diversity.png")
png(filename=output_png)
plot(p3)
dev.off()