import math

def setTest():

  print 'counting query words in documents'
  a = ['a','b','c','d', 'a', 'c']
  doc_tfidf = {}
  dd = set()
  for word in a:
    doc_tfidf[word]=[]
    doc_tfidf[word].append(0.0)
    dd.add(word)


  print doc_tfidf
  myarr=list(dd)
  print myarr




def sq(x):
	return x**2

def reduce_array(kkk):
	tmp = map(sq, kkk)
	return sum(tmp)

def normalise_array(arr):
    sum_sq = math.sqrt(sum(map(lambda x: (x+0.0) ** 2, arr)))
    result = []
    for val in arr:
        if sum_sq == 0:
            result.append(0.0)
        else:
            result.append(float(val) / float(sum_sq))
    return sum_sq, result

a = ['a','b','c','d']
if 'c' in a:
	print a.index('c')
else:
	print 'nope'


b = [1,3,5]

q = [float(2.3), float(1.2), float(0.7)]

c = reduce_array(b)

print 'c=%d' % c


sum_q, c = normalise_array(q)
print 'sum_q=%f' % sum_q
for f in c:
	print 'f=%f' % f


for i in range(10):
	print '%d' % i

setTest()

