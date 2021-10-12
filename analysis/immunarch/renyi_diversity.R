library(vegan)

v = c()

i <- 1
for (i in 1:length(immdata$data)){
  name <- names(immdata$data[i])
  v <- c(v, as.numeric(sum(immdata$data[[name]]$Clones)))
}
min_value <- min(v)


renyi_df_full <- data.frame(matrix(ncol = 11, nrow = 0))
names_vector = c()

for (i in 1:length(immdata$data)){
  name <- names(immdata$data[i])
}

for (d in 1:length(immdata$data)){
  df <- data.frame(matrix(ncol = 11, nrow = 0))
  name <- names(immdata$data[d])
  names_vector[d] <- name
  for (i in 1:100) { # bootstrap it 100 times
    rarefied <- rrarefy(immdata$data[[name]]$Clones, min_value) # downsample all samples to the sample with the smallest size 
    rarefied_renyi <- renyi(rarefied, scales = c(0,0.25,0.5,1,2,4,8,16,32,64,Inf), hill = TRUE)
    renyi_values <- unname(rarefied_renyi)
    df <- rbind(df, renyi_values)
  }
  means_df <- colMeans(df) # take average of the 100 bootstraps
  renyi_df_full <- rbind(renyi_df_full, means_df)
}
rownames(renyi_df_full) <- names_vector
x <- c("0", "0.25", "0.5", "1", "2", "4", "8", "16", "32", "64", "Inf")
colnames(renyi_df_full) <- x

# Save Renyi diversity table
output_file <- paste(output_dir, sep="", "/renyi_diversity.tsv")
write.table(renyi_df_full, file=output_file, quote=FALSE, sep='\t', col.names = NA)