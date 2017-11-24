library(data.table)
library(dplyr)
library(ranger)
library(gbm)
library(caret)
library(xgboost)

#train = fread("music/train.csv",header = T, sep = ",", encoding = "UTF-8")
#test = fread("music/test.csv",header = T, sep = ",", encoding = "UTF-8")
#songs = fread("music/songs.csv",header = T, sep = ",", encoding = "UTF-8")
#members = fread("music/members.csv",header = T, sep = ",", encoding = "UTF-8")
#song_extra_info = fread("music/song_extra_info.csv",header = T, sep = ",", encoding = "UTF-8")

#song = merge(song_extra_info, songs, by="song_id")
#data1 = merge(train, song, by="song_id", all.x = T)
#data = merge(data1, members, by="msno", all.x = T)
#finaldata1 = merge(test, song, by="song_id", all.x = T)
#finaldata = merge(finaldata1, members, by="msno", all.x = T)
#write.csv(data, file = "data.csv")
#write.csv(finaldata, file = "finaldata.csv")
###########################

data = fread("data/train_merged.csv")
finaldata = fread("data/test_merged.csv")


##### train, test
set.seed(1000)
ind = sample(nrow(data), nrow(data)*0.7)
traindata = data[ind,]
testdata = data[-ind,]
#traindata = traindata[1:(nrow(traindata)*0.05),]
#testdata = testdata[1:(nrow(testdata)*0.05),]

### ?Լ? ??��
variable = function(x){
  
  x = x

  #train
  trainvar1 = traindata[ , x, with = F]
  trainvar1[is.na(trainvar1),] = "na"   
  trainvar1[trainvar1=="",] = "na"
  trainvar2 = sapply(trainvar1, function(x) strsplit(x, split = "\\|"))
  trainvar3 = unlist(trainvar2)
  ntrvar = sapply(trainvar2, function(x) length(x))
  trindex = rep(1:nrow(trainvar1), ntrvar)
  trtarget = rep(traindata$target, ntrvar)
  trainvar4 = data.table(trindex, variable = trainvar3, trtarget)
  varmean = trainvar4[, mean(trtarget), by = "variable"]
  trainvar5 = merge(trainvar4, varmean, by = "variable", all.x = T)       #all.x  ?��?Ȯ??
  trainvar5[is.na(V1), V1 := 0.5]                                         #all.x  ?��?Ȯ??
  trainvar = trainvar5[, mean(V1), by = "trindex"] %>% arrange(trindex)
  trvar = trainvar$V1
  
  #test
  testvar1 = testdata[ , x, with = F]
  testvar1[is.na(testvar1),] = 0
  testvar1[testvar1=="",] = 0
  testvar2 = sapply(testvar1, function(x) strsplit(x, split = "\\|"))
  testvar3 = unlist(testvar2)
  ntevar = sapply(testvar2, function(x) length(x))
  teindex = rep(1:nrow(testvar1), ntevar)
  testvar4 = data.table(teindex, variable = testvar3)
  testvar5 = merge(testvar4, varmean, by = "variable", all.x = T)
  testvar5[is.na(V1), V1 := 0.5]
  testvar = testvar5[, mean(V1), by = "teindex"] %>% arrange(teindex)
  tevar = testvar$V1
  
  # finaltest
  ftestvar1 = finaldata[ , x, with = F]
  ftestvar1[is.na(ftestvar1),] = 0
  ftestvar1[ftestvar1=="",] = 0
  ftestvar2 = sapply(ftestvar1, function(x) strsplit(x, split = "\\|"))
  ftestvar3 = unlist(ftestvar2)
  fntevar = sapply(ftestvar2, function(x) length(x))
  fteindex = rep(1:nrow(ftestvar1), fntevar)
  ftestvar4 = data.table(fteindex, variable = ftestvar3)
  ftestvar5 = merge(ftestvar4, varmean, by = "variable", all.x = T)
  ftestvar5[is.na(V1), V1 := 0.5]
  ftestvar = ftestvar5[, mean(V1), by = "fteindex"] %>% arrange(fteindex)
  ftevar = ftestvar$V1
  
  variable = list(trvar, tevar, ftevar)
}

