import collections
import copy
import optparse

from ling.Tree import Tree
import ling.Trees as Trees
import pennParser.EnglishPennTreebankParseEvaluator as \
        EnglishPennTreebankParseEvaluator
import io.PennTreebankReader as PennTreebankReader
import io.MASCTreebankReader as MASCTreebankReader


class Parser:

    def train(self, train_trees):
        pass

    def get_best_parse(self, sentence):
        """
        Should return a Tree
        """
        pass


class BaselineParser(Parser):

    def train(self, train_trees):
    ##############################
        prebinary_trees = copy.deepcopy(train_trees)
        binary_trees = map(TreeAnnotations.annotate, prebinary_trees)

        self.grammar = Grammar(binary_trees)
        self.lexicon = Lexicon(binary_trees)

        self.backoff = BackoffParser(train_trees)
    ##############################

    def get_best_parse(self, sentence):
        stotal = len(sentence)
        srange = xrange(stotal + 1)

        binaries = self.grammar.binary_rules_by_left_child
        unaries = self.grammar.unary_rules_by_child

        score = [[collections.defaultdict(lambda:0) for x in srange] for y in srange]
        trace = [[collections.defaultdict(lambda:0) for x in srange] for y in srange]


        # initially fill low level mappings
        for i in range(0, stotal):
            scoreCell = score[i][i + 1]
            traceCell = trace[i][i + 1]
            word = sentence[i]

            for tag in self.lexicon.get_all_tags():
                prob = self.lexicon.score_tagging(word, tag)
                traceCell[tag] = [True, word, tag]
                scoreCell[tag] = prob

            # check for unary rewrites
            added = True
            while added:
                added = False

                for rules in unaries.values():
                    for rule in rules:

                        if scoreCell[rule.child] > 0:
                            prob = rule.score * scoreCell[rule.child]

                            if prob > scoreCell[rule.parent]:
                                traceCell[rule.parent] = [False, [[i, i + 1, tag]], rule.parent]
                                scoreCell[rule.parent] = prob
                                added = True


        # check for upper cells of triangle
        for span in range(2, stotal + 1):
            for begin in range(0, stotal + 1 - span):
                end = begin + span

                scoreCell = score[begin][end]
                traceCell = trace[begin][end]

                for split in range(begin + 1, end):
                    for rules in binaries.values():
                        for rule in rules:

                            leftProb = score[begin][split][rule.left_child]
                            prob = leftProb * score[split][end][rule.right_child] * rule.score

                            if prob > scoreCell[rule.parent]:
                                children = [[begin, split, rule.left_child], [split, end, rule.right_child]]
                                traceCell[rule.parent] = [False, children, rule.parent]
                                scoreCell[rule.parent] = prob

                # again check for unary rewrites
                added = True
                while added:
                    added = False

                    for rules in unaries.values():
                        for rule in rules:
                            prob = rule.score * scoreCell[rule.child]

                            if prob > scoreCell[rule.parent]:
                                traceCell[rule.parent] = [False, [[begin, end, rule.child]], rule.parent]
                                scoreCell[rule.parent] = prob
                                added = True

        return self.buildGuard(trace, stotal, sentence)

    def buildGuard(self, trace, leng, sentence):
        try:
            topLevel = trace[0][leng]['ROOT^ROOT']
            tree = self.buildTree(topLevel, trace)
        except:
            print '=====BACKING OFF====='
            tree = self.backoff.get_best_parse(sentence)

        return TreeAnnotations.unannotate_tree(tree)

    def buildTree(self, node, trace):
        (terminal, nodes, thetag) = node

        if terminal == False:
            trees = [self.buildTree(trace[st][en][tag], trace) for st, en, tag in nodes]
        else:
            lastTree = Tree(nodes)
            trees = [lastTree]

        return Tree(thetag, trees)




