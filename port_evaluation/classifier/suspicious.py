import pandas as pd

def classify(carriers, encounter, loitering, cutoff = 0.5):
    '''
    Input: Global Fishing Watch data
    Output: Adds column to each reefer indicating whether they are suspicious of IUU or not
    '''

    # count the num of encounter/loitering for each carrier
    num_encounter = []
    num_loitering = []
    for i in carriers.id:
        num_encounter.append(encounter[encounter['vessel1_id']==i].shape[0])
        num_loitering.append(loitering[loitering['vessel_id']==i].shape[0])

    # append the num info into new column in carrier table
    carrier = carriers.assign(encounter=num_encounter, loitering = num_loitering)
    # if cutoff*encounter >= (1-cutoff)*loitering then we set label = 0 as unsuspicious
    # if cutoff*encounter < (1-cutoff)*loitering then we set label = 1 as suspicious
    carrier['label'] = ((cutoff*carrier['encounter'] - (1-cutoff)*carrier['loitering']) < 0).astype(int)
    return carrier