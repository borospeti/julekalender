#!/usr/bin/env python3

import re
import sys
import pyparsing as pp


class Parser:
    def __init__(self, patched=False):
        self.rules = {}
        self.sentences = []
        self.grammar = None
        self.patched = patched

    def lookup(self, rule_id):
        if rule_id not in self.rules:
            self.rules[rule_id] = pp.Forward()
            self.rules[rule_id].setName(rule_id)
            #self.rules[rule_id].setDebug(True)
        return self.rules[rule_id]

    def make_rule(self, token):
        if token[0] == '"':
            return pp.Literal(token.strip('"'))
        return self.lookup(token)

    def make_and(self, alternative):
        tokens = [self.make_rule(token) for token in re.split(r'\s+', alternative)]
        if len(tokens) > 1:
            return pp.And(tokens)
        else:
            return tokens[0]

    def make_match_first(self, alternatives):
        alts = [self.make_and(alternative) for alternative in alternatives]
        if len(alts) > 1:
            return pp.MatchFirst(alts)
        else:
            return alts[0]

    def load(self, filename):
        with open(filename) as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                rule = re.split(r'\s*[:|]\s*', line)
                body = self.make_match_first(rule[1:])
                if rule[0] in self.rules:
                    self.rules[rule[0]] <<= body
                else:
                    self.rules[rule[0]] = body
            while True:
                line = f.readline().strip()
                if not line:
                    break
                self.sentences.append(line)
        self.grammar = self.lookup('0')
        self.grammar.validate()

    def parse(self, sentence):
        if not self.patched:
            return self.grammar.parseString(sentence, parseAll=True)
        # hack to allow rule 8 to work properly
        # MatchFirst goes for the first match (left to right), Or, goes for the longest.
        # In some cases, none of these are ok, but there is no backtracking.
        rule_8 = self.lookup('8')
        for i in range(1,6):
            rule_8 <<= self.lookup('42') * i
            try:
                return self.grammar.parseString(sentence, parseAll=True)
            except pp.ParseException as e:
                error = e
        raise error

    def parse_all(self):
        for sentence in self.sentences:
            try:
                yield (sentence, self.parse(sentence))
            except pp.ParseException:
                yield (sentence, None)

    def test(self, sentence):
        return self.grammar.runTests(sentence)


#parser = Parser()
#parser.load('midi-patched.txt')
#print(parser.test('bbabbbbaabaabba'))
#print(parser.parse('aaabbbbbbaaaabaababaabababbabaaabbababababaaa'))
#print(parser.parse('aaabbb'))
#sys.exit(1)

#print('part 1')
#parser = Parser()
#parser.load('input.txt')

print('part 2')
parser = Parser(patched=True)
parser.load('patched.txt')

count = 0
for sentence, parsed in parser.parse_all():
    print(sentence, parsed)
    if parsed:
        count += 1
print(count)
