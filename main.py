from os.path import exists

import pandas as pd

STATISTICS = "wordle_frequencys.csv"
WORD_LIST_TEXT = "words.txt"
WORD_LIST = []


def ret_wordle_num(word1, word2):
    final_score = ""
    for index in range(len(word1)):
        #print(word2)
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
    if exists(out_file):
        # File already exists
        return

    df = pd.DataFrame(index=in_list,
                      columns=in_list)
    df.to_csv(out_file)


def read_to_list(in_file):
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


if __name__ == '__main__':
    create_csv(read_to_list(WORD_LIST_TEXT), STATISTICS)
    gen_statistics(STATISTICS, "wordle_frequencys3.csv")
    # print(ret_wordle_num("aback", "abbey"))
    # print("22000")
