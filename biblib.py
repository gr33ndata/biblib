# Python library for parsing .bib files

import re

class BibLex:

	def __init__(self, data='', grammar={}):
		self.data = data
		self.grammar = grammar
	
	def parse(self):
		i = 0
		while True:
			for key in self.grammar:
				#print self.data[i:5], '...'
				match = re.search(self.grammar[key], self.data[i:])
				if match:
					#print 'Match Start-End:', match.start(0), match.end(0)
					print key, '=>', match.string[match.start(0):match.end(0)]
					i += match.end(0)
					if i == len(self.data):
						return
	
	
class Bib:

	def __init__(self, filename=''):
		self.file_name = filename

	def load(self):
		fd = open(self.file_name, 'r')
		file_data = fd.read()
		self.parse(file_data)
		fd.close()

	def parse(self, file_data):
		grammar = {
			'@': r'^@',
			'=': r'^=',
			'{': r'^{',
			'}': r'^}',
			',': r'^,',
			'STR': r'^[a-zA-Z0-9\-\s\:\.\(\)\\\"\']+'
		}
		lex = BibLex(file_data, grammar)
		lex.parse()

if __name__ == '__main__':

	b = Bib('siri.bib')
	b.load()
