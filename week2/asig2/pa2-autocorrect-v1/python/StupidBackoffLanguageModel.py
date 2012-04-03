import math


class StupidBackoffLanguageModel:
  unigrams = dict()
  bigrams = dict()
  total_tokens = 0
  total_vocab = 0


  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    self.load_unigrams(corpus)
    self.load_bigrams(corpus)

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

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.

        Steps 1) count(bigram)/count(unigram) if count(unigram) > 0 
        otherwise 2) 0.4 * Laplace unigram for known words
                    3) 0.4 * Laplace unigram fro unknown words 
            
            Laplace unigram is log(count(unigram) + 1) / V + N
    """
    # TODO your code here
    case3_probability = 0.4 * (1.0 / (self.total_tokens + self.total_vocab + 0.0))

    result = 0.0
    previous_word = ''
    for m in sentence:
        probability = case3_probability
        cntUnigram = 0.0
        cntBigram = 0.0

        if previous_word is '':
            if m in self.unigrams:
                cntUnigram = self.unigrams[m]
                probability = 0.4 * ((cntUnigram + 1.0) / (self.total_tokens + self.total_vocab + 0.0))
        else:
            current_bigram = previous_word + ' ' + m
            if previous_word in self.unigrams and current_bigram in self.bigrams:
                cntUnigram = self.unigrams[previous_word]
                cntBigram = self.bigrams[current_bigram]
                probability = (cntBigram+0.0) / (cntUnigram+0.0)
            else:
                if m in self.unigrams:
                    cntUnigram = self.unigrams[m]
                    probability = 0.4 * ((cntUnigram + 1.0) / (self.total_tokens + self.total_vocab + 0.0))

        result = result + math.log(probability)
        previous_word = m
    #print result
    return result
