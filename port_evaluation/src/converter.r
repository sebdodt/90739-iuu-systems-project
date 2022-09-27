library(openxlsx)

# reading in data
source("port_evaluation/src/loader.r")
data <- load_RDS_data("proc")

# writing data
openxlsx::write.xlsx(data, "port_evaluation/data/xlsx/gfw_data.xlsx")