#!/usr/bin/env python
# Python library for parsing .bib files

import re

VERBOSE = False


class BibLex:

    def __init__(self, data=''):
        self.data = data
        self.vocabulary = [
		    ('@', r'^@'),
		    ('=', r'^='),
		    ('{', r'^{'),
		    ('}', r'^}'),
		    (',', r'^,'),
            #('TITLE', r'^[\s]*[Tt]itle'),
            #('AUTHOR', r'^[\s]*[Aa]uthor'),
            #('YEAR', r'^[\s]*[Yy]ear'),
		    ('STR', r'''^[a-zA-Z0-9\-\s\:\.\(\)\\\"\']+'''),
        ]
        self.output = []
        
	
    def parse(self):
        i = 0
        while True:
            for vocab_item in self.vocabulary:
                match = re.search(vocab_item[1], self.data[i:])
                if match:
	                #print 'Match Start-End:', match.start(0), match.end(0)
                    k = vocab_item[0]
                    v = match.string[match.start(0):match.end(0)].strip()
                    #print (k,v)
                    self.output.append((k,v))
                    i += match.end(0)
                    if i == len(self.data):
                        return self.output
        # Probably, it will never reaches this return, but anyway
        return self.output



class BibYacc:
    
    def __init__(self, data=[]):	
        self.data = data
        print self.data[0:10], '\n'
        self.grammar_zip = [
            ('BSTR', ('{', 'STR', '}'),(1)),
            ('@TYPE', ('@', 'STR'),(1),(1)),
            ('ASSIGN', ('STR', '=', 'BSTR'),(1)),
            ('ASSIGN', ('STR', '=', 'STR'),(1)),
            ('ASSIGNS', ('ASSIGN', ',', 'ASSIGN'),(10)),
        ]
        self.grammar = []
        for gz_item in self.grammar_zip:
            for i in range(gz_item[2]):
                self.grammar.append((gz_item[0],gz_item[1]))
        print self.grammar
        self.output = []

    def match(self, gram_item, data_idx):
        if len(self.data[data_idx:]) < len(gram_item[1]):
            return False
        for i in range(len(gram_item[1])):
            if gram_item[1][i] != self.data[data_idx+i][0]:
                return False
        else:
            return True

    def _parse(self):
        #print self.data, len(self.data)
        i = 0
        while True:
            for gram_item in self.grammar:
                if self.match(gram_item, i):
                    print 'Yacc[', gram_item[0], ']', self.data[i:i+len(gram_item[1])]
                    i = i + len(gram_item[1])
                    continue
            i = i + 1
            #print i, len(self.data)
            if i >= len(self.data):
                return self.output
      
    def parse(self): 
        i = 0
        for gram_item in self.grammar:
            print gram_item, ':\n', self.data[0:40]
            while True:
                if i >=  min(20000,len(self.data)):
                    print i,  len(self.data)
                    self.data = self.output
                    self.output = []
                    i = 0 
                    break
                if self.match(gram_item, i):    
                    self.output.append((
                        gram_item[0], 
                        tuple(self.data[i:i+len(gram_item[1])])

                    ))
                    i = i + len(gram_item[1])
                else:
                    self.output.append(self.data[i])
                    i = i + 1
        print '\n\n========\n', self.output[0:5]

 
class Bib:

    def __init__(self, filename=''):
	    self.file_name = filename

    def load(self):
	    fd = open(self.file_name, 'r')
	    file_data = fd.read()
	    self.parse(file_data)
	    fd.close()

    def parse(self, file_data):
        lex = BibLex(file_data)
        o = lex.parse()
        #print o
        yacc = BibYacc(o)
        yacc.parse()

if __name__ == '__main__':

    b = Bib('siri.bib')
    b.load()
