#!/usr/bin/env python3
# coding:utf-8

import re
import MeCab
import pickle
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

"""
方針：
句読点や数字で区切られた文章の範囲を１つの評価単位長さとする。
各単位長さを表現するのにかかるコストを評価する。
コストの算出は、２つのキーを億語に連打した時にかかる時間をベースにする。
将来性につて確認
"""

def get_score(text):
    return len(text)

def load_dataset():
    try:
        data = pickle.load(open("disc.pickle", "rb"))
    except (OSError, IOError) as e:
        f = open('../../dataset/KWDLC/disc/disc.txt')
        lines = f.read()  # ファイル終端まで全て読んだデータを返す
        f.close()
        data = extract_vailed_texts(lines)
        data = list(map(lambda x: regularize_text(x), data))
        pickle.dump(data, open("./disc.pickle", "wb"))
    print(data[0])


def extract_vailed_texts(texts):
    # f = open('../dataset/KWDLC/disc/disc.txt')
    # line = f.readline()
    # texts = []
    # for line in lines2:
    #     print(line),
    # print
    # while line:
    #     texts.append(line)
    #     line = f.readline()

    texts = texts.splitlines()
    texts = filter(lambda x: not re.match(r'^\s*$', x), texts)
    texts = filter(lambda x: not re.match(r'^#.*$', x), texts)
    texts = map(lambda x: x.split(" ", 1)[1].rstrip(), list(texts))
    texts = list(texts)
    return texts


def regularize_text(text):
    pairs = [
        ["０", "0"],
        ["１", "1"],
        ["２", "2"],
        ["３", "3"],
        ["４", "4"],
        ["５", "5"],
        ["６", "6"],
        ["７", "7"],
        ["８", "8"],
        ["９", "9"],
        ["，", ","],
        ["、", ","],
        ["．", "."],
        ["。", "."]
    ]
    for p in pairs:
        text = text.replace(p[0], p[1])
    mecab = MeCab.Tagger("-Oyomi")
    text = mecab.parse(text).rstrip()
    return text


if __name__ == "__main__":
    load_dataset()
