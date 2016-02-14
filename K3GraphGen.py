#!/usr/bin/env python
import csv
import os.path

header = '''<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <meta lastmodifieddate="2009-03-20">
        <creator>BichengLUO</creator>
        <description>K3 Graph</description>
    </meta>
    <graph mode="static" defaultedgetype="undirected">
        <nodes>
'''
mid = '''
        </nodes>
        <edges>
'''
tail = '''
        </edges>
    </graph>
</gexf>
'''

def read_matrix_from_file(length):
    d_matrix = [[0 for x in range(length)] for x in range(length)]
    i = j = 0
    print '[Info] Start reading matrix from local cache...'
    with open('d_matrix', 'r') as matrix_file:
        for line in matrix_file:
            for word in line.split():
                d_matrix[i][j] = int(word)
                i = i + 1
            i = 0
            j = j + 1
    print '[Info] Reading matrix done!'
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
    print '[Info] Dictionary loaded!'
    return words

def generate_gexf(words, d_matrix):
    print '[Info] Generating GEXF file...'
    length = len(words)
    with open('k3.gexf', 'w') as gexf:
        gexf.write(header)
        for i in range(length):
            gexf.write('            <node id="' + str(i) + '" label="' + words[i]['word'] + '" />\n')
        gexf.write(mid)
        edge_id = 0
        for i in range(length):
            for j in range(i + 1, length):
                word_len = min(len(words[i]['word']), len(words[j]['word']))
                if word_len >= 9:
                    threshhold = word_len / 3.0
                elif word_len <= 4:
                    threshhold = 2.0
                else:
                    threshhold = 3.0
                if (d_matrix[i][j] < threshhold):
                    gexf.write('            <edge id="' + str(edge_id) + '" source="' + str(i) + '" target="' + str(j) + '" />\n')
                    edge_id = edge_id + 1
        gexf.write(tail)
    print '[Info] Generation of GEXF file completed!'

def main():
    words = load_dictionary()
    if os.path.isfile('d_matrix'):
        d_matrix = read_matrix_from_file(len(words))
        generate_gexf(words, d_matrix)
    else:
        print '[Error] Can not located matrix file'

if __name__ == '__main__':
    main()
