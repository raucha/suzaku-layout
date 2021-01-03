#!/usr/bin/env python3
# coding:utf-8

import re
import MeCab
import pickle
import os
from jaconv import kata2hira
import pandas as pd
import codecs
import mojimoji

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

"""
方針：
句読点や数字で区切られた文章の範囲を１つの評価単位長さとする。
各単位長さを表現するのにかかるコストを評価する。
コストの算出は、２つのキーを億語に連打した時にかかる時間をベースにする。
将来性につて確認

ToDo:
+ 下記のため、クラス化する。
    - 関数が多すぎる
    - データセットのロードが毎回行われる or ルートのスコープで保持しなければならない
+ テストをdoctestかnoseに切り替えたい。
"""

"""
母音、子音へのキー割り当て→　直積でカタカナ生成
カタカナ→キーストロークへの変換テーブル
"""


def char2stroke(char):
    """入力文字を押下するキーに変換

    Args:
        char (str): 文字。ASCIIまたはひらがなの一音(拗音含む)

    Returns:
        str: 押下するキー列
    """
    boin = {
        "a": "l",
        "i": ";",
        "u": "j",
        "e": "h",
        "o": "k",
        "ya": "o",
        "yu": "u",
        "yo": "i",
        "xa": "",
        "xi": "",
        "xu": "",
        "xe": "",
        "xo": "",
    }

    shiin = {
        "a": "a",
        "k": "s",
        "s": "d",
        "t": "f",
        "n": "c",
        "h": "g",
        "m": "v",
        "y": "",
        "r": "z",
        "w": "",
        "g": "w",
        "z": "e",
        "d": "r",
        "b": "t",
        "p": "b",
    }

    kana2key = {
        "あ": shiin["a"] + boin["a"],
        "い": shiin["a"] + boin["i"],
        "う": shiin["a"] + boin["u"],
        "え": shiin["a"] + boin["e"],
        "お": shiin["a"] + boin["o"],
        "か": shiin["k"] + boin["a"],
        "き": shiin["k"] + boin["i"],
        "く": shiin["k"] + boin["u"],
        "け": shiin["k"] + boin["e"],
        "こ": shiin["k"] + boin["o"],
        "さ": shiin["s"] + boin["a"],
        "し": shiin["s"] + boin["i"],
        "す": shiin["s"] + boin["u"],
        "せ": shiin["s"] + boin["e"],
        "そ": shiin["s"] + boin["o"],
        "た": shiin["t"] + boin["a"],
        "ち": shiin["t"] + boin["i"],
        "つ": shiin["t"] + boin["u"],
        "て": shiin["t"] + boin["e"],
        "と": shiin["t"] + boin["o"],
        "な": shiin["n"] + boin["a"],
        "に": shiin["n"] + boin["i"],
        "ぬ": shiin["n"] + boin["u"],
        "ね": shiin["n"] + boin["e"],
        "の": shiin["n"] + boin["o"],
        "は": shiin["h"] + boin["a"],
        "ひ": shiin["h"] + boin["i"],
        "ふ": shiin["h"] + boin["u"],
        "へ": shiin["h"] + boin["e"],
        "ほ": shiin["h"] + boin["o"],
        "ま": shiin["m"] + boin["a"],
        "み": shiin["m"] + boin["i"],
        "む": shiin["m"] + boin["u"],
        "め": shiin["m"] + boin["e"],
        "も": shiin["m"] + boin["o"],
        "や": shiin["y"] + boin["a"],
        "ゆ": shiin["y"] + boin["u"],
        "よ": shiin["y"] + boin["o"],
        "ら": shiin["r"] + boin["a"],
        "り": shiin["r"] + boin["i"],
        "る": shiin["r"] + boin["u"],
        "れ": shiin["r"] + boin["e"],
        "ろ": shiin["r"] + boin["o"],
        "が": shiin["g"] + boin["a"],
        "ぎ": shiin["g"] + boin["i"],
        "ぐ": shiin["g"] + boin["u"],
        "げ": shiin["g"] + boin["e"],
        "ご": shiin["g"] + boin["o"],
        "ざ": shiin["z"] + boin["a"],
        "じ": shiin["z"] + boin["i"],
        "ず": shiin["z"] + boin["u"],
        "ぜ": shiin["z"] + boin["e"],
        "ぞ": shiin["z"] + boin["o"],
        "だ": shiin["d"] + boin["a"],
        "ぢ": shiin["d"] + boin["i"],
        "づ": shiin["d"] + boin["u"],
        "で": shiin["d"] + boin["e"],
        "ど": shiin["d"] + boin["o"],
        "ば": shiin["b"] + boin["a"],
        "び": shiin["b"] + boin["i"],
        "ぶ": shiin["b"] + boin["u"],
        "べ": shiin["b"] + boin["e"],
        "ぼ": shiin["b"] + boin["o"],
        "ぱ": shiin["p"] + boin["a"],
        "ぴ": shiin["p"] + boin["i"],
        "ぷ": shiin["p"] + boin["u"],
        "ぺ": shiin["p"] + boin["e"],
        "ぽ": shiin["p"] + boin["o"],
        "きゃ": shiin["k"] + boin["ya"],
        "きゅ": shiin["k"] + boin["yu"],
        "きょ": shiin["k"] + boin["yo"],
        "しゃ": shiin["s"] + boin["ya"],
        "しゅ": shiin["s"] + boin["yu"],
        "しょ": shiin["s"] + boin["yo"],
        "ちゃ": shiin["t"] + boin["ya"],
        "ちゅ": shiin["t"] + boin["yu"],
        "ちょ": shiin["t"] + boin["yo"],
        "にゃ": shiin["n"] + boin["ya"],
        "にゅ": shiin["n"] + boin["yu"],
        "にょ": shiin["n"] + boin["yo"],
        "ひゃ": shiin["g"] + boin["ya"],
        "ひゅ": shiin["g"] + boin["yu"],
        "ひょ": shiin["g"] + boin["yo"],
        "みゃ": shiin["m"] + boin["ya"],
        "みゅ": shiin["m"] + boin["yu"],
        "みょ": shiin["m"] + boin["yo"],
        "りゃ": shiin["r"] + boin["ya"],
        "りゅ": shiin["r"] + boin["yu"],
        "りょ": shiin["r"] + boin["yo"],
        "ぎゃ": shiin["g"] + boin["ya"],
        "ぎゅ": shiin["g"] + boin["yu"],
        "ぎょ": shiin["g"] + boin["yo"],
        "じゃ": shiin["z"] + boin["ya"],
        "じゅ": shiin["z"] + boin["yu"],
        "じょ": shiin["z"] + boin["yo"],
        "ぢゃ": shiin["d"] + boin["ya"],
        "ぢゅ": shiin["d"] + boin["yu"],
        "ぢょ": shiin["d"] + boin["yo"],
        "びゃ": shiin["b"] + boin["ya"],
        "びゅ": shiin["b"] + boin["yu"],
        "びょ": shiin["b"] + boin["yo"],
        "ぴゃ": shiin["p"] + boin["ya"],
        "ぴゅ": shiin["p"] + boin["yu"],
        "ぴょ": shiin["p"] + boin["yo"],
        "わ": "zl",
        "を": "zk",
        "ん": "zh",
        "っ": "zj",
        "ー": "z;",
        "ぁ": "q" + boin["a"],
        "ぃ": "q" + boin["i"],
        "ぅ": "q" + boin["u"],
        "ぇ": "q" + boin["e"],
        "ぉ": "q" + boin["o"],
        # "ゃ": "q",
        # "ゅ": "q",
        # "ょ": "q",
        "・": "/",
        "･": "/",
        "「": "[",
        "」": "]",
        "｢": "]",
        "｣": "]",
        "ｰ": "z;",
        ",": "z;",
        "◆": "",
        "【": "",
        "】": "",
    }

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
        ["。", "."],
        ["：", ":"],
        # ["'", " "],
        # ['"', " "],
        ["払金", ""],
        ["試着", ""],
        # ["金", ""],
        ["々", ""],
        ["”", " "],
        ["“", " "],
        ["（", " "],
        ["）", " "],
        ["『", "「"],
        ["』", "」"],
        ["／", "/"],
        ["！", "!"],
        ["？", "?"],
        ["●", "まる"],
    ]
    for p in pairs:
        char = char.replace(p[0], p[1])

    # print(char)
    if 1 == len(char) and ord(char) < 128:
        return char
    else:
        return kana2key.get(char)


