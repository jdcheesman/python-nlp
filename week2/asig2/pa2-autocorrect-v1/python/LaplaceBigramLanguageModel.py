import re
import math


class LaplaceBigramLanguageModel:
  """following dictionaries are <token,count> pairs"""
  unigrams = dict()
  bigrams = dict()
  trigrams = dict()

  total_tokens = 0
  total_vocab = 0

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.train(corpus)

  def load_unigrams(self, corpus):
    """Load the unigrams dictionary """
    print 'load_unigrams'
    pattern = '\w+'
    word_finder = re.compile(pattern)

    for line in corpus.corpus:
        for m in line.cleanSentence().getCorrectSentence():
          if word_finder.match(m):
            self.total_tokens = self.total_tokens + 1
            val = 1
            if m in self.unigrams:
                val = self.unigrams[m] + 1
            else:
                self.total_vocab = self.total_vocab + 1
            self.unigrams[m] = val


  def load_bigrams(self, corpus):
    """Load the bigrams dictionary"""
    print 'load_bigrams'
    pattern = '[(]'
    word_finder = re.compile(pattern)

    last_word = ''
    for line in corpus.corpus:
        for m in line.cleanSentence().getCorrectSentence():
            if not word_finder.search(m):
                if last_word is '':
                    last_word = m
                else:
                    val = 1
                    new_bigram = last_word + ' ' + m
                    if new_bigram in self.bigrams:
                        val = self.bigrams[new_bigram] + 1
                    self.bigrams[new_bigram] = val
                    last_word = m


  def load_trigrams(self, corpus):
    """Load the bigrams dictionary"""
    print 'load_trigrams'

    pattern = '[(]'
    word_finder = re.compile(pattern)

    word_n_minus_1 = ''
    word_n_minus_2 = ''

    for line in corpus.corpus:
        for m in line.cleanSentence().getCorrectSentence():
            if not word_finder.search(m):
                if word_n_minus_1 is '' and word_n_minus_2 is '':
                    word_n_minus_1 = m
                elif word_n_minus_1 is not '' and word_n_minus_2 is '':
                    word_n_minus_2 = word_n_minus_1
                    word_n_minus_1 = m
                else:
                    val = 1
                    new_trigram = word_n_minus_2 + ' ' + word_n_minus_1 + ' ' + m
                    if new_trigram in self.trigrams:
                        val = self.trigrams[new_trigram] + 1
                    self.trigrams[new_trigram] = val
                    word_n_minus_2 = word_n_minus_1
                    word_n_minus_1 = m    

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    self.load_unigrams(corpus)
    self.load_bigrams(corpus)
    self.load_trigrams(corpus)

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    result = 0.0
    first_time = True
    last_word= ''
    for m in sentence:
        if first_time:
            first_time = False
        else:
            cntUnigram = 0
            if last_word in self.unigrams:
                cntUnigram = self.unigrams[last_word]
            
            cntCurrentBigram = 0
            currentBigram = last_word + ' ' + m
            if currentBigram in self.bigrams:
                cntCurrentBigram = self.bigrams[currentBigram]

            probability = (cntCurrentBigram + 1.0) / (cntUnigram + self.total_vocab + 0.0)

            #result = result + probability
            result = result + math.log(probability)
        last_word = m

    #print result
    return result