### ???? ??ȯ
msno = variable("msno")
song_id = variable("song_id")
source_system_tab = variable("source_system_tab")
source_screen_name = variable("source_screen_name")
source_type = variable("source_type")
song_length = variable("song_length")
genre_ids = variable("genre_ids")
artist_name = variable("artist_name")
composer = variable("composer")
lyricist = variable("lyricist")
language = variable("language")
city = variable("city")
bd = variable("bd")
gender = variable("gender")
registered_via = variable("registered_via")
registration_init_time = variable("registration_init_time")
expiration_date = variable("expiration_date")


### ?ܼ????? ?˰���??
ydata = data.table(msno[[2]], song_id[[2]], source_system_tab[[2]], source_screen_name[[2]], source_type[[2]], genre_ids[[2]], artist_name[[2]], composer[[2]], lyricist[[2]], gender[[2]])
pred = apply(ydata, 1, mean)
pred0 = ifelse(pred>=0.5, 1, 0)
confusionMatrix(pred0, testdata$target)


### train, test
train = data.table(traindata$target, msno[[1]], song_id[[1]], source_system_tab[[1]], source_screen_name[[1]], source_type[[1]], genre_ids[[1]], artist_name[[1]], composer[[1]], lyricist[[1]], gender[[1]])
test = data.table(testdata$target, msno[[2]], song_id[[2]], source_system_tab[[2]], source_screen_name[[2]], source_type[[2]], genre_ids[[2]], artist_name[[2]], composer[[2]], lyricist[[2]], gender[[2]])
ftest = data.table(msno[[3]], song_id[[3]], source_system_tab[[3]], source_screen_name[[3]], source_type[[3]], genre_ids[[3]], artist_name[[3]], composer[[3]], lyricist[[3]], gender[[3]])
#train = data.table(traindata$target, msno[[1]], song_id[[1]], source_system_tab[[1]], source_screen_name[[1]], source_type[[1]], traindata$song_length, genre_ids[[1]], artist_name[[1]], composer[[1]], lyricist[[1]], traindata$language, traindata$city, traindata$bd, gender[[1]], traindata$registered_via, traindata$registration_init_time, traindata$expiration_date)
#test = data.table(testdata$target, msno[[2]], song_id[[2]], source_system_tab[[2]], source_screen_name[[2]], source_type[[2]], testdata$song_length, genre_ids[[2]], artist_name[[2]], composer[[2]], lyricist[[2]], testdata$language, testdata$city, testdata$bd, gender[[2]], testdata$registered_via, testdata$registration_init_time, testdata$expiration_date)

##################################


###??????????Ʈ

model1 = ranger(V1~., data = train)
pred1 = predict(model1, data = test[, -1])
confusionMatrix(pred1$prediction, testdata$target)


### XGBOOST
param = list(
  objective="binary:logistic",
  eval_metric= "error",
  subsample= 0.95,
  max_depth= 10,
  min_child= 6,
  tree_method= "auto", 
  eta  = 0.3 , 
  nthreads = 3
)

dtrain = xgb.DMatrix(as.matrix(train[, -1]), label = train$V1)
dtest = xgb.DMatrix(as.matrix(test[, -1]), label = test$V1)
dftest = xgb.DMatrix(as.matrix(ftest))

model2 = xgb.train(data = dtrain, nrounds = 100, params = param, maximize= T, watchlist = list(val = dtest))

pred = predict(model2, dtest)
pred2 = ifelse(pred>=0.5, 1, 0)
confusionMatrix(pred2, testdata$target)





### ??�� ��?⺻
pred = data.table("id" = finaldata$id, "target" = pred2) %>% arrange(id)
write.csv(pred, file = "music/pred.csv", row.names = F)
