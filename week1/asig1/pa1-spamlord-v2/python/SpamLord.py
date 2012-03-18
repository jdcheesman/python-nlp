import sys
import os
import re
import pprint

text_filter_stanford = 'stanford'
text_filter_edu = 'edu'

email_pat_1 = '(\w+\.?\w+)@(\w+\.?\w+)\.(\w{2,3})\W+'
email_pat_4 = 'obfuscate\W+([\w\W]+edu)\W+(\w+)'


tel_pat_1 = '[(]?(\d{3})[)]?[- ]{1}(\d{3})[- ]{1}(\d{4})'
tel_pat_2 = '[(](\d{3})[)](\d{3})[- ]{1}(\d{4})'

excluded_pat_1 = '<title>403 forbidden</title>'
excluded_pat_2 = '<title>404 not found</title>'

""" 
TODO
This function takes in a filename along with the file object (or
an iterable of strings) and scans its contents against regex patterns.
It returns a list of (filename, type, value) tuples where type is either
and 'e' or a 'p' for e-mail or phone, and value is the formatted phone
number or e-mail.  The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (name))
    res = []
    http_error_403 = re.compile(excluded_pat_1)
    http_error_404 = re.compile(excluded_pat_2)
    obfuscate_re = re.compile(email_pat_4)

    re_filter_stanford = re.compile(text_filter_stanford)
    re_filter_edu = re.compile(text_filter_edu)

    has_2_3_letter_string = re.compile('\W+[a-z]{2,3}\W+')

    # Improvements (TODO)
    #
    # 1: Rolling, 3 element list of lines, concat and pass filters again (check for line-feed straddling emails, tel numbers)
    # 2: 1-800-ILOVEYOU type numbers
    # 3: HTML library for normalising text
    # 4: Generalise for all domains, not just EDU and COM - DONE
    # 5: Include other http error codes
 

    for line in f:
        # Basic normalisation:
        line = line.lower()

        # Following condition excludes HTML error responses.
        # If found, we stop processing the file:
        if http_error_403.search(line) or http_error_404.search(line):
            return res

        ###############################
        # Telephones
        ###############################        
        run_pattern_tel(name, line, tel_pat_1, res)
        run_pattern_tel(name, line, tel_pat_2, res)

        ###############################
        # email normalisation
        ###############################
        # HTML normalisation
        line = line.replace('&amp;', '&')
        line = line.replace('&lt;', '<')
        line = line.replace('&gt;', '>')
        line = line.replace('&ldquo;', '"')
        line = line.replace('%20', ' ')

        # fragile (data file dlwh)
        line = line.replace('-', '')

        if has_2_3_letter_string.search(line):
            # Normalise @ sign:
            line = line.replace(' at ', '@')
            line = line.replace(' where ', '@')
            line = line.replace('&#x40;', '@')
            line = line.replace(' @ ', '@')

            # fragile (data file ouster)
            line = line.replace(' (followed by "', '')

            # dot text substitutes
            line = line.replace(' dot ', '.')        
            line = line.replace(' dt ', '.')
            line = line.replace(' dom ', '.')

            # fragile (data file jks):
            line = line.replace(';', '.')

            # match all lines that contain stanford AND edu (probable emails):
            # fragile (data file pal)
            if re_filter_stanford.search(line) and re_filter_edu.search(line):
               line = line.replace(' ', '.')

            # obfuscate method, fragile:
            if obfuscate_re.search(line):
                matches = obfuscate_re.findall(line)
                email = '%s@%s' % (matches[0][1], matches[0][0])
                res.append((name, 'e', email))
               
            # here's where we really get all the emails:
            run_pattern_email(name, line, email_pat_1, res) 

    return res

"""
Helper method to run email patterns and avoid code repetition
"""
def run_pattern_email(name, line, pattern, res):
    matches = re.findall(pattern,line)
    for m in matches:
            email = '%s@%s.%s' % m
            res.append((name,'e',email))
    

"""
Helper method to run telephone patterns and avoid code repetition
"""
def run_pattern_tel(name, line, pattern, res):
    matches = re.findall(pattern,line)
    for m in matches:
            phone = '%s-%s-%s' % m
            res.append((name, 'p', phone))

   
"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
          continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
