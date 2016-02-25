#!/usr/bin/env python
import sys
import csv
import operator
import os.path
import platform
import random
import urllib2
import re
import HTMLParser

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

HTML_PS = HTMLParser.HTMLParser()
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def print_logo():
    logo_string = '''
  _  ______
 | |/ /___ \\
 | ' /  __) |
 |  <  |__ <
 | . \ ___) |
 |_|\_\____/            _
 |  __ \               | |
 | |__) |__ _ _ __   __| | ___  _ __ ___
 |  _  // _` | '_ \ / _` |/ _ \| '_ ` _ \\
 | | \ \ (_| | | | | (_| | (_) | | | | | |
 |_|__\_\__,_|_| |_|\__,_|\___/|_| |_| |_|
  / ____|          | |
 | (___   ___ _ __ | |_ ___ _ __   ___ ___
  \___ \ / _ \ '_ \| __/ _ \ '_ \ / __/ _ \\
  ____) |  __/ | | | ||  __/ | | | (_|  __/
 |_____/ \___|_| |_|\__\___|_| |_|\___\___
                    by Eagle Sky, 2016/2/25
    '''
    print logo_string

def print_manual():
    print '\n---------------------MANUAL------------------------\n'
    print '1. This script needs the network reachability supports, so keep your connection when you use this script.'
    print '2. The sentences are chosen randomly from Webster Learners Dictionary.'
    print '3. If you wanna see the definition of the word which the sentence includes, enter "n" to show it.'
    print '4. Enter "q" to quit the script.\n'
    print 'Thank you for your patience. Having fun when preparing for GRE!'
    print '\n---------------------------------------------------\n'

def main():
    print_logo()
    words_3k = load_dictionary('ZYNM3K.csv')
    words_hbs = load_dictionary('HBS.csv')
    words = merge_words(words_hbs, words_3k)
    print_manual()
    all_count = 0
    wrong_count = 0
    while True:
        random_item = random.choice(words)
        word = random_item['word']
        resp = urllib2.urlopen('http://learnersdictionary.com/definition/' + word)
        html = resp.read()
        result = re.findall('vi_content">(.*?)</div', html)
        if result:
            example = ''
            for i in range(min(len(result), 3)):
                example += '>> ' + HTML_PS.unescape(remove_tags(result[i])) + '\n'
            line = raw_input(example + '\n   y/n/q? ')
            if line == 'n' or line == 'N':
                print '\n   ' + word
                if platform.system() == 'Windows':
                    print '   ' + random_item['meaning'].decode('UTF-8')
                else:
                    print '   ' + random_item['meaning']
                wrong_count += 1
            elif line in ['quit', 'q', 'QUIT', 'Q']:
                print '---------------------------'
                print 'You got a score of ' + str((all_count - wrong_count) * 100 / all_count) + ' in this test!'
                print '[Info] The script is ending now'
                break
            all_count += 1
            print '---------------------------'

if __name__ == '__main__':
    main()
