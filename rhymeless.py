# -*- coding: utf-8 -*-
import os
import sys
import string
from math import log
from random import sample, random, randint
from rhuthmos.rhuthmos import Rhuthmos

class IdeaManager(object):
	def __init__(self):
		self.ideas = set(os.listdir('data/'))
		

class RhymelessUtilityBelt(object):
	def __init__(self):
		pass
	
	def _rhyme_gen(self):
		one_1, one_2 = None, None
		two_1, two_2 = None, None
		MINLENGTH = 3
		while True:
		
			one_1 = sample(self.lasts.keys(), 1)[0]
			# get all the words in last the rhyme with
			candidates_1 = self.find(one_1) & set(self.lasts.keys())
			if len(candidates_1) > 2:
				one_2 = sample(candidates_1, 1)[0]
				#print one_1, one_2, one_1 == one_2
				if one_2 == one_1: one_2 = None
			#sample(self.find(one_1), 1)
			
			if random() > .9:
				two_1 = sample(self.lasts.keys(), 1)[0]
				candidates_2 = self.find(two_1) & set(self.lasts.keys())
				
			else:
				two_1 = sample(self.firsts.keys(), 1)[0]
				candidates_2 = self.find(two_1) & set(self.firsts.keys())
				
			# get all the words in last the rhyme with
			if len(candidates_2) > 2:
				two_2 = sample(candidates_2, 1)[0]
				if two_2 == two_1: two_2 = None
			#sample(self.find(one_1), 1)
			
			if one_1 != None and one_2 != None and two_1 != None and two_2 != None and len(one_1) > MINLENGTH  and len(one_2) > MINLENGTH and len(two_1) > MINLENGTH and len(two_2) > MINLENGTH and one_1 != two_1:
				break
			else:
				one_1, one_2 = None, None
				two_1, two_2 = None, None
		return one_1, two_1, one_2, two_2
		
	
	def repair(self, data, method="deletion"):
		"""A wrapper function that selects from private, more complicated
		functions.
		
		method:
			deletion: deletes or adds one-syllable words to
			make the rhyme work.
		
		"""
		if method =="deletion":
			return self._deletion_repair(data)
	
	def count_syllables(self, list_of_text):
		if list_of_text != None or len(list_of_text) > 0 or len(w for w in list_of_text if w == None):
			return sum(len(self.word_meter(word)) for word in list_of_text)
		else:
			return 0
	



