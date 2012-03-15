#! /usr/bin/env python
#
# Download NLP-Class week 1 video lecture subtitles and provide a sorted list 
# of frequency of words, excluding stopwords
#
# Nathan Smith <nathan@smithfam.info>

import urllib

import nltk

# Values of the q parameter in the subtitles URL
subtitles = [124, 125, 13, 127, 126, 5, 6, 7, 8, 9, 10]
stops = nltk.corpus.stopwords.words('english')
url = "https://www.coursera.org/nlp/lecture/subtitles?q=%d_en&format=txt"
text = ""

for sub in subtitles:
    # Normalize to lowercase
    text += urllib.urlopen(url % sub).read().lower()

# I don't like how word_tokenize handles things (e.g. "gonna"), so providing a 
# basic tokenizer to include words with apostraphes
pattern = r"\w+('\w+)?"
subtitle_words = nltk.regexp_tokenize(text, pattern)

# Remove English stopwords to get a better sense of the significant tokens
fdist = nltk.FreqDist([w for w in subtitle_words if not w in stops])
for word, count in fdist.items()[:50]:
    print "%s - %d" % (word, count)
