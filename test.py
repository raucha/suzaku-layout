# coding: utf-8

import re

print('hello world')

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