class Rhymeless(RhymelessUtilityBelt, IdeaManager, Rhuthmos):
	def __init__(self):
		
		RhymelessUtilityBelt.__init__(self)
		IdeaManager.__init__(self)
		Rhuthmos.__init__(self)
		self.initiate_dictionary()
		
		self.firsts = {}
		self.lasts = {}
		self.unigram = {}
		self.bigram = {}
		self.trigram = {}
	
	def train(self, text):
		text = text.split('.')
		for elem in text:
			if len(elem) > 2:
				elem = self._clean_text(elem)
				elem = [word for word in elem if word != '']
				elem.reverse()
				#print elem
				for i, word in enumerate(elem):
				
					bigram = elem[i:i+2]
					trigram = elem[i:i+3]
					unigram = elem[i]
					#print elem[i], i, len(elem)
					#print bigram, trigram, unigram
					if i == 1 and elem[i] != "^":
						self._train_last(elem[i])
						#print elem[i], '!!!!!!!!'
					if i == len(elem)-2 and elem[i] != '^':
						self._train_first(elem[i])
					self._train_unigram(unigram)
					if len(bigram) == 2:
						self._train_bigram(bigram)
					if len(trigram) == 3:
						self._train_trigram(trigram)
				#print self.firsts, self.lasts
	
	def generate_haiku(self):
		"""First version - keep sampling until a line is made."""
		first_line = None
		second_line = None
		third_line = None
		first_line = self._haiku_line(5)
		second_line = self._haiku_line(7)
		third_line = self._haiku_line(5)
		return '\n'.join([first_line, second_line, third_line])
		
	
	def _until_valid(self, method, obj, criterion_checker):
		"""
		Feed a criterion.
		"""
		criterion_not_met = True
		while criterion_not_met:
			candidate = method(obj)
			criterion_not_met = criterion_checker(candidate)
			#print candidate, criterion_not_met
		return candidate
		
	def _haiku_line(self, length):
		final_line = None
		
		while final_line == None:
			 
			line = []
			first_word = self._until_valid(self._sample, self.lasts, self.word_in_rhuthmos)
			print first_word
			#sys.exit()
			line.append(first_word)
			#print line
			#print self.word_meter(first_word)
			#print [self.word_meter(word) for word in line]
			line_length = self.count_syllables(line)
			original_line = line
			if line_length < length:
				# sample again.
				while line_length <= length:
					# keep sampling.
					next_word = self._sample(self.bigrams[first_word])
					line.append(next_word)
					line_length = self.count_syllables(line)
					first_word = next_word
			elif line_length == length:
				# we're done
				return line
			else:
				return self._haiku_line(length)
			
			################################################
			# Check line length.  If too long, start over. #
			################################################
			
			if line_length > length:
				final_line == None
				
			else:
				final_line = line
		return final_line
	
	def generate_poem(self, method = 'naive', style="whatever"):
		"""
		Generates a short 4-line poem.
		
		"""
		
		args = {
			'style' : style,
			'words' : 0,
			'characters' : 0,
			'poem' : randint(7,15)
		}
		
		STYLES = {
			"tweet" : lambda ARGS: 
				ARGS['characters'] <=140,
			"whatever" : lambda ARGS: 
				True,
			"length" : lambda ARGS: 
				ARGS['words'] <= abs(self.average_length + randint(-5,5)),
			"poem" : lambda ARGS: 
				ARGS['words'] <= ARGS['poem'] + randint(-3,3)
		}
		
		
		stanzas = []
		ends = self._rhyme_gen()
		#print ends
		for first_word in ends:
		############
			
			sentence = []
		
			#first_word = self._sample(self.lasts)
			second_word = self._sample(self.bigram[first_word])
			sentence.append(first_word)
			sentence.append(second_word)
		
			args['characters'] = len(' '.join(sentence))
			args['words'] = len([word for word in sentence if word != "." and word != '^'])
		
			next_word = ''
			
			######################################
			# Here's where we grow random vines. #
			######################################
			
			while STYLES[style](args) and first_word != "^" and second_word != '^' and next_word != '^':
				
				if first_word in self.trigram and second_word in self.trigram[first_word]:
					next_word = self._sample(self.trigram[first_word][second_word])
				elif second_word in self.bigram:
					next_word = self._sample(self.bigram[second_word])
				sentence.append(next_word)
				first_word = second_word
				second_word = next_word
				args['characters'] = len(' '.join(sentence))
				args['words'] = len([word for word in sentence if word != "." and word != '^'])
			
			sentence.reverse()
			sentence = sentence[1:]
			sentence = sentence[1:] if sentence[0] == ',' else sentence
			sentence = ' '.join(sentence)
			sentence = sentence.replace(' ,', ',')
			sentence = sentence.replace(' :', ':')
			sentence = sentence.replace(' ;', ';')
			stanzas.append(''.join([sentence, '.']))
			
		return '\n'.join(stanzas)
	
	
	#################################################
	# Private guys                                  #
	#################################################
	
	def _is_not_punct(self, char):
		return char not in '!"#$%&\'()*+-./<=>?@[\\]^_`{|}~' + '\n\t\r'
	
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
		elem = filter(self._is_not_punct, elem)
		elem = elem.replace(',', ' ,')
		elem = elem.replace(':', ' :')
		elem = elem.replace(';', ' ;')
		elem = elem.split()
		elem.insert(0, '^')
		elem.append('.')
		return elem
	
	def _train_first(self, word):
		if word not in self.firsts:
			self.firsts[word] = 0
		self.firsts[word] += 1
	
	def _train_last(self, word):
		if word not in self.lasts:
			self.lasts[word] = 0
		self.lasts[word] += 1
	
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
	from time import sleep
	#a = Growl.GrowlNotifier("arg.py", ['wtf'])
	#a.register()
	books = ['otoos11.txt']#, 'dscmn10.txt']
	monster = Rhymeless()
	
	for book in books:
		
		book = open('books/otoos11.txt')
		lines = []
		for line in book:
			# for other books:
			# lines.append(line)
			temp_lines = line.split()
			try:
				int(temp_lines[0])
			except:
				lines.append(line)
		book.close()
		book = ' '.join(lines)
		monster.train(book) 
	
	
	#for i in ['hello', 'awful', 'make', 'terrorist']:
	#	print monster.pick_appropriate()
	print "working:"
	while True:
		one = monster.generate_poem(style="poem")
		print one
		#monster.sample_in_meter()
		print '\n\n'
		#two = monster.generate_haiku()
		#print two
		#print two
		#print '\n\n'
		#a.notify('wtf', "", one)
		sleep(3)
	
	#while True:
	#	print monster.sample_in_meter()
	#while True:
	#	monster.sample_meter()
	#	sleep(2)
		

if __name__ == '__main__':
	main()
