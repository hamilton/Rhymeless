# -*- coding: utf-8 -*-
import os
import string
from math import log
from random import sample, random, randint

class IdeaManager(object):
	def __init__(self):
		self.ideas = set(os.listdir('data/'))
		

class ContextUtilityBelt(object):
	"""
	A collection of functions used for specific applications, separate
	from the main Contextless class.  These include sql inserts and updates.
	"""
	def __init__(self):
		pass


class Contextless(ContextUtilityBelt, IdeaManager):
	"""
	Class needs a train() and walk() method.
	train() should take text nd build a bigram and trigram out of it.
	"""
	def __init__(self):
		
		ContextUtilityBelt.__init__(self)
		IdeaManager.__init__(self)
		
		self.firsts = {}
		self.unigram = {}
		self.bigram = {}
		self.trigram = {}
		
		self.walk_methods = set(['naive', 'a1', 'a*'])
	
	
	def train(self, text):
		# clean the text.  Build the frequencies.
		text = text.split('.')
		for elem in text:
			
			elem = self._clean_text(elem)
			elem = [word for word in elem if word != '']
			
			for i, word in enumerate(elem):
				
				bigram = elem[i:i+2]
				trigram = elem[i:i+3]
				unigram = elem[i]
				
				if i == 1 and elem[i]  != '.':
					
					self._train_first(elem[1])
				
				self._train_unigram(unigram)
				if len(bigram) == 2:
					self._train_bigram(bigram)
				if len(trigram) == 3:
					self._train_trigram(trigram)
	
	
	def generate_sentence(self, method = 'naive', style="tweet"):
		#if method in self.walk_methods:
		# sample from the first word distribution.
		
		args = {
			'style' : style,
			'words' : 0,
			'characters' : 0
		}
		
		STYLES = {
			"tweet" : lambda ARGS: ARGS['characters'] <=140,
			"whatever" : lambda ARGS: True,
			"length" : lambda ARGS: ARGS['words'] <= abs(self.average_length + randint(-5,5)),
		}
		
		LENGTH = 0
		
		sentence = []
		
		first_word = self._sample(self.firsts)
		second_word = self._sample(self.bigram[first_word])
		
		sentence.append(first_word)
		sentence.append(second_word)
		
		args['characters'] = len(' '.join(sentence))
		args['words'] = len([word for word in sentence if word != "." and word != '^'])
		
		next_word = ''
		
		while STYLES[style](args) and next_word != '.':
			
			if first_word in self.trigram and second_word in self.trigram[first_word]:
				next_word = self._sample(self.trigram[first_word][second_word])
			elif second_word in self.bigram:
				next_word = self._sample(self.bigram[second_word])
			sentence.append(next_word)
			first_word = second_word
			second_word = next_word
			args['characters'] = len(' '.join(sentence))
			args['words'] = len([word for word in sentence if word != "." and word != '^'])
			
		sentence = ' '.join(sentence[0:-1])
		return ''.join([sentence, '.'])
	
	#################################################
	# Private helper methods		                #
	#################################################
	
	def _is_not_punct(self, char):
		return char not in '!"#$%&\'()*+-./:;<=>?@[\\]^_`{|}~' + '\n\t\r'
	
	def _clean_text(self, elem):
		"""
		Preprocesses text for training through string methods.
		"""
		elem = elem.strip()
		elem = elem.lower()
		elem = elem.replace('mr.', 'mr').replace('mrs.', 'mrs').replace('ms.', 'ms').replace('etc.', 'etc')
		elem = elem.split()
		names = [(i, name) for i, name in enumerate(elem) if name[0] == "@"]
		for i, word in names:
			elem[i] = "PERSON"
		elem = ' '.join(elem)
		# attempt to add commas and other punctuation to the mix.
		elem = filter(self._is_not_punct, elem)
		elem = elem.replace(',', ' ,')
		elem = elem.split()
		elem.insert(0, '^')
		elem.append('.')
		return elem
	
	def _train_first(self, word):
		if word not in self.firsts:
			self.firsts[word] = 0
		self.firsts[word] += 1
	
	def _train_unigram(self, unigram):
		if unigram not in self.unigram:
			self.unigram[unigram] = 0
		self.unigram[unigram] += 1
	
	def _train_bigram(self, bigram):
		if len(bigram) == 2:
			# teach the model this bigram.
			first, second = bigram[0], bigram[1]
			if first not in self.bigram:
				self.bigram[first] = {}
			if second not in self.bigram[first]:
				self.bigram[first][second] = 0
			self.bigram[first][second] =+ 1
	
	def _train_trigram(self, trigram):
		if len(trigram) == 3:
			# now teach the model this bigram.
			first, second, third = trigram[0], trigram[1], trigram[2]
			if first not in self.trigram:
				self.trigram[first] = {}
			if second not in self.trigram[first]:
				self.trigram[first][second] = {}
			if third not in self.trigram[first][second]:
				self.trigram[first][second][third] = 0
			self.trigram[first][second][third] += 1
	
	def _sample(self, d):
		m = sum(d[k] for k in d)
		d = dict((k, log(d[k]) - log(m)) for k in d)
		candidate = None
		while candidate == None:
			current_sample = sample(d, 1)[0]
			r = log(random())
			if d[current_sample] > r:
				candidate = current_sample
			else:
				candidate = None
		return candidate

def main():
	'''
	import sqlite3
	db = sqlite3.connect('data/test')
	c = db.cursor()
	c.execute("""SELECT tweet from tweets""")
	data = c.fetchall()
	monster = Contextless()
	for (datum,) in data:
		monster.train(datum)
	print "done training."
	for i in xrange(30):
		print monster.generate_sentence()
	'''
	book = open('books/zara.txt')
	lines = []
	for line in book:
		lines.append(line)
	book.close()
	book = ' '.join(lines)
	monster = Contextless()
	monster.train(book)
	for i in xrange(5):
		print "W:", monster.generate_sentence(style="whatever")
		print "T:", monster.generate_sentence(style="tweet")
		print "-"*80

if __name__ == '__main__':
	main()
