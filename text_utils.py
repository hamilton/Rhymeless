
class TextUtils(object):
	def __init__(self):
		pass
	
	def read_file(self, path):
		"""Turns a file into a large string."""
		opened_file = open(path, 'w')
		text = []
		for line in opened_file:
			text.append(line)
		text = ''.join(text)
		opened_file.close()
		return text
	
	def clean_text(self, text):
		"""Removes unwanted characters (some punctuation) and
		lower-cases everything."""
		return self._clean_text(text)
	
	def _is_not_punct(self, char):
		return char not in '!"#$%&\'()*+-./<=>?@[\\]^_`{|}~' + '\n\t\r'
	
	def _clean_text(self, elem):
		"""Preprocesses text for training through string methods.
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