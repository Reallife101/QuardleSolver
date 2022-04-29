import copy
import itertools
import math
from os.path import exists

import pandas as pd

STATISTICS = "wordle_frequencys.csv"
WORD_LIST_TEXT = "words.txt"
BIT_VAL_CSV = "words_to_bits.csv"

WORD_LIST = []
POSSIBLE_WORDLE_VALUES = [''.join(i) for i in itertools.product(["0", "1", "2"], repeat=5)]
WORD1 = []
WORD2 = []
WORD3 = []
WORD4 = []

WORD1_DONE = False
WORD2_DONE = False
WORD3_DONE = False
WORD4_DONE = False



def get_weighted_bits(list_of_probabilities):
    """Given a list of probabilities, calculate the weighted exepected bits of information gained
    :param list_of_probabilities: a list of floats representing probabilities. Should add to 1
    :return: a float representing expected bits of information gained"""

    # keep running tally of bits gained so far
    ret_val = 0

    for prob in list_of_probabilities:
        ret_val += prob * bits_of_information(prob)

    return ret_val


def bits_of_information(probability):
    """Given a probability, calculate the bits of information gained"""
    return math.log2(1 / probability) if probability > 0 else 0


def ret_wordle_num(word1, word2):
    """Takes in 2 words and returns the wordle frequency where 0 is black, 1 is yellow and 2 is green.

    :param word1: The guess
    :param word2: The correct answer
    :return: Wordle frequency score"""
    final_score = ""
    for index in range(len(word1)):
        # print(word2)
        if word1[index] == word2[index]:
            final_score = final_score + "2"
            word2 = word2[:index] + "*" + word2[index + 1:]
            word1 = word1[:index] + "+" + word1[index + 1:]
        else:
            final_score = final_score + "0"

    for index in range(len(word1)):
        if word1[index] in word2:
            for j in range(len(word2)):
                if word1[index] == word2[j]:
                    word2 = word2[:j] + "*" + word2[j + 1:]
                    break
            final_score = final_score[:index] + "1" + final_score[index + 1:]

    return final_score


def gen_statistics(in_file, out_file):
    df = pd.read_csv(in_file)

    for index, row in df.iterrows():
        counter = 0
        for word in WORD_LIST:
            print(f"Index: {index}, {counter}")
            counter += 1
            val = ret_wordle_num(WORD_LIST[index], word)
            df.at[index, word] = val

    df.to_csv(out_file)


def create_csv(in_list, out_file):
    """Creates a csv crossing a word list with itself"""
    if exists(out_file):
        # File already exists
        return

    df = pd.DataFrame(index=in_list,
                      columns=in_list)
    df.to_csv(out_file)


def read_to_list(in_file):
    """Reads a file containing a bunch of words and returns the words compiled into a list"""
    global WORD_LIST
    global WORD1, WORD2, WORD3, WORD4
    # opening the file in read mode
    my_file = open(in_file, "r")

    # reading the file
    data = my_file.read()

    # replacing end of line('/n') with ' ' and
    # splitting the text it further when '.' is seen.
    WORD_LIST = data.replace('\n', ' ').split(" ")
    WORD1 = copy.deepcopy(WORD_LIST)
    WORD2 = copy.deepcopy(WORD_LIST)
    WORD3 = copy.deepcopy(WORD_LIST)
    WORD4 = copy.deepcopy(WORD_LIST)

    my_file.close()
    return WORD_LIST


def get_possible_sol_dist(tally_list):
    """Given a list tallying the number of each type of answer in Wordle, return a list converting them to a
    distribution

    :param tally_list: a list of ints representing how many of each it is"""

    total = sum(tally_list)

    for i in range(len(tally_list)):
        tally_list[i] = tally_list[i] / total

    return tally_list


def gen_tallies(in_file, search_space, out_file):
    """Given a file of solutions"""
    df = pd.read_csv(in_file, dtype=str)

    sol_dict = {}

    for index, row in df.iterrows():
        if WORD_LIST[index] in search_space:
            dict = {key: 0 for key in POSSIBLE_WORDLE_VALUES}

            for word in search_space:
                dict[df.iloc[index][word]] = dict[df.iloc[index][word]] + 1

            sol_dict[WORD_LIST[index]] = get_weighted_bits(get_possible_sol_dist(list(dict.values())))

    df2 = pd.DataFrame.from_dict(sol_dict, orient="index")
    df2.to_csv(out_file)


