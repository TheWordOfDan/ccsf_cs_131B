RAW_TABLE = 0
STANDARD_TABLE = 1
CHAR_TABLE = 2



import string



def formatRunningResults(mustInclude_, mustNotInclude_):
	'''
	- menuF helper function
	- displays the in-progress results of the character list search
	'''
	result = f'(Your search criteria so far:'


	if mustInclude_ != []:
		mustInclude = str([ch for ch in mustInclude_])[1:-1]
	else:
		mustInclude = '-none-'

	if mustNotInclude_ != []:
		mustNotInclude = str([ch for ch in mustNotInclude_])[1:-1]
	else:
		mustNotInclude = '-none-'

	
	result += f'\n  Must contain:		{mustInclude}'
	result += f'\n  Must NOT contain: 	{mustNotInclude})'
	
	
	return result


def getCharList(prompt_):
	'''
	- menuF helper function
	- constructs a list of characters that will serve as a
		parameter of the search
	'''
	flagFirstTime = True
	runningResults = []
	while True:
		if len(runningResults) != 0:
			print(f'\nYou have thus far entered: '
				f'{len(runningResults)} distinct charater(s) - ',
				f'{str([ch for ch in runningResults])[1:-1]}')


		if not flagFirstTime:
			print(f'-> {prompt_}')

		print(f'Enter a character, or enter a string '
			f'(for example "Foo123!@#").')
		print(f'Entering a string will add every character in the '
			f'string to your search.')
		userInput = input(makeSysPrompt(
			f'Enter your character/string here '
			f"OR enter nothing when done: "))
		flagFirstTime = False
		
		if userInput in [None, '', ' ']:
			return runningResults

		
		runningResults.extend([ch for ch in userInput if ch != ' '])
		runningResults = list(set(runningResults))
		runningResults.sort()



def rSearch(searchSpace_, searchFor_, include_):
	'''
	- menuF/conductSearch helper function
	- pops a parameter from seachFor_, updates the search space
		based on the character, then calls itself with the new
		search space and a smaller parameter list
	'''
	if len(searchFor_) == 0:
		return searchSpace_
	ch = searchFor_.pop()

	results = []
	for word in searchSpace_:
		found = False
		if ch in word:
			found = True
		if found and include_:
			# Found a required letter
			results.append(word)
		if found and not include_:
			# Found a forbidden letter
			continue
		if not found and include_:
			# Didn't find a required letter
			continue
		if not found and not include_:
			# Didn't find a forbidden letter
			results.append(word)


	return rSearch(results, searchFor_, include_)



def handleResults(results_, freqTable_):
	'''
	- menuF/conductSearch helper function
	- takes the results from the search and formats them
	'''
	if len(results_) == 0:
		print('No results found for your criteria!')
		return None
	lengthDict = {}
	for key in results_:
		print(f'({freqTable_[key]}x) - {key}')
		if lengthDict.get(len(key), None) == None:
			lengthDict[len(key)] = [key]
		else:
			lengthDict[len(key)].append(key)
				

	# Display by length, then freq count, then unicode order
	sortedLengths = [key for key in lengthDict.keys()]
	sortedLengths.sort()
	shortest = sortedLengths[0]
	longest = sortedLengths[-1]
	shortestWords = lengthDict[shortest]
	longestWords = lengthDict[longest]
	

	# Combine each word into tuple (freq, word) 
	# sort() on a list of these tuples will sort by 
	# tuple[0] asc (freq lo->hi), then tuple[1] unicode asc (~alphabetical)
	# we want freq hi->lo, then alphabetical
	# 	make freq = freq**-1, making the highest freq word
	# 	into the smallest number, then sort will work correctly
	temp = [(freqTable_[word]**-1, word) for word in shortestWords]
	temp2 = [(freqTable_[word]**-1, word) for word in longestWords]
	temp.sort()
	temp2.sort() 
	resultShortest = [f'{tup[1]} ({freqTable_[tup[1]]}x)' for tup in temp]
	resultLongest = [f'{tup[1]} ({freqTable_[tup[1]]}x)' for tup in temp2]


	# Format the results
	ttable = ''.maketrans({'[': None, ']': None, "'": None})
	print(
		f'Longest	({longest}ch):		{str(resultLongest).translate(ttable)}')		
	print(
		f'Shortest ({shortest}ch):		{str(resultShortest).translate(ttable)}')
	
	
	return None



def conductSearch(mustInclude_, mustNotInclude_, freqTables_):
	'''
	- menuF helper function
	- given the parameters obtained in getCharList, conduct
		the search
	'''
	print('\n-> Conducting search...')
	prompt = 'Please choose from the following:'
	choices = {
		'a': 'Search the raw words list.',
		'b': 'Search the standardized words list.'}
	userInput = validateMenu(prompt, choices)
	if userInput == 'a':
		freqTable = freqTables_[0]
	if userInput == 'b':
		freqTable = freqTables_[1]
	
		
	results = rSearch(
		rSearch(freqTable, mustNotInclude_, False),
		mustInclude_, 
		True)
	print(f'\nResults found - {len(results)}')
	handleResults(results, freqTable)
	


	return None



