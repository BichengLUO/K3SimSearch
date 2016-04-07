#!/usr/bin/env python
import sys
import csv
import operator
import os.path
import platform
import urllib
import urllib2
import json
from datetime import datetime
from colorama import init
from colorama import Fore, Back, Style

session_dir = 'sessions'

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

def write_matrix_to_multiple_file(d_matrix):
    print '[Info] Start writing matrix from local cache...'
    unit = 4000
    length = len(d_matrix)
    for k in range(length // unit + 1):
        with open('d_matrix' + str(k), 'wb') as matrix_file:
            for i in range(k * unit, min((k + 1) * unit, length)):
                for j in range(length):
                    matrix_file.write(chr(d_matrix[i][j]))
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

def read_matrix_data_from_multiple_file(length):
    matrix_bytes = []
    print '[Info] Start reading matrix from local cache...'
    unit = 4000
    for k in range(length // unit + 1):
        with open('d_matrix' + str(k), 'rb') as matrix_file:
            matrix_bytes.extend(matrix_file.read())
    print '[Info] Reading matrix data done!'
    return matrix_bytes

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
    if os.path.isfile('d_matrix0'):
        matrix_data = read_matrix_data_from_multiple_file(len(words))
    else:
        print Fore.RED + "[Error] Can't locate the local cache file..." + Fore.RESET
        matrix_data = calc_matrix(words)
        write_matrix_to_multiple_file(matrix_data)
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
        print Fore.RED + "[Error] Sorry, can't find the word!" + Fore.RESET
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
            print Fore.RED + "[Error] We can't find " + word + ' in the local dictionary'  + Fore.RESET
            search_online(word)
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
    for i in range(len(sorted_results)):
        print Back.BLUE + Style.BRIGHT + sorted_results[i]['item']['word'] + Style.RESET_ALL + Back.RESET,
    print ''
    raw_input("Press Enter to show definitions...")
    print '=============== Definitions =================='
    for r in sorted_results:
        print Back.BLUE + '[' + str(r['edit_dist']) + '] ' + Style.BRIGHT + r['item']['word'] + Style.RESET_ALL + Back.RESET
        if platform.system() == 'Windows':
            print r['item']['meaning'].decode('UTF-8')
        else:
            print r['item']['meaning']
        print '-----------------------------------'
        today = datetime.now().strftime('%Y-%m-%d.csv')
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        with open(session_dir + '/' + today, 'a') as today_file:
            today_file.write(r['item']['word'] + ',"' + r['item']['meaning'].decode('UTF-8').encode('GBK') + '"\n')

def merge_words(words_1, words_2):
    print '[Info] Start merging words...'
    merged = {}
    for item in words_1 + words_2:
        if item['word'] in merged:
            merged[item['word']].update(item)
        else:
            merged[item['word']] = item
    print '[Info] Two dictionaries merged!'
    return sorted([val for (_, val) in merged.items()], key = operator.itemgetter('word'))

def merge_words3(words_1, words_2, words_3):
    print '[Info] Start merging words...'
    merged = {}
    for item in words_1 + words_2 + words_3:
        if item['word'] in merged:
            merged[item['word']].update(item)
        else:
            merged[item['word']] = item
    print '[Info] Three dictionaries merged!'
    return sorted([val for (_, val) in merged.items()], key = operator.itemgetter('word'))

def print_logo():
    logo_string = '''
  _  ___________  _           ____                      _
 | |/ /___ / ___|(_)_ __ ___ / ___|  ___  __ _ _ __ ___| |__
 | ' /  |_ \___ \| | '_ ` _ \\\\___ \ / _ \/ _` | '__/ __| '_ \\
 | . \ ___) |__) | | | | | | |___) |  __/ (_| | | | (__| | | |
 |_|\_\____/____/|_|_| |_| |_|____/ \___|\__,_|_|  \___|_| |_|
                                         By Eagle, 2016/02/04
    '''
    print Fore.CYAN + logo_string + Fore.RESET

def search_online(word):
    print 'Try finding ' + word + ' online...'
    params = urllib.urlencode({'s': '|1{'.join(word.split())})
    resp = urllib2.urlopen('http://www.iciba.com/index.php?c=search&a=suggestnew&%s' % params)
    obj = json.loads(resp.read())
    if obj['status'] == 1:
        print '-----------------------------------'
        n_word = obj['message'][0]['key']
        print Back.BLUE + Style.BRIGHT + n_word + Style.RESET_ALL + Back.RESET
        all_definition = ''
        for i in range(len(obj['message'][0]['means'])):
            definition = obj['message'][0]['means'][i]['part']
            l = len(obj['message'][0]['means'][i]['means'])
            for j in range(l - 1):
                definition = obj['message'][0]['means'][i]['means'][j] + ', '
            definition += obj['message'][0]['means'][i]['means'][l - 1]
            if platform.system() == 'Windows':
                print definition
            else:
                print definition.encode('UTF-8')
            all_definition += definition + ' '
        today = datetime.now().strftime('%Y-%m-%d.csv')
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        with open(session_dir + '/' + today, 'a') as today_file:
            today_file.write(n_word.encode('GBK') + ',"' + all_definition.encode('GBK') + '"\n')
        print '-----------------------------------'
    else:
        print "Sorry, we still can't find it"

def main():
    init()
    print_logo()
    words_3k = load_dictionary('ZYNM3K.csv')
    words_hbs = load_dictionary('HBS.csv')
    words_econ = load_dictionary('ECON.csv')
    words = merge_words3(words_econ, words_hbs, words_3k)
    matrix_data = dist_matrix(words)
    while True:
        line = raw_input(Back.GREEN + 'Enter the word to search ("q" to exit):' + Back.RESET + ' ')
        if line in ['quit', 'q', 'QUIT', 'Q']:
            print '[Info] The script is ending now'
            break
        if line == '':
            continue
        ind = similarity_search(line, words)
        if ind == -1:
            search_online(line)
        else:
            output_result(ind, words, matrix_data)

if __name__ == '__main__':
    main()
