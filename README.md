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