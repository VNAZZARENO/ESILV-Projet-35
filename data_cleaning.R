---
title: "splitData"
output: html_document
date: "2022-11-10"
---

# Import library 
```{r}
library(data.table)
library(anytime)
```

```{r}
SplitCalcul <- function(a,b){
  path=paste("C:/Users/LeopoldPL/Desktop/Data/",a,sep="")
  data <- read.csv(path,sep=",")
  date_string <- data$Timestamp
  date_time <- as.POSIXlt(date_string, format = "%Y-%m-%d %H:%M:%OS", tz = "UTC")
  milliseconds <- substr(date_string, 21, 23) #recup les milisecondes
  data$Timestamp <- paste(date_time, milliseconds, sep = ".") # les ajoute au timestamp
  tab <- split(data, substr(data$Timestamp, 1, 10)) # split les donnees par jour en prenant les 10 premiers caracteres : 'YYYY-MM-DD'
  dates <- names(tab); # Regroupement de l'ensemble des dates dans un tableau
  for (i in 1 : length(dates)-1){
    head <- "'Exness' 'Symbol' 'Timestamp' 'Bid' 'Ask'"
    path <- paste("C:/Users/LeopoldPL/Desktop/DataSplit/", b , dates[i] ,".csv", sep = "")
    write.table(head, path, sep = "," , col.names = FALSE, append = TRUE, row.names = FALSE)
    write.table(tab[i], path,sep=",", col.names = FALSE, append = TRUE, row.names = FALSE)
  }
}
```



```{r}
#EURGBPm
#SplitCalcul("Exness_EURGBPm_2018.csv","EURGBP_")
#SplitCalcul("Exness_EURGBPm_2019.csv","EURGBP_")
#SplitCalcul("Exness_EURGBPm_2020.csv","EURGBP_")
#SplitCalcul("Exness_EURGBPm_2021.csv","EURGBP_")

#EURJPYm
#SplitCalcul("Exness_EURJPYm_2018.csv","EURJPY_")
#SplitCalcul("Exness_EURJPYm_2019.csv","EURJPY_")
#SplitCalcul("Exness_EURJPYm_2020.csv","EURJPY_")
#SplitCalcul("Exness_EURJPYm_2021.csv","EURJPY_")

#EURUSDm
#SplitCalcul("Exness_EurUSDm_2018.csv","EurUSD_")
#SplitCalcul("Exness_EurUSDm_2019.csv","EurUSD_")
#SplitCalcul("Exness_EurUSDm_2020.csv","EurUSD_")
#SplitCalcul("Exness_EurUSDm_2021.csv","EurUSD_")

#GBPUSDm
#SplitCalcul("Exness_GBPUSDm_2018.csv","GBPUSD_")
#SplitCalcul("Exness_GBPUSDm_2019.csv","GBPUSD_")
#SplitCalcul("Exness_GBPUSDm_2020.csv","GBPUSD_")
SplitCalcul("Exness_GBPUSDm_2021.csv","GBPUSD_")

#USDJPYm
SplitCalcul("Exness_USDJPYm_2018.csv","USDJPY_")
SplitCalcul("Exness_USDJPYm_2019.csv","USDJPY_")
SplitCalcul("Exness_USDJPYm_2020.csv","USDJPY_")
SplitCalcul("Exness_USDJPYm_2021.csv","USDJPY_")

#XAUUSDm
SplitCalcul("Exness_XAUUSDm_2019.csv","XAUUSD_")
SplitCalcul("Exness_XAUUSDm_2020.csv","XAUUSD_")
```