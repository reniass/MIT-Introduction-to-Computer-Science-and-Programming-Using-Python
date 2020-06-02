from ps4a import *
import time



def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand = {}
    numVowels = n // 3

    for i in range(numVowels):
        x = VOWELS[random.randrange(0, len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1

    for i in range(numVowels, n):
        x = CONSONANTS[random.randrange(0, len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1

    return hand

def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it.

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    new_hand = hand.copy()
    for letter in word:
        new_hand[letter] -= 1
        if new_hand[letter] == 0:
            del new_hand[letter]

    return new_hand




#
#
# Computer chooses a word
#
#
def compChooseWord(hand, wordList, n):
    """
    Given a hand and a wordList, find the word that gives
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the wordList.

    If no words in the wordList can be made from the hand, return None.

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)

    returns: string or None
    """
    # Create a new variable to store the maximum score seen so far (initially 0)
    bestScore = 0
    # Create a new variable to store the best word seen so far (initially None)
    bestWord = None
    # For each word in the wordList
    for word in wordList:
        # If you can construct the word from your hand
        if isValidWord(word, hand, wordList):
            # find out how much making that word is worth
            score = getWordScore(word, n)
            # If the score for that word is higher than your best score
            if (score > bestScore):
                # update your best score, and best word accordingly
                bestScore = score
                bestWord = word
    # return the best word you found.
    return bestWord


#
# Computer plays a hand
#
def compPlayHand(hand, wordList, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is
    displayed, the remaining letters in the hand are displayed, and the
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).

    hand: dictionary (string -> int)
    wordList: list (string)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    # Keep track of the total score
    totalScore = 0
    # As long as there are still letters left in the hand:
    while (calculateHandlen(hand) > 0):
        # Display the hand

        print("Current Hand: ", end=' ')
        displayHand(hand)
        # computer's word
        word = compChooseWord(hand, wordList, n)
        # If the input is a single period:
        if word == None:
            # End the game (break out of the loop)
            break

        # Otherwise (the input is not a single period):
        else:
            # Tell the user how many points the word earned, and the updated total score
            score = getWordScore(word, n)
            totalScore += score
            print('"' + word + '" earned ' + str(score) + ' points. Total: ' + str(totalScore) + ' points')
            # Update hand and show the updated hand to the user
            hand = updateHand(hand, word)


            print()
    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    print('Total score: ' + str(totalScore) + ' points.')


#
# Problem #6: Playing a game
#
#
def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.

        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    wordList: list (string)
    """
    L1 = []
    L2 = []
    var1 = 0
    var2 = 0
    while True:
        word = input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
        if word == 'n':
            a2 = ''
            while a2 != 'u' and a2 != 'c':
                a2 = input("Enter u to have yourself play, c to have the computer play:")
                if a2 == 'u':
                    var1 += 1
                    user_saving_hand = dealHand(HAND_SIZE)
                    L1.append(user_saving_hand)
                    playHand(user_saving_hand, wordList, HAND_SIZE)
                elif a2 == 'c':
                    var2 += 1
                    comp_saving_hand = dealHand(HAND_SIZE)
                    L2.append(comp_saving_hand)
                    compPlayHand(comp_saving_hand, wordList, HAND_SIZE)
                else:
                    print("Invalid comand.")
        elif word == 'r':
            if var1 == 0 and  var2 == 0:
                print("You have not played a hand yet. Please play a new hand first!")
            else:
                a2 = ''
                while a2 != 'u' and a2 != 'c':
                    a2 = input("Enter u to have yourself play, c to have the computer play:")
                    if a2 == 'u' and var1 == 0:
                        print("You have not played a hand yet. Please play a new hand first!")
                    elif a2 == 'u' and var1 != 0:
                        playHand(L1[var1 - 1], wordList, HAND_SIZE)
                    elif a2 == 'c' and var2 == 0:
                        print("You have not played a hand yet. Please play a new hand first!")
                    elif a2 == 'c' and var2 != 0:
                        compPlayHand(L2[var2 - 1], wordList, HAND_SIZE)
                    else:
                        print("Invalid command.")
        elif word == 'e':
            break
        else:
            print("Invalid syntax.")




#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)





