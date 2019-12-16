install.packages("NbClust")

cat("---- started ----\n") # all cat gets printed to the web ui
library(NbClust)
#library(parallel)
warnings()
cores <- detectCores()
cat("Nodes available: ", cores,"\n")
cat("spawning cluster...\n")
#cl4_1 <- makeCluster(cores, outfile="") # number of nodes to use in pool
args = commandArga(trailingOnly=TRUE)
if(length(args)==0) {
  stop("Input file must be supplied")
}

path = './'
#path = 'C:\\Users\\Nicholas\\Downloads\\' # <-- this is only for testing purposes
# ****** FILE INPUT ******
cat("reading file...\n")
file = args[1]

# ************************
dir.create(paste(path, "partitions/", file, '/', sep=""))
#clear anything that's already there
system(paste("rm ", path, "partitions/", file, "/*", sep=""))

mtb <- t(read.table(paste(path, file, '', sep=""), header=TRUE, row.names=1, sep="\t"))       # this reads the input file referenced above
#print(mtb)

methods <- c("kmeans","ward.D")
distances <- c("euclidean", "maximum", "manhattan", "canberra", "binary", "minkowski")
indexes <- c("kl", "ch", "hartigan", "ccc", "scott", "marriot", "trcovw", "tracew", "friedman", "rubin", "cindex", "db", "silhouette", "duda", "pseudot2", "beale", "ratkowsky", "ball", "ptbiserial", "gap", "frey", "mcclain", "gamma", "gplus", "tau", "dunn", "sdindex", "sdbw")
#distances <- c("euclidean") # used only when testing ,"manhattan"
#indexes <- c("kl","cindex")             # ^

cat("analyzing...\n")

for (m in methods) {
  cat(paste(m,"\n"))
  for (d in distances) {
    cat(" ",d,"\n","\t")
    if (m == 'ward.D' && d == 'binary' || m == 'ward.D' && d == 'canberra') {
      next ## this combo kills the cluster for whatever reason
    }
    #clusterExport(cl4_1, c("m", "d", "mtb", "path", "file"), envir = environment())
    #comp <- clusterApply(cl4_1, indexes, function(i) {
    for (i in indexes) {
      cat(i)
      warnings()
      tryCatch({
        cat(".\n\t")
        library(NbClust)  # not for testing
        res <- NbClust(data=mtb, diss=NULL, method=m, distance=d, index=i, min.nc=2, max.nc=12 )
        #cat(res$Best.partition)
        
        zf = paste(path, 'partitions/', file, '/', paste(m,d,i, sep='_'), '.tsv', sep="")
        zzf = file(zf, open = 'w+')
        write.table(res$Best.partition, zzf)
        close(zzf)
        #return()
      },
      warning = function(e) { cat(toString(paste("WARN: ",m,d,i))); },
      error = function(e) { cat(toString(paste("ERR: ",m,d,i))); })
    }
    cat("*>\n")
  }
}

cat("killing the cluster... \n")
stopCluster(cl4_1)