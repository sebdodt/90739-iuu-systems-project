library(openxlsx)

# reading in data
source("port_evaluation/src/loader.r")
data <- load_RDS_data("input/GFW/api/unlisted")

# writing data
openxlsx::write.xlsx(data, "port_evaluation/data/proc/GFW/gfw_data-v3.xlsx")