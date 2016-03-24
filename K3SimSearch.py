#!/usr/bin/env python
import sys
import csv
import operator
import os.path
import platform
import urllib2
import re

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
    print '[Info] Start writing matrix from local cache...'
    length = len(d_matrix)
    with open('d_matrix', 'wb') as matrix_file:
        last = 0
        for i in range(length):
            for j in range(length):
                matrix_file.write(chr(d_matrix[i][j]))
            if i - last >= length / 20.0:
                sys.stdout.write('#')
                sys.stdout.flush()
                last = i
    print '\n[Info] Writing matrix done!'

def read_matrix_from_file(length):
    d_matrix = [[0 for x in range(length)] for x in range(length)]
    i = j = 0
    print '[Info] Start reading matrix from local cache...'
    with open('d_matrix', 'rb') as matrix_file:
        matrix_bytes = matrix_file.read()
        last = 0
        for i in range(length):
            for j in range(length):
                d_matrix[i][j] = ord(matrix_bytes[i * length + j])
            if i - last >= length / 20.0:
                sys.stdout.write('#')
                sys.stdout.flush()
                last = i
    print '\n[Info] Reading matrix done!'
    return d_matrix

def read_matrix_data_from_file(length):
    matrix_bytes = []
    print '[Info] Start reading matrix from local cache...'
    with open('d_matrix', 'rb') as matrix_file:
        matrix_bytes = matrix_file.read()
    print '[Info] Reading matrix data done!'
    return matrix_bytes

def calc_matrix(words):
    print '[Info] Start calculating matrix from dictionary...'
    length = len(words)
    print '[Info] Total words count: ' + str(length)
    d_matrix = [[0 for x in range(length)] for x in range(length)]
    last = 0
    for i in range(length):
        for j in range(i + 1, length):
            word_i = words[i]['word']
            word_j = words[j]['word']
            edit_dist = levenshtein(word_i, word_j)
            d_matrix[i][j] = d_matrix[j][i] = edit_dist
        if i - last >= length / 20.0:
            sys.stdout.write('#')
            sys.stdout.flush()
            last = i
    print '\n[Info] Calculation done!'
    return d_matrix

def dist_matrix(words):
    if os.path.isfile('d_matrix'):
        matrix_data = read_matrix_data_from_file(len(words))
    else:
        print "[Error] Can't locate the local cache file..."
        d_matrix = calc_matrix(words)
        write_matrix_to_file(d_matrix)
    print '[Info] Matrix established!'
    return matrix_data

def load_dictionary_gen(csvfile):
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        yield {key : value for key, value in row.iteritems()}

def load_dictionary(name):
    words = []
    with open(name, 'rb') as csvfile:
        dictionary = load_dictionary_gen(csvfile)
        for word in dictionary:
            words.append(word)
    print '[Info] ' + name + ' dictionary loaded!'
    return words

def similarity_search(word, words):
    length = len(words)
    match_list = [i for i in range(length) if levenshtein(words[i]['word'], word) < 2]
    if len(match_list) == 0:
        print "[Error] Sorry, can't find the word!"
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
            print "[Error] We can't find " + word + ' in the dictionary'
            print '[Info] Are you looking for ' + words[closest]['word'] + '?'

        return closest

def output_result(ind, words, matrix_data):
    length = len(words)
    results = []
    word_len = len(words[ind]['word'])
    if word_len >= 9:
        threshhold = word_len / 3.0
    elif word_len <= 5:
        threshhold = 2.0
    else:
        threshhold = 3.0
    for i in range(length):
        ed = ord(matrix_data[ind * length + i])
        if (ed < threshhold):
            results.append({'edit_dist' : ed, 'item' : words[i]})
    sorted_results = sorted(results, key = operator.itemgetter('edit_dist'))
    print '============= Visually Similar ==============='
    print ''
    for i in range(len(sorted_results) - 1):
        print sorted_results[i]['item']['word'] + ', ',
    print sorted_results[-1]['item']['word']
    print ''
    raw_input("Press Enter to show definitions...")
    print '=============== Definitions =================='
    for r in sorted_results:
        print '[' + str(r['edit_dist']) + '] ' + r['item']['word']
        if platform.system() == 'Windows':
            print r['item']['meaning'].decode('UTF-8')
        else:
            print r['item']['meaning']
        print '-----------------------------------'

def merge_words(words_1, words_2):
    print '[Info] Start merging words...'
    merged = {}
    for item in words_1 + words_2:
        if item['word'] in merged:
            merged[item['word']].update(item)
        else:
            merged[item['word']] = item
    print '[Info] Two dictionaries merged!'
    return [val for (_, val) in merged.items()]

def print_logo():
    logo_string = '''
  _  ___________  _           ____                      _
 | |/ /___ / ___|(_)_ __ ___ / ___|  ___  __ _ _ __ ___| |__
 | ' /  |_ \___ \| | '_ ` _ \\\\___ \ / _ \/ _` | '__/ __| '_ \\
 | . \ ___) |__) | | | | | | |___) |  __/ (_| | | | (__| | | |
 |_|\_\____/____/|_|_| |_| |_|____/ \___|\__,_|_|  \___|_| |_|
                                         By Eagle, 2016/02/04
    '''
    print logo_string

def search_online(word):
    print 'Try finding ' + word + ' online...';
    resp = urllib2.urlopen('http://learnersdictionary.com/definition/' + word)
    html = resp.read()
    result = re.findall('def_text">(.*?)</span', html)
    if result:
        print '-----------------------------------'
        print word
        for i in range(len(result)):
            print '[' + str(i + 1) + '] ' + result[i]
        print '-----------------------------------'
    else:
        print "Sorry, we still can't find it"

def main():
    print_logo()
    words_3k = load_dictionary('ZYNM3K.csv')
    words_hbs = load_dictionary('HBS.csv')
    words = merge_words(words_hbs, words_3k)
    matrix_data = dist_matrix(words)
    while True:
        line = raw_input('Enter the word to search ("q" to exit): ')
        if line in ['quit', 'q', 'QUIT', 'Q']:
            print '[Info] The script is ending now'
            break
        ind = similarity_search(line, words)
        if ind == -1:
            search_online(line)
        else:
            output_result(ind, words, matrix_data)

if __name__ == '__main__':
    main()