class BackoffParser(BaselineParser):
    def __init__(self, train_trees):
    ##############################
        prebinary_trees = copy.deepcopy(train_trees)
        binary_trees = [TreeAnnotations.annotate(tree, 'ROOT', False) for tree in prebinary_trees]

        self.grammar = Grammar(binary_trees)
        self.lexicon = Lexicon(binary_trees)
    ##############################

    def buildGuard(self, trace, leng, sentence):
        return self.buildTree(trace[0][leng]['ROOT'], trace)


class PCFGParser(BaselineParser):
    pass


class TreeAnnotations:

    @classmethod
    def annotate(cls, tree, label = 'ROOT', mark = True):
        if tree.is_leaf() or (tree.children[0].is_leaf() and len(tree.children) == 1): return tree
        subtrees = tree.children

        if len(subtrees) > 2:
            first = subtrees.pop(0)
            newLabel = '@%s->%s' % (tree.label, first.label)

            newTree = Tree(newLabel, subtrees)
            subtrees = [first, newTree]

        subtrees = [TreeAnnotations.annotate(subtree, tree.label, mark) for subtree in subtrees]
        if mark: return Tree('%s^%s' % (tree.label, label), subtrees)
        else: return Tree(tree.label, subtrees)


    @classmethod
    def at_filter(cls, string):
        return string.startswith('@')

    @classmethod
    def unannotate_tree(cls, annotated_tree):
        debinarized_tree = Trees.splice_nodes(annotated_tree, TreeAnnotations.at_filter)
        unannotated_tree = Trees.FunctionNodeStripper.transform_tree(debinarized_tree)
        return unannotated_tree

class Lexicon:
    """
    Simple default implementation of a lexicon, which scores word,
    tag pairs with a smoothed estimate of P(tag|word)/P(tag).

    Instance variables:
    word_to_tag_counters
    total_tokens
    total_word_types
    tag_counter
    word_counter
    type_tag_counter
    """

    def __init__(self, train_trees):
        """
        Builds a lexicon from the observed tags in a list of training
        trees.
        """
        self.total_tokens = 0.0
        self.total_word_types = 0.0
        self.word_to_tag_counters = collections.defaultdict(lambda: \
                collections.defaultdict(lambda: 0.0))
        self.tag_counter = collections.defaultdict(lambda: 0.0)
        self.word_counter = collections.defaultdict(lambda: 0.0)
        self.type_to_tag_counter = collections.defaultdict(lambda: 0.0)

        for train_tree in train_trees:
            words = train_tree.get_yield()
            tags = train_tree.get_preterminal_yield()
            for word, tag in zip(words, tags):
                self.tally_tagging(word, tag)


    def tally_tagging(self, word, tag):
        if not self.is_known(word):
            self.total_word_types += 1
            self.type_to_tag_counter[tag] += 1
        self.total_tokens += 1
        self.tag_counter[tag] += 1
        self.word_counter[word] += 1
        self.word_to_tag_counters[word][tag] += 1


    def get_all_tags(self):
        return self.tag_counter.keys()


    def is_known(self, word):
        return word in self.word_counter


    def score_tagging(self, word, tag):
        p_tag = float(self.tag_counter[tag]) / self.total_tokens
        c_word = float(self.word_counter[word])
        c_tag_and_word = float(self.word_to_tag_counters[word][tag])
        if c_word < 10:
            c_word += 1
            c_tag_and_word += float(self.type_to_tag_counter[tag]) \
                    / self.total_word_types
        p_word = (1.0 + c_word) / (self.total_tokens + self.total_word_types)
        p_tag_given_word = c_tag_and_word / c_word
        return p_tag_given_word / p_tag * p_word


