# -*- coding: utf-8 -*-
import os
import sys
import string
from math import log
from random import sample, random, randint
from rhuthmos.rhuthmos import Rhuthmos

import sqlite3


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
			
			if (one_1 != None and one_2 != None and two_1 != None and two_2 != None) and \
				len(one_1) > MINLENGTH and \
				len(one_2) > MINLENGTH and \
				len(two_1) > MINLENGTH and \
				len(two_2) > MINLENGTH and \
				one_1 != two_1 and \
				one_1 not in set(["whatever", "whenever"]) and \
				one_2 not in set(["whatever", "whenever"]) and \
				two_1 not in set(["whatever", "whenever"]) and \
				two_2 not in set(["whatever", "whenever"]):
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
	



class Rhymeless(RhymelessUtilityBelt,  Rhuthmos):
	def __init__(self):
		
		RhymelessUtilityBelt.__init__(self)
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
	
	def generate_poem(self, method = 'naive', style="poem", output="plain"):
		"""
		Generates a short 4-line poem.
		
		"""
		
		outputs = set(["plain", "html", "sqlite"])
		if output not in outputs:
			raise ValueError, "output '%s' not valid." % output
			
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
			sentence[0] = sentence[0].capitalize()
			
			sentence = ' '.join(sentence)
			sentence = sentence.replace(' ,', ',')
			sentence = sentence.replace(' :', ':')
			sentence = sentence.replace(' ;', ';')

			stanzas.append(''.join([sentence, ".  " if randint(0,1) == 1 or len(stanzas) == 3 else ""
			]))
			
		if output == "html" or output == "sqlite":
			stanzas = ["\n\t%s" % stanza for stanza in stanzas]
			poem = '<br>'.join(stanzas)
			poem = "%s<br>" % poem
			#print poem
			poem = "<div class='poem'>%s\n</div>" % poem
		elif output == "plain":
			poem = "\n".join(stanzas)
		return poem

	
	
	#################################################
	# Private guys                                  #
	#################################################
	
	def _is_not_punct(self, char):
		return char not in '!"#$%&\'();*+-./<=>?@[\\]^_`{|}~' + '\n\t\r'
	
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


#######################################################
# Some command line helper functions, variables, etc. #
#######################################################

def usage():
	print "usage: python rhymeless.py <task> <additional arguments>"

help = """
#############################################
# The Rhymeless Stochastic Stanza Generator #
#############################################

Generates poetry using a text file, a pronunciation dictionary,
and lots of hacky random walks.

SIMPLE EXAMPLES:

python rhymeless.py plain bible.txt > bible_verse.txt
	Puts results in new text file.

python rhymeless.py html prince.txt nietzsche.txt --number=100  > mashup.html
	Trains on said text files, and formats them to html.  As with the rest of these,
	the --number=N argument tells me how many to output.  Default is 100.
	Check out the HTML section below.

python rhymeless.py sqlite prince.txt nietzsche.txt --using=my_config.cnf
	Dumps the output into a sqlite database, according to my_config.cnf, which must
	be in the same directory as the script.


What you can or should put in <other args>:

	-- Required:

first.txt second.txt third.txt                 <= any number of raw text files. These are the training sets.

	-- Optional:
[--number=100]                                 <= specifies the number of stanzas to print. default 100.


"""

def train_these_books(book_list, config):
	########################
	# load configparser.   #
	########################
	
	
	#print dir(config)
	#print config.options("directory")
	book_dir = config.get("directory", "book_dir")
	
	if not os.path.isdir(book_dir):
		raise IOError, "The path defined in your config.cnf file does not exist: %s" % book_dir
	
	######################################################################
	# Check for existence of each book before parsing.  Should save user #
	# some time if there is in fact an error.                            #
	######################################################################
	
	books = args[1:]
	
	for book in books:
		#if not os.path.isfile("%s/%s" % (book_dir, book)):
		#	raise IOError, "%s does not seem to exist." % book
		# the preceding method is apparently insecure, as a maliciously created race condition
		# can ruin your day.
		try:
			test = open("%s/%s" % (book_dir, book))
			test.close()
		except:
			raise IOError, "%s does not exist." % book
	
	######################################################################
	# Begin Parsing.                                                     #
	######################################################################
	
	monster = Rhymeless()
	
	for book in books:
		
		book = open("%s/%s" % (book_dir, book))
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
	return monster

def get_rhymeless_sqlite_con_and_cursor(config):
	try:
		sqlite_path = config.get("sqlite", "db_dir")
	except:
		print config.get("sqlite", "db_dir")
		raise IOError, "Your sqlite section of your config.cnf has an error.  Check the examples to see what's wrong with %s" %"%s/%s" % (sqlite_path, "sqlite.db")
	full_path = "%s/%s" % (sqlite_path, "sqlite.db")
	try:
		if os.path.exists(full_path):
			os.remove(full_path)
		conn = sqlite3.connect(full_path)
	except:
		raise ValueError, "could not connect to %s" % full_path
	c = conn.cursor()
	# create database.
	c.execute("""
	create table entries(
		used TINYINT,
		content TEXT
	)
	""")
	return conn, c



if __name__ == '__main__':
	""""""
	
	import sys
	
	if len(sys.argv) == 1:
		usage()
		print "run 'python rhymeless.py -h' for a list of options."
		sys.exit()
	
	import getopt
	#optlist, args = getopt.getopt(sys.argv[1:], "hn", ['--number=', '--using='])
	#print optlist, args
	try:
		optlist, args = getopt.getopt(sys.argv[1:], "h", ['number=', 'using='])
	except:
		sys.exit()
	optlist = dict(optlist)
	
	if '--number' not in optlist:
		optlist['--number'] = 100
	else:
		try:
			optlist['--number'] = int(optlist['--number'])
		except TypeError, err:
			print err
	#print args
	#sys.exit()
	if ("-h", "") in optlist:
		print help
		sys.exit()
	if len(args) > 0 and args[0] in set(["plain", "html", "sqlite"]):
		MODE = args[0]
	else:
		raise IOError, "\n\nYou didn't specify a mode.\n\nSee python rhymeless.py -h for more details.\n\n"
	
	
	
	from time import sleep
	
	books = args[:1]
	
	import ConfigParser
	config = ConfigParser.ConfigParser()
	
	try:
		config.read('config.cnf')
	except:
		raise IOError, "you have not properly defined a config.cnf file.  See the accompanying README file for more details."
	
	##################################################################
	# If in sqlite mode, check that everything works before parsing. #
	##################################################################
	
	if MODE == "sqlite":
		conn, cursor = get_rhymeless_sqlite_con_and_cursor(config)
	
	monster = train_these_books(books, config)
	
	for i in xrange(optlist['--number']):
		one = monster.generate_poem(style="poem", output=MODE)
		if MODE == "sqlite":
			# insert results into the db.
			cursor.execute("""INSERT INTO entries values(0, ?)""", [one])
		else:
			print one
			print "\n"
	if MODE == "sqlite":
		conn.commit()
