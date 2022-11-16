

library(devtools)
devtools::install_github("GlobalFishingWatch/gfwr")
library(gfwr)
library(dotenv)
library(tidyr)
library(tidyverse)
library(openxlsx)


## loading token
# load_dot_env(file = "port_evaluation/src/GlobalFishingWatch/.env")
# Sys.getenv("GFW_TOKEN")
GFW_TOKEN<-"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7Im5hbWUiOiJJVVVQcm9qZWN0IiwidXNlcklkIjoyMDUwMCwiYXBwbGljYXRpb25OYW1lIjoiSVVVUHJvamVjdCIsImlkIjoxODQsInR5cGUiOiJ1c2VyLWFwcGxpY2F0aW9uIn0sImlhdCI6MTY2MzExNjY4MiwiZXhwIjoxOTc4NDc2NjgyLCJhdWQiOiJnZnciLCJpc3MiOiJnZncifQ.bvgbI7Hgl7AdfsfZOtsGd8aevNxRQcYqXLuLxRZZqbf49ztzwi190FmkqYsHVclvFDpfV0eizrvzaCBVXO2TI3KT_3CAoiYOBboTA5tp034p7QDSHR76c2w_0fX3E-H6lXXnK7ny3PppulDZrKovyH-KY8Efk031wXrFrPxK-HyAIZStVOMAySxh4IOQu1v-IAz6jLg0hHxmJl6jfGViWdB_MPN6K-wNY1e3JTbcJh-KpjSyqPa0NAmHMBW75_5MEA196dZ6E9CqILd3qezuklrn168qt9gKrKf3qe316cYd3BM24n4VH1nJWqOqLFcYOLsCWXaTgoK-Ozqm7c8zRqKTCfgVJV-YXRtM4K-FDZ7-jfVTTS3-QqzMGAEaJkLwfLrEUzToieS8bjvXeuwtW5-BBJTRs_xeQRfPmOSEfRshy6O1hchzDLe64ZnhOAycbk61LFMxuZc59siLzgxKMu-8H7KyDxLDb7wsCdycfM_plJhlFawk2TZ_b5j7EePF"


# ## downloading vessel data
# carrier <- get_vessel_info(
#     query = "lastTransmissionDate > '2021-01-01'",
#     search_type = "advanced",
#     dataset = "carrier_vessel",
#     key = GFW_TOKEN
#     )

# usa_trawlers <- gfwr::get_vessel_info(
#   query = "flag = 'USA' AND geartype = 'trawlers'", 
#   search_type = "advanced", 
#   dataset = "fishing_vessel",
#   key = GFW_TOKEN
#   )

# # Collapse vessel ids into a commas separated list to pass to Events API
# usa_trawler_ids <- paste0(usa_trawlers$id[1:10], collapse = ',')


fishing <- get_event(
    event_type = "fishing",
    start_date = "2022-10-21",
    end_date = "2022-10-31",
    key = GFW_TOKEN
    )

fishing %>%
    saveRDS(file = "port_evaluation/data/input/GFW/api/fishing/2022-10-21.RDS")



fishing %>%
	rename(
		event_id = id,
		event_type = type) %>%
    head() %>% 
    unnest_wider(vessel) %>% 
    unnest_wider(regions) %>%
    View()


usa_trawlers <- gfwr::get_vessel_info(
  query = "flag = 'USA' AND geartype = 'trawlers'", 
  search_type = "advanced", 
  dataset = "fishing_vessel",
  key = GFW_TOKEN
  )


## new approach

folder <- "/Users/sebastiandodt/OneDrive/Uni/Carnegie Mellon University/Modules/2022 Fall/Systems Project/Coding/all_fishing_vessel_data/mmsi-daily-csvs-10-v2-2020"

## reading in

f11 <- readRDS("port_evaluation/data/input/GFW/api/fishing/2022-11.RDS")
f11 %>%
	rename(
		event_id = id,
		event_type = type) %>%
    unnest_wider(vessel) %>%
    unnest_wider(regions) %>%
    unnest_wider(event_info) %>%
    write.xlsx('port_evaluation/data/input/GFW/api/fishing/2022-11.xlsx')

View(head(f11))

eezs <- data.frame()
for (country in c('CHL', 'PER', 'ECU')) {
    eez_new <- get_region_id(
        region_name = country,
        region_source = 'eez',
        key = GFW_TOKEN)
    eezs <- rbind(eezs, eez_new)
}

