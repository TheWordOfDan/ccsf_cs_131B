'''
	On my honor as a CCSF student, I, Daniel Jimenez, have neither
	given nor recieved inappropriate help with this assignment.
'''

'''
DESIGN:

	Before the main loop begins:
	- Load aiw_funcs (separate file containing functions required
		for program logic)
	- Load nlp_funcs (separate file containing functions required
		for nlp processing)
	- load alice.txt into a string (using an aiw_funcs function)
	- create the frequency tables

	- create the main menu
		- a dictionary with k, v
			- k => the letter to select
			- v => the prompt
			
			k   v
			a - Display the number of raw words in AiW
			b - Display the humber of standardized words in AiW
			c - Counts of frequently used characters
			d - Counts of frequently used words, raw or standard
			e - Display all the standardized words that occur a 
				certain number of times
			f - Display longest/shortest words that contain:
				All the characters from a given list
				No characters from another given list
			g - Display frequency counts for words that start
				with a certain string
			q - quit

	Begin main loop
		First user choice: inquiry or quit
			if quit, break from the loop

		If inquiry, display the menu
			- Upon selecting an item, it will use the
				user selected value as the key to a different
				dictionary, with k, v as the menu choice
				and v as a function that the menu choice will
				call.

				k - v 
				a	- menuA (a function defined in aiw_funcs)
				b	- menuB
				c	- menuC

			- unless the user chooises q to quit

Menu functions (general strategy):
menu A - the raw text of AiW split on the spaces; count the keys
	in the frequency table created at the beginning of the program
menu B - the words standardized according to the criteria given
	in nlp_funcs; count the keys in the frequency table created
	at the beginning of the program
menu C - reverse the character frequency table created at the beginning
	of the program, sort the keys in reverse order, display the first
	n results where n is given by the user
menu D - Reverse the standard or raw words dictionary, sort the keys
	in reverse order, display the first n results where n is given
	by the user
menu E - Reverse the standard words dictionary and search by
	the user given n
menu F - Accept user inputted required characters, and forbidden
	characters, narrow down the chosen dictionary given those
	parameters and return the results ordered by frequency descending,
	then alphabetical order, and single out the longest and shortest result
	Note- menu F can be taken in its entirety from lab 6)
menu G - get the appropriate dictionary, sort it's keys, search the
	keys for words that begin with a user defined string, using binary
	search. From that position, search every subsequent string until
	the results no longer contain the defined prefix.
 
'''


import aiw_funcs
import nlp_funcs



#---BEGIN---#
PROGRAM_RUN = True
print('\n -- Welcome to aiw.py! --\n')


#---Load AiW---#
strAlice = aiw_funcs.loadAlice()


#---Create Frequency Tables---#
rawFreqTable = nlp_funcs.getRawFreqTable(strAlice)
stdFreqTable = nlp_funcs.standardizeWords(rawFreqTable)
charFreqTable = nlp_funcs.getCharFreqTable(strAlice)
freqTables = (rawFreqTable, stdFreqTable, charFreqTable)


#---Create the menu---#
dictOptions = {
	'a': 'Display the number of raw words in AiW',
	'b': 'Display the number of standardized words in AiW',
	'c': 'Counts of frequently used characters',
	'd': 'Counts of frequently used words, raw or standard',
	'e': f'Display all the standardized words that occur '
		+ f'a certain number of times',
	'f': f'Display longesti/shortest words that contain: '
		+ f'\n	- all characters from a given list'
		+ f'\n	- no characters from another given list ',
	'g': f'Display frequency counts for words that start '
		+ f'with a certain string.',
	'q': 'Quit'
}


#---Create menu to functions translator---#
dictMenuFuncs = {
	'a': aiw_funcs.menuA,
	'b': aiw_funcs.menuB,
	'c': aiw_funcs.menuC,
	'd': aiw_funcs.menuD,
	'e': aiw_funcs.menuE,
	'f': aiw_funcs.menuF,
	'g': aiw_funcs.menuG
}


#---MAIN LOOP---#
while PROGRAM_RUN:
	userInput = aiw_funcs.validateYesNo(
		'Would you like to make an inquiry? [y/n]: ')
	if userInput == 'n':
		PROGRAM_RUN = False
		continue


	prompt = 'Please choose from the following:'
	userInput = aiw_funcs.validateMenu(prompt, dictOptions)
	if userInput == 'q':
		PROGRAM_RUN = False
		continue
	else:
		dictMenuFuncs[userInput](freqTables)


print('\n -- Goodbye! -- \n')
