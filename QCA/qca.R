library(TeachingDemos)
#txtStart("results.txt", append=T)


#sink("results.txt", append=T, split=T, type = c("output", "message"))

ineg=read.csv(file='QCA_10y_3c.csv', row.names='index')
library(QCA)
tt<-truthTable(ineg, outcome="g", conditions=c("gini","gdp", 'nat_re'), incl.cut1=.6, sort.by='n', show.cases=T, n.cut=3)
tt
#eqmcc(tt,details=T, show.cases=T)


#txtStop()
