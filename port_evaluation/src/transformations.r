# loading necessary libraries
library(tibble)
library(tidyr)
library(tidyverse)
library(dplyr)
library(rlang)
library(broom)


# loading data from RDS files
source("port_evaluation/src/loader.r")
data <- load_RDS_data()


# carrier_port_visit
data[['carrier_port_visit']] %>%
	rename(
		event_id = id,
		event_type = type,
		event_start = start,
		event_end = end,
		event_lat = lat,
		event_lon = lon
	) %>%
	unnest_wider(vessel) %>%
	rename(
		vessel_id = id,
		vessel_flag = flag,
		vessel_name = name,
		vessel_type = type,
		vessel_ssvid = ssvid
	) %>%
	unnest_wider(regions) %>%
	unnest_wider(distances) %>%
	unnest_wider(event_info) %>%
	unnest_wider(port_visit) %>%
	unnest_wider(startAnchorage) %>%
	unnest_wider(intermediateAnchorage, names_repair = tidyr_legacy) %>%
	unnest_wider(endAnchorage, names_repair = tidyr_legacy) %>%
	saveRDS("port_evaluation/data/proc/carrier_port_visit.RDS")


# carriers 
data[['carriers']] %>%
	saveRDS("port_evaluation/data/proc/carriers.RDS")


# encounter
data[['encounter']]  %>%
	rename(
		event_id = id,
		event_type = type,
		event_start = start,
		event_end = end,
		event_lat = lat,
		event_lon = lon
	) %>%
	unnest_wider(vessel) %>%
	rename(
		vessel1_id = id,
		vessel1_flag = flag,
		vessel1_name = name,
		vessel1_type = type,
		vessel1_ssvid = ssvid
	) %>%
	unnest_wider(regions) %>%
	unnest_wider(distances) %>%
	unnest_wider(event_info) %>%
    unnest_wider(encounter) %>%
    rename(encounter_type = type) %>%
    unnest_wider(vessel) %>%
	rename(
		vessel2_id = id,
		vessel2_flag = flag,
		vessel2_name = name,
		vessel2_type = type,
		vessel2_ssvid = ssvid
	) %>%
    saveRDS("port_evaluation/data/proc/encounter.RDS")


# fishers
data[['fishers']] %>%
    saveRDS("port_evaluation/data/proc/fishers.RDS")


# fishing port visits
data[['fishing_port_visit']] %>%
	rename(
		event_id = id,
		event_type = type,
		event_start = start,
		event_end = end,
		event_lat = lat,
		event_lon = lon
	) %>%
    unnest_wider(regions) %>%
	unnest_wider(distances) %>%
	unnest_wider(vessel) %>%
    rename(
		vessel_id = id,
		vessel_flag = flag,
		vessel_name = name,
		vessel_type = type,
		vessel_ssvid = ssvid
	) %>%
    unnest_wider(event_info) %>%
    unnest_wider(port_visit) %>%
    unnest_wider(startAnchorage) %>%
	unnest_wider(intermediateAnchorage, names_repair = tidyr_legacy) %>%
	unnest_wider(endAnchorage, names_repair = tidyr_legacy) %>%
    saveRDS("port_evaluation/data/proc/fishing_port_visit.RDS")


# loitering
data[['loitering']] %>%
	rename(
		event_id = id,
		event_type = type,
		event_start = start,
		event_end = end,
		event_lat = lat,
		event_lon = lon
	) %>%
	unnest_wider(vessel) %>%
	rename(
		vessel_id = id,
		vessel_name = name,
		vessel_type = type,
		vessel_ssvid = ssvid
	) %>%
	unnest_wider(regions) %>%
	unnest_wider(distances) %>%
	unnest_wider(event_info) %>%
    unnest_wider(loitering) %>%
    saveRDS("port_evaluation/data/proc/loitering.RDS")