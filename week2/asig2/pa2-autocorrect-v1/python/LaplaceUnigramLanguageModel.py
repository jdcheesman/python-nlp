import math

class LaplaceUnigramLanguageModel:
  """following dictionary is <token,count> pairs"""
  unigrams = dict()
  total_tokens = 0
  total_vocab = 0



  word_prob = dict()

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



  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    self.load_unigrams(corpus)


  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    result = 0.0
    for m in sentence:
        cntUnigram = 0
        if m in self.unigrams:
            cntUnigram = self.unigrams[m]
        

        probability = (cntUnigram + 1.0) / (self.total_tokens + self.total_vocab + 0.0)

        #result = result + probability
        result = result + math.log(probability)
    
    #print result
    return result
