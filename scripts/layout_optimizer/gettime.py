#!/usr/bin/env python3
# coding:utf-8

import readchar
import datetime
import itertools
import pickle
import pandas as pd


key_l = "qwertasdfgzxcvb"
key_r = "yuiop@[hjkl;:]nm,./\\"
key_all = key_l+key_r

keymove_l = list(map(lambda x: x[0]+x[1], itertools.product(key_l,key_l)))
keymove_r = list(map(lambda x: x[0]+x[1], itertools.product(key_r,key_r)))
keymove_all = list(map(lambda x: x[0]+x[1], itertools.product(key_all,key_all)))


try:
    df = pd.read_csv('./2stroke_timetable.csv', index_col=0)
except (OSError, IOError) as e:
    df = pd.DataFrame(9999, columns = list(key_all), index=list(key_all))
    df.to_csv('./2stroke_timetable.csv')
print(df)

# try:
#     tl = pickle.load(open("./2stroke_timetable.pickle", "rb"))
# except (OSError, IOError) as e:
#     tl = {x: 9999 for x in keymove_all}
#     pickle.dump(tl, open("./2stroke_timetable.pickle", "wb"))



key_buf = []
tim_buf = []
while 1:
    kb = readchar.readchar()
    key_buf += kb
    key_buf = key_buf[-10:]
    tim_buf.append(datetime.datetime.now())
    tim_buf = tim_buf[-10:]

    if all([ key_buf[0:2] == key_buf[i*2:i*2+2] for i in range(5) ]):
        t = (tim_buf[-1]-tim_buf[-10]).total_seconds()/10  # ToDo: ここ本来は9で割るべきだった。
        print('suc', end=' ')
        print(tim_buf[-1]-tim_buf[-10], end=' ')
        c_bef, c_aft = key_buf[0], key_buf[1]
        if df.loc[ c_bef, c_aft ] > t: 
            df.loc[ c_bef, c_aft ] = t
            df.to_csv('./2stroke_timetable.csv')
            print('updated', end=' ')
        print(' ')

    if "".join(key_buf[-4:]) == 'exit':
        print(kb, end='', flush=True)
        break

