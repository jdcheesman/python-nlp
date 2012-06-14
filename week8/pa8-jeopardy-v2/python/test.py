import re
from nltk.corpus import gazetteers


USCITIES = set(gazetteers.words('uscities.txt'))
COUNTRIES = set([country for filename in ('isocountries.txt','countries.txt')
                 for country in gazetteers.words(filename)])

US_STATES = set([state.lower() for filename in
                 ('usstates.txt','usstateabbrev.txt') for state in
                 gazetteers.words(filename)])



#print USCITIES
print US_STATES
#print COUNTRIES