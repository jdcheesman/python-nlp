import re

a = '<TT>ullman @ cs.stanford.edu</TT><BR>' 

print 'Testing: %s' % (a)


pattern = '\w{2,3}'

if re.search(pattern, a):
    print 'found'
else:
    print 'not found'


