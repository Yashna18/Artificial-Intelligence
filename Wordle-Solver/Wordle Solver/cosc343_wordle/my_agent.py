__author__ = "Yashna Shetty"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "sheya140@student.otago.ac.nz"

import random
import copy
import numpy as np


class WordleAgent:
    """
       A class that encapsulates the code dictating the
       behaviour of the Wordle playing agent

       ...

       Attributes
       ----------
       dictionary : list
           a list of valid words for the game
       letter : list
           a list containing valid characters in the game
       word_length : int
           the number of letters per guess word
       num_guesses : int
           the max. number of guesses per game
       mode: str
           indicates whether the game is played in 'easy' or 'hard' mode

       Methods
       -------
       AgentFunction(percepts)
           Returns the next word guess given state of the game in percepts
       """

    def __init__(self, dictionary, letters, word_length, num_guesses, mode):
        """
      :param dictionary: a list of valid words for the game
      :param letters: a list containing valid characters in the game
      :param word_length: the number of letters per guess word
      :param num_guesses: the max. number of guesses per game
      :param mode: indicates whether the game is played in 'easy' or 'hard' mode
      :param poss_words: a list which initialises a copy of the dictionary and has words eliminated from it as the
                        program progresses
      :param good_letter:a list of letters which should not be reasons to eliminate the current word
      """

        self.dictionary = dictionary
        self.letters = letters
        self.word_length = word_length
        self.num_guesses = num_guesses
        self.mode = mode
        self.poss_words = copy.copy(self.dictionary)
        self.good_letter = []

    def AgentFunction(self, percepts):
        """Returns the next word guess given state of the game in percepts

      :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
      :return: string - a word from self.dictionary that is the next guess
      """

        # This is how you extract three different parts of percepts.
        guess_counter, letter_indexes, letter_states = percepts

        # At the first guess, initialise poss_words and good_letter variables and guess a
        # random word from the dictionary.
        if guess_counter == 0:
            self.poss_words = copy.copy(self.dictionary)
            self.good_letter = []
            first_guess = random.randint(0, len(self.poss_words)-1)
            return self.poss_words[first_guess]

        # If letter states returns all 1's, then we have the solution
        if np.sum(letter_states) == len(letter_states):
            return None

        # Add all the letters that fit the criteria into the good_letter variable
        for j in range(len(letter_states)):
            if letter_states[j] == 1:
                if self.letters[letter_indexes[j]] not in self.good_letter:
                    self.good_letter.append(self.letters[letter_indexes[j]])
            elif letter_states[j] == -1:
                if self.letters[letter_indexes[j]] not in self.good_letter:
                    self.good_letter.append(self.letters[letter_indexes[j]])

        # Initialise the bad_words list at the beginning of every guess
        # then iterate through all the words in the dictionary
        bad_words = []
        for word in self.poss_words:
            # Iterate through each state returned by the guess for each word
            # in the set of possible words
            for i in range(self.word_length):
                curr_letter = self.letters[letter_indexes[i]]
                # If the letter states returns a 0, and it is not in the list of good_letters,
                # append it to the list of bad_words
                if letter_states[i] == 0 and curr_letter in word:
                    if curr_letter not in self.good_letter:
                        bad_words.append(word)
                        break
                    # If the letter state returns a 0, and it is in the list of good_letters,
                    # append all words that have the letter in that spot (treat it like the -1 state case)
                    elif curr_letter in self.good_letter:
                        if curr_letter == word[i]:
                            bad_words.append(word)
                # If the letter states returns 1 and the letter in the guess is not
                # in the correct position in the word, append it to bad_words
                elif letter_states[i] == 1 and curr_letter != word[i]:
                    bad_words.append(word)
                    break
                # If the letter states returns -1 and the letter is not in the word in
                # the dictionary, append it to bad_words list
                elif letter_states[i] == -1 and curr_letter not in word:
                    bad_words.append(word)
                    break
                # If the letter states returns a -1 and the letter in the word is in the
                # wrong position, append the word to the bad_words list
                elif letter_states[i] == -1 and curr_letter == word[i]:
                    bad_words.append(word)
                    break
        # The new poss_words list is every word in the original poss_words list excluding the words that are
        # not in the bad_words list as initialised above.
        self.poss_words = [x for x in self.poss_words if x not in bad_words]
        # The next guess will be a random word the set of possible solutions
        try:
            this_guess = random.randint(0, len(self.poss_words)-1)
        except ValueError:
            this_guess = 0
        # Return the guess
        return self.poss_words[this_guess]