def rBinSearch(searchSpace_, target_, start_, end_):
	'''
	- menuG helper function
	'''
	#input(f'Target: {target_} Start: {start_} End: {end_}')
	if start_ == end_:
		if target_ ==  searchSpace_[start_]:
			return start_
		else:
			return (start_,)


	mid = (start_ + end_) // 2


	if searchSpace_[mid] == target_:
		return mid
	if searchSpace_[mid] > target_:
		return rBinSearch(searchSpace_, target_, start_, mid)
	if searchSpace_[mid] < target_:
		return rBinSearch(searchSpace_, target_, mid + 1, end_)


	return None



def makeSysPrompt(prompt_):


	return '\n[aiw.py] ' + prompt_



def validateNumber(prompt_):
	while True:
		userInput = input(makeSysPrompt(prompt_))	
		try:
			return int(userInput)
		except ValueError:
			print(f'You entered "{userInput}" -- please enter a number!')



def validateYesNo(prompt_):
	while True:
		userInput = input(makeSysPrompt(prompt_))
		if userInput.upper() == 'Y':
			return 'y'
		elif userInput.upper() == 'N':
			return 'n'
		else:
			print("I didn't understand. Enter 'y' for 'yes' or 'n' for 'no'.")


	return None



def validateMenu(prompt_, dictOptions_, optAddtl_ = None):
	print('')
	prompt = prompt_[:]
	while True:
		
		print(prompt)
		for option in dictOptions_:
			print(f' {option}) {dictOptions_[option]} ')
		if optAddtl_ != None:
			print(optAddtl_)
		userInput = input(makeSysPrompt('Enter your choice here: '))


		if userInput == None:
			print('-> Please enter a response!')
			continue
		if userInput.lower() not in dictOptions_:
			print(f'-> Response not recognized!')
			recognized = str([opt for opt in dictOptions_])[1:-1]
			print(f"(You entered: '{userInput}'. Possible choices: {recognized})")
			prompt = '\nPlease choose from the following:'
			continue

		
		finalResponse = userInput.lower()
		print(f'-> {dictOptions_[finalResponse]}')
		return finalResponse



def loadAlice(path = './alice.txt'):
	print('Loading AiW...')
	with open(path, 'r', encoding = 'utf-8') as f:
		strAlice = f.read();
	print('Complete.')


	return strAlice



def menuA(freqTables_):
	'''
	Menu option 'a'. 
	- Display the number of raw words in AiW. 
	'''
	count = len(freqTables_[RAW_TABLE].keys())
	print(f'There are {count} raw words in Alice in Wonderland.')


	return None	
	


def menuB(freqTables_):
	'''
	Menu option 'b'
	- Display the number of standardized words in AiW
	'''
	count = len(freqTables_[STANDARD_TABLE].keys())
	print(f'There are {count} standardized words in Alice in Wonderland.')


	return None



def menuC(freqTables_):
	'''
	Menu option 'c'
	- Counts for frequently used characters
	'''
	n = validateNumber(f'Enter n to find the n most frequently '
		f'used characters: ')
	

	charFreqTable = freqTables_[CHAR_TABLE]
	reversedTable = {}
	for key in charFreqTable.keys():
		value = charFreqTable[key]
		if reversedTable.get(value, None) == None:
			reversedTable[value] = [key]
		else:
			reversedTable[value].append(key)


	if n > len(reversedTable):
		print(f'Warning: {n} is greater than the total '
			f'number of distinct characters!')
		n = len(reversedTable)
		print(f'(Displaying all {n} results)')


	searchSpaceIter = reversed(sorted(reversedTable.keys()))
	print(f'The {n} most commonly occuring characters in AiW are: ')
	for i in range(n):
		try:
			char = reversedTable[next(searchSpaceIter)]
		except StopIteration:
			break

		results = f'{i+1}.	'
		if len(char) == 1:
			results += f'"{char[0]}"	{charFreqTable[char[0]]}x'
			print(results)
		else:
			for j in range(len(char)):
				print(f'*{results}' + f'"{char[j]}"	{charFreqTable[char[j]]}x')


	return None



