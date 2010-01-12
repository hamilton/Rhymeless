import sys
import os.path

class Rhuthmos(object):
	def __init__(self):
		self.wts = {}
		self.stw = {}
		self.RHYTHM_FORMS ={
			"iambic pentameter": [0,1,0,1,0,1,0,1,0,1],
		}

	def initiate_dictionary(self):
		dictionary = open(os.path.join(os.path.dirname(__file__), 'cmudict/cmudict.0.7a'), 'r')
		for line in dictionary:
			line = line.split()
			real_word = line[0].lower()
			real_word = ' '.join(real_word.split('_'))
			pronunciation = line[1:]
			#print "%-20s %s" % (real_word, pronunciation)
			if real_word not in self.wts:
				
				self.wts[real_word] = pronunciation
			
			pronunciation.reverse()
			for i, phone in enumerate(pronunciation):
				phone_subset = ''.join(pronunciation[0:i+1])
				if phone_subset not in self.stw:
					self.stw[phone_subset] = set()
				self.stw[phone_subset].add(real_word)
	
	def find(self, word):
		"""Returns all words that rhyme with word."""
		if word in self.wts:
			pronunciation = self.wts[word]
			rhymes = set()
			for i, phone in enumerate(pronunciation):
				phone_subset = ''.join(pronunciation[0:i+1])
				#print i, pronunciation
				if "1" in phone_subset:#"'" in phone_subset or "," in phone_subset:
					phone_subset = ''.join(pronunciation[0:i+1])
					#print self.stw[phone_subset]
					rhymes = rhymes | self.stw[phone_subset]
			return rhymes
		else:
			return set()
	
	def determine_meter(self, text, already_list=True):
		try:
			text = self._clean_text(text)
		except:
			pass
		meter = []
		previous_meter = []
		start_of_sentence = True
		#print text 
		for word in text:
			print word, self.word_to_meter(word)
			word_to_meter = self.word_to_meter(word)
			meter.append(word_to_meter)
			previous_meter = word_to_meter
		return meter
	
	def word_to_meter(self, word):
		"""input == word string.
		output == []"""
		word = ''.join(self._clean_text(word))
		if word in self.wts:
			word = self.wts[word]
		else:
 			return None
		word.reverse()
		# how to determine meter.
		meter = []
		for elem in word:
			if '0' in elem:
				meter.append('0')
			elif '1' in elem:
				meter.append('1')
			elif '2' in elem:
				meter.append('2')
			else:
				pass
		return meter
		
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
		elem = elem.split()
		return elem
	
	def _is_not_linebreak(self, char):
		return char not in '\n\t\r'
	
	def _is_not_punct(self, char):
		return char not in '!"#$%&\'()*+-,./:;<=>?@[\\]^_`{|}~' + '\n\t\r'

def main():
	r = Rhuthmos()
	r.initiate_dictionary()
	#print r.find('slack')
	#print r.find('know')
	#print r.word_to_meter('I')
	print r.determine_meter('I am absolutely livid about it.')
	print r.determine_meter('forth disturbing fortune lividly killing and thrill seekers.')
	
	

if __name__ == '__main__':
	main()