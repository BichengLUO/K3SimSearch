#!/usr/bin/env python
import csv
import operator
import os.path

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def write_matrix_to_file(d_matrix):
    length = len(d_matrix)
    with open('d_matrix', 'w') as matrix_file:
        for i in range(length):
            for j in range(length - 1):
                matrix_file.write(str(d_matrix[i][j]) + ' ')
            matrix_file.write(str(d_matrix[i][length - 1]) + '\n')

def read_matrix_from_file(length):
    d_matrix = [[0 for x in range(length)] for x in range(length)]
    i = j = 0
    print 'Start reading matrix from local cache...'
    with open('d_matrix', 'r') as matrix_file:
        for line in matrix_file:
            for word in line.split():
                d_matrix[i][j] = int(word)
                i = i + 1
            i = 0
            j = j + 1
    print 'Reading matrix done!'
    return d_matrix

def calc_matrix(words):
    length = len(words)
    d_matrix = [[0 for x in range(length)] for x in range(length)]
    for i in range(length):
        for j in range(i + 1, length):
            word_i = words[i]['word']
            word_j = words[j]['word']
            edit_dist = levenshtein(word_i, word_j)
            d_matrix[i][j] = d_matrix[j][i] = edit_dist
    return d_matrix

def dist_matrix(words):
    if os.path.isfile('d_matrix'):
        d_matrix = read_matrix_from_file(len(words))
    else:
        d_matrix = calc_matrix(words)
        write_matrix_to_file(d_matrix)
    print 'Matrix established!'
    return d_matrix

def load_dictionary_gen(csvfile):
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        yield {key : value for key, value in row.iteritems()}

def load_dictionary():
    words = []
    with open('ZYNM3K.csv', 'rb') as csvfile:
        dictionary = load_dictionary_gen(csvfile)
        for word in dictionary:
            words.append(word)
    print 'Dictionary loaded!'
    return words

def similarity_search(word, words):
    length = len(words)
    match_list = [i for i in range(length) if levenshtein(words[i]['word'], word) < 2]
    if len(match_list) == 0:
        print "Can't find the word!  The script quited now..."
        return -1
    else:
        min_dist = 999
        closest = 0
        for i in match_list:
            dist = levenshtein(words[i]['word'], word)
            if (dist < min_dist):
                closest = i
                min_dist = dist
        if min_dist != 0:
            print "We can't find " + word + ' in the dictionary'
            print 'Are you looking for ' + words[closest]['word'] + '?'

        return closest

def output_result(ind, words, d_matrix):
    length = len(words)
    results = []
    word_len = len(words[ind]['word'])
    if word_len >= 9:
        threshhold = word_len / 3.0
    else:
        threshhold = 3.0
    for i in range(length):
        ed = d_matrix[ind][i]
        if (ed < threshhold):
            results.append({'edit_dist' : ed, 'item' : words[i]})
    sorted_results = sorted(results, key = operator.itemgetter('edit_dist'))
    for r in sorted_results:
        print '[' + str(r['edit_dist']) + '] ' + r['item']['word']
        print r['item']['meaning']
        print '-----------------------------------'

def main():
    words = load_dictionary()
    d_matrix = dist_matrix(words)
    while True:
        line = raw_input('Enter the word: ')
        ind = similarity_search(line, words)
        if ind != -1:
            output_result(ind, words, d_matrix)
        else:
            break

if __name__ == '__main__':
    main()