fishing <- data.frame()
for (year in 2012:2022) {
    date_range <- paste0(year, "-01-01,", year, "-12-31")
    for (eez in eezs$id) {
        new_fishing <- get_raster(spatial_resolution = 'low',
            temporal_resolution = 'monthly',
            group_by = 'flagAndGearType',
            date_range = date_range,
            region = eez,
            region_source = 'eez',
            key = GFW_TOKEN)
        new_fishing$eez <- eez
        fishing <- rbind(fishing, new_fishing)
    }
}

eezs <- eezs %>% rename(eez = id)

fishing <- fishing %>%
    full_join(eezs, by="eez") %>%
    rename("month" = "Time Range",
        "Fishing_hours" = "Apparent Fishing hours")


by_eez <- fishing %>%
    group_by(month,eez,iso3.x) %>%
    summarise(Total_Hours_per_eez = sum(Fishing_hours)) %>%
    rename("eez_country" = "iso3.x") %>%
    select(-eez_country) %>%
    pivot_wider(names_from = eez, values_from = Total_Hours_per_eez)

by_country <- fishing %>%
    group_by(month,iso3.x) %>%
    summarise(Total_Hours_per_country = sum(Fishing_hours)) %>%
    rename("eez_country" = "iso3.x") %>%
    pivot_wider(names_from = eez_country, values_from = Total_Hours_per_country)

by_gear <- fishing %>%
    group_by(month,Geartype) %>%
    summarise(Total_Hours_per_gear = sum(Fishing_hours)) %>%
    # rename("eez_country" = "iso3.x") %>%
    pivot_wider(names_from = Geartype, values_from = Total_Hours_per_gear)

by_flag <- fishing %>%
    group_by(month,Flag) %>%
    summarise(Total_Hours_per_flag = sum(Fishing_hours)) %>%
    # rename("eez_country" = "iso3.x") %>%
    pivot_wider(names_from = Flag, values_from = Total_Hours_per_flag)

by_eez_and_flag <- fishing %>%
    group_by(Flag,iso3.x) %>%
    summarise(Total_Hours_per_country_eez = sum(Fishing_hours)) %>%
    rename("eez_country" = "iso3.x") %>%
    pivot_wider(names_from = eez_country, values_from = Total_Hours_per_country_eez)

rfmo_fishing <- data.frame()
for (year in 2012:2022) {
    date_range <- paste0(year, "-01-01,", year, "-12-31")
    for (rfmo in c('IATTC')) {
        new_r_fishing <- get_raster(spatial_resolution = 'low',
            temporal_resolution = 'monthly',
            group_by = 'flagAndGearType',
            date_range = date_range,
            region = rfmo,
            region_source = 'trfmo',
            key = GFW_TOKEN)
        rfmo_fishing <- rbind(rfmo_fishing, new_r_fishing)
    }
}

rfmo_by_month <- rfmo_fishing %>%
    rename("month" = "Time Range",
        "Fishing_hours" = "Apparent Fishing hours") %>%
    group_by(month) %>%
    summarise(Total_Hours_per_month = sum(Fishing_hours))

rfmo_by_month_and_gear <- rfmo_fishing %>%
    rename("month" = "Time Range",
        "Fishing_hours" = "Apparent Fishing hours") %>%
    group_by(month,Geartype) %>%
    summarise(Total_Hours_per_gear = sum(Fishing_hours)) %>%
    pivot_wider(names_from = Geartype, values_from = Total_Hours_per_gear)


rfmo_by_month_and_flag <- rfmo_fishing %>%
    rename("month" = "Time Range",
        "Fishing_hours" = "Apparent Fishing hours") %>%
    group_by(month,Flag) %>%
    summarise(Total_Hours_per_flag = sum(Fishing_hours)) %>%
    pivot_wider(names_from = Flag, values_from = Total_Hours_per_flag)





data <- list(
    ungrouped = fishing,
    by_eez = by_eez,
    eez_dict = eezs,
    by_country = by_country,
    by_gear = by_gear,
    by_flag = by_flag,
    by_eez_and_flag = by_eez_and_flag,
    # iattc_fishing = rfmo_fishing,
    iattc_by_month = rfmo_by_month,
    iattc_by_month_and_gear = rfmo_by_month_and_gear,
    iattc_by_month_and_flag = rfmo_by_month_and_flag
)

data %>% write.xlsx("port_evaluation/data/input/GFW/api/fishing/grouped-v3.xlsx")