class Grammar:
    """
    Simple implementation of a PCFG grammar, offering the ability to
    look up rules by their child symbols.  Rule probability estimates
    are just relative frequency estimates off of training trees.

    self.binary_rules_by_left_child
    self.binary_rules_by_right_child
    self.unary_rules_by_child
    """

    def __init__(self, train_trees):
        self.unary_rules_by_child = collections.defaultdict(lambda: [])
        self.binary_rules_by_left_child = collections.defaultdict(
                lambda: [])
        self.binary_rules_by_right_child = collections.defaultdict(
                lambda: [])

        unary_rule_counter = collections.defaultdict(lambda: 0)
        binary_rule_counter = collections.defaultdict(lambda: 0)
        symbol_counter = collections.defaultdict(lambda: 0)

        for train_tree in train_trees:
            self.tally_tree(train_tree, symbol_counter,
                    unary_rule_counter, binary_rule_counter)
        for unary_rule in unary_rule_counter:
            unary_prob = float(unary_rule_counter[unary_rule]) \
                    / symbol_counter[unary_rule.parent]
            unary_rule.score = unary_prob
            self.add_unary(unary_rule)
        for binary_rule in binary_rule_counter:
            binary_prob = float(binary_rule_counter[binary_rule]) \
                    / symbol_counter[binary_rule.parent]
            binary_rule.score = binary_prob
            self.add_binary(binary_rule)


    def __unicode__(self):
        rule_strings = []
        for left_child in self.binary_rules_by_left_child:
            for binary_rule in self.get_binary_rules_by_left_child(
                    left_child):
                rule_strings.append(str(binary_rule))
        for child in self.unary_rules_by_child:
            for unary_rule in self.get_unary_rules_by_child(child):
                rule_strings.append(str(unary_rule))
        return "%s\n" % "".join(rule_strings)


    def add_binary(self, binary_rule):
        self.binary_rules_by_left_child[binary_rule.left_child].\
                append(binary_rule)
        self.binary_rules_by_right_child[binary_rule.right_child].\
                append(binary_rule)


    def add_unary(self, unary_rule):
        self.unary_rules_by_child[unary_rule.child].append(unary_rule)


    def get_binary_rules_by_left_child(self, left_child):
        return self.binary_rules_by_left_child[left_child]


    def get_binary_rules_by_right_child(self, right_child):
        return self.binary_rules_by_right_child[right_child]


    def get_unary_rules_by_child(self, child):
        return self.unary_rules_by_child[child]


    def tally_tree(self, tree, symbol_counter, unary_rule_counter,
            binary_rule_counter):
        if tree.is_leaf():
            return
        if tree.is_preterminal():
            return
        if len(tree.children) == 1:
            unary_rule = self.make_unary_rule(tree)
            symbol_counter[tree.label] += 1
            unary_rule_counter[unary_rule] += 1
        if len(tree.children) == 2:
            binary_rule = self.make_binary_rule(tree)
            symbol_counter[tree.label] += 1
            binary_rule_counter[binary_rule] += 1
        if len(tree.children) < 1 or len(tree.children) > 2:
            raise Exception("Attempted to construct a Grammar with " \
                    + "an illegal tree (most likely not binarized): " \
                    + str(tree))
        for child in tree.children:
            self.tally_tree(child, symbol_counter, unary_rule_counter,
                    binary_rule_counter)


    def make_unary_rule(self, tree):
        return UnaryRule(tree.label, tree.children[0].label)


    def make_binary_rule(self, tree):
        return BinaryRule(tree.label, tree.children[0].label,
                tree.children[1].label)


class BinaryRule:
    """
    A binary grammar rule with score representing its probability.
    """

    def __init__(self, parent, left_child, right_child):
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.score = 0.0


    def __str__(self):
        return "%s | %s -> %s %% %s" % (self.parent, self.left_child, self.right_child, self.score)


    def __hash__(self):
        result = hash(self.parent)
        result = 29 * result + hash(self.left_child)
        result = 29 * result + hash(self.right_child)
        return result


    def __eq__(self, o):
        if self is o:
            return True

        if not isinstance(o, BinaryRule):
            return False

        if (self.left_child != o.left_child):
            return False
        if (self.right_child != o.right_child):
            return False
        if (self.parent != o.parent):
            return False
        return True


class UnaryRule:
    """
    A unary grammar rule with score representing its probability.
    """

    def __init__(self, parent, child):
        self.parent = parent
        self.child = child
        self.score = 0.0

    def __str__(self):
        return "%s | %s %% %s" % (self.parent, self.child, self.score)

    def __hash__(self):
        result = hash(self.parent)
        result = 29 * result + hash(self.child)
        return result

    def __eq__(self, o):
        if self is o:
            return True

        if not isinstance(o, UnaryRule):
            return False

        if (self.child != o.child):
            return False
        if (self.parent != o.parent):
            return False
        return True


