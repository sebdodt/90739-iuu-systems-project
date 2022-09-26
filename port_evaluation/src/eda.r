source("port_evaluation/src/loader.r")

get_data <- function() {
    data <- load_RDS_data()
    return(data)
}

data <- get_data()