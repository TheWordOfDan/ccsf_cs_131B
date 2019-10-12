'''

	On my honor as a CCSF student, I, Daniel Jimenez, have neither
	given nor recieved inappropriate help with this assignment.

'''
# LAB 6



import string



def validateYesNo(prompt_):
	while True:

		userInput = input(prompt_)	
		if userInput.upper() == 'Y':
			return 'y'
		elif userInput.upper() == 'N':
			return 'n'
		else:
			print("I didn't understand. Enter 'y' for 'yes or 'n' for 'no'.")



def validateMenu(prompt_, dictOptions_, optAddtl_ = None):
	prompt = prompt_[:]
	while True:
		
		print(prompt)
		for option in dictOptions_:
			print(f' {option}) {dictOptions_[option]} ')
		if optAddtl_ != None:
			print(optAddtl_)
		userInput = input('Enter your choice here: ')


		if userInput == None:
			print('\n --> Please enter a response!')
			continue
		if userInput.lower() not in dictOptions_:
			print(f'\n --> Response not recognized!')
			recognized = str([opt for opt in dictOptions_])[1:-1]
			print(f" (You entered: '{userInput}'. Possible choices: {recognized})")
			prompt = '\nPlease choose from the following:'
			continue

		
		return userInput.lower()



def getCharList(prompt_):
	runningResults = []
	print('\n -- Building search parameters! --')
	while True:

		if len(runningResults) != 0:
			print(f'\nYou have thus far entered: '
				f'{len(runningResults)} distinct charater(s) - ',
				f'{str([ch for ch in runningResults])[1:-1]}')


		print(f'-> {prompt_}')
		print(f'-> You may enter one character at a time, or enter a string '
			f'(for example "Foo123!@#").',
			f'\n-> Entering a string will add every character in the string to',
			f'your search criteria.')
		userInput = input(
			f'Enter your character/string here '
			f"OR enter nothing when done: ")

		
		if userInput in [None, '', ' ']:
			return runningResults

		
		runningResults.extend([ch for ch in userInput if ch != ' '])
		runningResults = list(set(runningResults))
		runningResults.sort()



def formatRunningResults(mustInclude_, mustNotInclude_):
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



def rSearch(searchSpace_, searchFor_, include_):
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
	

	# Combine each word into tuple (freq, word); sort() on a list of these tuples 
	# 	will sort by tuple[0] asc (freq lo->hi), 
	# 	then tuple[1] unicode asc (~alphabetical)
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
	print(f'Longest ({longest}ch): 	{str(resultLongest).translate(ttable)}')		
	print(f'Shortest ({shortest}ch): 	{str(resultShortest).translate(ttable)}')
	
	
	return None



def conductSearch(mustInclude_, mustNotInclude_, freqTables_):
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
	

	userInput = validateYesNo('\nSearch again? [y/n]: ') 
	if userInput == 'y':
		return True
	return False



def getRawFreqTable(rawStr_):
	# note: string.split() will split on spaces and newline chars
		
	rawWords = rawStr_.split()
	print(f'AiW split; {len(rawWords)} nondistinct raw words detected.')
	rawFreqTable = {}
	for word in rawWords:
		rawFreqTable[word] = rawFreqTable.get(word, 0) + 1


	print(f'Raw frequency table created: '
		f'{len(rawFreqTable)} distinct raw words.')


	return rawFreqTable



def standardizeWords(rawFreqTable_):
	
	# Standardized words criteria:
	# [x] Words separated by '-' are one word
	# [x] Words separated by '--' are separate words
	# [x] Strip all punctuation except the apostrophe
	# [x] all letters are lowercase

	# Add puntuation in AiW not already in string.punctuation
	# Leave CLOSE_SINGLE_QUOTE/APOSTROPHE alone -- dealt with later
	OPEN_SINGLE_QUOTE = "‘"
	APOSTROPHE = "’"
	CLOSE_SINGLE_QUOTE = APOSTROPHE
	OPEN_DBL_QUOTE = '“'
	CLOSE_DBL_QUOTE = '”'
	AiW_punc = string.punctuation
	AiW_punc += OPEN_SINGLE_QUOTE + OPEN_DBL_QUOTE
	AiW_punc += CLOSE_DBL_QUOTE

	
	# Do not strip dashes -- they will be dealt with later.
	AiW_punc_final = (ch for ch in AiW_punc if ch != '-')
	translation_table = {}
	for ch in AiW_punc_final:
		translation_table[ch] = None
	translation_table = ''.maketrans(translation_table)

	
	# Leave '-' alone. On '--' split on the double dash and add
	# each word separately
	tempFreqTable = {}
	for key in rawFreqTable_.keys():
		newKey = key.translate(translation_table)		
		newKey = newKey.rstrip(APOSTROPHE)
		newKey = newKey.lower()

		if '--' in newKey:
			sepKeys = newKey.split('--')
			for sepKey in sepKeys:
				tempFreqTable[sepKey] = tempFreqTable.get(sepKey, 0) + 1
		else:
			tempFreqTable[newKey] = tempFreqTable.get(newKey, 0) + 1

	
	tempFreqTable.pop('')
	print(f'Std frequency table created: '
		f'{len(tempFreqTable)} distinct standardized words.')


	return tempFreqTable

		

# --- Begin! ---

print('\nLoading AiW...')
with open('./alice.txt', 'r') as f:
	strAlice = f.read()
print('Complete.')


rawFreqTable = getRawFreqTable(strAlice)
stdFreqTable = standardizeWords(rawFreqTable)
freqTables = (rawFreqTable, stdFreqTable)


PROGRAM_RUN = True
print('\n -- Hello! --\n')
while PROGRAM_RUN:
	prompt = 'Would you like to search for a word? [y/n]: '
	userInput = validateYesNo(prompt)
	if userInput == 'n':
		PROGRAM_RUN = False
		continue

	
	mustInclude, mustNotInclude = [], []
	while True:
		prompt = '\n -- Setting up search! --\n'
		prompt += 'Please choose from the following: '
		dictOptions = {
			'a': 'Enter the characters, if any, that the word MUST contain.',
			'b': 'Enter the characters, if any, that the word must NOT contain.',
			'c': 'SEARCH for words that meet your criteria.',
			'q': 'QUIT without searching.'
			} 
		if not(mustInclude == [] and mustNotInclude == []):
			strRunningResults = formatRunningResults(mustInclude, mustNotInclude)
		else:
			strRunningResults = '(You have not yet entered any criteria!)'
		userInput = validateMenu(prompt, dictOptions, strRunningResults)
		

		if userInput == 'q':
			PROGRAM_RUN = False
			break
		if userInput == 'a':
			mustInclude = getCharList(dictOptions['a'])	
		if userInput == 'b':
			mustNotInclude = getCharList(dictOptions['b'])
		if userInput == 'c':
			keepGoing = conductSearch(
				mustInclude, 
				mustNotInclude, 
				freqTables)
			if not keepGoing:
				PROGRAM_RUN = False
				break
			else:
				continue

		

print('\n -- Goodbye! --\n')
