
# Downloading data from Global Fishing Watch API

## libraries
library(devtools)
devtools::install_github("GlobalFishingWatch/gfwr")
library(gfwr)
library(dotenv)


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

port <- get_event(
    event_type = 'port',
    key = GFW_TOKEN
    )

gap <- get_event(
    event_type = 'gap',
    key = GFW_TOKEN
    )

port_visit <- get_event(
    event_type = 'port_visit',
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
saveRDS(port, file = "port_evaluation/data/port.RDS")
saveRDS(gap, file = "port_evaluation/data/gap.RDS")
saveRDS(port_visit, file = "port_evaluation/data/port_visit.RDS")
saveRDS(fishing, file = "port_evaluation/data/fishing.RDS")