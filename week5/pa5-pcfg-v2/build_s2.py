items = ['Misc','Adj', 'Adv', 'CompAdj', 'Conj', 'Det', 'Do', 'Does', 'EOS', 'Expl', 'GenS', 'Modal',
  'Not', 'Noun', 'NounP', 'Num', 'PastParticiple', 'Pause', 'Places', 'PersonalPronoun', 'PersonalPronounP',
  'PosPersonalPronoun', 'Prep', 'PresentParticiples', 'Proper', 'PNP',
  'ProperP', 'SubConj', 'SupAdj', 'To', 'TravelVerb', 'TravelVerbPT', 'VerbBase', 'VerbPastTense', 'VerbT', 'VerbTPP',
  'VerbTPS', 'WhAdv', 'WhDet', 'WhPosPronoun', 'What', 'Who',
  'Are', 'Is', 'Have', 'Has', 'Loc', 'It', 'They', 'Was', 'Were', 'Been']



print '1\tS2'

for item in items:
	print '1\tS2\t_%s' % item

for item in items:
	print '1\t_%s\t%s' % (item, item)
	for item2 in items:
		print '1\t_%s\t%s _%s' % (item, item, item2)

