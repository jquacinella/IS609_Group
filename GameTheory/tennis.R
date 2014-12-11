#IS609 Project
#Tennis Game Theory

#load data, set factor variables
tennis <- read.csv("tennisdata.csv")

tennis$Set <- as.factor(as.character(tennis$Set))
tennis$Game <- as.factor(as.character(tennis$Game))
tennis$ServerGameNum <- as.factor(as.character(tennis$ServerGameNum))
tennis$PointNum <- as.factor(as.character(tennis$PointNum))
tennis$ServeNum <- as.factor(as.character(tennis$ServeNum))

tennis[is.na(tennis)] <- 0 #change NAs to 0
tennis$ServeDir <- as.factor(ifelse(tennis$Left_FH==1, "L", "R")) #combine serve direction to one factor var
str(tennis)

#Function to compare win% on each service side - Chi-square test of equal proportions
pointGame <- function(tennis_data, server, court, serve_num=tennis_data$ServeNum, set=tennis_data$Set) {
  
  df <- subset(tennis_data, Server==server & Court==court & ServeNum==serve_num & Set==set)

  serve_left <- sum(df$Left_FH)
  serve_right <- sum(df$Right_BH)
  point_left <- sum(df[df$ServeDir=="L",]$PointWon)
  point_right <- sum(df[df$ServeDir=="R",]$PointWon)
  
  chi_sq <- prop.test(c(point_left, point_right), c(serve_left, serve_right))  
  chisq_val <- round(chi_sq$statistic, 3)
  p_val <- round(chi_sq$p.value, 3)
  
  df2 <- data.frame(server=server, court=court, set=paste(unique(set),collapse=""), serve_num=paste(unique(serve_num),collapse=""), serve_left=serve_left, 
                    serve_right=serve_right, point_left=point_left, point_right=point_right, 
                    perc_winLeft=round((point_left/serve_left)*100, 1), perc_winRight=round((point_right/serve_right)*100, 1), 
                    chisq_val=chisq_val, p_val=p_val)
  
  rownames(df2) <- NULL  
  return(df2)
}

#Exclude faults, lets and center serves
tennisIn <- subset(tennis, Fault==0 & Note!="L" & Note!= "Let" & Note!="C")

#Calculate results based on chosen parameters: function (dataset, server, court, serveNum)

#--- CHOOSE SERVE, ALL SETS --- 
#1st serve, all sets
ps1d <- pointGame(tennisIn, "PS", "D", 1, )
ps1a <- pointGame(tennisIn, "PS", "A", 1, )
aa1d <- pointGame(tennisIn, "AA", "D", 1, )
aa1a <- pointGame(tennisIn, "AA", "A", 1, )
result_1serve <- rbind(ps1d, ps1a, aa1d, aa1a)
print(result_1serve)

#2nd serve, all sets
ps2d <- pointGame(tennisIn, "PS", "D", 2, )
ps2a <- pointGame(tennisIn, "PS", "A", 2, )
aa2d <- pointGame(tennisIn, "AA", "D", 2, )
aa2a <- pointGame(tennisIn, "AA", "A", 2, )
result_2serve <- rbind(ps2d, ps2a, aa2d, aa2a)
print(result_2serve)

#All serves, all sets
psd <- pointGame(tennisIn, "PS", "D", ,)
psa <- pointGame(tennisIn, "PS", "A", ,)
aad <- pointGame(tennisIn, "AA", "D", ,)
aaa <- pointGame(tennisIn, "AA", "A", ,)
result_all <- rbind(psd, psa, aad, aaa)
print(result_all)

#Combine all serve results
result_allserves <- rbind(result_1serve, result_2serve, result_all)
result_allserves <- result_allserves[order(result_allserves$server, result_allserves$court, result_allserves$set),]
print(result_allserves)
write.csv(result_allserves, "tennis_results.csv")


#--- 1ST SERVE, CHOOSE SET --- 

#1st serves, 1st set
ps1d1 <- pointGame(tennisIn, "PS", "D", 1, 1)
ps1a1 <- pointGame(tennisIn, "PS", "A", 1, 1)
aa1d1 <- pointGame(tennisIn, "AA", "D", 1, 1)
aa1a1 <- pointGame(tennisIn, "AA", "A", 1, 1)
result_serve1set1 <- rbind(ps1d1, ps1a1, aa1d1, aa1a1)
print(result_serve1set1)

#1st serves, 2nd set
ps1d2 <- pointGame(tennisIn, "PS", "D", 1, 2)
ps1a2 <- pointGame(tennisIn, "PS", "A", 1, 2)
aa1d2 <- pointGame(tennisIn, "AA", "D", 1, 2)
aa1a2 <- pointGame(tennisIn, "AA", "A", 1, 2)
result_serve1set2 <- rbind(ps1d2, ps1a2, aa1d2, aa1a2)
print(result_serve1set2)

#1st serves, 3rd set
ps1d3 <- pointGame(tennisIn, "PS", "D", 1, 3)
ps1a3 <- pointGame(tennisIn, "PS", "A", 1, 3)
aa1d3 <- pointGame(tennisIn, "AA", "D", 1, 3)
aa1a3 <- pointGame(tennisIn, "AA", "A", 1, 3)
result_serve1set3 <- rbind(ps1d3, ps1a3, aa1d3, aa1a3)
print(result_serve1set3)

#1st serves, 4th set
ps1d4 <- pointGame(tennisIn, "PS", "D", 1, 4)
ps1a4 <- pointGame(tennisIn, "PS", "A", 1, 4)
aa1d4 <- pointGame(tennisIn, "AA", "D", 1, 4)
aa1a4 <- pointGame(tennisIn, "AA", "A", 1, 4)
result_serve1set4 <- rbind(ps1d4, ps1a4, aa1d4, aa1a4)
print(result_serve1set4)

