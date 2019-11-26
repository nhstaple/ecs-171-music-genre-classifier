library(ggplot2)

#Program to plot figure 1

types <- c(rep("SVM", 4), rep("Logistic Regression", 4), rep("ANN", 4)) #3 types of classification
features <- c(rep(c("mfcc", "spectral_contrast", "spectral_contrast \nand mfcc", "MRMR Top 200"), 3)) #4 Features were used
scores <- c(0.41, 0.39, 0.49, 0.42, 0.48, 0.40, 0.49, 0.56, 0.56, 0.52, 0.67, 0.55) #Results

df <- data.frame(types, features, scores)

plot <- ggplot(df, aes(fill=types, y=scores, x=features)) + geom_bar(position="dodge", stat="identity")
plot <- plot + labs(title = "Different Classification Methods",
                    x = "Features",
                    y = "F-1 Score",
                    fill = "Classification Types")
plot <- plot + theme_minimal()