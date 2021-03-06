import json, sys
import base64
import re
from Datum import Datum
import nltk
from nltk.corpus import names

class FeatureFactory:
    re_is_lower_char = re.compile('/[a-z]/')
    re_is_upper_char = re.compile('/[A-Z]/')
    re_is_numeric = re.compile('/[0-9]/')


    """
    Add any necessary initialization steps for your features here
    Using this constructor is optional. Depending on your
    features, you may not need to intialize anything.
    """
    def __init__(self):
        pass


    """
    Words is a list of the words in the entire corpus, previousLabel is the label
    for position-1 (or O if it's the start of a new sentence), and position
    is the word you are adding features for. PreviousLabel must be the
    only label that is visible to this method.
    """

    def computeFeatures(self, words, previousLabel, position):
        features = []
        currentWord = words[position]

        """ Baseline Features """
        features.append("word=" + currentWord)
        features.append("prevLabel=" + previousLabel)
        features.append("word=" + currentWord + ", prevLabel=" + previousLabel)
        """
            Warning: If you encounter "line search failure" error when
            running the program, considering putting the baseline features
        back. It occurs when the features are too sparse. Once you have
            added enough features, take out the features that you don't need.
        """


        """ TODO: Add your features here
            Baseline score:
                precision = 0.801673640167364 #number selected items that are correct
                recall = 0.5229257641921398 #number correct items that are selected
                F1 = 0.6329699372315825
        """
        # precision = 0.8603736479842674
        # recall = 0.47762008733624456
        # F1 = 0.6142506142506142


        if (position-1) > 0:
            features.append("word=" + currentWord + ",prevWord=" + words[position-1])
            features.append("prevWord=" + words[position-1])
        #     features.append("bigram=" + words[position-1] + ' ' + currentWord)
        #     prepositions = ['to','for','by','besides','from','about']
        #     if words[position-1] in prepositions:
        #         features.append("word=" + currentWord + ",preposition=" + words[position-1])
        #     pospositions = ['of']
        #     if currentWord in pospositions:
        #         features.append("posposition=" + currentWord + ",prevWord=" + words[position-1])
        #     if words[position-1] in names.words():
        #         features.append("fullname=" + words[position-1] + ' ' + currentWord)
        #         features.append("surname_1=" + currentWord)
            if re.search('^[A-Za-z]\.$', words[position-1]):
                features.append("initial=" + words[position-1])
                features.append("surname_2=" + currentWord)
                features.append("fullname_2=" + words[position-1] + ' ' + currentWord)
        #     speaking = ['said', 'told', 'says', 'say', 'tells', 'tell']
        #     ignored = ['I', 'You', 'He', 'She', 'It', 'We', 'They']
        #     if words[position-1][0].isupper() and currentWord in speaking and words[position-1] not in ignored and not words[position-1].isupper():
        #         features.append("said=" + words[position-1])

        #     if words[position-1][0].isupper() and currentWord == ',':
        #         features.append("comma=" + words[position-1])
        #     if words[position-1][0].isupper() and currentWord == "'s":
        #         features.append("genitive_s=" + words[position-1])

        # if (position-2) > 0:
        #     speaking = ['said', 'told', 'says', 'say', 'tells', 'tell']
        #     ignored = ['I', 'You', 'He', 'She', 'It', 'We', 'They']
        #     punctuation = ['.', ',', ';', ':']

        #     if currentWord in punctuation:
        #         if words[position-2][0].isupper() and words[position-1] in speaking and words[position-2] not in ignored and not words[position-2].isupper():
        #             features.append("said_2=" + words[position-2])
        #         if words[position-2] in punctuation:
        #             features.append("leading_ending=" + words[position-2] + words[position-1] + currentWord)
        #     if words[position-2] == '\"' and words[position-1][0].isupper() and currentWord in speaking:
        #         features.append("said_3=" + words[position-1])
        #     if currentWord == '\"' and words[position-1][0].isupper() and words[position-2] in speaking:
        #         features.append("said_4=" + words[position-1])




        # features.append("word=" + currentWord + ", prevLabel=" + previousLabel)


        if currentWord in names.words():
            features.append("name=" + currentWord)


        #features.append(self.getCharsFeature(currentWord))
        case = ''
        titleCase = False
        if self.re_is_numeric.search(currentWord):
            case = "numeric=True"
        else:
            if currentWord.isupper():
                case = "case=Upper"
            elif currentWord[0].isupper():
                cnt = 0
                titleCase = True
                for c in currentWord:
                    if cnt > 0:
                        if c.isupper():
                            titleCase = False
                    cnt += 1
                if currentWord.startswith('O\'') or (currentWord.startswith('Mc') and currentWord[2].isupper()) or (currentWord.startswith('Mac') and currentWord[3].isupper()):
                    titleCase = True
                if titleCase:
                    case = "case=Title"
                    if previousLabel == 'PERSON':
                        features.append("surname="+currentWord)
        features.append(case)
        if (position-1) > 0:
            features.append("prevWord=" + words[position-1] + ',' + case)

        return features



    """
    getCharsFeature
    """
    def getCharsFeature(self, currentWord):
        firstLetterCapital = False
        allCapitals = True
        mixedCapitals = False
        hasNumeric = False
        allNumeric = True
        weirdStuff = False

        cnt = 0
        for c in currentWord:
            allNumeric &= self.isNumeric(c)
            hasNumeric |= self.isNumeric(c)
            if not self.isCapital(c):
                allCapitals = False
            if cnt==0:
                firstLetterCapital = self.isCapital(c)
            if (cnt>0):
                mixedCapitals |= self.isCapital(c)

            weirdStuff |= not self.isAlphaNumeric(c)
            cnt += 1

        if (weirdStuff):
            charsFeature = "case=Weird"
        elif (allNumeric):
            charsFeature = "case=Numeric"
        elif (hasNumeric):
            charsFeature = "case=MixedNumeric"
        elif (allCapitals):
            charsFeature = "case=Capitals"
        elif (mixedCapitals):
            charsFeature = "case=Mixed"
        elif (firstLetterCapital):
            charsFeature = "case=Title"
        else:
            charsFeature = "case=Lower"
        return charsFeature;

    def isAlphaNumeric(self, c):
        return self.isNumeric(c) or self.isCapital(c) or self.isLower(c)

    def isNumeric(self, c):
        return self.re_is_numeric.search(c) is not None


    def isCapital(self, c):
        return self.re_is_upper_char.search(c) is not None

    def isLower(self, c):
        return self.re_is_lower_char.search(c) is not None


    """ Do not modify this method """
    def readData(self, filename):
        data = []

        for line in open(filename, 'r'):
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data

    """ Do not modify this method """
    def readTestData(self, ch_aux):
        data = []

        for line in ch_aux.splitlines():
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data


    """ Do not modify this method """
    def setFeaturesTrain(self, data):
        newData = []
        words = []

        for datum in data:
            words.append(datum.word)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        previousLabel = "O"
        for i in range(0, len(data)):
            datum = data[i]

            newDatum = Datum(datum.word, datum.label)
            newDatum.features = self.computeFeatures(words, previousLabel, i)
            newDatum.previousLabel = previousLabel
            newData.append(newDatum)

            previousLabel = datum.label

        return newData

    """
    Compute the features for all possible previous labels
    for Viterbi algorithm. Do not modify this method
    """
    def setFeaturesTest(self, data):
        newData = []
        words = []
        labels = []
        labelIndex = {}

        for datum in data:
            words.append(datum.word)
            if not labelIndex.has_key(datum.label):
                labelIndex[datum.label] = len(labels)
                labels.append(datum.label)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        for i in range(0, len(data)):
            datum = data[i]

            if i == 0:
                previousLabel = "O"
                datum.features = self.computeFeatures(words, previousLabel, i)

                newDatum = Datum(datum.word, datum.label)
                newDatum.features = self.computeFeatures(words, previousLabel, i)
                newDatum.previousLabel = previousLabel
                newData.append(newDatum)
            else:
                for previousLabel in labels:
                    datum.features = self.computeFeatures(words, previousLabel, i)

                    newDatum = Datum(datum.word, datum.label)
                    newDatum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum.previousLabel = previousLabel
                    newData.append(newDatum)

        return newData

    """
    write words, labels, and features into a json file
    Do not modify this method
    """
    def writeData(self, data, filename):
        outFile = open(filename + '.json', 'w')
        for i in range(0, len(data)):
            datum = data[i]
            jsonObj = {}
            jsonObj['_label'] = datum.label
            jsonObj['_word']= base64.b64encode(datum.word)
            jsonObj['_prevLabel'] = datum.previousLabel

            featureObj = {}
            features = datum.features
            for j in range(0, len(features)):
                feature = features[j]
                featureObj['_'+feature] = feature
            jsonObj['_features'] = featureObj

            outFile.write(json.dumps(jsonObj) + '\n')

        outFile.close()

