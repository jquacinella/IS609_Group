#IS609 Project
#Tennis Game Theory

#load data, set factor variables
tennis <- read.csv("tennisdata.csv")
str(tennis)
tennis$Set <- as.factor(as.character(tennis$Set))
tennis$Game <- as.factor(as.character(tennis$Game))
tennis$ServerGameNum <- as.factor(as.character(tennis$ServerGameNum))
tennis$PointNum <- as.factor(as.character(tennis$PointNum))
tennis$ServeNum <- as.factor(as.character(tennis$ServeNum))

tennis[is.na(tennis)] <- 0 #change NAs to 0
tennis$ServeDir <- as.factor(ifelse(tennis$Left_FH==1, "L", "R")) #combine serve direction to one factor var
str(tennis)

#Function to compare win% on each service side - Chi-square test of equal proportions
pointGame <- function(tennis_data, server, court, serve_num) {
  df <- subset(tennis_data, Server==server & Court==court & ServeNum==serve_num)
  
  serve_left <- sum(df$Left_FH)
  serve_right <- sum(df$Right_BH)
  point_left <- sum(df[df$ServeDir=="L",]$PointWon)
  point_right <- sum(df[df$ServeDir=="R",]$PointWon)
  
  chi_sq <- prop.test(c(point_left, point_right), c(serve_left, serve_right))  
  chisq_val <- chi_sq$statistic
  p_val <- chi_sq$p.value
 
  df2 <- data.frame(server=server, court=court, serve_num=serve_num, serve_left=serve_left, 
                       serve_right=serve_right, point_left=point_left, point_right=point_right, 
                       perc_left=point_left/serve_left, perc_right=point_right/serve_right, 
                       chisq_val=chisq_val, p_val=p_val)
  
  rownames(df2) <- NULL  
  return(df2)
}


#Exclude faults, lets and center serves
tennisIn <- subset(tennis, Fault==0 & Note!="L" & Note!="C")

#Calculate results for both servers, both sides
ps1d <- pointGame(tennisIn, "PS", "D", "1")
ps1a <- pointGame(tennisIn, "PS", "A", "1")
aa1d <- pointGame(tennisIn, "AA", "D", "1")
aa1a <- pointGame(tennisIn, "AA", "A", "1")

result <- rbind(ps1d, ps1a, aa1d, aa1a)
print(result)






#rough work
table(ps$ServeDir, ps$PointWon)
prop.table(table(ps$ServeDir, ps$PointWon), 1)

temp <- table(aa$ServeDir, aa$PointWon)
prop.table(table(aa$ServeDir, aa$PointWon), 1)
temp
aaChi <- prop.test(temp)
aaChi
aaChi$statistic
str(aaChi)
aaFisher <- fisher.test(temp)
str(aaFisher)
chisq.test(temp, simulate.p.value=TRUE)

psDir <- table(ps$ServeDir)
psDir
prop.table(psDir)

aaDir <- table(aa$ServeDir)
prop.table(aaDir)
