

cat("---- started ----\n") # all cat gets printed to the web ui
library(NbClust)
warnings()
args = commandArgs(trailingOnly=TRUE)
if(length(args) < 4) {
  stop("Usage: <method> <distance> <index> <filename> [--] <output_dir>")
}

#path = 'C:\\Users\\Nicholas\\Downloads\\' # <-- this is only for testing purposes
# ****** FILE INPUT ******
cat("reading file...\n")
file = args[4]
m = args[1]
d = args[2]
i = args[3]
path = paste(args[5], "/", sep="")
if (length(args) == 6) {
  path = paste(args[6], "/", sep="")
}

# ************************

mtb <- t(read.table(file, header=TRUE, row.names=1, sep="\t"))       # this reads the input file referenced above
#print(mtb)

cat("analyzing...\n")

  cat(paste(m,"\n"))
    cat(">",d,"\n")

      cat('>>', i, '\n')
      warnings()
      tryCatch({
        res <- NbClust(data=mtb, diss=NULL, method=m, distance=d, index=i, min.nc=2, max.nc=12 )
        
        zf = paste(path, paste(m,d,i, sep='_'), '.tsv', sep="")
        zzf = file(zf, open = 'w+')
        write.table(res$Best.partition, zzf)
        close(zzf)
      },
      warning = function(e) { cat(toString(paste("WARN: ",m,d,i,format(e),'', sep="\n"))); },
      error = function(e) { cat(toString(paste("ERR: ",m,d,i,format(e),'', sep="\n"))); })
    
    cat("*>\n")
  
