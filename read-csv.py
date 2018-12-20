#!/usr/bin/python

from sklearn import tree
import csv
import sys
import sqlite3

def read_everyone_from_db():
    conn = sqlite3.connect('/Users/julio.barros/mxmtch.db')
    cursor = conn.cursor()

    cursor.execute("SELECT distinct track_id from lyrics")
    everyone = cursor.fetchall()
    conn.close()
    return everyone

def fetch_words():
    conn = sqlite3.connect('/Users/julio.barros/mxmtch.db')
    cursor = conn.cursor()

    cursor.execute("SELECT ROWID, word from words")
    everyone = cursor.fetchall()
    conn.close()
    return dict((x[1], x[0]) for x in everyone[0:])

def generate_input_array(lyric_rows, words):
    input = [0] * 5001
    for row in lyric_rows:
        input[words[row[2]]] = row[3]

    return input


def fetch(track_id):
    conn = sqlite3.connect('/Users/julio.barros/mxmtch.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * from lyrics where track_id = '" + track_id + "'")
    lines = cursor.fetchall()
    conn.close()
    return lines

def find_genre(track_id):
    with open('/Users/julio.barros/Downloads/msd_tagtraum_cd2.cls', newline='') as csvfile:
        songreader = csv.reader(csvfile, delimiter='\t', dialect='unix')
        for row in songreader:
            if row[0].strip() == track_id:
                return style_to_number(row[1].strip())

def style_to_number(style):
    return {
        'Metal': 1,
        'Punk': 2,
        'World': 3,
        'Pop': 4,
        'Rock': 5,
        'Electronic': 6,
        'Rap': 7,
        'Jazz': 8,
        'Latin': 9,
        'RnB': 10,
        'International': 11,
        'Country': 12,
        'Reggae': 13,
        'Blues': 14,
        'Vocal': 15,
        'Folk': 16,
        'New Age': 17
    }[style]

def number_to_style(number):
    return {
        1: 'Metal',
        2: 'Punk',
        3: 'World',
        4: 'Pop',
        5: 'Rock',
        6: 'Electronic',
        7: 'Rap',
        8: 'Jazz',
        9: 'Latin',
        10: 'RnB',
        11: 'International',
        12: 'Country',
        13: 'Reggae',
        14: 'Blues',
        15: 'Vocal',
        16: 'Folk',
        17: 'New Age'
    }[number]

if __name__ == '__main__':
    words = fetch_words()
    x = []
    y = []
    i = 0

    with open('/Users/julio.barros/chamine-learning/musicas_nos_2_2.csv', newline='') as csvfile:
        songreader = csv.reader(csvfile, delimiter='\t', dialect='unix')
        for row in songreader:
            x.append( generate_input_array(fetch(track_id=row[0].strip()), words) )
            y.append( find_genre(track_id=row[0].strip()) )
            i += 1
            if i > 5000: break

    print('Finished creating inputs, classifying...')
    clf = tree.DecisionTreeClassifier()
    clf.fit(list(x), list(y))
    print('Classified! Let`s fit, write a track_id and we will try to predict')
    print('(Press [x] to exit)')

    x2 = []
    for line in sys.stdin:
        if line.strip() == 'x': break
        x2.append(generate_input_array(fetch(track_id=line.strip()), words))
        print('Result: ', number_to_style(clf.predict(x2)[0]))
        print('Expected: ', number_to_style(find_genre(track_id=line.strip())))
        x2.clear()
        pass
            # print('musica id:', row[0].strip(), ' | estilo:', row[1].strip())