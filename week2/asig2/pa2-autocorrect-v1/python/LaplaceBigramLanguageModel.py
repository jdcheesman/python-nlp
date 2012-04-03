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
    for sentence in corpus.corpus:
        for datum in sentence.data: # iterate over datums in the sentence
            m = datum.word # get the word
            self.total_tokens += 1
            val = 1
            if m in self.unigrams:
                val = self.unigrams[m] + 1
            else:
                self.total_vocab += 1
            self.unigrams[m] = val


  def load_bigrams(self, corpus):
    """Load the bigrams dictionary"""
    last_word = ''
    for sentence in corpus.corpus:
        for datum in sentence.data: # iterate over datums in the sentence
            m = datum.word # get the word
            if last_word is not '':
                val = 1
                new_bigram = last_word + ' ' + m
                if new_bigram in self.bigrams:
                    val = self.bigrams[new_bigram] + 1
                self.bigrams[new_bigram] = val
            last_word = m


  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    self.load_unigrams(corpus)
    print 'Total vocab: %d' % self.total_vocab

    self.load_bigrams(corpus)

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
