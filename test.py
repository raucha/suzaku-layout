# coding: utf-8

import re
import pykakasi
# import cutlet
import MeCab

print('hello world')

"""
方針：
句読点や数字で区切られた文章の範囲を１つの評価単位長さとする。
各単位長さを表現するのにかかるコストを評価する。
コストの算出は、２つのキーを億語に連打した時にかかる時間をベースにする。
将来性につて確認
"""

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

f = open('./dataset/KWDLC/disc/disc.txt')
line = f.readline()
texts = []
while line:
    texts.append(line)
    line = f.readline()

texts = filter(lambda x: not re.match(r'^\s*$', x), texts)
texts = filter(lambda x: not re.match(r'^#.*$', x), texts)
texts = map(lambda x: x.split(" ")[1].rstrip(), texts)
texts = list(texts)
for i, _ in enumerate(texts):
    for p in pairs:
        texts[i] = texts[i].replace(p[0], p[1])
texts = list(texts)
print(texts[0:10])

kks = pykakasi.kakasi()

# texts[0]
for item in kks.convert(texts[0]):
    print("{}: kana '{}', hiragana '{}', romaji: '{}'".format(
        item['orig'], item['kana'], item['hira'], item['hepburn']))
    

mecab = MeCab.Tagger("-Oyomi")
print(mecab.parse(texts[0]))
# katsu = cutlet.Cutlet()
# print(katsu.romaji(texts[0]))