print("loading csv")
df = pd.read_csv("./../2stroke_timetable.csv", index_col=0)
print("loaded csv")


def keystrokes2score(keystrokes, head=None):
    """キー押下の列から所要時間を算出。再帰関数。

    Args:
        keystrokes (str): 評価対象キー押下列
        head ([str], optional): 1つ前の文字。行頭の場合はNone。

    Returns:
        float: 所要時間
    """
    # 文字数が0はスコア0
    if 0 == len(keystrokes):
        return 0.0

    # headがない場合は文字列の先頭の文字を利用
    if None == head:
        head = keystrokes[0]

    # df = pd.read_csv('./../2stroke_timetable.csv', index_col=0)
    # print("loaded csv")
    return df.loc[head, keystrokes[0]] + keystrokes2score(keystrokes[1:])


def devide_strokes_side(strokes):
    """キー押下の列を左手右手に分割

    Args:
        strokes (str): 押下するキー列

    Returns:
        左手で押すキー、右手で押すキー
    """
    key_l = "qwertasdfgzxcvb"
    key_r = "yuiop@[hjkl;:]nm,./\\"
    strk_l = "".join([c for c in strokes if c in key_l])
    strk_r = "".join([c for c in strokes if c in key_r])
    return strk_l, strk_r


def text2keystrokes(text):
    """文字列を押下するキー列に変換。キーの左手右手の区別は行わない。

    Args:
        text (Unicode)): 日本語を含んだ文字列

    Returns:
        str: 押下するキー列
    """
    # この関数の引数はすべてキーボードで直接入力可能なASCIIとする。
    # assert(all([(c in "qwertasdfgzxcvbyuiop@[hjkl;:]nm,./\\") for c in text]))
    text_orig = text
    strks_all = ""
    while 0 < len(text):
        for i in [2, 1, 0]:
            # ひらがな2or1文字→ 1ストローク に変換
            if 0 == i:
                # print(text)
                print(
                    text_orig,
                    sep="\n",
                    end="\n",
                    file=codecs.open("変換できなかった文字.txt", "a", "utf-8"),
                )
                # print(text_orig, sep="\n\r", end="\n\r", file=codecs.open('変換できなかった文字.txt', 'w', 'utf-8'))
                # assert(False)
                text = text[1:]
                break

            if None != char2stroke(text[0:i]):
                st = char2stroke(text[0:i])
                text = text[i:]
                strks_all += st
                break
    return strks_all


