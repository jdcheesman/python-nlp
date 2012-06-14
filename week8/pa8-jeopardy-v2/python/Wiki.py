import sys, traceback

import re

import nltk
from nltk.corpus import names


class Wiki:

    def get_element(self, line):
      name = line.split('\b')[0].strip()
      clean_name = ''
      non_alpha = False
      for c in name:
        if (c != ' ' and c != '.' and c != '"') and re.search('\W', c):
          non_alpha = True
        if not non_alpha:
          clean_name += c
      return clean_name.strip()

    def get_spouse(self, line):
      spouses = line.split('<br>')
      result = []
      for cnt, spouse in enumerate(spouses):
        if cnt == 0:
          spouse = spouse.partition('=')[2]
        spouse = spouse.replace('[', '')
        spouse = spouse.replace(']', '')
        if spouse.find('|') > 0:
            spouse = spouse.split('|')[1]
        spouse = self.get_element(spouse)
        result.append(spouse)
        if spouse.find('"') > 0:
            new_spouse = ''
            inside_quotes = False
            for c in spouse:
                if c == '"':
                  inside_quotes = not inside_quotes
                elif not inside_quotes:
                    new_spouse += c
            new_spouse = new_spouse.replace('  ', ' ')
            print new_spouse
            result.append(new_spouse)



      #print result
      return result

    def process_infobox(self, f):
      infobox = re.compile('{{\s*infobox')
      start_element = re.compile('{{')
      end_element = re.compile('}}')

      indent_level = 0
      in_box = False

      relations = {}
      clean_name = ''
      birthname = ''
      clean_spouse = []
      for cnt, line in enumerate(f):
        line = line.replace('&amp;', '&')
        line = line.replace('&quot;', '"')
        line = line.replace('&lt;', '<')
        line = line.replace('&gt;', '>')
        line = line.replace('&ldquo;', '"')
        line = line.replace('%20', ' ')
        line = line.strip()

        if infobox.search(line.lower()):
          if clean_name == '':
            clean_name = birthname
          if cnt != 0:
            if not clean_name in relations:
              relations[clean_name] = []
            relations[clean_name].extend(clean_spouse)

          clean_name = ''
          birthname = ''
          clean_spouse = []
          in_box = True

        if in_box:
          indent_level += len(start_element.findall(line))
          indent_level -= len(end_element.findall(line))


        if indent_level == 0:
          in_box = False

        if in_box:
          #print '%d:%d\t%s' % (cnt, indent_level, line)
          if re.search(r'[|]\s*name\s*\=', line.lower()):
            line = line.partition('=')[2]
            clean_name = self.get_element(line)
          if re.search(r'[|]\s*birthname\s*\=', line.lower()):
            line = line.partition('=')[2]
            birthname = self.get_element(line)
          if re.search('^\s*[|]\s*spouse\s*[=]', line.lower()):
            clean_spouse = self.get_spouse(line)

      print relations
      self.relations = relations

    def process_no_infobox(self, f):
      infobox = re.compile('{{\s*infobox')
      start_element = re.compile('{{')
      end_element = re.compile('}}')
      possible_name1 = re.compile('[\']{3}(.*)[\']{3}')
      possible_name2 = re.compile('[\[]{2}(.*)[\]]{2}')
      title = re.compile('<title>(.+)</title>')
      indent_level = 0
      in_box = False

      relations = {}

      current_title = 'unknown'
      possible_names = {}
      possible_names[current_title] = []
      # text_blocks = {}
      # text_blocks[current_title] = []

      for cnt, line in enumerate(f):
        line = line.replace('&amp;', '&')
        line = line.replace('&quot;', '"')
        line = line.replace('&lt;', '<')
        line = line.replace('&gt;', '>')
        line = line.replace('&ldquo;', '"')
        line = line.replace('%20', ' ')
        #line = line.strip()

        if infobox.search(line.lower()):
          in_box = True

        if in_box:
          indent_level += len(start_element.findall(line))
          indent_level -= len(end_element.findall(line))

        if indent_level == 0:
          in_box = False


        if not in_box:

          tmp = title.findall(line)
          if len(tmp) > 0:
            current_title = ' '.join(tmp).strip()
            print 'title: [%s]' % current_title
            # text_blocks[current_title] = []
            possible_names[current_title] = []

          # text_blocks[current_title].append(line)

          if len(tmp) == 0:
            tmp = possible_name1.findall(line)
          if len(tmp) == 0:
            tmp = possible_name2.findall(line)
          else:
            tmp.extend(possible_name2.findall(line))

          if len(tmp) > 0:
            for n in tmp:
              accept_name = True
              tmp_names = n.split()

              if len(tmp_names) > 1: # and tmp_names[0] in names.words():
                for w in tmp_names:
                  if not w.istitle() and (w[0].islower() or w[0].isdigit()):
                    accept_name = False

                if accept_name:
                  possible_names[current_title].append(n)
          current_name = ''
          is_bigram = False

          for w in line.split():

            if w.istitle():
              if current_name == '' and w in names.words():
                is_bigram = False
                current_name = w
              elif current_name != '':
                current_name += ' ' + w
                is_bigram = True
            else:
                if current_name != '' and is_bigram:
                    possible_names[current_title].append(current_name)
                    current_name = ''



      for key in possible_names.keys():
        possible_names[key] = list(set(possible_names[key]))
        relations[key] = []
        if len(possible_names[key]) == 0:
          del possible_names[key]
        else:
          relations[key] = []
          for tmpname in possible_names[key]:
            tmpname = tmpname.replace('[', '')
            tmpname = tmpname.replace(']', '')
            relations[key].append(tmpname)


        # get all the lines with words relating to marriage:
        # block_marriages = []
        # for line in text_blocks[key]:
        #   line = line.replace('[', '')
        #   line = line.replace(']', '')
        #   if line.find('married') > 0 or line.find('marriage') > 0:
        #     block_marriages.append(line)
        #   if line.find('wife') > 0 or line.find('husband') > 0:
        #     block_marriages.append(line)
        #   if line.find('divorce') > 0 or line.find('separation from') > 0:
        #     block_marriages.append(line)

        # for all the lines previously selected, check if any of our
        # possible names are in them:
        # for possible_marriage in block_marriages:
        #   if possible_marriage != '':
        #     for wife in possible_names[key]:
        #       if wife in possible_marriage:
        #         relations[key].append(wife)


      for key in relations.keys():
        print '=' * 10
        print key
        print relations[key]

      self.relations = relations

    # reads in the list of wives
    def addWives(self, wivesFile):
        try:
            input = open(wivesFile)
            wives = input.readlines()
            input.close()
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            sys.exit(1)
        return wives

    # read through the wikipedia file and attempts to extract the matching husbands. note that you will need to provide
    # two different implementations based upon the useInfoBox flag.
    def processFile(self, f, wives, useInfoBox):

        if useInfoBox:
            self.process_infobox(f)
        else:
            self.process_no_infobox(f)

        husbands = []

        # TODO:
        # Process the wiki file and fill the husbands Array
        # +1 for correct Answer, 0 for no answer, -1 for wrong answers
        # add 'No Answer' string as the answer when you dont want to answer
        for cnt, wife in enumerate(wives):
            print '%d:\t%s' % (cnt, wife)
            wife_added = False
            wife = wife.strip() # ooer missus
            for husband in self.relations:
                if wife in self.relations[husband] and not wife_added:
                    wife_added = True
                    husbands.append('Who is ' + husband + '?')
                else:
                    for candidate_wife in self.relations[husband]:
                        if wife in candidate_wife and not wife_added:
                            wife_added = True
                            husbands.append('Who is ' + husband + '?')

            if not wife_added:
                firstname = wife.split()[0].strip()
                for husband in self.relations:
                    arr = husband.split()
                    if len(arr) > 1:
                      surname = husband.split()[-1].strip()
                      fullname = firstname + ' ' + surname
                      for wife in self.relations[husband]:
                          if fullname in wife and not wife_added:
                              wife_added = True
                              husbands.append('Who is ' + husband + '?')

            if not wife_added:
                husbands.append('No Answer')

        f.close()
        for c, h in enumerate(husbands):
            print '%d:\t%s' % (c, h)

        return husbands

    # scores the results based upon the aforementioned criteria
    def evaluateAnswers(self, useInfoBox, husbandsLines, goldFile):
        correct = 0
        wrong = 0
        noAnswers = 0
        score = 0
        try:
            goldData = open(goldFile)
            goldLines = goldData.readlines()
            goldData.close()

            goldLength = len(goldLines)
            husbandsLength = len(husbandsLines)

            if goldLength != husbandsLength:
                print('Number of lines in husbands file should be same as number of wives!')
                sys.exit(1)
            for i in range(goldLength):
                if husbandsLines[i].strip() in set(goldLines[i].strip().split('|')):
                    correct += 1
                    score += 1
                elif husbandsLines[i].strip() == 'No Answer':
                    noAnswers += 1
                else:
                    print 'Wrong: %s' % husbandsLines[i].strip()
                    wrong += 1
                    score -= 1
        except IOError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
        if useInfoBox:
            print('Using Info Box...')
        else:
            print('No Info Box...')
        print('Correct Answers: ' + str(correct))
        print('No Answers: ' + str(noAnswers))
        print('Wrong Answers: ' + str(wrong))
        print('Total Score: ' + str(score))

if __name__ == '__main__':
    wikiFile = '../data/small-wiki.xml'
    wivesFile = '../data/wives.txt'
    goldFile = '../data/gold.txt'
    useInfoBox = True;
    wiki = Wiki()
    wives = wiki.addWives(wivesFile)
    husbands = wiki.processFile(open(wikiFile), wives, useInfoBox)
    wiki.evaluateAnswers(useInfoBox, husbands, goldFile)