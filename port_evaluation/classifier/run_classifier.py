from load_data import import_data
from suspicious import classify


# the hyperparameter to be tuned
    # if cutoff*encounter >= (1-cutoff)*loitering then we set label = 0 as unsuspicious
    # if cutoff*encounter < (1-cutoff)*loitering then we set label = 1 as suspicious
cutoff = 0.66


carriers, encounter, loitering = import_data()

#classified_data return the carriers info with new cols: num of encounter, num of loitering and label
classified_data = classify(carriers, encounter, loitering, cutoff)