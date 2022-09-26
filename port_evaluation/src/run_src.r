print("Starting R Environment")

library(tidyr)
library(tidyverse)
source("port_evaluation/src/loader.r")

run_src <- function() {
    data <- load_RDS_data()
    return(data)
}

print("Done.")