library(data.table)
library(dplyr)

data = fread("data/train_merged.csv")
finaldata = fread("data/test_merged.csv")

variable = function(dataset,x){
    
    x = x
    
    #train
    trainvar1 = dataset[ , x, with = F]
    trainvar1[is.na(trainvar1),] = "na"   
    trainvar1[trainvar1=="",] = "na"
    trainvar2 = sapply(trainvar1, function(x) strsplit(x, split = "\\|"))
    trainvar3 = unlist(trainvar2)
    ntrvar = sapply(trainvar2, function(x) length(x))
    trindex = rep(1:nrow(trainvar1), ntrvar)
    trtarget = rep(dataset$target, ntrvar)
    trainvar4 = data.table(trindex, variable = trainvar3, trtarget)
    varmean = trainvar4[, mean(trtarget), by = "variable"]
    trainvar5 = merge(trainvar4, varmean, by = "variable", all.x = T)       #all.x  ?��?Ȯ??
    trainvar5[is.na(V1), V1 := 0.5]                                         #all.x  ?��?Ȯ??
    trainvar = trainvar5[, mean(V1), by = "trindex"] %>% arrange(trindex)
    trvar = trainvar$V1
    
    variable = trvar
}

genre_ids = variable(data,"genre_ids")
data$genre_ids = genre_ids
str(data)

write.csv(data,'data/input.csv',row.names = FALSE)