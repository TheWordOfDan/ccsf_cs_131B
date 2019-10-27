import string



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



def getCharFreqTable(rawStr_):
	charFreqTable = {}
	for ch in rawStr_:
		charFreqTable[ch] = charFreqTable.get(ch, 0) + 1

	
	charFreqTable.pop('\n')
	print(f'Char freq table created: '
		f'{len(charFreqTable)} distinct characters.')


	return charFreqTable
