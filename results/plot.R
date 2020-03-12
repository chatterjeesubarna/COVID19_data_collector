
base_dir = "/Users/subarnachatterjee/Dropbox/COVID19_data_collector/results"
data <- read.delim(file = paste(base_dir, "/USA_corona_stats.csv", sep=""), head = TRUE, sep = ",")
plot_colors <- c("red","blue","black","green")

setEPS()
postscript(paste(base_dir, "/result.eps", sep=""), family="Times", width=5.5, height=5)

x <- data$date_time
y1 <- data$new_cases
y2 <- data$total_deaths
y3 <- data$total_cases

min_y = min(y1);
max_y <- max(y1);

mar.default <- c(5.1,4.1,4.1,2.1) + 0.1
par(mar = mar.default + c(0, 1.4, 0, 0.4))
par(las=1, lwd=1.5)
x_min_lab = 1
x_max_lab = length(x)
x_min=as.character(x[x_min_lab])
x_max=as.character(x[x_max_lab])

# for(i in x_max_lab:2) {
#   # i-th element of `u1` squared into `i`-th position of `usq`
#   y1[i] <- y1[i] - y1[i-1]
# }
# y1[1] = 0

plot(x, y2, type="o", pch = 4, cex=1.3, lty=1, col="black", ylim=c(min_y, max_y), xlim=c(x_min_lab,x_max_lab), axes=FALSE, ann=FALSE)
lines(x, y1, type="o", pch = 4, cex=1.3, lty=1, col="black")


axis(1, at=c(x_min_lab,x_max_lab), label=c(x_min, x_max), cex.axis=0.5, mgp=c(0, 1.25, 0))
axis(2, at=c(min_y, max_y), cex.axis=0.5, mgp=c(0, 0.75, 0))


box()
title(xlab=expression('Timestamp'), cex.lab=1.5, mgp=c(3, 0, 0))
title(ylab="Corona cases", cex.lab=1.5, mgp=c(3.75, 0, 0))
#mtext(expression("(x"~10^12~")"), line = 0, side=1, at=4, cex=1.25, font=5)

dev.off()