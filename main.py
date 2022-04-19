import math
from os.path import exists

import pandas as pd

STATISTICS = "wordle_frequencys.csv"
WORD_LIST_TEXT = "words.txt"
WORD_LIST = []


def safe_log2(x):
    return math.log2(x) if x > 0 else 0


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
    return safe_log2(1 / probability)


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
    # opening the file in read mode
    my_file = open(in_file, "r")

    # reading the file
    data = my_file.read()

    # replacing end of line('/n') with ' ' and
    # splitting the text it further when '.' is seen.
    WORD_LIST = data.replace('\n', ' ').split(" ")

    my_file.close()
    return WORD_LIST


def get_possible_sol_dist(tally_list):
    """Given a list tallying the number of each type of answer in Wordle, return a list converting them to a
    distribution

    :param tally_list: a list of ints representing how many of each it is"""

    total = sum(tally_list)

    for i in range(len(tally_list)):
        tally_list[i] = tally_list[i]/total

    return tally_list

if __name__ == '__main__':
    # create_csv(read_to_list(WORD_LIST_TEXT), STATISTICS)
    # gen_statistics(STATISTICS, "wordle_frequencys3.csv")

    print(get_possible_sol_dist([2, 0, 1, 1]))
