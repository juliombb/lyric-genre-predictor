#!/usr/bin/python

from sklearn import tree
from sklearn import neighbors
import numpy as np
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

def find_genre2(track_id, songs):
    for row in songs:
        if row[0].strip() == track_id:
            return style_to_number(row[1].strip())

def find_genre(row):
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
    TRAIN = 20000
    songs = np.genfromtxt('musicas_cons2.csv', delimiter='\t', usecols=range(2), dtype=str)

    print("Songs fetched.")

    for row in songs:
        x.append( generate_input_array(fetch(track_id=row[0].strip()), words) )
        y.append( find_genre(row) )
        i += 1
        if i > TRAIN: break

    print('Finished creating inputs, classifying...')
    clf = neighbors.NearestNeighbors(n_neighbors=2, algorithm='ball_tree')
    # clf = tree.DecisionTreeClassifier()
    clf.fit(list(x), list(y))
    print('Classified! Let`s test')

    x2 = []
    i = 0
    right = 0

    while i < 6000:
        x2.append(generate_input_array(fetch(track_id=songs[i+TRAIN][0].strip()), words))
        result = number_to_style(clf.predict(x2)[0])
        expected = number_to_style(find_genre(songs[i+TRAIN]))
        if (result == expected):
            right += 1

        x2.clear()
        i += 1

    print('Trialed accuracy: ', right*100 / i, '%')

    print('Let`s fit, write a track_id and we will try to predict')
    print('(Press [x] to exit)')

    for line in sys.stdin:
        if line.strip() == 'x': break
        x2.append(generate_input_array(fetch(track_id=line.strip()), words))
        print('Result: ', number_to_style(clf.predict(x2)[0]))
        print('Expected: ', number_to_style(find_genre2(track_id=line.strip(), songs=songs)))
        x2.clear()
        pass
            # print('musica id:', row[0].strip(), ' | estilo:', row[1].strip())