def gen_tallies2(in_file, search_space1, search_space2, search_space3, search_space4):
    """Given a file of solutions"""
    df = pd.read_csv(in_file, dtype=str)

    sol_dict1 = {}
    sol_dict2 = {}
    sol_dict3 = {}
    sol_dict4 = {}

    for index, row in df.iterrows():
        if WORD_LIST[index] in search_space1:
            dict = {key: 0 for key in POSSIBLE_WORDLE_VALUES}

            for word in search_space1:
                dict[df.iloc[index][word]] = dict[df.iloc[index][word]] + 1

            sol_dict1[WORD_LIST[index]] = get_weighted_bits(get_possible_sol_dist(list(dict.values())))

        if WORD_LIST[index] in search_space2:
            dict = {key: 0 for key in POSSIBLE_WORDLE_VALUES}

            for word in search_space2:
                dict[df.iloc[index][word]] = dict[df.iloc[index][word]] + 1

            sol_dict2[WORD_LIST[index]] = get_weighted_bits(get_possible_sol_dist(list(dict.values())))

        if WORD_LIST[index] in search_space3:
            dict = {key: 0 for key in POSSIBLE_WORDLE_VALUES}

            for word in search_space3:
                dict[df.iloc[index][word]] = dict[df.iloc[index][word]] + 1

            sol_dict3[WORD_LIST[index]] = get_weighted_bits(get_possible_sol_dist(list(dict.values())))

        if WORD_LIST[index] in search_space4:
            dict = {key: 0 for key in POSSIBLE_WORDLE_VALUES}

            for word in search_space4:
                dict[df.iloc[index][word]] = dict[df.iloc[index][word]] + 1

            sol_dict4[WORD_LIST[index]] = get_weighted_bits(get_possible_sol_dist(list(dict.values())))

    print(f"Word 1 Possible Solutions Left: {sol_dict1.keys()}")
    print(f"Word 2 Possible Solutions Left: {sol_dict2.keys()}")
    print(f"Word 3 Possible Solutions Left: {sol_dict3.keys()}")
    print(f"Word 4 Possible Solutions Left: {sol_dict4.keys()}")

    #Combine all dictionaries
    sol_dictmid1 = {}
    sol_dictmid2 = {}
    sol_dictmid3 = {}

    for key in sol_dict1:
        if key in sol_dict2:
            sol_dictmid1[key] = sol_dict1[key] + sol_dict2[key]

    sol_dictmid1 = sol_dict1|sol_dict2|sol_dictmid1

    for key in sol_dict3:
        if key in sol_dict4:
            sol_dictmid2[key] = sol_dict3[key] + sol_dict4[key]

    sol_dictmid2 = sol_dict3 | sol_dict4 | sol_dictmid2

    for key in sol_dictmid2:
        if key in sol_dictmid1:
            sol_dictmid3[key] = sol_dictmid2[key] + sol_dictmid1[key]

    sol_dictmid3 = sol_dictmid2 | sol_dictmid1 | sol_dictmid2

    return max(sol_dictmid3, key=sol_dictmid3.get), max(sol_dictmid3.values()), len(sol_dictmid3)


def get_smaller_list(in_file, search_space, guess, match):
    """Given a file of solutions"""
    df = pd.read_csv(in_file, dtype=str)

    sol = []
    # print(f"-----SEARCH SPACE--------:{search_space}")

    for word in search_space:
        if df.iloc[WORD_LIST.index(guess)][word] == match:
            sol.append(word)

    return sol


def loop():
    global WORD1, WORD2, WORD3, WORD4, WORD1_DONE, WORD2_DONE, WORD3_DONE, WORD4_DONE
    guess = input("Word: Enter your guess (ex: raise): ")

    # Get smaller lists
    if not WORD1_DONE:
        result1 = input("Word1: Enter your result (ex: 10201): ")
        WORD1 = get_smaller_list(STATISTICS, WORD1, guess, result1)

        if result1 == "22222":
            WORD1_DONE = True

    if not WORD2_DONE:
        result2 = input("Word2: Enter your result (ex: 10201): ")
        WORD2 = get_smaller_list(STATISTICS, WORD2, guess, result2)

        if result2 == "22222":
            WORD2_DONE = True

    if not WORD3_DONE:
        result3 = input("Word3: Enter your result (ex: 10201): ")
        WORD3 = get_smaller_list(STATISTICS, WORD3, guess, result3)

        if result3 == "22222":
            WORD3_DONE = True

    if not WORD4_DONE:
        result4 = input("Word4: Enter your result (ex: 10201): ")
        WORD4 = get_smaller_list(STATISTICS, WORD4, guess, result4)

        if result4 == "22222":
            WORD4_DONE = True

    for tpl in [(WORD1, WORD1_DONE), (WORD2, WORD2_DONE), (WORD3, WORD3_DONE), (WORD4, WORD4_DONE)]:
        if not tpl[1] and len(tpl[0]) == 1:
            print("\n----------NEXT GUESS------------")
            print(f"Suggested guess is '{tpl[0][0]}' as it is a solution.")
            return


    word, score, l = gen_tallies2(STATISTICS, WORD1, WORD2, WORD3, WORD4)

    print("\n----------NEXT GUESS------------")
    print(f"{l} possible words left.")
    print(f"Suggested guess is '{word}' with a score of {score} bits of info on average.")


if __name__ == '__main__':

    # create_csv(read_to_list(WORD_LIST_TEXT), STATISTICS)
    # gen_statistics(STATISTICS, "wordle_frequencys3.csv")

    read_to_list(WORD_LIST_TEXT)

    # gen_tallies(STATISTICS, WORD_LIST, BIT_VAL_CSV)
    # smaller_space = get_smaller_list(STATISTICS, WORD_LIST, 'raise', '10010')
    # gen_tallies(STATISTICS, smaller_space, "guess2.csv")
    # smaller_space2 = get_smaller_list(STATISTICS, smaller_space, 'short', '20222')
    # gen_tallies(STATISTICS, smaller_space2, "guess3.csv")
    # smaller_space3 = get_smaller_list(STATISTICS, smaller_space2, 'crave', '12202')
    # gen_tallies(STATISTICS, smaller_space3, "guess3.csv")
    print("Note: 0 = Gray, 1 = Yellow, 2 = Green.")
    print("2309 possible words left.")
    print("Suggested guess is 'raise' with a score of 5.878 bits of info on average.")

    while True:
        loop()
