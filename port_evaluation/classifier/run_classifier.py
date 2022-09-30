from load_data import import_data
from suspicious import classify

# First we sum the number of encounters and loiterings for each carrier.
# Then make a classification: if there are more encounters than loiterings, the carrier is not suspicious, if there is more loitering, the carrier is suspicious. (Don't hard-code the cutoff. We may want to do 66% loitering and 33% encounters in the future instead of 50-50)
# For every carrier in the carriers table, label a value 1 (suspicious) or 0 (not suspicious).


# the hyperparameter to be tuned
    # if cutoff*encounter >= (1-cutoff)*loitering then we set label = 0 as unsuspicious
    # if cutoff*encounter < (1-cutoff)*loitering then we set label = 1 as suspicious
cutoff = 0.66


carriers, encounter, loitering = import_data()

#classified_data return the carriers info with new cols: num of encounter, num of loitering and label
classified_data = classify(carriers, encounter, loitering, cutoff)