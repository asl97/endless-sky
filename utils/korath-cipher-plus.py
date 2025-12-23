#! /usr/bin/env python

# Copyright (c) 2023 by an anonymous author
#
# Endless Sky is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# Endless Sky is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.


# This script is base on korath-cipher.py that implements the cipher by Lia Gerty described here:
#
#    https://github.com/endless-sky/endless-sky/pull/7101
#
# Works with Python 2.7 or newer.


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# INSTRUCTIONS
#
# Note: Also see instructions in korath-cipher.py
#
# Before you run this script, first you need to translate your desired
# phrase from English to Indonesian. Here's an example:
#
# English: Within truth, I see only lies.
# Indonesian: Dalam kebenaran, saya hanya melihat kebohongan.
#
# Next, send that Indonesian text into this script's stdin, and you'll see:
#
# ORIGINAL:  Dalam kebenaran, saya hanya melihat kebohongan.
# REVERSED*: Malad naranebek, ayas aynah tahilem nagnohobek.
# EXILE:     Famas ralarehet, aga' agrap kapimef ranrupuhet.
# EFRETI:    Fanat raparebes, adam adrah kahinef ralruhubes.
#
# This version of the script tries to put the punctuation and capitalization correctly
# Note that it's probably best to avoid common names and religious concepts.
# (Adam = the first man in some religions.)
# You should also make sure the end product is pronounceable, with
# particular attention to ' characters in Exile words. These are meant
# to represent glottal stops; if you are unfamiliar, imagine what the
# word would sound like with a k in place of the '. If it is too
# difficult, add some vowels or move letters around. After manual
# tweaking, you might end up with something like this:
#
# EXILE:  Famas ralarehet, aga' agrap kapimef ranrupuhet.
# EFRETI: Fanat raparebes, adas adrah kahinef ralruhubes.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# GENERAL TRANSLATION NOTES
#
# There are a few words with standard translations you'll need to apply manually:
#
# humans => humanika                          (Exile, Efreti, and Quarg)
# human (noun, member of species) => humani   (Exile, Efreti, and Quarg)
# Quarg => Kuwaru                             (Efreti)
# Drak => Drak                                (both Exile and Efreti)
# Ember Space => Nraol Alaj                   (Exile)
# There Might Be Riots => Ter Mite Bee Riot   (both Exile and Efreti)
#
# The easiest way to do this is to put them in ALL CAPS to whatever
# translation program you're using to get Indonesian from English. The
# cipher will produce gibberish in AOFEM MCAV (that's "all caps" in
# Efreti) which you can then replace with the correct translation.
#
# A word of warning: sometimes the cipher will produce obscene or
# objectionable words, or words that are sacred to some people. Use
# discretion and manually correct them. "Ember Space" had that problem.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys;

# This is the table from PR #7101. Each string has:
#    'GNL'
#     ^^^
#     |||-- Kor Efret letter
#     ||--- Korath Exile letter
#     |---- Indonesian letter
replace = [
	'AAA', 'EEE', 'III', 'OUU', 'UOO', 'BHB', 'CDV', 'DST',
	'FJY', 'GNL', 'HPH', 'JVW', 'KTS', 'LMN', 'MFF', 'NRR',
	'PBC', 'QZT', 'RLP', "S'M", 'TKK', 'VQR', 'WCG', 'XYS',
	'YGD', 'ZWK',

	'aaa', 'eee', 'iii', 'ouu', 'uoo', 'bhb', 'cdv', 'dst',
	'fjy', 'gnl', 'hph', 'jvw', 'kts', 'lmn', 'mff', 'nrr',
	'pbc', 'qzt', 'rlp', "s'm", 'tkk', 'vqr', 'wcg', 'xys',
	'ygd', 'zwk',
]

# Transfer the table into a pair of dictionaries:
to_exile = {}
to_efreti = {}

for ixf in replace:
	to_exile[ixf[0]] = ixf[1]
	to_efreti[ixf[0]] = ixf[2]

# Loop over every line in stdin, processing it
for line in sys.stdin:
	words = line.split()       # words in the line, as a list
	sdrow = []                 # the same words, with letters reversed
	exiles = []                # those words after the exile cipher
	efretis = []               # those words after the efret cipher

	for word in words:
		# Check if the word is capitalize
		iscap = word[0].isupper() and word[1:].islower()
		
		# Check for punctuation and exclude them from the reversal
		punctuation = ""
		while word[-1] in ",.?!": # not .isalnum
			punctuation = word[-1] + punctuation
			word = word[:-1]

		# Reverse the word:
		drow = ''.join(reversed(word))

		# Add back the punctuation if any was found
		drow += punctuation

		# capitalize the word if the original was capitalize
		if iscap:
			drow = drow.capitalize()

		sdrow.append(drow)

		# Run the reversed word through the cipher:
		exile=''
		efreti=''
		for char in drow:
			if char in to_exile:
				exile += to_exile[char]
			else:
				exile += char
			if char in to_efreti:
				efreti += to_efreti[char]
			else:
				efreti += char

		# Append the ciphered word to the list:
		exiles.append(exile)
		efretis.append(efreti)

	# Print the results of this line:
	print("ORIGINAL:  "+" ".join(words))
	print("REVERSED*: "+" ".join(sdrow))
	print("EXILE:     "+" ".join(exiles))
	print("EFRETI:    "+" ".join(efretis))
	print("")
