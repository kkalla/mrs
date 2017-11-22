rm(list=ls())

library(data.table) 

### bd(나이) 1번 방안
# 나이 이상한 사람들을 각 성별의 평균 나이로 한번에 넣어버린 것
# 나이가 제대로 안 된 데이터가 더 많다보니 평균나이를 일괄해서 넣어버리면 한 두 나이에만 데이터가 몰리게 됌

members <- fread('music/members.csv',header=T,encoding='UTF-8')
# 데이터 불러오는 건 각자 경로에 맞게끔


# 나이는 각 성별 median을 기준으로 함
members[which(members$bd<1&members$gender=='female'),'bd']=27
members[which(members$bd<1&members$gender=='male'),'bd']=27
members[which(members$bd<1&members$gender==''),'bd']=28

members[which(members$bd>100&members$gender=='female'),'bd']=27
members[which(members$bd>100&members$gender=='male'),'bd']=27
# 성별데이터가 없는 100살 넘는 사람은 없었음

# 나이 구간화

# 1~16 child
# 17~26 young
# 27~36 adult
# 37~62 mid-age
# 63~ senior

members[members$bd<17,'bd']=1 # child
members[members$bd>=17&members$bd<27,'bd']=2 # young
members[members$bd>=27&members$bd<37,'bd']=3 # adult
members[members$bd>=37&members$bd<63,'bd']=4 # mid-age
members[members$bd>=63,'bd']=5 # senior
table(members$bd)


#### 2번 방안
# 나이가 있는 사람들의 각각 나이가 전체에서 얼마나 차지하는지 비율을 보고 랜덤해서 분배
# ex) 현재 데이터에서 22세인 사람이 전체의 5%면 나이 이상한 사람들의 데이터의 5%를 22세로

members <- fread('music/members.csv',header=T,encoding='UTF-8')

members_0<-members[members$bd>0&members$bd<100,] # 나이 0 초과 100미만

aa <- members_0 %>% 
  group_by_('bd') %>% 
  count() %>% 
  arrange(desc(n))

b=data.frame(bd=aa$bd,count=aa$n)

c=c()

for (i in 1:79){
  c=c(c,b[i,2]/sum(b$count))
}

b=cbind(b,ratio=c)

members_00<-members[members$bd<1|members$bd>99,] # 나이 0 이거나 100이상

ind<-sample(b$bd,19956,prob=b$ratio,replace=T) # 각각의 나이들이 전체에서 차지하는 비율만큼


for(i in 1:79){
  members_00[which(ind==b$bd[i]),'bd']<-b$bd[i]
}

members2<-rbind(members_0,members_00)
table(members2$bd)

# 나이 구간화

members2[members2$bd<17,'bd']=1 # child
members2[members2$bd>=17&members2$bd<27,'bd']=2 # young
members2[members2$bd>=27&members2$bd<37,'bd']=3 # adult
members2[members2$bd>=37&members2$bd<63,'bd']=4 # mid-age
members2[members2$bd>=63,'bd']=5 # senior
table(members2$bd)



### registerd_via

library(data.table)

members <- fread('music/members.csv',header=T,encoding='UTF-8')

table(members$registered_via)
# 가입경로 자체가 6개만 존재하는데 16이라는 factor는 전체 member중 1명밖에 없었음
# merge시켜서 확인했을 때는 아예 그 member가 있지도 않아서 가장 많은 member를 보유한 4에 넣어도 될 것 가다 판단함
# 상황에 따라서는 13의 경우에도 바꿀 수는 있다고 생각하는데 얘기를 좀 해보고 결정해야 할듯
members[which(members$registered_via==16),'registered_via'] <- 4