MAX_LENGTH = 20

def test_parser(parser, test_trees):
    evaluator = EnglishPennTreebankParseEvaluator.LabeledConstituentEval(
            ["ROOT"], set(["''", "``", ".", ":", ","]))
    for test_tree in test_trees:
        test_sentence = test_tree.get_yield()
        if len(test_sentence) > 20:
            continue
        guessed_tree = parser.get_best_parse(test_sentence)
        print "Guess:\n%s" % Trees.PennTreeRenderer.render(guessed_tree)
        print "Gold:\n%s" % Trees.PennTreeRenderer.render(test_tree)
        evaluator.evaluate(guessed_tree, test_tree)
    print ""
    return evaluator.display(True)


def read_trees(base_path, low=None, high=None):
    trees = PennTreebankReader.read_trees(base_path, low, high)
    return [Trees.StandardTreeNormalizer.transform_tree(tree) \
        for tree in trees]


def read_masc_trees(base_path, low=None, high=None):
    print "Reading MASC from %s" % base_path
    trees = MASCTreebankReader.read_trees(base_path, low, high)
    return [Trees.StandardTreeNormalizer.transform_tree(tree) \
        for tree in trees]


if __name__ == '__main__':
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--path", dest="path",
            default="../data/parser")
    opt_parser.add_option("--data", dest="data", default = "masc")
    opt_parser.add_option("--parser", dest="parser",
            default="BaselineParser")
    opt_parser.add_option("--maxLength", dest="max_length",
            default="20")
    opt_parser.add_option("--testData", dest="test_data", default="")

    (options, args) = opt_parser.parse_args()
    options = vars(options)

    print "PCFGParserTest options:"
    for opt in options:
        print "  %-12s: %s" % (opt, options[opt])
    print ""
    MAX_LENGTH = int(options['max_length'])

    parser = globals()[options['parser']]()
    print "Using parser: %s" % parser.__class__.__name__

    base_path = options['path']
    pre_base_path = base_path
    data_set = options['data']
    if not base_path.endswith('/'):
        base_path += '/'

    print "Data will be loaded from: %s" % base_path

    train_trees = []
    validation_trees = []
    test_trees = []

    if data_set == 'miniTest':
        base_path += 'parser/%s' % data_set

        # training data: first 3 of 4 datums
        print "Loading training trees..."
        train_trees = read_trees(base_path, 1, 3)
        print "done."

        # test data: last of 4 datums
        print "Loading test trees..."
        test_trees = read_trees(base_path, 4, 4)
        print "done."

    if data_set == "masc":
        base_path += "parser/"

        # training data: MASC train
        print "Loading MASC training trees... from: %smasc/train" % base_path
        train_trees.extend(read_masc_trees("%smasc/train" % base_path, 0, 38))
        print "done."
        print "Train trees size: %d" % len(train_trees)
        print "First train tree: %s" % \
                Trees.PennTreeRenderer.render(train_trees[0])
        print "Last train tree: %s" % \
                Trees.PennTreeRenderer.render(train_trees[-1])

        # test data: MASC devtest
        print "Loading MASC test trees..."
        test_trees.extend(read_masc_trees("%smasc/devtest" % base_path, 0, 11))
        #test_trees.extend(read_masc_trees("%smasc/blindtest" % base_path, 0, 8))
        print "done."
        print "Test trees size: %d" % len(test_trees)
        print "First test tree: %s" % \
                Trees.PennTreeRenderer.render(test_trees[0])
        print "Last test tree: %s" % \
                Trees.PennTreeRenderer.render(test_trees[-1])


    if data_set not in ["miniTest", "masc"]:
        raise Exception("Bad data set: %s: use miniTest or masc." % data_set)

    print ""
    print "Training parser..."
    parser.train(train_trees)

    print "Testing parser"
    test_parser(parser, test_trees)