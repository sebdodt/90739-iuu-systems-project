# 90739-iuu-systems-project

## Structure

This repo is structured in the following way

    .
    ├── pipeline                # Our "attempt" for the backend of the dashboard
    |     ├── app.py            # This is where we were planning to run the pipeline from but we ran out of time to finish
    |     └── table_for_pres..  # This is how @YingzheJin actually compiled the data. Refer to him for questions
    |
    ├── port_evaluation         # This is where we were researching. Originally, just ports -- later, networks etc.
    |     ├── data              # Data Folder (not synced through GitHub because of size. See link below.)
    |     ├── eda               # All of our fun analysis is done here.
    |     |     ├── midterm     # 90% of the analysis is here (even if it was done after midterm, sorry <3)
    |     |     ├── personal_.. # some more ad-hoc data explorations that I did for different people in the team 
    |     |     └── post-proj.. # this is where I am pushing my current analysis to
    |     ├── output            # this is where I stored most of the produced plots and networks
    |     └── src               # this is code to query the GFW API in R
    |
    └── requirements.txt        # all python libraries and versions used in this repo. 


## Network analysis

The code for the network graphs is at:

`port_evaluation/eda/midterm/1_reefers/network.py`


## Data

There are two data folders that we used. One for the general analysis and one for the backend pipeline. We should probably go through them together in case you want to use any of them. They are not synced to github because of their size.

You can download the folders here:

1. Pipeline

Download from https://1drv.ms/u/s!ArdJVZgdFDvWkYFK58HFgklnVo0gCA?e=xMo9Lx
Place in `pipeline/data`


2. Analysis

Download from https://1drv.ms/u/s!ArdJVZgdFDvWkPAgEZXndBC8xspp2Q?e=lfQFcc
Place in `port_evaluation/data`