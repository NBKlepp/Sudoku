import numpy as np
'''
I'm only keeping the unique substrings.
'''
def getSubstrings(inString):
    inString = inString.lower()
    substrings = []
    for l in range(2,len(inString)+1):
        for i in range(0,len(inString)-l+1):
            j = i+l
            if not inString[i:j] in substrings : substrings += [inString[i:j]]
    return substrings

'''
I'm assuming that we're using ASCII characters here.
'''
def validateSubstring(substring):
    validator = np.array([0]*256)
    substring = [ord(x) for x in substring]
    for x in substring:
        validator[x] += 1
    repeats = np.sum(np.where(validator > 1,1,0))
    if repeats == 1 : return True
    else : return False