def menuD(freqTables_):
	'''
	Menu option 'd'
	- Counts of frequently used words (raw or standard)
	'''
	prompt = 'Search the raw or standardized dictionary?'
	dictOptions = {
		'a': 'Raw words dictionary',
		'b': 'Standardized words dictionary'
	}
	userInput = validateMenu(prompt, dictOptions)
	freqTable = {}
	if userInput == 'a':
		print('Now searching the RAW words dictionary!')
		freqTable = freqTables_[RAW_TABLE]
	if userInput == 'b':
		print('Now searching the STANDARDIZED words dictionary!')
		freqTable = freqTables_[STANDARD_TABLE]

	
	n = validateNumber(f'Enter n to find the n most frequently '
		f'used words: ')


	reversedTable = {}
	for key in freqTable.keys():
		value = freqTable[key]
		if reversedTable.get(value, None) == None:
			reversedTable[value] = [key]
		else:
			reversedTable[value].append(key)


	print(f'The {n} most frequently used words are: ')
	searchSpaceIter = reversed(sorted(reversedTable.keys())) 
	for i in range(n):
		try:
			word = reversedTable[next(searchSpaceIter)]
		except StopIteration:
			break

		results = f'{i+1}.	'
		if len(word) == 1:
			results += f'{freqTable[word[0]]}x	"{word[0]}"'
			print(results)
		else:
			for j in range(len(word)):
				print(f'*{results}' + f'{freqTable[word[j]]}x	"{word[j]}"')


	return None



def menuE(freqTables_):
	'''
	Menu option 'e'
	- Show the standardized words that occur a specified
		number of times.
	'''
	freqTable = freqTables_[STANDARD_TABLE]
	prompt = 'Enter n to find the standardized words that appear n times: '
	n = validateNumber(prompt)


	reversedTable = {}
	for key in freqTable.keys():
		value = freqTable[key]
		if reversedTable.get(value, None) == None:
			reversedTable[value] = [key]
		else:
			reversedTable[value].append(key)


	try:
		results = str([i for i in reversedTable[n]])[1:-1]
		ttable = ''.maketrans({"'":'"'})
		print(f'The following word(s) appear(s) {n} time(s): ')
		print(f'{results.translate(ttable)}')
	except KeyError:
		print(f'There are no words in Alice in Wonderland that occur '
			f'{n} times!')


	return None



def menuF(freqTables_):
	'''
	Menu option 'f'
	- Show the longest and shortest raw or standardized words that
		contain every character in one list, and no characters in another
	'''
	mustInclude, mustNotInclude = [], []
	while True:
		prompt = 'AiW option F - search controls:'
		dictOptions = {
			'a': 'Enter the characters, if any, that the word MUST contain.',
			'b': 'Enter the characters, if any, that the word must NOT contain.',
			'c': 'SEARCH for words that meet your criteria.',
			'q': 'QUIT - return to the main program without searching.'
			} 
		if not(mustInclude == [] and mustNotInclude == []):
			strRunningResults = formatRunningResults(mustInclude, mustNotInclude)
		else:
			strRunningResults = '(You have not yet entered any criteria!)'
		userInput = validateMenu(prompt, dictOptions, strRunningResults)
		

		if userInput == 'q':
			return None
		if userInput == 'a':
			mustInclude = getCharList(dictOptions['a'])	
		if userInput == 'b':
			mustNotInclude = getCharList(dictOptions['b'])
		if userInput == 'c':
			conductSearch(mustInclude, mustNotInclude, freqTables_)
			

	return None



def menuG(freqTables_):
	'''
	Menu option 'g'
	- Show the frequency counts for a specified number of raw or
		standardized words that begin with a particular string.
		
	'''
	prompt = 'Search the raw or standardized dictionary?'
	dictOptions = {
		'a': 'Raw words dictionary',
		'b': 'Standardized words dictionary'
	}
	userInput = validateMenu(prompt, dictOptions)
	freqTable = {}
	if userInput == 'a':
		print('Now searching the RAW words dictionary!')
		freqTable = freqTables_[RAW_TABLE]
	if userInput == 'b':
		print('Now searching the STANDARDIZED words dictionary!')
		freqTable = freqTables_[STANDARD_TABLE]


	prompt = 'Search for words that begin with the following sequence: '
	userInput = input(makeSysPrompt(prompt))


	prompt = f'Enter n to find the first n words that begin '
	prompt += f'with "{userInput}": '
	n = validateNumber(prompt)


	searchSpace = [key for key in freqTable.keys()]
	searchSpace.sort()


	idx = rBinSearch(searchSpace, userInput, 0, len(searchSpace) - 1)
	'''
	- Note: 'nn' < 'nn$' where $ is any character.
	If the seach finds an exact match, we have the
	beginning of the sequence of words that begin
	with our target string.

	If the search doesn't find an exact match, we still know
	that the list is sorted--the last place we checked
	is where the exact match would have gone.

	We can thus begin searching forward from there anyway.
	'''


	if type(idx) == tuple:
		idx = idx[0]


	results = []
	while(searchSpace[idx][:len(userInput)] == userInput):
		results.append(searchSpace[idx])
		if len(results) == n:
			break

		idx += 1


	if len(results) == 0:
		print(f'No results for words that begin with "{userInput}"!')
	else:
		print(f'Displaying words that begin with "{userInput}": ')
		for i in range(len(results)):
			print(f'{i+1}. {results[i]} ({freqTable[results[i]]}x)')


	return None



if __name__ == '__main__':
	testList = [i for i in range(10)]
	idx = rBinSearch(testList, -1, 0, len(testList) - 1)
	print(idx)