#Combine 1st serve, all set results
result_1serve_allsets <- rbind(result_serve1set1, result_serve1set2, result_serve1set3, result_serve1set4)
result_1serve_allsets <- result_1serve_allsets[order(result_1serve_allsets$server, result_1serve_allsets$court, 
                                                     result_1serve_allsets$set),]
print(result_1serve_allsets)
write.table(result_1serve_allsets, "tennis_results.csv", append=TRUE, col.names=FALSE, sep=",")

#--- ALL SERVES, CHOOSE SET --- 

#All serves, 1st set
psd1 <- pointGame(tennisIn, "PS", "D", , 1)
psa1 <- pointGame(tennisIn, "PS", "A", , 1)
aad1 <- pointGame(tennisIn, "AA", "D", , 1)
aaa1 <- pointGame(tennisIn, "AA", "A", , 1)
result_set1 <- rbind(psd1, psa1, aad1, aaa1)
print(result_set1)

#All serves, 2nd set
psd2 <- pointGame(tennisIn, "PS", "D", , 2)
psa2 <- pointGame(tennisIn, "PS", "A", , 2)
aad2 <- pointGame(tennisIn, "AA", "D", , 2)
aaa2 <- pointGame(tennisIn, "AA", "A", , 2)
result_set2 <- rbind(psd2, psa2, aad2, aaa2)
print(result_set2)

#All serves, 3rd set
psd3 <- pointGame(tennisIn, "PS", "D", , 3)
psa3 <- pointGame(tennisIn, "PS", "A", , 3)
aad3 <- pointGame(tennisIn, "AA", "D", , 3)
aaa3 <- pointGame(tennisIn, "AA", "A", , 3)
result_set3 <- rbind(psd3, psa3, aad3, aaa3)
print(result_set3)

#All serves, 4th set
psd4 <- pointGame(tennisIn, "PS", "D", , 4)
psa4 <- pointGame(tennisIn, "PS", "A", , 4)
aad4 <- pointGame(tennisIn, "AA", "D", , 4)
aaa4 <- pointGame(tennisIn, "AA", "A", , 4)
result_set4 <- rbind(psd4, psa4, aad4, aaa4)
print(result_set4)

#Combine all serves, all set results
result_allsets <- rbind(result_set1, result_set2, result_set3, result_set4)
result_allsets <- result_allsets[order(result_allsets$server, result_allsets$court, result_allsets$set),]
print(result_allsets)
write.table(result_allsets, "tennis_results.csv", append=TRUE, col.names=FALSE, sep=",")

#ROUGH, not working yet
#--- 1ST SERVES, BY SERVER GAME --- 

pointGame2 <- function(tennis_data, server, court, serve_num=tennis_data$ServeNum) {
  
  df2 <- data.frame(server=character(), court=character(), set=character(), server_game_num=character(), serve_num=character(), serve_left=numeric(), 
                    serve_right=numeric(), point_left=numeric(), point_right=numeric(), perc_winLeft=numeric(), perc_winRight=numeric(), 
                    chisq_val=numeric(), p_val=numeric())
  
  for (i in 1:length(unique(tennis_data[tennis_data$Server==server,]$ServerGameNum))) {
    df <- subset(tennis_data, Server==server & Court==court & ServeNum==serve_num & ServerGameNum==i) 
    
    serve_left <- sum(df$Left_FH)
    serve_right <- sum(df$Right_BH)
    point_left <- ifelse(serve_left>0, sum(df[df$ServeDir=="L",]$PointWon), NA)
    point_right <- ifelse(serve_right>0, sum(df[df$ServeDir=="R",]$PointWon), NA)
    perc_winLeft <- ifelse(point_left != "NA", round((point_left/serve_left)*100, 1), NA)
    perc_winRight <- ifelse(point_right != "NA", round((point_right/serve_right)*100, 1), NA)                    
    str(serve_left)
    str(serve_right)
    str(point_left)
    str(point_right)
    str(perc_winLeft)
    str(perc_winRight)
    
    chi_sq <- ifelse((serve_left>0) & (serve_right>0), prop.test(c(point_left, point_right), c(serve_left, serve_right)), NA)  
    #chi_sq <- ifelse((serve_left>0) & (serve_right>0), print("yes"), print("no"))  
    print(chi_sq)
    chisq_val <- ifelse((chi_sq != "NA"), round(chi_sq$statistic, 3), NA)
    p_val <- ifelse((chi_sq != "NA"), round(chi_sq$p.value, 3), NA)
    
    df2[i,] <- data.frame(server=server, court=court, set=df[i,]$Set, server_game_num=i, serve_num=paste(unique(serve_num),collapse=""), serve_left=serve_left, 
                  serve_right=serve_right, point_left=point_left, point_right=point_right, 
                  perc_winLeft=perc_winLeft, perc_winRight=perc_winRight, 
                  chisq_val=chisq_val, p_val=p_val)
  }  
    
  rownames(df2) <- NULL  
  return(df2)
}

write.csv(result_1serve_allsets, "tennis_results.csv")

psd1g <- pointGame2(tennisIn, "PS", "D", "10")

psg1d <- subset(tennisIn, Server=="PS" & ServeNum=="1" & Court=="D")
library(plyr)

psg1d_agg <- ddply(psg1d, .(ServerGameNum), summarise, serve_left=sum(Left_FH), point_left=sum(PointWon))
psg1d_agg <- psg1d_agg[sort(as.numeric(psg1d_agg$ServerGameNum)),]
psg1d_agg

#Segment 1st serve all, 2nd serve all, All serves all, 1st serve by set, All serves by set
#Time series
#Predictive model
#Serial independence
#Compare to another low level match

