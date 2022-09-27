load_RDS_data <- function(subfolder = "orig") {
    folder <- paste0("port_evaluation/data/", subfolder)
    file_names <- list.files(path = folder, pattern = ".RDS")

    datalist <- list()
    for (file in file_names) {
        path <- paste(folder, file, sep = "/")
        variable_name <- substring(file, 1, nchar(file) - 4)
        datalist[[variable_name]] <- readRDS(path)
    }
    return(datalist)
}