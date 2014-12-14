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

#Function to compare win% on each service side - Chi-square test and Fisher's Exact test
pointGame <- function(tennis_data, server, court, serve_num=tennis_data$ServeNum, set=tennis_data$Set) {
  
  df <- subset(tennis_data, Server==server & Court==court & ServeNum==serve_num & Set==set)

  serve_left <- sum(df$Left_FH)
  serve_right <- sum(df$Right_BH)
  point_left <- sum(df[df$ServeDir=="L",]$PointWon)
  point_right <- sum(df[df$ServeDir=="R",]$PointWon)
  m <- matrix(c(point_left, serve_left-point_left, point_right, serve_right-point_right), ncol=2, byrow=TRUE)
  
  chi_sq <- chisq.test(m, corr=TRUE)  
  chisq_val <- round(chi_sq$statistic, 3)
  p_val <- round(chi_sq$p.value, 3)
  fish_pval <- round(fisher.test(m)$p.val, 3)
  
  df2 <- data.frame(server=server, court=court, set=paste(unique(set),collapse=""), serve_num=paste(unique(serve_num),collapse=""), serve_left=serve_left, 
                    serve_right=serve_right, point_left=point_left, point_right=point_right, 
                    perc_winLeft=round((point_left/serve_left)*100, 1), perc_winRight=round((point_right/serve_right)*100, 1), 
                    chisq_val=chisq_val, chisq_pval=p_val, fisher_pval=fish_pval)
  
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


#--- 1ST SERVES, BY SERVER GAME --- 
percSet <- function(df, server, serveNum, court, title) {

  psg1d <- subset(df, Server==server & ServeNum==serveNum & Court==court)
  
  psg_agg <- ddply(psg1d, .(Set), summarise, serveLeft=sum(Left_FH), serveRight=sum(Right_BH), 
                   perc_serveLeft=(sum(Left_FH)/(sum(Left_FH)+sum(Right_BH))), 
                   perc_serveRight=(sum(Right_BH)/(sum(Left_FH)+sum(Right_BH))))
  psg_agg$Set <- as.numeric(as.character(psg_agg$Set))
  psg_agg <- psg_agg[sort(as.numeric(psg_agg$Set)),]
  psg_agg
  
  
  psg_aggL <- ddply(psg1d, .(Set, ServeDir), summarise, serveLeft=sum(Left_FH), serveRight=sum(Right_BH), PointWon=sum(PointWon), perc_won=(sum(PointWon)/(sum(Left_FH)+sum(Right_BH))))
  psg_aggL$Set <- as.numeric(as.character(psg_aggL$Set))
  psg_aggL <- subset(psg_aggL, ServeDir=="L")
  
  psg_aggR <- ddply(psg1d, .(Set, ServeDir), summarise, serveLeft=sum(Left_FH), serveRight=sum(Right_BH), PointWon=sum(PointWon), perc_won=(sum(PointWon)/(sum(Left_FH)+sum(Right_BH))))
  psg_aggR$Set <- as.numeric(as.character(psg_aggR$Set))
  psg_aggR <- subset(psg_aggR, ServeDir=="R")
  
  
  psg_agg3 <- merge(psg_agg, psg_aggL, by="Set")
  psg_agg4 <- merge(psg_agg3, psg_aggR, by="Set")
  
  g <- ggplot(psg_agg4, aes(Set), group=c(perc_serveLeft, perc_won.x, perc_won.y)) + geom_line(aes(y=perc_serveLeft), size=1.5, colour="blue", linetype="dotted") + 
    geom_line(aes(y=perc_won.x), size=1.5, colour="blue") +  
    geom_line(aes(y=perc_won.y), size=1.5, colour="red")
  
  g <- g + ylab("Percent served, point won") + xlab("Set") + ggtitle(title) +
    theme(axis.title.y=element_text(face="bold", size=14), axis.title.x=element_text(face="bold", size=14), 
          plot.title=element_text(face="bold", size=16), axis.text.y=element_text(face="bold", size=12), 
          axis.text.x=element_text(face="bold", size=12))
  
  return(g) 

}

#Plot side-by-side graphs. Borrowed from...
#http://www.cookbook-r.com/Graphs/Multiple_graphs_on_one_page_(ggplot2)
multiplot <- function(..., plotlist=NULL, file, cols=2, layout=NULL) {
  require(grid)
  
  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)
  
  numPlots = length(plots)
  
  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                     ncol = cols, nrow = ceiling(numPlots/cols))
  }
  
  if (numPlots==1) {
    print(plots[[1]])
    
  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
    
    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
      
      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

#1st serve results by set, graphs
g_psd <- percSet(tennisIn, "PS", 1, "D", "Sampras Deuce court")
g_psa <- percSet(tennisIn, "PS", 1, "A", "Sampras Ad court")
multiplot(g_psd, g_psa)
g_aad <- percSet(tennisIn, "AA", 1, "D", "Agassi Deuce court")
g_aaa <- percSet(tennisIn, "AA", 1, "A", "Agassi Ad court")
multiplot(g_aad, g_aaa)

