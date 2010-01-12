from text_utils import TextUtils

class BackoffModel(TextUtils):
	def __init__(self):
		TextUtils.__init__(self)
		self.firsts = {}
		self.lasts = {}
		self.unigram = {}
		self.bigram = {}
		self.trigram = {}
	
	def generic_train(self, text):
		"""Trains the model.
		
		When instantiating a BackoffModel 
		(e.g. 'm = BackoffModel(model = "backwards"")')  
		the choice of model determines the type of
		training that occurs.
		
		This training method should get replaced by 
		classes that inherit the BackoffModel.
		"""
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
	
	
	#######################################################################
	#######################################################################
	####                       Private Methods ...                     ####
	#######################################################################
	#######################################################################
	
	
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

if __name__=="__main__":
	m = BackoffModel()
	help(m)