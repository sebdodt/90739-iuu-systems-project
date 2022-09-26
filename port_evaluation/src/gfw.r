
# Downloading data from Global Fishing Watch API

## libraries
library(devtools)
devtools::install_github("GlobalFishingWatch/gfwr")
library(gfwr)
library(dotenv)
library(tidyr)
library(tidyverse)


## loading token
load_dot_env(file = "port_evaluation/src/GlobalFishingWatch/.env")
Sys.getenv("GFW_TOKEN")
GFW_TOKEN <- Sys.getenv("GFW_TOKEN")


## downloading vessel data
carrier <- get_vessel_info(
    query = "lastTransmissionDate > '1990-01-01'",
    search_type = "advanced",
    dataset = "carrier_vessel",
    key = GFW_TOKEN
    )

fishers <- get_vessel_info(
    query = "lastTransmissionDate > '1990-01-01'",
    search_type = "advanced",
    dataset = "fishing_vessels",
    key = GFW_TOKEN
    )


## downloading event data
loitering <- get_event(
    event_type = 'loitering',
    key = GFW_TOKEN
    )

encounter <- get_event(
    event_type = 'encounter',
    key = GFW_TOKEN
    )


## downloading port visits for carriers/reefers
vessels <- carrier$id %>%
    unique()

get_port_visits <- function(vessels_string) {
    port_visit <- get_event(
        event_type = 'port_visit',
        vessel = vessels_string,
        key = GFW_TOKEN
        )
    print("API called")
    return(port_visit)
}

port_visit_func <- function(vessels, divisor) {
    bins <- ceiling(length(vessels) / divisor)
    print(paste0(bins, " bins"))
    for (i in seq_len(bins)) {
        from <- i + (100 * (i - 1))
        to <- min(i * 100, length(vessels))
        vessels_string <- paste0(
            vessels[from:to],
            collapse = ",")
        port_visit <- get_port_visits(vessels_string)
        if (i == 1) {
            df <- port_visit
        } else {
            df <- rbind(df, port_visit)
        }
    }
    return(df)
}

recursive_check_func <- function(vessels, divisor) {
    df <- tryCatch(port_visit_func(vessels, divisor),
        error = function(e) {
            print(paste0("Divisor ", divisor, " was too large."))
            recursive_check_func(vessels, divisor * 1.1)
        }
    )
    return(df)
}

carrier_ports <- recursive_check_func(vessels, length(vessels))
saveRDS(carrier_ports, file = "port_evaluation/data/carrier_port_visit.RDS")



port_visit <- get_event(
    event_type = 'port_visit',
    vessel = vessels_string,
    key = GFW_TOKEN
    )

fishing <- get_event(
    event_type = 'fishing',
    key = GFW_TOKEN
    )


## saving data
saveRDS(carrier, file = "port_evaluation/data/carriers.RDS")
saveRDS(fishers, file = "port_evaluation/data/fishers.RDS")
saveRDS(loitering, file = "port_evaluation/data/loitering.RDS")
saveRDS(encounter, file = "port_evaluation/data/encounter.RDS")
saveRDS(carrier_ports, file = "port_evaluation/data/carrier_port_visit.RDS")
saveRDS(fishing, file = "port_evaluation/data/fishing.RDS")