def text2score(text):
    """日本語文字列から所要時間を算出

    Args:
        text (Unicode): 日本語含む文字列

    Returns:
        float: 所要時間
    """
    st = text2keystrokes(text)
    st_l, st_r = devide_strokes_side(st)
    score_l = keystrokes2score(st_l)
    score_r = keystrokes2score(st_r)
    return max(score_l, score_r)


def load_dataset():
    """WEB文字コーパスのロード

    Returns:
        list of Unicode: ロードしたデータセットの日本語配列。前処理済み。23000行ほど。
    """
    try:
        print("Loading dataset pickle")
        # data = pickle.load(open("disc.pickle", "rb"))
        lines = pickle.load(open("disc.pickle", "rb"))
        print("Loaded")
    except (OSError, IOError) as _:
        print("Converting txt -> pickle")
        f = open("../../dataset/KWDLC/disc/disc.txt")
        lines = f.read()  # ファイル終端まで全て読んだデータを返す
        f.close()
        pickle.dump(lines, open("./disc.pickle", "wb"))
    print("前処理開始")
    data = extract_vailed_texts(lines)
    data = list(map(lambda x: regularize_text(x), data))
    print("前処理完了")
    # pickle.dump(data, open("./disc.pickle", "wb"))
    # print(data[0])
    # print(data[1])
    # print(data[2])
    # print(len(data))
    return data


def extract_vailed_texts(texts):
    """WEB文章日本語コーパスの前処理

    Args:
        texts (Unicode): 1行の日本語文字列

    Returns:
        Unicode: 前処理実施済みの評価対象日本語文字列
    """

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
    texts = filter(lambda x: not re.match(r"^\s*$", x), texts)
    texts = filter(lambda x: not re.match(r"^#.*$", x), texts)
    texts = map(lambda x: x.split(" ", 1)[1].rstrip(), list(texts))
    texts = list(texts)
    return texts


def regularize_text(text):
    """数字や句読点を半角に統一

    Args:
        text (Unicode): 日本語含む文字列

    Returns:
        Unicode: 日本語含む文字列
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
        ["。", "."],
        ["：", ":"],
        # ["'", " "],
        # ['"', " "],
        ["払金", ""],
        ["試着", ""],
        # ["金", ""],
        ["々", ""],
        ["”", " "],
        ["“", " "],
        ["（", " "],
        ["）", " "],
        ["『", "「"],
        ["』", "」"],
        ["｢", "」"],
        ["｣", "」"],
        ["／", "/"],
        ["！", "!"],
        ["？", "?"],
        ["●", "まる"],
        ["～", ""],
        ["〜", ""],
        ["…", ""],
        ["…", ""],
        ["《", ""],
        ["》", ""],
    ]
    for p in pairs:
        text = text.replace(p[0], p[1])
    mecab = MeCab.Tagger("-Oyomi")
    text = mecab.parse(text).rstrip()
    text = kata2hira(text)
    text = mojimoji.zen_to_han(text)
    for p in pairs:
        text = text.replace(p[0], p[1])
    return text


if __name__ == "__main__":
    t = load_dataset()
    score = 0.0
    for n in t:
        # print("          {}".format(n))
        cs = text2score(n)
        score += cs
        print("{:.2f}  {}".format(cs, n))
    print("total core: {}".format(score))
    # print(load_dataset()[:10])
