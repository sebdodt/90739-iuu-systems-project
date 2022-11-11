

def in_eez(output):
    '''
    appends columns:
    - 'in_us_eez': whether boat is currently in U.S. EEZ
    - 'in_nato_eez': whether boat is currently in the EEZ of a nato-allied country
    - 'in_five_eyes_eez': whether boat is currently in the EEZ of a five eye member
    - 'in_eez': whether boat is currently in any EEZ
    - 'eez': name of the EEZ where boat is currently in
    '''
    return output