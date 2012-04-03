import math

class CustomLanguageModel:
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


  def load_trigrams(self, corpus):
    """Load the bigrams dictionary"""
    word_n_minus_1 = ''
    word_n_minus_2 = ''

    for sentence in corpus.corpus:
        for datum in sentence.data: # iterate over datums in the sentence
            if word_n_minus_1 is not '' and word_n_minus_2 is not '':
                val = 1
                new_trigram = word_n_minus_2 + ' ' + word_n_minus_1 + ' ' + datum.word
                if new_trigram in self.trigrams:
                    val = self.trigrams[new_trigram] + 1
                self.trigrams[new_trigram] = val
            word_n_minus_2 = word_n_minus_1
            word_n_minus_1 = datum.word

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
    case3_probability = 0.4 * (1.0 / (self.total_tokens + self.total_vocab + 0.0))

    result = 0.0
    word_n_minus_1 = ''
    word_n_minus_2 = ''

    for m in sentence:
        cntUnigram = 0.0
        cntBigram = 0.0
        cntTrigram = 0.0
        
        current_trigram = (word_n_minus_2 + ' ' + word_n_minus_1 + ' ' + m).strip()
        current_bigram = (word_n_minus_1 + m).strip()
        current_unigram = m

        weight_trigram = 0
        weight_bigram = 0
        weight_unigram = 0
        not_found = 0

        if current_trigram in self.trigrams:
            cntTrigram = self.trigrams[current_trigram]
        if current_bigram in self.bigrams:
            cntBigram = self.bigrams[current_bigram]
        if current_unigram in self.unigrams:
            cntUnigram = self.unigrams[m]
        else:
            not_found = case3_probability


        probability = (cntTrigram+0.0) / (len(self.trigrams)+0.0) +  (cntBigram+0.0) / (len(self.trigrams)+0.0) + (cntUnigram+0.0) / (len(self.unigrams)+0.0) + not_found

        if probability > 1:
            probability = 1

        result = result + math.log(probability)
        
        word_n_minus_2 = word_n_minus_1
        word_n_minus_1 = m

    #print result
    return result

