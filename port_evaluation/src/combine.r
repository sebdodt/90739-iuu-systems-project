library(openxlsx)

# reading in data
source("port_evaluation/src/loader.r")
data_api <- load_RDS_data("input/GFW/api/unlisted")

data_download <- load_csv_data("input/GFW/download/Carriers_v20220124")

View(data_api)
View(data_download)


data_download <- data_download %>%
    rename(

    )



# writing data
# openxlsx::write.xlsx(data, "port_evaluation/data/proc/GFW/gfw_data-v3.xlsx")


unique_events_api <- unique(data_api$encounter$event_id)
unique_events_down <- unique(data_download$encounter$id)

both <- c(unique_events_api, unique_events_down)
unique_events_both <- unique(both)

print(length(unique_events_api))
print(length(unique_events_down))
print(length(unique_events_both))

## none of the event_ids overlap. This should be examined.