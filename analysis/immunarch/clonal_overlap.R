library(RColorBrewer)
col.pal <- RColorBrewer::brewer.pal(9, "YlOrRd")

# Number of clonal overalp between samples
imm_ov1 <- repOverlap(immdata$data, .method = "public", .verbose = F)
output_file <- paste(output_dir, sep="", "/heatmap_clonal_overlap.tsv")
write.table(imm_ov1, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the clonal overalp between samples plot
ov1 <- vis(imm_ov1, "heatmap2", .color = colorRampPalette(col.pal)(1024))

# Save the number of clonotypes plot
# output_png <- paste(output_dir, sep="", "/heatmap_clonal_overlap.png")
# png(filename=output_png)
# plot(ov1)
# dev.off()


# Morisita Horn index between each sample
imm_ov2 <- repOverlap(immdata$data, .method = "morisita", .verbose = F)
output_file <- paste(output_dir, sep="", "/heatmap_morisita_horn.tsv")
write.table(imm_ov1, file=output_file, quote=FALSE, sep='\t', col.names = NA)

#Create the Morisita horn overlap index heatmap
ov2 <- vis(imm_ov2, "heatmap2", .color = colorRampPalette(col.pal)(1024))

# Save the Morisita horn overlap index heatmap
# output_png <- paste(output_dir, sep="", "/heatmap_morisita_horn.png")
# png(filename=output_png)
# plot(ov2)
# dev.off()