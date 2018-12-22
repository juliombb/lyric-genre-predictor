import numpy as np


def find(track_id, songreader):
    for row in songreader:
        if row[0].strip() == track_id:
            return row

if __name__ == '__main__':
    songreader = np.genfromtxt('/Users/julio.barros/Downloads/msd_tagtraum_cd2.cls', delimiter='\t', usecols=range(2), dtype=str)
    songreader2 = np.genfromtxt('/Users/julio.barros/chamine-learning/musicas_nos_2_2.csv', delimiter='\t', usecols=range(1), dtype=str)

    dic = {}

    for row in songreader2:
        dic[row] = True

    for row in songreader:
        if (dic.get(row[0], False)):
            print(row[0], '\t', row[1])