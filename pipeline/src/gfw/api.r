## libraries
lib <- c("devtools",
    "tidyr",
    "tidyverse",
    "openxlsx",
    "dotenv",
    "tibble",
    "dplyr",
    "rlang",
    "broom")
    
lib_na <- lib[!(lib %in% installed.packages()[, "Package"])]
if (length(lib_na)) install.packages(lib_na)
lapply(lib, library, character.only = TRUE)
devtools::install_github("GlobalFishingWatch/gfwr")


## loading token
# load_dot_env(file = "port_evaluation/src/GlobalFishingWatch/.env")
# Sys.getenv("GFW_TOKEN") # TODO get this to work
# GFW_TOKEN <- Sys.getenv("GFW_TOKEN")
GFW_TOKEN <- "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImtpZEtleSJ9.eyJkYXRhIjp7Im5hbWUiOiJJVVVQcm9qZWN0IiwidXNlcklkIjoyMDUwMCwiYXBwbGljYXRpb25OYW1lIjoiSVVVUHJvamVjdCIsImlkIjoxODQsInR5cGUiOiJ1c2VyLWFwcGxpY2F0aW9uIn0sImlhdCI6MTY2MzExNjY4MiwiZXhwIjoxOTc4NDc2NjgyLCJhdWQiOiJnZnciLCJpc3MiOiJnZncifQ.bvgbI7Hgl7AdfsfZOtsGd8aevNxRQcYqXLuLxRZZqbf49ztzwi190FmkqYsHVclvFDpfV0eizrvzaCBVXO2TI3KT_3CAoiYOBboTA5tp034p7QDSHR76c2w_0fX3E-H6lXXnK7ny3PppulDZrKovyH-KY8Efk031wXrFrPxK-HyAIZStVOMAySxh4IOQu1v-IAz6jLg0hHxmJl6jfGViWdB_MPN6K-wNY1e3JTbcJh-KpjSyqPa0NAmHMBW75_5MEA196dZ6E9CqILd3qezuklrn168qt9gKrKf3qe316cYd3BM24n4VH1nJWqOqLFcYOLsCWXaTgoK-Ozqm7c8zRqKTCfgVJV-YXRtM4K-FDZ7-jfVTTS3-QqzMGAEaJkLwfLrEUzToieS8bjvXeuwtW5-BBJTRs_xeQRfPmOSEfRshy6O1hchzDLe64ZnhOAycbk61LFMxuZc59siLzgxKMu-8H7KyDxLDb7wsCdycfM_plJhlFawk2TZ_b5j7EePF"


## downloading vessel data
print("Downloading carrier info...")
carrier <- gfwr::get_vessel_info(
    query = "lastTransmissionDate > '1990-01-01'",
    search_type = "advanced",
    dataset = "carrier_vessel",
    key = GFW_TOKEN
    )

# fishers <- get_vessel_info(
#     query = "lastTransmissionDate > '1990-01-01'",
#     search_type = "advanced",
#     dataset = "fishing_vessels",
#     key = GFW_TOKEN
#     )


## downloading event data
print("Downloading loiterings...")
loitering <- gfwr::get_event(
    event_type = 'loitering',
    key = GFW_TOKEN
    )

print("Downloading encounters...")
encounter <- gfwr::get_event(
    event_type = 'encounter',
    key = GFW_TOKEN
    )


## downloading port visits for carriers/reefers
vessels <- carrier$id %>%
    unique()

print("Downloading port visits...")
get_port_visits <- function(vessels_string) {
    port_visit <- gfwr::get_event(
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

# fishing_ports <- recursive_check_func(vessels, length(vessels))
# saveRDS(fishing_ports, file = "port_evaluation/data/fishing_port_visit.RDS")

carrier_ports <- recursive_check_func(vessels, length(vessels))
# saveRDS(carrier_ports, file = "port_evaluation/data/carrier_port_visit.RDS")

# print("Downloading port visits (version 2)...")
# vessels_string <- paste0(vessels,collapse = ",")
# port_visit <- get_event(
#     event_type = 'port_visit',
#     vessel = vessels_string,
#     key = GFW_TOKEN
#     )

# fishing <- get_event(
#     event_type = 'fishing',
#     key = GFW_TOKEN
#     )


# ## saving data
# saveRDS(carrier, file = "pipeline/data/api/carriers.RDS")
# # saveRDS(fishers, file = "port_evaluation/data/fishers.RDS")
# saveRDS(loitering, file = "pipeline/data/api/loitering.RDS")
# saveRDS(encounter, file = "pipeline/data/api/encounter.RDS")
# saveRDS(carrier_ports, file = "pipeline/data/api/carrier_port_visit.RDS")
# # saveRDS(fishing, file = "port_evaluation/data/fishing.RDS")



# merging data
data <- list(
    "carriers" = carrier,
    "encounter" = encounter,
    "loitering" = loitering,
    "carrier_port_visit" = carrier_ports
)


# carrier_port_visit
print(" > Processing port visits...")
data[['carrier_port_visit']] <- data[['carrier_port_visit']] %>%
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
	unnest_wider(startAnchorage) %>%
	unnest_wider(intermediateAnchorage, names_repair = tidyr_legacy) %>%
	unnest_wider(endAnchorage, names_repair = tidyr_legacy)


# carriers 
print(" > Processing carriers...")
data[['carriers']] <- data[['carriers']] 


# encounter
print(" > Processing encounters...")
data[['encounter']] <- data[['encounter']]  %>%
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
    # unnest_wider(encounter) %>%
    rename(encounter_type = type) %>%
    unnest_wider(vessel) %>%
	rename(
		vessel2_id = id,
		vessel2_flag = flag,
		vessel2_name = name,
		vessel2_type = type,
		vessel2_ssvid = ssvid
	) 


# # fishers
# data[['fishers']] %>%
#     saveRDS("port_evaluation/data/proc/fishers.RDS")


# # fishing port visits
# data[['fishing_port_visit']] %>%
# 	rename(
# 		event_id = id,
# 		event_type = type,
# 		event_start = start,
# 		event_end = end,
# 		event_lat = lat,
# 		event_lon = lon
# 	) %>%
#     unnest_wider(regions) %>%
# 	unnest_wider(distances) %>%
# 	unnest_wider(vessel) %>%
#     rename(
# 		vessel_id = id,
# 		vessel_flag = flag,
# 		vessel_name = name,
# 		vessel_type = type,
# 		vessel_ssvid = ssvid
# 	) %>%
#     unnest_wider(event_info) %>%
#     unnest_wider(port_visit) %>%
#     unnest_wider(startAnchorage) %>%
# 	unnest_wider(intermediateAnchorage, names_repair = tidyr_legacy) %>%
# 	unnest_wider(endAnchorage, names_repair = tidyr_legacy) %>%
#     saveRDS("port_evaluation/data/proc/fishing_port_visit.RDS")


# loitering
print(" > Processing loitering...")
data[['loitering']] <- data[['loitering']] %>%
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
	unnest_wider(event_info)

print(" > Saving data to 'pipeline/data/api/api_data.xlsx'...")
openxlsx::write.xlsx(data, "pipeline/data/api/api_data.xlsx")
print(" > Done.")
